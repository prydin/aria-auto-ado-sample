import base64
import yaml
import time

import requests


class Job:
    def __init__(self, backend, job_data):
        self.backend = backend
        self.job_data = job_data

    def refresh(self):
        id = self.job_data["id"]
        pipeline_id = self.job_data['pipeline']['id']
        self.job_data = self.backend.get(f"/pipelines/{pipeline_id}/runs/{id}")

    def get_state(self):
        self.refresh()
        return self.job_data["state"]

    def wait_for_completion(self):
        while self.get_state() == "inProgress":
            time.sleep(5)
        return self.job_data["result"]


class Backend:
    org = ""
    project = ""
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    url_root = ""

    def __init__(self, pat, org, project):
        self.org = org
        self.project = project
        authorization = str(base64.b64encode(bytes(':' + pat, 'ascii')), 'ascii')
        self.url_root = f"https://dev.azure.com/{self.org}/{self.project}/_apis"
        self.headers["Authorization"] = "Basic " + authorization

    def post(self, url, payload):
        url = self.url_root + url
        print(f"POST: {url}")
        resp = requests.post(url, json=payload, headers=self.headers)
        print("Content: " + str(resp.content))
        if resp.status_code < 200 or resp.status_code > 299:
            raise Exception(f"API Error: {resp.status_code}: {resp.text}")
        return resp.json(
        )

    def get(self, url):
        url = self.url_root + url
        print(f"GET: {url}")
        resp = requests.get(url, headers=self.headers)
        if resp.status_code < 200 or resp.status_code > 299:
            raise Exception(f"API Error: {resp.status_code}: {resp.text}")
        return resp.json()

    def get_job_data(self, pipeline_id, job_id):
        return self.get(f"/pipelines/{pipeline_id}/runs/{job_id}")

    def get_pipeline_id_by_name(self, name):
        resp = self.get("/pipelines?api-version=7.0")
        found = list(filter(lambda p: p["name"] == name, resp["value"]))
        return found[0]["id"] if len(found) else None

    def run_pipeline(self, repo_ref, pipeline_id, parameters, variables):
        # Complex types must be passed as yaml strings
        for k, v in parameters.items():
            if type(v) not in (str, int, float, bool):
                parameters[k] = yaml.safe_dump(v)
        payload = {
            "resources": {
                "repositories": {
                    "self": {
                        "refName": repo_ref
                    }
                }
            },
            "templateParameters": parameters,
            "variables": variables,
        }
        return Job(self, self.post(f"/pipelines/{pipeline_id}/runs?api-version=7.0", payload))


def run_pipeline(context, inputs, pipeline_name):
    token = context.getSecret(inputs["ado_pat"])
    backend = Backend(token, inputs["org"], inputs["project"])
    pipeline_id = backend.get_pipeline_id_by_name(pipeline_name)
    if not pipeline_id:
        raise Exception(f"Pipeline {pipeline_name} not found")
    job = backend.run_pipeline(inputs["repoRef"], pipeline_id, inputs.get("parameters", {}),
                               inputs.get("variables", {}))
    result = job.wait_for_completion()
    if result != "succeeded":
        raise Exception("Pipeline execution failed")
    return job.job_data
