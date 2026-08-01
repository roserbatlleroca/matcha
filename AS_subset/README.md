# AS Subset 

This folder contains all data, scripts, and generated audio related to the **AS** subset of the dataset, in which comparison samples were generated using [Stable Audio Open](https://github.com/Stability-AI/stable-audio-tools) via a text-conditioned, DDIM-inversion-based pipeline.

For an overview of the full dataset, the annotation task, and the other subsets, see the [main repository README](../README.md).

> Note that this folder is a work contains basic code and instructions. Full implementation instructions, environment setup, dependency versions, and pretrained checkpoint download links will be provided upon paper acceptance.

## Pipeline Overview

For each reference track, the pipeline produces two comparison samples: one intended to be **more similar** and one **less similar** to the reference. We follow three sequential steps:

| Step | Script | Description |
|------|--------|-------------|
| 1 | `pre_process_FMA.py` | Selects the raw FMA audio for each track in `data/fma_selected.csv` and trims it to a fixed 10-second window (10s–20s). |
| 2 | `get_text_prompt.py` | Generates a text description of each trimmed excerpt using Music Flamingo, then condenses it into a single summary sentence with Qwen3-8B. |
| 3 | `generate_sao_samples.py` | Generates the two comparison samples with Stable Audio Open: one from random initial noise (less similar), and one from DDIM-inverted noise of the reference with added stochasticity (more similar). Both are conditioned on the same text prompt. |

Each script's docstring documents its expected inputs/outputs in more detail.


## Models Used

- **Stable Audio Open** (`stabilityai/stable-audio-open-1.0`): Audio generation and DDIM inversion.
- **Music Flamingo** (`nvidia/music-flamingo-hf`): Audio description generation.
- **Qwen3-8B** (`Qwen/Qwen3-8B`): Description summarization.
- **CLAP** (`music_audioset_epoch_15_esc_90.14.pt`): Used to log a text-audio alignment score for each generation; **not used for filtering or selecting samples** in this work.