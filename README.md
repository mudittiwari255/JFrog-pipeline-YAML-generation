# JFROG Pipeline's YAML Generation

This repository provides a solution to generate YAML files for JFROG Pipelines.

## Prerequisites

Ensure you have `conda` and `pip` installed on your machine.

## Setup and Run

Follow these steps to set up and run the API:

### 1. Create a conda virtual environment

```bash
conda create -n jfrog-llm
```

### 2. Activate the conda environment

```bash
conda activate jfrog-llm
```

### 3. Install pip in the conda environment

```bash
conda install -y pip
```

### 4. Install the necessary Python packages

```bash
pip install -r requirements.txt
```

### 5. Add OPENAI API Key in yaml_gen.py file.

### 6. Run the API

```bash
uvicorn main:app --reload
```

## Feedback

If you have any issues or suggestions, feel free to open an issue or a pull request.

