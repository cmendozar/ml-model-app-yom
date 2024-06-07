import os
import neptune

model_version = neptune.init_model_version(
    model="YOM-PRODML",
    project=os.environ.get("NEPTUNE_PROJECT"),
    api_token=os.environ.get("NEPTUNE_API_TOKEN"),
)
