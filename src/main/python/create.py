from common import run_pipeline


def handler(context, inputs):
    job_data = run_pipeline(context, inputs, inputs["creationPipeline"])
    inputs["jobData"] = job_data
    return inputs
