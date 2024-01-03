"""Project pipelines."""
from __future__ import annotations

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline
from .pipelines.model_training import regressor_pipeline
from .pipelines.model_training import tensorflow_pipeline
from .pipelines.data_preprocessing.standard_preprocessing_pipeline import (
    create_data_preprocessing_pipeline,
)
from .pipelines.data_preprocessing.tensorflow_prep_pipeline import (
    create_tensor_flow_prep_pipeline,
)


def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = find_pipelines()
    data_processing_pipeline = create_data_preprocessing_pipeline()
    model_train_pipeline = regressor_pipeline.create_model_training_pipeline()
    tensorflow_prep_pipeline = create_tensor_flow_prep_pipeline()
    tensorflow_train_pipeline = tensorflow_pipeline.create_model_training_pipeline()

    return {
        "__default__": model_train_pipeline,
        "data_processing": data_processing_pipeline,
        "model_train": model_train_pipeline,
        "tf_prep": tensorflow_prep_pipeline,
        "tf_train": tensorflow_train_pipeline,
    }
