from common import Backend


def handler(context, inputs):
    backend = Backend(context.get_secret(inputs["ado_pat"]), inputs["org"], inputs["project"])
    if "customProperties" not in inputs:
        return
    cp = inputs["customProperties"]
    job_data = backend.get_job_data(cp["pipeline"]["id"], cp["id"])
    inputs["customProperties"] = job_data
    return inputs
