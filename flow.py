import asyncio
import json
import os
from datetime import timedelta
from time import sleep
from typing import Any, List

import boto3
import pandas as pd
from botocore.exceptions import ClientError, NoCredentialsError
from prefect import flow, tags, task
from prefect.artifacts import create_markdown_artifact, create_table_artifact
from prefect.logging import get_run_logger
from prefect.tasks import exponential_backoff, task_input_hash
from pydantic import BaseModel, Field

import random


class Animal(BaseModel):
    name: str = Field(..., description="Name of the animal")
    weight: float = Field(..., description="Weight of the animal in kg")
    speed: float = Field(..., description="Maximum speed of the animal in km/h")


def download_object_and_parse(bucket_name, object_name):
    # Create an S3 client
    s3_client = boto3.client(
        "s3",
    )

    try:
        # Download the object content
        object_content = s3_client.get_object(Bucket=bucket_name, Key=object_name)
        json_content = object_content["Body"].read()

        # Parse the JSON content into a Python dictionary
        data = json.loads(json_content)
        return pd.DataFrame(data)

    except NoCredentialsError:
        print("Credentials not available")
        return None
    except ClientError as e:
        print(f"An AWS Client error occurred: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def avg_weight(df: pd.DataFrame) -> float:
    # 1. Calculate the average weight of animals
    return df["weight"].mean().round(2)


def fastest_animal(df: pd.DataFrame) -> str:
    # 2. Find the fastest animal and its speed
    sleep(2)
    return df.loc[df["speed"].idxmax()]["name"]


def top_speed(df: pd.DataFrame) -> float:
    return df["speed"].max()


def combine(
    avg_weight: float,
    fastest_animal: str,
    fastest_speed: float,
) -> dict[str, Any]:
    return {
        "Average Weight in Lbs": avg_weight,
        "Fastest Animal": fastest_animal,
        "Speed of Fastest Animal": fastest_speed,
    }


def animal_data(artifact_title: str = "Animal Insights", example_bool: bool = True):
    df = download_object_and_parse("se-demo-raw-data-files", "demo/animals.json")
    insights = combine(
        avg_weight(df),
        fastest_animal(df),
        top_speed(df),
    )


if __name__ == "__main__":
    animal_data()
