# WHO LBM v8 manual double-check

## Check Results

| Check | Status | Detail |
|---|---|---|
| A4-2 row count | PASS | rows=22 |
| A4-2 category first row | PASS | ['Faulty design or construction', '', ''] |
| A4-2 domestic refrigerator split | PASS | ['Explosion in domestic-', 'Dangerous chemical not', '• Store low-flashpoint solvents'] |
| A4-2 fire photometer split | PASS | ['Fire in flame', 'Incorrect reassembly of', '• Train and supervise staff.'] |
| A5-1 no index overcapture | PASS | rows=701 |
| A5-1 Acetaldehyde split | PASS | ['Acetaldehyde', 'Colourless liquid or', 'Mild eye and', 'Extremely flammable;', 'No open flames, no', 'Can form explosive'] |
| Chapter 9 title phrase kept | PASS | present expected phrase |
| Chapter 9 no double-space title deletion | PASS | no The  has |
| Known detergent continuation fixed | PASS | detergent sentence present |
| Heading present: Access | PASS | heading lookup |
| Heading present: Personal protection | PASS | heading lookup |
| Heading present: Infectious materials | PASS | heading lookup |
| Heading present: Chemicals and radioactive substances | PASS | heading lookup |
| Lowercase infectious materials not used as heading | PASS | heading lookup |
| No C:Users in manifest.yaml | PASS | absolute path check |
| No tab in manifest.yaml | PASS | tab check |
| No trailing spaces in manifest.yaml | PASS | trailing=[] |
| No C:Users in who_lbm_3rd_2004_9241546506.meta.yaml | PASS | absolute path check |
| No tab in who_lbm_3rd_2004_9241546506.meta.yaml | PASS | tab check |
| No trailing spaces in who_lbm_3rd_2004_9241546506.meta.yaml | PASS | trailing=[] |
| No C:Users in who_lbm_3rd_2004_9241546506.parser_profile.yaml | PASS | absolute path check |
| No tab in who_lbm_3rd_2004_9241546506.parser_profile.yaml | PASS | tab check |
| No trailing spaces in who_lbm_3rd_2004_9241546506.parser_profile.yaml | PASS | trailing=[] |
| No C:Users in who_lbm_3rd_2004_9241546506.regdoc_ir.yaml | PASS | absolute path check |
| No tab in who_lbm_3rd_2004_9241546506.regdoc_ir.yaml | PASS | tab check |
| No trailing spaces in who_lbm_3rd_2004_9241546506.regdoc_ir.yaml | PASS | trailing=[] |
| No C:Users in who_lbm_3rd_2004_9241546506.regdoc_profile.yaml | PASS | absolute path check |
| No tab in who_lbm_3rd_2004_9241546506.regdoc_profile.yaml | PASS | tab check |
| No trailing spaces in who_lbm_3rd_2004_9241546506.regdoc_profile.yaml | PASS | trailing=[] |
| No C:Users in GOAL_CHECK.md | PASS | absolute path check |
| No tab in GOAL_CHECK.md | PASS | tab check |
| No trailing spaces in GOAL_CHECK.md | PASS | trailing=[] |
| No C:Users in SPECIAL_STRUCTURE_AUDIT.md | PASS | absolute path check |
| No tab in SPECIAL_STRUCTURE_AUDIT.md | PASS | tab check |
| No trailing spaces in SPECIAL_STRUCTURE_AUDIT.md | PASS | trailing=[] |

## Reconstructed Table A4-2 Sample

| Accident | Accident cause | Reducing or eliminating the hazard |
| --- | --- | --- |
| Faulty design or construction |  |  |
| Electrical fires in | No over-temperature cut-out | • Compliance with national |
| incubators |  | standards. |
| Electrical shock | Failure to provide reliable |  |
|  | earthing/grounding |  |
| Improper use |  |  |
| Centrifuge accident | Failure to balance buckets | • Train and supervise staff. |
|  | on swing-out rotors |  |
| ... | ... | ... |
|  | leaking screw cap |  |
| Lack of proper maintenance |  |  |
| Fire in flame | Incorrect reassembly of | • Train and supervise staff. |
| photometer | components during |  |
|  | maintenance |  |

## Reconstructed Table A5-1 Sample

| Chemical | Physical properties | Health hazards | Fire hazards | Safety precautions | Incompatible chemicals / other hazards |
| --- | --- | --- | --- | --- | --- |
| Acetaldehyde | Colourless liquid or | Mild eye and | Extremely flammable; | No open flames, no | Can form explosive |
| CH3CHO | gas with a pungent, | respiratory tract | vapour/air mixtures | sparks, no smoking, | peroxides in contact |
|  | fruity odour; | irritation. Effects on | are explosive; | no contact with hot | with air. May polymerize |
|  | m.p. –121 °C | the central nervous | flash point –39 °C | surfaces. Store in | under influence of acids, |
|  | b.p. 21 °C. | system, respiratory | flammable range | tightly sealed | alkaline materials, in |
|  |  | tract and kidneys. | 4–57%. | containers in areas | the presence of trace |
|  |  | Possible carcinogen. |  | separate from | metals. A strong |
|  |  |  |  | oxidizers; store only if | reducing agent, reacts |
| ... | ... | ... | ... | ... | ... |
|  |  | the skin. Non-specific |  |  |  |
|  |  | neurological impairment. |  |  |  |
|  |  | Exposure may enhance |  |  |  |
|  |  | hearing damage caused |  |  |  |
|  |  | by exposure to noise. |  |  |  |
|  |  | Animal tests suggest |  |  |  |
|  |  | toxicity to human repro- |  |  |  |
|  |  | duction or development. |  |  |  |

## Verdict

PASS
