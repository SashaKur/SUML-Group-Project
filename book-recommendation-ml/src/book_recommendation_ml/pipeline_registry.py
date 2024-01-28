"""Project pipelines."""
from __future__ import annotations

from kedro.framework.project import find_pipelines
from kedro.pipeline import Pipeline
from .pipelines.data_preprocessing import preprocessing_pipeline
from .pipelines.model_bulding import collab_filtering_pipeline
from .pipelines.model_bulding import popularity_pipeline

from .pipelines.data_preprocessing.preprocessing_pipeline import create_preprocessing_pipeline
from .pipelines.model_bulding.collab_filtering_pipeline import create_model_pipeline
from .pipelines.model_bulding.popularity_pipeline import create_popularity_books_pipeline



def register_pipelines() -> dict[str, Pipeline]:
    """Register the project's pipelines.

    Returns:
        A mapping from pipeline names to ``Pipeline`` objects.
    """
    pipelines = find_pipelines()
    data_processing_pipeline = create_preprocessing_pipeline()
    model_build_pipeline = create_model_pipeline()
    popularity_model_pipeline = create_popularity_books_pipeline()

    return {
        "__default__": collab_filtering_pipeline,
        "data_processing": data_processing_pipeline,
        "model_build": model_build_pipeline,
        "popular_books": popularity_model_pipeline
    }
