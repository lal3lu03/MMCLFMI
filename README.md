# MultiModel Contrastive Learning for Medical Images

This repository contains the code and documentation for the bachelor thesis project of Maximilian Hageneder, a student in Artificial Intelligence at the University of Linz. The project aims to utilize the MIMIC-CRX dataset for zero-shot image classification using CLIP and CLOOB models.

## Introduction

The objective of this project is to apply multi-model contrastive learning techniques, specifically CLIP and CLOOB, to the MIMIC-CRX dataset. The goal is to achieve similar results as the work conducted by Ekin Tiu et al. in their study called CheXzero.

## Acknowledgements

Special thanks to Elisabeth Rumetshofer ([GitHub](https://github.com/elirum)) and Andreas Fürst ([GitHub](https://github.com/fuersta)) for their contributions as bachelor thesis supervisors and for their work on the CLOOB repository. Their expertise and guidance were invaluable in the development of this project.


## Getting Started

To get started with this project, follow these steps:

1. Copy the MIMIC-CRX dataset to the `data/MIMIC_CRX` folder.
2. Run NegBio on the dataset to obtain labels for the classes. Instructions for running NegBio can be found in the `NegBio` folder.
3. Create a conda environment using the `environment.yml` file provided.
4. Run `converter.py` to convert DICOM images to JPEG format and save them in the `jpg` folder.
5. Proceed to run the visualization notebook (`visualization.ipynb`) and the metadata preprocessing notebook (`meta_data_pre.ipynb`). These notebooks generate the required data for further analysis and training.
6. Next, run the `embedding_cloob.ipynb` and `embedding_clip.ipynb` notebooks to obtain embeddings for the CLOOB and CLIP models, respectively.
7. Once the embeddings are generated, you can decide to perform a zero-shot classification based on the presence of findings or all symptoms. Adjust the parameters and follow the instructions in the respective notebook (`zero_shot_findings.ipynb` or `zero_shot_all_symptoms.ipynb`) to perform the zero-shot classification accordingly.

Please make sure to follow the instructions in each notebook carefully to ensure a successful execution.

## File Structure

The repository is structured as follows:

```
├── MultiModel_Contrastive_Learning_for_Medical_Imaging
│ ├── clip_
│ ├── data
│ │ ├── checkpoints
│ │ ├── csv
│ │ ├── embedding
│ │ ├── jpg
│ │ ├── MIMIC_CXR
│ │ └── model_config
│ ├── df_prepearing.ipynb
│ ├── preprocess_dicoms
│ ├── Visualization_preprocessing
│ └── Zero_shot
├── NegBio
└── readme.md
```

The `MultiModel_Contrastive_Learning_for_Medical_Imaging` directory contains the main project code, including folders for `clip_`, `data`, `preprocess_dicoms`, `Visualization_preprocessing`, and `Zero_shot`. The `NegBio` folder contains the code and instructions for running the NegBio NLP tool on the MIMIC-CRX dataset.

The `data` directory within the `MultiModel_Contrastive_Learning_for_Medical_Imaging` folder now includes subfolders for `checkpoints`, `csv`, `embedding`, `jpg`, `MIMIC_CXR`, and `model_config`. These subfolders are used for storing checkpoints, CSV files, embeddings, JPEG images, the MIMIC_CXR dataset, and model configurations, respectively. Please make sure to create these subfolders within the `data` directory and organize your files accordingly.

## Usage

Detailed instructions for running the different components of the project can be found within the respective notebooks and code files in the repository. Make sure to follow the instructions carefully to ensure a successful execution.

## References

- MIMIC-CRX Dataset: [Link](https://www.researchgate.net/publication/330552843_MIMIC-CXR_A_large_publicly_available_database_of_labeled_chest_radiographs)
- CLIP: [Link](https://arxiv.org/abs/2103.00020)
- CLOOB: [Link](https://arxiv.org/abs/2110.11316)
- NegBio: [Link](https://arxiv.org/abs/1712.05898)
- CheXzero: [Link](https://doi.org/10.1038/s41551-022-00936-9)

## Contact Information

For any questions or further information about this project, please contact [Maximilian Hageneder](mailto:max.hageneder@gmail.com).