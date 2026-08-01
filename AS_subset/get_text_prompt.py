"""
get_text_prompt.py

Generates a short natural-language description for each reference
excerpt, later used as text conditioning for Stable Audio Open generation.

For every audio file in INPUT_PATH, this script:
  1. Prompts Music Flamingo (nvidia/music-flamingo-hf) to produce a detailed
     description of the track (genre, mood, melody, tempo/BPM, chords, and
     main instruments).
  2. Feeds that description to Qwen3-8B, which condenses it into a single
     summary sentence covering the same attributes.

Results are appended incrementally to OUTPUT_CSV (track_id, genre,
mf_prompt, qwen_summary, track_path). The script can be safely resumed
after an interruption: already-processed track IDs (read back from
OUTPUT_CSV) are skipped on subsequent runs.

Input:
    INPUT_PATH  : folder of reference excerpts, named "{track_id}_{genre}.wav"

Output:
    OUTPUT_CSV  : track_id, genre, mf_prompt, qwen_summary, track_path.
                  Input to generate_sao_samples.py.

Usage:
    python get_text_prompt.py

Dependencies:
    pip install torch transformers
    Requires GPU access to run Music Flamingo and Qwen3-8B inference.
"""

import torch
import glob
import csv
import os
from pathlib import Path
from transformers import AudioFlamingo3ForConditionalGeneration, AutoProcessor
from transformers import AutoModelForCausalLM, AutoTokenizer

# ========================================================
# config
# ========================================================
INPUT_PATH = "fma/selected_samples" # path with selected samples to process
OUTPUT_CSV = "text_prompt.csv" # name of the output CSV file to save the results

PROMPT_MF = "Describe this track in detail. Include genre, mood, melody, tempo with BPM, chord, and main instruments." # prompt for Music Flamingo
PROMPT_QWEN = 'Summarize this text in one sentence starting with "A ...", including the genre, mood, melody, tempo with BPM, chord, and main instruments: ' # prompt for Qwen3.5

# ========================================================
# initialize models
# ========================================================
def load_models():
    print("loading Music Flamingo...")
    processor = AutoProcessor.from_pretrained("nvidia/music-flamingo-hf")
    model_mf = AudioFlamingo3ForConditionalGeneration.from_pretrained(
        "nvidia/music-flamingo-hf", # weights for Music Flamingo
        device_map="auto",
    )
    model_mf = torch.compile(model_mf)

    print("loading Qwen3...")
    tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen3-8B")
    model_qwen = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen3-8B", # weights for Qwen3.5
        torch_dtype="auto",
        device_map="auto",
    )

    print("MF and Qwen ready.\n")
    return processor, model_mf, tokenizer, model_qwen

# ========================================================
# inference functions
# ========================================================
def get_mf_prompt(track_path, processor, model_mf):
    conversation = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": PROMPT_MF},
                {"type": "audio", "path": track_path},
            ],
        }
    ]
    inputs = processor.apply_chat_template(
        conversation,
        tokenize=True,
        add_generation_prompt=True,
        return_dict=True,
    ).to(model_mf.device)

    outputs = model_mf.generate(**inputs, max_new_tokens=1024)
    decoded = processor.batch_decode(
        outputs[:, inputs.input_ids.shape[1]:],
        skip_special_tokens=True,
    )
    return decoded[0]


def get_qwen_summary(mf_prompt, tokenizer, model_qwen):
    messages = [{"role": "user", "content": PROMPT_QWEN + mf_prompt}]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
        enable_thinking=False,
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model_qwen.device)
    generated_ids = model_qwen.generate(**model_inputs, max_new_tokens=150)
    output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()
    return tokenizer.decode(output_ids, skip_special_tokens=True)

# ========================================================
#  pipeline
# ========================================================
def main():
    processor, model_mf, tokenizer, model_qwen = load_models()

    samples = sorted(glob.glob(f"{INPUT_PATH}/*"))
    print(f"found {len(samples)} samples.\n")

    # load already-processed track IDs to allow resuming if interrupted or new tracks added
    processed = set()
    if os.path.exists(OUTPUT_CSV):
        with open(OUTPUT_CSV, newline="") as f:
            reader = csv.DictReader(f)
            processed = {row["track_id"] for row in reader}
        print(f"resuming — {len(processed)} samples already processed.\n")

    with open(OUTPUT_CSV, "a", newline="") as csvfile:
        fieldnames = ["track_id", "genre", "mf_prompt", "qwen_summary", "track_path"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # write header only if file is new
        if not processed:
            writer.writeheader()

        for track_path in samples:
            track_id = Path(track_path).name

            if track_id in processed:
                print(f"skipping {track_id} (already processed).")
                continue

            print(f"processing {track_id}...")

            mf_prompt = get_mf_prompt(track_path, processor, model_mf).replace("\n", " ")

            qwen_summary = get_qwen_summary(mf_prompt, tokenizer, model_qwen)

            writer.writerow({
                "track_id": track_id,
                "genre": track_id.split("_")[1].split(".")[0],  # extract genre from filename
                "track_path": track_path,
                "qwen_summary": qwen_summary,
                "mf_prompt": mf_prompt,                
            })
            csvfile.flush()  # save after each sample (to allow recover in case of crash)


if __name__ == "__main__":
    main()