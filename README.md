# JFROG Pipeline's YAML Generation Tool

This repository offers a tool to automate the generation of YAML configuration files for JFROG Pipelines. It provides an API endpoint to fetch the generated YAML based on user query.

## Prerequisites

Before getting started, ensure that both `conda` and `pip` are installed on your machine.

## Installation & Usage

Here's a step-by-step guide to setting up and running the tool:

### 1. Create a conda virtual environment:

```bash
conda create -n jfrog-llm
```

### 2. Activate the created environment:

```bash
conda activate jfrog-llm
```

### 3. Ensure `pip` is installed within the conda environment:

```bash
conda install -y pip
```

### 4. Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 5. Configure the OpenAI API:

Add your OPENAI API key to the `yaml_gen.py` file.

### 6. Start the API server:

```bash
uvicorn main:app --reload
```

### Testing the API:

You can test the API using the following `curl` command:

```bash
curl --location --request POST 'http://127.0.0.1:8000/getresponse' \
--header 'accept: application/json' \
--header 'Content-Type: application/json' \
--data-raw '{
  "query": "how to build a pipeline for docker build and publish"
}'
```

## Contributing

Your feedback is invaluable. If you encounter any issues or have suggestions, please open an issue or submit a pull request.