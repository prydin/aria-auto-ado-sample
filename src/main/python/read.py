from common import Backend


def handler(context, inputs):
    backend = Backend(context.get_secret(inputs["ado_pat"]), inputs["org"], inputs["project"])
    inputs["jobData"] = backend.get_job_info()
