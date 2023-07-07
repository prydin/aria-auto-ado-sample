from common import run_pipeline


def handler(context, inputs):
    job_data = run_pipeline(context, inputs, inputs["creationPipeline"])
    return {
        "customProperties": job_data,
        "jobId": job_data["id"],
        "pipelineId": job_data["pipeline"]["id"],
        "state": job_data["state"],
        "result": job_data["result"]
    }
