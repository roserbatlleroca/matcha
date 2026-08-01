#!/usr/bin/env python3
"""
pre_process_FMA.py

Prepares the reference excerpts used to condition Stable Audio Open
generation. Starting from the fixed list of previously selected FMA
tracks (fma_selected.csv), this script locates each track's raw audio
file in the FMA directory structure, extracts a fixed 10-second window
(10s-20s), and exports it as a WAV file named "{track_id}_{genre}.wav".

Input:
    fma_selected.csv    : metadata for the selected tracks (id, title,
                          author, url, genre, all_genres).
    SOURCE_BASE_DIR     : root of the FMA dataset (fma_large), where
                          tracks are stored under subdirectories named
                          after the first 3 digits of the zero-padded
                          6-digit track ID (e.g. track 2 ->
                          fma_large/000/000002.mp3).

Output:
    fma_trimmed.csv     : same columns as the input, plus a `sample_path`
                          column pointing to the trimmed WAV file. This
                          file is the input to get_text_prompt_pipeline.py.

Dependencies:
    pip install pydub pandas
    ffmpeg must be installed and on your PATH
"""

import os
import pandas as pd
from pydub import AudioSegment

# ========================================================
# config
# ========================================================
SELECTED_CSV     = "fma_selected.csv"
SOURCE_BASE_DIR  = "fma/fma_large"
OUTPUT_DIR       = "audio/trimmed"  # folder where trimmed WAV files will be saved
OUTPUT_CSV       = "data/fma_trimmed.csv"

TRIM_START_MS = 10_000   # skip first 10 s
TRIM_END_MS   = 20_000   # end at 20 s -> 10 s clip


def track_id_to_path(track_id: int) -> str:
    """
    FMA stores tracks under subdirs named after the first 3 digits of the
    zero-padded 6-digit track ID.
      e.g. track 2 -> fma_large/000/000002.mp3
    """
    padded = f"{int(track_id):06d}"
    return os.path.join(SOURCE_BASE_DIR, padded[:3], f"{padded}.mp3")


def trim_to_wav(src_path: str, dst_path: str) -> bool:
    """Loads src_path, extracts [TRIM_START_MS, TRIM_END_MS], exports as WAV."""
    try:
        audio = AudioSegment.from_file(src_path)
        if len(audio) < TRIM_END_MS:
            print(f"  too short ({len(audio)/1000:.1f}s), skipping: {src_path}")
            return False
        audio[TRIM_START_MS:TRIM_END_MS].export(dst_path, format="wav")
        return True
    except Exception as e:
        print(f"  error processing {src_path}: {e}")
        return False


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print(f"Loading '{SELECTED_CSV}'...")
    df = pd.read_csv(SELECTED_CSV)
    df["id"] = pd.to_numeric(df["id"], errors="coerce").astype("Int64")
    df = df.dropna(subset=["id"])
    print(f"  {len(df)} selected tracks loaded.")

    sample_paths, failed_ids = [], []

    for _, row in df.iterrows():
        track_id = int(row["id"])
        genre = str(row["genre"]).lower().replace(" ", "_").replace("/", "-")

        src = track_id_to_path(track_id)
        if not os.path.exists(src):
            print(f"  [{track_id}] raw file not found, skipping: {src}")
            sample_paths.append(None)
            failed_ids.append(track_id)
            continue

        dst = os.path.join(OUTPUT_DIR, f"{track_id}_{genre}.wav")
        print(f"  [{track_id}] trimming...", end=" ", flush=True)
        if trim_to_wav(src, dst):
            sample_paths.append(dst)
            print("done")
        else:
            sample_paths.append(None)
            failed_ids.append(track_id)

    df["sample_path"] = sample_paths
    df.to_csv(OUTPUT_CSV, index=False)

    print(f"\nDone!")
    print(f"  Trimmed samples CSV : {OUTPUT_CSV} ({len(df) - len(failed_ids)} succeeded)")
    if failed_ids:
        print(f"  Failed / missing    : {len(failed_ids)} track(s): {failed_ids}")


if __name__ == "__main__":
    main()