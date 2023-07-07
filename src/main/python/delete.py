import os

from common import run_pipeline


def handler(context, inputs):
    return run_pipeline(context, inputs, inputs["deletionPipeline"])
    return inputs
