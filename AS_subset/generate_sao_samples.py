#!/usr/bin/env python3
"""
generate_sao_samples.py

Generates the two comparison samples (one "more similar", one "less
similar") for each reference track, using Stable Audio Open.

For every track listed in CSV_PATH (output of get_text_prompt.py),
this script produces:
  - a "less similar" sample: generated from random initial noise,
    conditioned on the track's extracted text prompt.
  - a "more similar" sample: generated from the DDIM-inverted noise of
    the reference audio, conditioned on the same prompt, with added
    stochasticity via eta_ddim (balanced across tracks between 0.3 and
    0.5) to avoid exact reconstruction.

Both samples are scored against the prompt with CLAP for logging
purposes (not used for filtering or selection in this work).

Input:
    INPUT_PATH  : folder with the trimmed reference excerpts (output of
                  pre_process_FMA.py).
    CSV_PATH    : track_id, genre, mf_prompt, qwen_summary, track_path
                  (output of get_text_prompt.py).

Output:
    OUTPUT_PATH : generated .wav files for both samples per track.
    OUTPUT_CSV  : track_id, genre, qwen_prompt, inv_noise_path,
                  inv_noise_clap, inv_noise_eta, rand_noise_path,
                  rand_noise_clap, rand_noise_eta.

Dependencies:
    pip install torch torchaudio stable-audio-tools laion-clap librosa einops pandas
    Requires GPU access (see paper appendix for hardware used).
"""

import torch
import torchaudio
import pandas as pd
from pathlib import Path
from stable_audio_tools import get_pretrained_model
from stable_audio_tools.inference.generation import ddim_invert_audio, generate_diffusion_cond
from einops import rearrange
import laion_clap
from laion_clap.training.data import get_audio_features
from laion_clap.training.data import int16_to_float32, float32_to_int16
import librosa
import math
import random

# ========================================================
# config details
# ========================================================
INPUT_PATH  = "audio/trimmed"                 # folder with trimmed reference samples 
CSV_PATH    = "data/text_prompt.csv"          # track_id, genre, mf_prompt, qwen_summary, track_path
OUTPUT_PATH = "audio/generated_sao/"          # folder where generated samples will be saved
OUTPUT_CSV  = "data/generation_results.csv"

CLAP_CKPT_PATH = "checkpoints/music_audioset_epoch_15_esc_90.14.pt"  # download separately, see README

# set generation length
LENGTH_SECONDS = 10  # seconds

# inversion parameters
INV_CFG   = -6.0
INV_ETA   = 0.0
INV_STEPS = 100

# generation parameters
GEN_CFG   = 6.0
GEN_STEPS = 100

ETA_OPTIONS = [0.3, 0.5]   # will be balanced across prompts


# ========================================================
# balanced eta assignment
# ========================================================
def make_balanced_eta_list(n: int, options: list) -> list:
    """
    Returns a shuffled list of length n where each value in options
    appears as equally as possible (e.g. 60x 0.3 and 60x 0.5 for n=120).
    """
    per_option = n // len(options)
    remainder  = n % len(options)
    pool = options * per_option + options[:remainder]
    random.shuffle(pool)
    return pool


# ========================================================
# helpers
# ========================================================
def save_audio(tensor, path, sample_rate):
    audio = rearrange(tensor, "b d n -> d (b n)")
    audio = audio.to(torch.float32).div(torch.max(torch.abs(audio))).clamp(-1, 1).cpu()
    torchaudio.save(str(path), audio, sample_rate)
    print(f"    saved: {path}")


def compute_clap_score(prompt: str, audio_path: str, model_clap) -> float:
    print("    computing CLAP score...")
    model_clap.to(device)
    audio_waveform, sr = librosa.load(audio_path, sr=48000)
    seg_max_len = sr * 10

    if len(audio_waveform) > seg_max_len:
        splits       = math.ceil(len(audio_waveform) / 480000)
        split_length = int(round(len(audio_waveform) / splits, 0))
        offset       = 0
        segment_embeddings = []

        for _ in range(splits):
            segment = audio_waveform[offset:offset + split_length]
            offset += split_length
            audio   = int16_to_float32(float32_to_int16(segment))
            audio   = torch.from_numpy(audio).float()
            temp_dict = get_audio_features(
                {}, audio, 480000,
                data_truncating='fusion' if model_clap.enable_fusion else 'rand_trunc',
                data_filling='repeatpad',
                audio_cfg=model_clap.model_cfg['audio_cfg'],
                require_grad=audio.requires_grad,
            )
            segment_embeddings.append(model_clap.model.get_audio_embedding([temp_dict]))

        audio_embed = torch.mean(torch.stack(segment_embeddings), dim=0)
    else:
        audio_embed = model_clap.get_audio_embedding_from_filelist(x=[audio_path], use_tensor=True)

    text_embed  = model_clap.get_text_embedding([prompt, prompt], use_tensor=True, tokenizer=None)
    cosine_sim  = torch.nn.functional.cosine_similarity(audio_embed, text_embed, dim=1, eps=1e-8)
    clap_score  = (cosine_sim.sum() / cosine_sim.size(0)).item()
    print(f"    CLAP score: {clap_score:.4f}")
    model_clap.to("cpu")
    torch.cuda.empty_cache()
    return clap_score


# ========================================================
# generation functions
# ========================================================
def generate_from_inverted_noise(
    model, audio: torch.Tensor, sr: int,
    conditioning: list, sample_size: int,
    eta: float, device: str,
) -> torch.Tensor:
    """Inverts audio to noise, then reconstructs with conditioning."""
    print("  inverting audio to noise...")
    model.to(device)
    inverted_noise = ddim_invert_audio(
        model,
        audio_to_invert=(sr, audio),
        steps=INV_STEPS,
        cfg_scale=INV_CFG,
        conditioning=conditioning,
        sample_size=sample_size,
        seed=42,
        sigma_min=0.1,
        sigma_max=1.0,
        sampler_type="v-ddim",
        device=device,
        return_latents=True,
        eta_ddim=INV_ETA,
    )

    print(f"  reconstructing from inverted noise (eta={eta})...")
    output = generate_diffusion_cond(
        model,
        steps=GEN_STEPS,
        cfg_scale=GEN_CFG,
        conditioning=conditioning,
        sample_size=sample_size,
        seed=42,
        sigma_min=0.1,
        sigma_max=1.0,
        sampler_type="v-ddim",
        device=device,
        init_noise=inverted_noise,
        eta_ddim=eta,
    )

    model.to("cpu")
    torch.cuda.empty_cache()
    return output


def generate_from_random_noise(
    model, conditioning: list, sample_size: int,
    eta: float, device: str,
) -> torch.Tensor:
    """Generates audio from random noise with conditioning."""
    print(f"  generating from random noise (eta={eta})...")
    model.to(device)
    output = generate_diffusion_cond(
        model,
        steps=GEN_STEPS,
        cfg_scale=GEN_CFG,
        conditioning=conditioning,
        sample_size=sample_size,
        seed=42,
        sigma_min=0.1,
        sigma_max=1.0,
        sampler_type="v-ddim",
        device=device,
        eta_ddim=eta,
    )
    model.to("cpu")
    torch.cuda.empty_cache()
    return output


# ========================================================
# generation with clap
# ========================================================
def generate_with_clap(
    gen_fn,
    prompt: str,
    filename_stem: str,
    sample_rate: int,
    model_clap,
) -> tuple[Path, float]:
    """Calls gen_fn() and computes CLAP score."""
    tensor = gen_fn()
    output_path = Path(OUTPUT_PATH) / f"{filename_stem}.wav"
    save_audio(tensor, output_path, sample_rate)
    score = compute_clap_score(prompt, str(output_path), model_clap)

    return output_path, score


# ========================================================
# main
# ========================================================
device = "cuda" if torch.cuda.is_available() else "cpu"

Path(OUTPUT_PATH).mkdir(parents=True, exist_ok=True)

print("loading Stable Audio Open model...")
model, model_config = get_pretrained_model("stabilityai/stable-audio-open-1.0")
sample_rate = model_config["sample_rate"]
sample_size = sample_rate * LENGTH_SECONDS
model = model.to(device)

# load CLAP model
print("loading CLAP model...")
model_clap = laion_clap.CLAP_Module(enable_fusion=False, amodel='HTSAT-base', device="cpu")
model_clap.load_ckpt(CLAP_CKPT_PATH)

prompts_df = pd.read_csv(CSV_PATH)
n_tracks   = len(prompts_df)

# build balanced eta list upfront so assignment is even across all tracks
eta_list = make_balanced_eta_list(n_tracks, ETA_OPTIONS)
print(f"\neta distribution across {n_tracks} tracks: "
      + ", ".join(f"{e}: {eta_list.count(e)}" for e in ETA_OPTIONS))

results = []

for idx, row in prompts_df.iterrows():
    track_id   = str(row["track_id"].split(".")[0].split("_")[0])  # extract track ID from filename
    genre      = str(row["genre"])
    prompt     = row["qwen_summary"]
    track_path = Path(row["track_path"])
    eta        = eta_list[idx]

    print(f"\n{'='*60}")
    print(f"[{idx+1}/{n_tracks}] Track {track_id} | genre={genre} | eta={eta}")
    print(f"  prompt: {prompt[:80]}...")

    if not track_path.exists():
        print(f"file not found: {track_path} — skipping.")
        continue

    # load and truncate reference audio
    audio, sr = torchaudio.load(str(track_path))
    audio = audio[:, : sr * LENGTH_SECONDS]

    conditioning = [{
        "prompt": prompt,
        "seconds_start": 0,
        "seconds_total": LENGTH_SECONDS,
    }]

    # inverted noise generation ("more similar" sample)
    print("\n  [INV] inverted-noise generation")
    inv_stem = f"{track_id}_{genre}_inv_noise_eta_{eta}"

    inv_path, inv_clap = generate_with_clap(
        gen_fn=lambda: generate_from_inverted_noise(
            model, audio, sr, conditioning, sample_size, eta, device
        ),
        prompt=prompt,
        filename_stem=inv_stem,
        sample_rate=sample_rate,
        model_clap=model_clap,
    )

    # random noise generation ("less similar" sample)
    print("\n  [RAND] random-noise generation")
    rand_stem = f"{track_id}_{genre}_rand_noise_eta_{eta}"

    rand_path, rand_clap = generate_with_clap(
        gen_fn=lambda: generate_from_random_noise(
            model, conditioning, sample_size, eta, device
        ),
        prompt=prompt,
        filename_stem=rand_stem,
        sample_rate=sample_rate,
        model_clap=model_clap,
    )

    results.append({
        "track_id":        track_id,
        "genre":           genre,
        "qwen_prompt":     prompt,
        "inv_noise_path":  str(inv_path),
        "inv_noise_clap":  round(inv_clap, 4),
        "inv_noise_eta":   eta,
        "rand_noise_path": str(rand_path),
        "rand_noise_clap": round(rand_clap, 4),
        "rand_noise_eta":  eta,
    })

    # save CSV after every track so progress isn't lost on a crash
    pd.DataFrame(results).to_csv(OUTPUT_CSV, index=False)
    print(f"  CSV updated: {OUTPUT_CSV}")

print(f"\nDone! Results saved to {OUTPUT_CSV}")