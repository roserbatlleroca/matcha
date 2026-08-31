# MATCHA Dataset Datasheet

Documented in accordance with the *Datasheets for Datasets* framework ([Gebru et al., 2021](https://doi.org/10.1145/3458723)).

---

## 1. Motivation

### For what purpose was the dataset created?
The MATCHA dataset was created to support the evaluation of attribute-level musical similarity and assess the alignment between human perception and computational similarity metrics in the context of music replication assessment (e.g., AI-generated music, cover songs, plagiarism). It addresses the gap where human judgments across distinct musical attributes (melody, harmony, rhythm, voice, timbre) remain underexplored.

### Who created this dataset?
MATCHA was created by Roser Batlle-Roca<sup>1</sup>, Woosung Choi<sup>2</sup>, Joan Serrà<sup>2</sup>, Fabio Morreale<sup>2</sup>, Wei-Hsiang Liao<sup>2</sup>, Xavier Serra<sup>1</sup>, Emilia Gómez<sup>1,3</sup>, and Yuki Mitsufuji<sup>2,4</sup>

(1) Music Technology Group, Universitat Pompeu Fabra (MTG-UPF); (2) Sony AI; (3) Joint Research Centre, European Commission; (4) Sony Group Corporation

### Who funded the creation of the dataset?
This dataset was developed under [the TRAMUCA project](https://www.upf.edu/web/mtg/ongoing-projects/-/asset_publisher/DneGVrJZ7tmE/content/transparency-in-music-creation-algorithms/maximized), a joint collaboration between the Music Technology Group (Universitat Pompeu Fabra), Sony AI and the European Commission's Joint Research Centre. 

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
The dataset is self-contained for research use, but derives from external sources. The audio clips originate from externalsources (SMP dataset, Discogs-VI, Free Music Archive, and media reports). To avoid reliance on fragile external links, all audio excerpts, annotations, and metadata are packaged together and hosted on Zenodo under restricted research access managed by the MTG-UPF.

### Does the dataset contain data that might be considered confidential? 
No.  

### Does the dataset contain data that might be offensive, insulting, threatening, or cause anxiety?
No.  

### Does the dataset relate to people?
Yes. It involves human annotators who evaluated the triplets, as well as the original artists and composers of the evaluated tracks.  

### Does the dataset identify any subpopulations?
Yes. Demographic data on participants was collected, including age, gender, country of origin or residence, role within the music industry and self-reported musical background by selecting one out of four categories. 

### Is it possible to identify individuals from the dataset?
Annotators: No, participants were assigned random alphanumeric IDs and cannot be identified.  
Artists: Publicly named artists and composers appear in the metadata for commercial songs.  

### Does the dataset contain sensitive data?
No.  

### Any other comments?
None.


---

## 3. Collection Process

### How was the data acquired?
* **Audio excerpts:** Extracted using MIR toolkits (`madmom` for beat tracking, `Essentia` for chroma and MFCC features) for HV pairs, and conditional diffusion modelling (Stable Audio Open with prompts extracted via Music Flamingo and Qwen 3.5) for AS triplets.
* **Perceptual annotations:** Directly reported by expert participants using a custom web-based forced-choice triplet task.

### What mechanisms or procedures were used to collect the data?
Data was collected via a custom web application. Quality control was enforced using **30 control cases (10% of total cases)**. Participants scoring $\le 0.25$ in ground-truth agreement were excluded.

### If the dataset is a sample from a larger set, what was the sampling strategy?
Manually curated selection. Human pairs were drawn from established plagiarism (SMP) and version (Discogs-VI) datasets. AS cases were generated under controlled conditions ("more similar" via DDIM inversion, and "less similar" via prompt conditioning).

### Who was involved in the data collection process and how were they compensated?
Voluntary participants were recruited via music mailing lists, online communities, and professional networks. Participants who completed at least 10 cases were eligible to opt into a prize draw for four €25 vouchers. In total, 184 people accessed the experiment.

### Over what timeframe was the data collected?
Annotations were collected over approximately 2 months (March 10 to May 11, 2026).

### Were any ethical review processes conducted?
Yes, reviewed and approved by the [Institutional Committee for Ethical Review of Projects](https://www.upf.edu/web/cirep/) from Universitat Pompeu Frabra before relase. 

Does the dataset relate to people?
Yes. 

### Did you collect the data from the individuals in question directly, or obtain it via third parties?
Annotations were collected directly from participants.
Audio source metadata was obtained from third-party public datasets and web sources.

### Were the individuals in question notified about the data collection?
Yes, participants were provided with detailed information on the experiment purpose, task and general instructions upon accessing the web application. 

### Did the individuals in question consent to the collection and use of their data?
Yes, participants answered an informed consent prior to participation in the experiment. 

### If consent was obtained, were consenting individuals provided with a mechanism to revoke their consent?
Yes, participants could pause, quit, or resume at any time. Moreover, data protection information included contact information to address any further request. 

### Has an analysis of the potential impact of the dataset on data subjects been conducted?
Participating in the study did not entail risks greater than those ordinarily encountered in daily life. 

### Any other comments?
None. 


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

### Any other comments?
None. 

---

## 5. Uses

### Has the dataset been used for any tasks already?
Yes, it was used to analyze human inter-annotator agreement across musical attributes and to evaluate the alignment of computational similarity metrics in the MiRA framework (CoverID, KL divergence, CLAP, Discogs-EffNet) against human perception.

### Is there a repository that links to any or all papers or systems that use the dataset?
Yes: [https://github.com/roserbatlleroca/matcha](https://github.com/roserbatlleroca/matcha)

### What (other) tasks could the dataset be used for?
Benchmarking MIR similarity algorithms, evaluating generative music models, training attribute-specific similarity models, and conducting music perception research.

### Is there anything about the composition or collection that might impact future uses?
The dataset focuses on strongly matching music pairs within Western music traditions. Annotator consensus levels observed here may not generalise to arbitrary song pairs or non-Western musical genres

### Are there tasks for which the dataset should not be used?
It should not be used as an final legal decision or definitive evidence for copyright infringement or plagiarism disputes.

### Any other comments?
None. 

---

## 6. Distribution

### Will the dataset be distributed to third parties outside of the entity?
Yes, publicly available to the research community.

### How will the dataset be distributed?

| Component | Distribution Channel | License / Access Terms |
| :--- | :--- | :--- |
| **Metadata & Annotations** | GitHub Repository | Publicly available |
| **Commercial Audio (HP, HV, AM)** | Restricted | Restricted due to original copyright restrictions |
| **Stable Audio (AS) Audio Files** | Zenodo | CC-BY-NC 4.0 *(upon paper acceptance)* |


When will the dataset be distributed?}
Complete public release following paper acceptance.

### Will the dataset be distributed under a copyright or IP license, and/or Terms of Use?
Metadata and annotations are publicly available in the GitHub repository with corresponding license. The Stable Audio Open (AS) audio subset will be released under Creative Commons Attribution-NonCommercial (CC-BY-NC 4.0) upon paper acceptance. 

### Have any third parties imposed IP-based or other restrictions on the data?
Commercial audio tracks referenced in human and media subsets are subject to original copyright holders' terms. 

### Do any export controls or other regulatory restrictions apply?
None. 

### Any other comments?
None. 

---

## 7. Maintenance

### Who will be supporting/hosting/maintaining the dataset?
The dataset is supported by the MTG-UPF. 

### How can the owner/curator/manager of the dataset be contacted?
Roser Batlle-Roca is the responisble for this dataset and may be contacted at roser.batlle@upf.edu. 

### Is there an erratum?
None currently. An erratum will be provided in the GitHub repository if necessary. 

### Will the dataset be updated?
Updates will be communicated via the GitHub repository.

### If the dataset relates to people, are there applicable limits on the retention of the data?
No personal identification data was collected or stored.

### Will older versions of the dataset continue to be supported/hosted/maintained?
Older versions of the dataset will continue to be hosted in GitHub and Zenodo.

### If others want to extend/augment/build on/contribute to the dataset, is there a mechanism for them to do so?
No. 

### Any other comments?
None. 