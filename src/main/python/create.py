from common import run_pipeline
import copy


def handler(context, inputs):
    job_data = run_pipeline(context, inputs, inputs["creationPipeline"])
    outputs = copy.deepcopy(inputs)
    outputs['jobData'] = job_data
    outputs["jobId"] = job_data["id"]
    outputs["pipelineId"] = job_data["pipeline"]["id"]
    outputs["state"] = job_data["state"]
    outputs["result"] = job_data["result"]
    return outputs
