"""Project pipelines."""
from __future__ import annotations

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline
from .pipelines.model_training.pipeline import create_model_training_pipeline
from .pipelines.data_preprocessing.pipeline import create_data_preprocessing_pipeline


def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = find_pipelines()
    data_processing_pipeline = create_data_preprocessing_pipeline()
    model_train_pipeline = create_model_training_pipeline()

    return {
        "__default__": model_train_pipeline,
        "dp": data_processing_pipeline,
        "mt": model_train_pipeline,
    }
