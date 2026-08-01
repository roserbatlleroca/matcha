# Participant Demographics

This folder contains the demographic breakdown of the final participant pool ($N = 83$) used in the perceptual experiment, as reported in the paper. Each CSV summarises responses to one section of the demographic survey (see Appendix A.2).

## Summary

The final sample was predominantly composed of men (60.2%), aged between 25 and 34 years (56.6%, mean age 31.3, median 29.5). Participants were geographically diverse, though most were based in Europe (68.7%), followed by Asia (14.5%); Spain and Germany were the two most represented countries individually (37.3% and 10.8%, respectively). Regarding musical expertise, the majority of participants fell into the two highest categories — *Trained Music Practitioner* and *Expert Music Professional* — together accounting for 63.8% of the sample, indicating that the target population of musically experienced listeners was successfully reached. Participants reported a variety of roles within the music field, most commonly music researcher (33.7%), musician/performer (32.5%), and sound engineer (20.5%).

### Note on Participant Screening

These figures reflect the **final, filtered** participant pool. Of 184 participants who accessed the experiment, 75 were excluded for incomplete case evaluation (0 or 1 case completed), 5 for low performance on the control case (≤0.25), and 21 for not completing any control case (due to submitting fewer than 10 evaluation cases). Full screening criteria are detailed in Appendix A.3. 

## Files

| File | Description |
|------|-------------|
| `age.csv` | Age range distribution, plus mean and median age (computed from range midpoints). |
| `gender.csv` | Gender distribution. |
| `continent.csv` | Continent of origin or residence. |
| `country.csv` | Country of origin or residence, with corresponding continent. |
| `music_level.csv` | Self-reported musical expertise level (see category definitions below). |
| `music_role.csv` | Self-reported role within the music field. |

Each file contains `count` and `percentage` columns computed over $N = 83$ valid participants.

## Musical Expertise Categories

Participants self-reported their musical background by selecting one of four categories, ordered by level of training and professional experience:

- **Engaged Music Listener**: No formal training, but attentive and regular listening with reliable ability to distinguish core musical elements.
- **Skilled Musician**: Self-directed or informal musical practice, active engagement through performance, production, or composition.
- **Trained Music Practitioner**: Formal training in music or a related field, solid theoretical and practical understanding.
- **Expert Music Professional** : Professional-level music studies and extensive training or professional experience.

