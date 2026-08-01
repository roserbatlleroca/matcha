# MATCHA: Music Attribute-based Triplet Comparison with Human Annotations

*Anonymous authors*

This repository is complementary to the paper *On the Human and Computer Aligment of Attribute-Based Music Matches*, currently under-review. It contains main documentation of the MATCHA dataset, as well as complemetary results of the perceptual experiment conducted in this study. We plan to provide additional materials upon paper acceptance, including a complete dataset datasheet. 

### Abstract

Recent advances in generative AI are raising ethical concerns regarding the originality of generated content and the potential replication of training data, with further implications for transparency, attribution, and intellectual property. In music, several computational approaches have been proposed to identify potential replication, using audio-based similarity metrics. Yet, their alignment with human judgments across distinct musical attributes remains underexplored. To address this gap, we conduct a perceptual experiment on music matches, defined as strongly similar musical excerpts. We focus on five musical attributes: melody, harmony, rhythm, voice, and timbre. We design a triplet-based forced-choice task comprising 300 cases, including plagiarism examples, cover songs, and AI-generated music. From this experiment, we introduce the MATCHA (Musical Attribute-based Triplet Comparison with Human Annotations) dataset: a collection of 1105 perceptual assessments of attribute-based music matches from 83 expert participants. Our findings reveal measurable agreement among participants in identifying matches across attributes. We further observe partial alignment between human judgments and computational similarity measures. Overall, this work underscores the importance of domain-specific and perceptually grounded evaluation frameworks for generative AI in creative practice.

---

## Dataset

MATCHA (Musical Attribute-based Triplet Comparison with Human Annotations) comprises 300 music triplets evaluated by 83 expert music participants as part of a forced-choice perceptual experiment. Each triplet (case) consists of a **reference** excerpt and two **comparison** samples (**A** and **B**). The dataset contains 1105 perceptual assessments of attribute-based musical similarity across five musical dimensions: melody, harmony, rhythm, voice, and timbre. It includes both human-composed and AI-generated musical excerpts, as summarised in the table below.

| Origin | Section | Source | Cases | w/ Vocals | % |
|--------|------|--------|------:|-------:|--:|
| Human | Human-Plagirism (HP) | [SMP Dataset](https://github.com/Mippia/Music-Plagiarism-Detection) | 75 | 61 | 25 |
| | Human-Version (HV) | [Discogs-VI](https://github.com/MTG/discogs-vi-dataset) | 75 | 63 | 25 |
| AI | AI-SAO (AS)| [Stable Audio Open](https://huggingface.co/stabilityai/stable-audio-open-1.0) | 120 | 0 | 40 |
| | AI-Media (AM) | Media Articles [[1](https://www.musicbusinessworldwide.com/suno-is-amusic-ai-company-aiming-to-generate-120-billion-peryear-newton-rex/),[2](https://www.gema.de/en/news/ai-and-music/ai-lawsuit/audio-samples-suno)] | 30 | 27 | 10 |

*Stimuli distribution across reference sources, by origin, section, source name, number of cases, number of cases containing vocals, and overall percentage.*

### Materials

* [Cases Metadata](metadata/raw_cases.csv): Raw metadata of all the cases included in the dataset, including original source, song title and auhtors, timestamps, and triplet criteria composition. 
* [Individual Annotations](annotations/annotations_individual.csv): All 1105 annotations included in the dataset. 
* [Aggregated Annotations per Case](annotations/annotations_per_case.csv): Summary decision per case, including inter-rater agreement and Fleiss' k per case. 
* [Tied Cases](annotations/disagreement_cases.txt): List of cases that currently present a tie (that is, two or more response options received the same number of votes without a winning case).
* [Aggregated Decision Scores](annotations/decisions_individual.csv): Aggregate scores across cases, considering whether participants preferred sample A, sample B or Neither for each case. 
* [Participants Demographics](annotations/participants_demographics/): Complete analysis of the 83 elegible participants demographics per category (age, gender, location, music level and music role). 
* [MATACHA dataset](): Link to Zenodo repository with the complete MATCHA dataset, including metadata, annotations and audio samples. Access to the audio samples is restricted to research-purpose only and handled by [Anonymised Institution]. *Note that this link will only be provided upon publication acceptance.*
* [AS Subset](): Link to 120 samples, generated with Stable Audio Open. *Note that we will only openly relase these samples under CC-BY-NC licensing, complying with Stable Audio License.*
* [Datasheet](): Complete datasheet for the MATCHA dataset, following [*Datahseet for Dataset*](https://dl.acm.org/doi/10.1145/3458723) template. *Note that we are planning to share the datasheet upon paper acceptance.* 
* [MiRA Evaluation](mira_eval): Folder containing the raw results from the evaluation with the MiRA tool. 

## Stimuli Examples

Below are 8 representative cases (two per subset category) with the audio excerpts, the
majority decision, and the inter-rater agreement statistics. N indicates the number of responses received per cases (min. 3). For each musical attribute, winning decision is reported, together with the inter-annotator agreement. Overall column details the inter-annotator agreement and Fleiss' κ per case. 

> **Note:** GitHub does not support inline audio Playback in README files. Click a link
> below to listen to the excerpt in your browser. *A complementary website with direct playable audio including the following examples will be released upon paper acceptance.*

### HP

| Case | Ref. | A | B | N | Melody | Harmony | Rhythm | Voice | Timbre | Overall |
|------|-----------|----------|----------|:------------:|:------:|:-------:|:------:|:-----:|:------:|:-------:|
| c_005 | [Play](examples/c_005/c_ref_005.wav) | [Play](examples/c_005/c_sA_005.wav) | [Play](examples/c_005/c_sB_005.wav) | 4 | A (100.0%) | A (100.0%) | A (100.0%) | Neither (100.0%) | A (50.0%) | 90.0% (κ=0.6825) |
| c_113 | [Play](examples/c_113/c_ref_113.wav) | [Play](examples/c_113/c_sA_113.wav) | [Play](examples/c_113/c_sB_113.wav) | 4 | A (100.0%) | A (50.0%) | A (50.0%) | Neither (50.0%) | B (50.0%) | 60.0% (κ=0.0181) |

### HV

| Case | Ref. | A | B | N | Melody | Harmony | Rhythm | Voice | Timbre | Overall |
|------|-----------|----------|----------|:------------:|:------:|:-------:|:------:|:-----:|:------:|:-------:|
| c_033 | [Play](examples/c_033/c_ref_033.wav) | [Play](examples/c_033/c_sA_033.wav) | [Play](examples/c_033/c_sB_033.wav) | 3 | A (100.0%) | A (100.0%) | A (66.7%) | B (100.0%) | B (66.7%) | 86.7% (κ=0.4915) |
| c_244 | [Play](examples/c_244/c_ref_244.wav) | [Play](examples/c_244/c_sA_244.wav) | [Play](examples/c_244/c_sB_244.wav) | 4 | Neither (75.0%) | Neither (75.0%) | B (100.0%) | B (50.0%) | B (100.0%) | 80.0% (κ=0.351) |

### AS

| Case | Ref. | A | B | N | Melody | Harmony | Rhythm | Voice | Timbre | Overall |
|------|-----------|----------|----------|:------------:|:------:|:-------:|:------:|:-----:|:------:|:-------:|
| c_087 | [Play](examples/c_087/c_ref_087.wav) | [Play](examples/c_087/c_sA_087.wav) | [Play](examples/c_087/c_sB_087.wav) | 5 | Neither (80.0%) | Neither (60.0%) | Neither (60.0%) | N/A | B (100.0%) | 75.0% (κ=0.2672) |
| c_256 | [Play](examples/c_256/c_ref_256.wav) | [Play](examples/c_256/c_sA_256.wav) | [Play](examples/c_256/c_sB_256.wav) | 5 | Neither (60.0%) | Tie A/B | A (60.0%) | N/A | Tie A/B | 60.0% (κ=-0.1364) |

### AM

| Case | Ref. | A | B | N | Melody | Harmony | Rhythm | Voice | Timbre | Overall |
|------|-----------|----------|----------|:------------:|:------:|:-------:|:------:|:-----:|:------:|:-------:|
| c_283 | [Play](examples/c_283/c_ref_283.wav) | [Play](examples/c_283/c_sA_283.wav) | [Play](examples/c_283/c_sB_283.wav) | 3 | Neither (100.0%) | A (66.7%) | A (100.0%) | Neither (66.7%) | A (66.7%) | 80.0% (κ=0.2857) |
| c_298 | [Play](examples/c_298/c_ref_298.wav) | [Play](examples/c_298/c_sA_298.wav) | [Play](examples/c_298/c_sB_298.wav) | 3 | B (100.0%) | B (100.0%) | A (66.7%) | A (100.0%) | A (100.0%) | 93.3% (κ=0.7321) |
