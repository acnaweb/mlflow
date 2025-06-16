import os
import uuid

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

import mlflow
import mlflow.sklearn
from mlflow.entities import Dataset

tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000/")


# Helper function to compute metrics
def compute_metrics(actual, predicted):
    rmse = mean_squared_error(actual, predicted)
    mae = mean_absolute_error(actual, predicted)
    r2 = r2_score(actual, predicted)
    return rmse, mae, r2


def run():

    # Load Iris dataset and prepare the DataFrame
    iris = load_iris()
    iris_df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
    iris_df["quality"] = (iris.target == 2).astype(
        int
    )  # Create a binary target for simplicity

    # Split into training and testing datasets
    train_df, test_df = train_test_split(iris_df, test_size=0.2, random_state=42)

    mlflow.set_tracking_uri(tracking_uri)
    # Start a run to represent the training job
    run_name = f"run-${uuid.uuid4()}"
    with mlflow.start_run(run_name=run_name):
        # Load the training dataset with MLflow.
        # We will link training metrics to this dataset.
        train_dataset: Dataset = mlflow.data.from_pandas(train_df, name="train")
        train_x = train_dataset.df.drop(["quality"], axis=1)
        train_y = train_dataset.df[["quality"]]

        # Fit a model to the training dataset
        lr = ElasticNet(alpha=0.5, l1_ratio=0.5, random_state=42)
        lr.fit(train_x, train_y)

        # Log the model, specifying its ElasticNet parameters (alpha, l1_ratio)
        # As a new feature, the LoggedModel entity is linked to its name and params
        model_info = mlflow.sklearn.log_model(
            sk_model=lr,
            name="elasticnet",
            params={
                "alpha": 0.5,
                "l1_ratio": 0.5,
            },
            input_example=train_x,
        )

        # Inspect the LoggedModel and its properties
        logged_model = mlflow.get_logged_model(model_info.model_id)
        print(logged_model.model_id, logged_model.params)

        # Evaluate the model on the training dataset and log metrics
        # These metrics are now linked to the LoggedModel entity
        predictions = lr.predict(train_x)
        (rmse, mae, r2) = compute_metrics(train_y, predictions)
        mlflow.log_metrics(
            metrics={
                "rmse": rmse,
                "r2": r2,
                "mae": mae,
            },
            model_id=logged_model.model_id,
            dataset=train_dataset,
        )

        # Inspect the LoggedModel, now with metrics
        logged_model = mlflow.get_logged_model(model_info.model_id)
        print(logged_model.model_id, logged_model.metrics)
