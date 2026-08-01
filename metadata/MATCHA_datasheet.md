# MATCHA Dataset — Datasheet

> **Musical Attribute-based Triplet Comparison with Human Annotations**  
> Documented in accordance with the *Datasheets for Datasets* framework ([Gebru et al., 2021](https://doi.org/10.1145/3458723)).

---

## 1. Motivation

### For what purpose was the dataset created?
The MATCHA dataset was created to support the evaluation of attribute-level musical similarity and assess the alignment between human perception and computational similarity metrics in the context of music replication assessment (e.g., AI-generated music, cover songs, plagiarism). It addresses the gap where human judgments across distinct musical attributes (melody, harmony, rhythm, voice, timbre) remain underexplored.

### Who created this dataset?
*[Anonymised response]*

### Who funded the creation of the dataset?
*[Anonymised response]*

### Any other comments?
None.

---

## 2. Composition

### What do the instances that comprise the dataset represent?
Each instance represents an audio triplet (case) consisting of one reference audio excerpt and two comparison audio excerpts (**A** and **B**). All samples are approximately 10 seconds long. Excerpt durations vary slightly, as boundaries were adjusted to preserve musical coherence, melodic lines, and phrase structures, ensuring that the musical attribute under evaluation is complete and not interrupted mid-phrase.

Annotations represent perceptual human judgments comparing whether sample A or sample B best matches the reference across five distinct musical attributes: **melody, harmony, rhythm, voice, and timbre**.

### How many instances are there in total?
There are **300 audio triplets** in total:
* **150 Human-composed triplets:**
  * 75 from the SMP (*Segment-based Music Plagiarism*) dataset (Go et al., 2026), containing detected pairs of musical plagiarism.
  * 75 from Discogs-VI (Araz et al., 2024), a collection of musical versions.
* **150 AI-generated triplets:**
  * 120 generated with Stable Audio Open (Evans et al., 2025).
  * 30 sourced from media articles documenting potential AI plagiarism cases (Newton-Rex, 2024; GEMA, 2024).

The dataset contains **1,105 attribute-level perceptual evaluations** collected from **83 expert participants** (an average of ~3.7 evaluations per triplet).

### Does the dataset contain all possible instances or is it a sample?
It is a curated sample specifically selected to contain strong similarity relationships across Western music genres, such as rock, pop, jazz, and electronic.

### What data does each instance consist of?
Audio metadata, timestamp boundaries for 10-second excerpts, triplet composition details, raw human annotations, and aggregated preference scores. Direct audio files for commercial tracks are restricted due to copyright, though metadata and annotations are publicly available.

### Is there a label or target associated with each instance?
Yes. Each instance contains participant choice selections for each attribute (selecting **A**, **B**, or **Neither**) and an aggregated normalized preference score $s$ calculated as:

$$s = \frac{n_B - n_A}{n_A + n_B + n_N}$$

*Where $s \in [-1, +1]$, ranging from -1 (strong preference for sample A) to +1 (strong preference for sample B).*

### Is any information missing from individual instances?
Raw audio files for copyrighted commercial songs are restricted due to licensing restrictions. Only the AS (Audio Sub-subset) will be released under CC-BY-NC following paper acceptance, in compliance with the Stable Audio license.

### Are relationships between individual instances made explicit?
Yes. Within each triplet, explicit relationships link the reference track to comparison tracks A and B (e.g., cover version, same artist, different section of the same track, AI generation via DDIM inversion, or style match). Such information is detailed in the cases metadata.

### Are there recommended data splits?
No explicit training/validation/testing splits are provided, as the dataset is intended purely as an evaluation benchmark.

### Are there any errors, sources of noise, or redundancies?
* 6 out of 300 cases (2% of the dataset) resulted in ties across annotations.
* The AS subset exhibited high perceptual ambiguity due to acoustic artifacts introduced during diffusion generation, leading to near-chance agreement among raters and high selection rates of *Neither* (52% to 64%).

### Is the dataset self-contained, or does it rely on external resources?
The dataset relies on external audio sources (SMP dataset, Discogs-VI, Free Music Archive, and media reports). Because raw audio for commercial tracks is not hosted directly, external audio links cannot be guaranteed long-term.

### Confidentiality & Safety
* **Contains confidential data?** No.
* **Contains offensive content?** No.
* **Relates to people?** Yes. It involves human annotators who evaluated the triplets, as well as the original artists and composers of the evaluated tracks.
* **Identifies subpopulations?** Yes. Demographic data on participants was collected, including age, gender, country of origin/residence, role within the music industry, and self-reported musical background across four categories.
* **Identifiable individuals?** 
  * *Annotators:* No, participants were assigned random alphanumeric IDs.
  * *Artists:* Publicly named artists and composers appear in the metadata for commercial songs.
* **Contains sensitive data?** No.

---

## 3. Collection Process

### How was the data acquired?
* **Audio excerpts:** Extracted using MIR toolkits (`madmom` for beat tracking, `Essentia` for chroma and MFCC features) for HV pairs, and conditional diffusion modelling (Stable Audio Open with prompts extracted via Music Flamingo and Qwen 3.5) for AS triplets.
* **Perceptual annotations:** Directly reported by expert participants using a custom web-based forced-choice triplet task.

### Collection mechanisms & Quality Control
Data was collected via a custom web application. Quality control was enforced using **30 control cases (10% of total cases)**. Participants scoring $\le 0.25$ in ground-truth agreement were excluded.

### Sampling strategy
Manually curated selection. Human pairs were drawn from established plagiarism (SMP) and version (Discogs-VI) datasets. AS cases were generated under controlled conditions ("more similar" via DDIM inversion, and "less similar" via prompt conditioning).

### Participants & Compensation
Voluntary participants were recruited via music mailing lists, online communities, and professional networks. Participants who completed at least 10 cases were eligible to opt into a prize draw for four €25 vouchers. In total, 184 people accessed the experiment.

### Collection Timeframe
Annotations were collected over approximately 2 months (**March 10 to May 11, 2026**).

### Ethical Reviews & Consent
* **Ethical Review:** Reviewed and approved by the *[Anonymised Ethical Committee]* from *[Anonymised University]* prior to release.
* **Consent:** Participants answered an informed consent form before participating and were provided with detailed instructions on experiment purpose and tasks.
* **Revocation:** Participants could pause, quit, or resume at any time. Contact information was provided for data requests.
* **Risk Assessment:** Participation did not entail risks greater than those ordinarily encountered in daily life.

---

## 4. Preprocessing, Cleaning, & Labeling

### Was any preprocessing/cleaning/labeling done?
* Audio files were trimmed to ~10-second excerpts with boundaries adjusted to maintain musical coherence.
* Low-quality participant data was filtered out (excluding raters scoring $\le 0.25$ on control cases).
* Annotator choices were aggregated into normalized preference scores $s$.

### Was "raw" data saved?
Yes, raw individual annotator selections and case metadata are preserved in the repository.

### Is preprocessing software available?
Yes, preliminary processing scripts and code are provided in the repository. Complete processing pipelines will be made available upon paper acceptance.

---

## 5. Dataset Uses

### Has the dataset been used for any tasks already?
Yes, it was used to analyze human inter-annotator agreement across musical attributes and to evaluate the alignment of computational similarity metrics in the MiRA framework (CoverID, KL divergence, CLAP, Discogs-EffNet) against human perception.

### Repository Link
[https://anonymous.4open.science/r/matcha-aisi](https://anonymous.4open.science/r/matcha-aisi)

### Recommended Tasks
* Benchmarking Music Information Retrieval (MIR) similarity algorithms.
* Evaluating generative music models.
* Training attribute-specific similarity models.
* Conducting music perception research.

### Limitations & Impact on Future Use
* The dataset focuses on strongly matching music pairs within Western music traditions. Annotator consensus levels observed here may not generalize to arbitrary song pairs or non-Western musical genres.
* **Prohibited Use:** This dataset **should not** be used as a final legal decision or definitive evidence for copyright infringement or plagiarism disputes.

---

## 6. Distribution

### Distribution Channel & Licensing

| Component | Distribution Channel | License / Access Terms |
| :--- | :--- | :--- |
| **Metadata & Annotations** | GitHub Repository | Publicly available |
| **Stable Audio (AS) Audio Files** | Zenodo | CC-BY-NC 4.0 *(upon paper acceptance)* |
| **Commercial Audio (HP, HV, AM)** | Restricted | Restricted due to original copyright restrictions |

### Release Timeline
Complete public release will follow paper acceptance. No export controls or additional regulatory restrictions apply.

---

## 7. Maintenance

### Support & Contact
* **Maintainer:** *[Anonymised response]*
* **Contact:** *[Anonymised response]*

### Versioning & Errata
* **Errata:** None currently. Any future errata will be documented in the GitHub repository.
* **Updates:** Updates will be communicated via the GitHub repository. Older versions of the dataset will continue to be hosted on GitHub and Zenodo.