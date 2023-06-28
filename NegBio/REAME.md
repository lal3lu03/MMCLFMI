# NegBio

The NegBio folder contains code and instructions for running the NegBio NLP tool on the MIMIC-CXR dataset.

## Requirements

Before using NegBio, ensure the following requirements are met:

1. Sectioned report CSVs: Generate sectioned report CSVs using the `create_section_files.py` script. Refer to the [txt folder](/txt/) for detailed instructions.
   - Note the path containing the CSVs, for example: `/data/mimic-cxr/sections`. This folder should contain 22 files with filenames like `mimic_cxr_000.csv`, `mimic_cxr_001.csv`, and so on.

2. Conda environment: NegBio utilizes the `conda` package manager to create a virtual environment for running the code. To use `conda`, you need to install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/). Miniconda is a lightweight alternative to Anaconda.

## Installation

Follow these steps to install NegBio:

1. Open a terminal in the NegBio folder.

2. Create the virtual environment:

   ```bash
   conda env create -f NegBio_env.yml
   ```

3. Copy the MIMIC-CXR specific NegBio code:

   ```bash
   git clone --single-branch --branch MIMIC-CXR https://github.com/ncbi-nlp/NegBio.git negbio-mimic-cxr
   ```

4. For reproducibility, checkout the exact commit hash of NegBio used to generate these labels:

   ```bash
   cd negbio-mimic-cxr
   git checkout 962690b6789920fb0abab4fe05fc8ce6bc1a349d
   cd ..
   ```

5. Run the bash script that calls NegBio. The first argument should be the location of the sectioned files, and the second argument should be the path to NegBio on the MIMIC-CXR branch.
   - The script loops through each file in the specified `BASE_FOLDER`.
   - NegBio is executed on files that match the pattern `mimic_cxr_####.csv`.
   - The results are output to `BASE_FOLDER/mimic_cxr_####/`, where the folder name corresponds to the file name (excluding the .csv extension).

**Warning: Running this on the entire MIMIC-CXR dataset will consume approximately 15 GB of disk space.**

```bash
bash run_negbio_on_files.sh /db/mimic-cxr/sections negbio-mimic-cxr
```

Please exercise caution when executing this script due to the disk space requirements.