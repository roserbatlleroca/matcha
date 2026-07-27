# MATCHA: Music Attribute-based Triplet Comparison with Human Annotations

*Anonymous authors*

This repository is complementary to the paper *On the Human and Computer Aligment of Attribute-Based Music Matches*, currently under-review. It contains main documentation of the MATCHA dataset, as well as complemetary results of the perceptual experiment conducted in this study. We plan to provide additional materials upon paper acceptance, including a complete dataset datasheet. 

---
### Abstract

Recent advances in generative AI are raising ethical concerns regarding the originality of generated content and the potential replication of training data, with further implications for transparency, attribution, and intellectual property. In music, several computational approaches have been proposed to identify potential replication, using audio-based similarity metrics. Yet, their alignment with human judgments across distinct musical attributes remains underexplored. To address this gap, we conduct a perceptual experiment on music matches, defined as strongly similar musical excerpts. We focus on five musical attributes: melody, harmony, rhythm, voice, and timbre. We design a triplet-based forced-choice task comprising 300 cases, including plagiarism examples, cover songs, and AI-generated music. From this experiment, we introduce the MATCHA (Musical Attribute-based Triplet Comparison with Human Annotations) dataset: a collection of 1105 perceptual assessments of attribute-based music matches from 83 expert participants. Our findings reveal measurable agreement among participants in identifying matches across attributes. We further observe partial alignment between human judgments and computational similarity measures. Overall, this work underscores the importance of domain-specific and perceptually grounded evaluation frameworks for generative AI in creative practice.

### Dataset

MATCHA (Musical Attribute-based Triplet Comparison with Human Annotations) comprises 300 music triplets evaluated by 83 expert music participants as part of a forced-choice perceptual experiment. The dataset contains 1105 perceptual assessments of attribute-based musical similarity across five musical dimensions: melody, harmony, rhythm, voice, and timbre. It includes both human-composed and AI-generated musical excerpts, as summarised in the table below.

| Origin | Section | Source | Cases | w/ Vocals | % |
|--------|------|--------|------:|-------:|--:|
| Human | Human-Plagirism (HP) | [SMP Dataset](https://github.com/Mippia/Music-Plagiarism-Detection) | 75 | 61 | 25 |
| | Human-Version (HV) | [Discogs-VI](https://github.com/MTG/discogs-vi-dataset) | 75 | 63 | 25 |
| AI | AI-SAO (AS)| [Stable Audio Open](https://huggingface.co/stabilityai/stable-audio-open-1.0) | 120 | 0 | 40 |
| | AI-Media (AM) | Media Articles [[1](https://www.musicbusinessworldwide.com/suno-is-amusic-ai-company-aiming-to-generate-120-billion-peryear-newton-rex/),[2](https://www.gema.de/en/news/ai-and-music/ai-lawsuit/audio-samples-suno)] | 30 | 27 | 10 |

*Stimuli distribution across reference sources, by origin, section (Sec.), source name, number of cases, number of cases containing vocals, and overall percentage.*

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

