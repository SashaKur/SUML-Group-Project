# Book recommendation system
SUML Group #4 Project \
Made by Polina Lysenko, Dominic Dąbrowski, Oleksandr Kurchak, Andrii Mostovyi

## Dataset
[Book recommendation system](https://www.kaggle.com/code/midouazerty/book-recommendation-system-with-machine-learning)

## Overview

Book recommendation system that implements several methods for book prediction such as collaborative filtering and popularity approach.

## Project Structure

The project structure follows the Kedro template and is organized as follows:

```bash
├───conf/
├───data/
│   ├───01_raw/
│   ├───02_intermediate/
│   ├───03_primary/
│   ├───04_feature/
│   ├───05_model_input/
│   ├───06_models/
│   ├───07_model_output/
│   └───08_reporting/
├───notebooks/
├───src/
|   ├───book_recommendation_ml/
|   │   ├───pipelines/
|   │   │   ├───data_preprocessing/
|   │   │   └───model_bulding/
|   └───tests/
├── .gitignore
└── pyproject.toml
```

- `conf`: Configuration files.
- `data`: Raw and processed data.
- `src`: Source code.
  - `book_recommendation_ml`: Main module for book recommendation model.
    - `pipelines`: Folder containing all the pipelines.
        - `data_preprocessing`: Folder containing data processing pipeline along with its nodes
        - `model_building`: Folder containing model building pipelines along with their nodes
    - `pipeline_registry.py`: Code for registering and mapping pipelines
- `tests`: Unit tests for the project.
- `.gitignore`: Git ignore file.
- `pyproject.toml`: Project metadata and dependencies.

## Getting Started

### Prerequisites

Make sure you have Python and Kedro installed. You can install Kedro using the following:

```bash
pip install kedro
```
### Installation

1. Clone the repository
```bash
git clone https://github.com/SashaKur/SUML-Group-Project.git
```
2. Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

To run pipelines, use the following commands:
```bash
kedro run
```
To execute separate pipelines, use the following commands:
```bash
kedro run --pipeline=data_processing // For data processing
kedro run --pipeline=model_build // For collaborative filtering model
kedro run --pipeline=popular_books // For getting books based on popularity
```
