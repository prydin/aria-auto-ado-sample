import copy

from common import run_pipeline


def handler(context, inputs):
    new_inputs = copy.deepcopy(inputs)
    del new_inputs["parameters"]
    new_inputs["variables"] = {
        "tfm.airid": {"value": inputs["parameters"]["airid"]},
        "tfm.project_name": {"value": inputs["parematers"]["project_name"]},
        "tfm.service_name": inputs["serviceName"]
    }
    return run_pipeline(context, new_inputs, inputs["deletionPipeline"])
    return inputs # Yes, inputs! We want to return the original data
