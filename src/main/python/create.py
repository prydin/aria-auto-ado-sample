from common import run_pipeline


def handler(context, inputs):
    run_pipeline(context, inputs, inputs["creationPipeline"])
    inputs["token"] = context.getSecret(inputs["pat"])
    return inputs
