<div align="center">

# MATCHA: Music Attribute-based Triplet Comparison with Human Annotations

**Roser Batlle-Roca**<sup>1</sup>, **Woosung Choi**<sup>2</sup>, **Joan Serrà**<sup>2</sup>, **Fabio Morreale**<sup>2</sup>,<br> **Wei-Hsiang Liao**<sup>2</sup>,
**Xavier Serra**<sup>1</sup>, **Emilia Gómez**<sup>1,3</sup>, **Yuki Mitsufuji**<sup>2,4</sup>

<sup>1</sup>Music Technology Group, Universitat Pompeu Fabra · <sup>2</sup>Sony AI ·<br> 
<sup>3</sup>Joint Research Centre, European Commission ·
<sup>4</sup>Sony Group Corporation


This repository is complementary to the paper *On the Human and Computer Aligment of Attribute-Based Music Matches*, currently under-review. It contains main documentation of the MATCHA dataset, as well as complemetary results of the perceptual experiment conducted in this study. Additional materials will be provided upon paper acceptance. 

[![Website](https://img.shields.io/badge/Website-MATCHA-003366?style=flat&logo=googlechrome&logoColor=white)](https://roserbatlleroca.github.io/matcha/index.html) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
<!-- [![arXiv](https://img.shields.io/badge/arXiv-260X.XXXXX-B31B1B.svg)](https://arxiv.org/abs/YOUR_ARXIV_ID) -->

</div>

---

## Dataset

MATCHA (Musical Attribute-based Triplet Comparison with Human Annotations) comprises 300 music triplets evaluated by 83 expert music participants as part of a forced-choice perceptual experiment. Each triplet (case) consists of a **reference** excerpt and two **comparison** samples (**A** and **B**). The dataset contains 1105 perceptual assessments of attribute-based musical similarity across five musical dimensions: melody, harmony, rhythm, voice, and timbre. It includes both human-composed and AI-generated musical excerpts, as summarised in the table below.

| Origin | Section | Source | Cases | w/ Vocals | % |
|--------|------|--------|------:|-------:|--:|
| Human | Human-Plagirism (HP) | [SMP Dataset](https://github.com/Mippia/Music-Plagiarism-Detection) | 75 | 61 | 25 |
| | Human-Version (HV) | [Discogs-VI](https://github.com/MTG/discogs-vi-dataset) | 75 | 63 | 25 |
| AI | AI-SAO (AS)| [Stable Audio Open](https://huggingface.co/stabilityai/stable-audio-open-1.0) | 120 | 0 | 40 |
| | AI-Media (AM) | Media Articles [[1](https://www.musicbusinessworldwide.com/suno-is-a-music-ai-company-aiming-to-generate-120-billion-per-year-newton-rex/),[2](https://www.gema.de/en/news/ai-and-music/ai-lawsuit/audio-samples-suno)] | 30 | 27 | 10 |

*Stimuli distribution across reference sources, by origin, section, source name, number of cases, number of cases containing vocals, and overall percentage.*

Listen to some stimuli examples [here](https://roserbatlleroca.github.io/matcha/index.html#examples)! 

## Materials

* [Cases Metadata](metadata/raw_cases.csv): Raw metadata of all the cases included in the dataset, including original source, song title and auhtors, timestamps, and triplet criteria composition. 
* [Individual Annotations](annotations/annotations_individual.csv): All 1105 annotations included in the dataset. 
* [Aggregated Annotations per Case](annotations/annotations_per_case.csv): Summary decision per case, including inter-rater agreement and Fleiss' k per case. 
* [Tied Cases](annotations/disagreement_cases.txt): List of cases that currently present a tie (that is, two or more response options received the same number of votes without a winning case).
* [Aggregated Decision Scores](annotations/decisions_individual.csv): Aggregate scores across cases, considering whether participants preferred sample A, sample B or Neither for each case. 
* [Participants Demographics](annotations/participants_demographics/): Complete analysis of the 83 elegible participants demographics per category (age, gender, location, music level and music role). 
* [Datasheet](metadata/MATCHA_datasheet.md): Complete datasheet for the MATCHA dataset, following [*Datahseet for Dataset*](https://dl.acm.org/doi/10.1145/3458723) template. 
* [MiRA Evaluation](mira_eval): Folder containing the raw results from the evaluation with the MiRA tool. 

## Citation

If you find MATCHA or its repository useful in your research, please cite our paper:

```
@article{batlleroca2026matcha,
  title   = {On the Human and Computer Alignment of Attribute-Based Music Matches},
  author  = {Batlle-Roca, Roser and Choi, Woosung and Serr\`a, Joan and Morreale, Fabio and Liao, Wei-Hsiang and Serra, Xavier and G\'omez, Emilia and Mitsufuji, Yuki},
  year    = {2026}
```
