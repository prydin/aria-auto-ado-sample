import base64
import time

import requests


class Job:
    backend = None

    id = -1
    state = ""
    result = ""
    pipeline_id = -1

    def __init__(self, backend, raw):
        self.backend = backend
        self.id = raw["id"]
        self.state = raw["state"]
        self.pipeline_id = raw["pipeline"]["id"]

    def refresh(self):
        resp = self.backend.get(f"/pipelines/{self.pipeline_id}/runs/{self.id}")
        self.state = resp["state"]
        self.result = resp.get("result", None)

    def get_state(self):
        self.refresh()
        return self.state

    def wait_for_completion(self):
        while self.get_state() == "inProgress":
            time.sleep(5)
        return self.result


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
        print(f"POST: {url}")
        resp = requests.post(self.url_root + url, json=payload, headers=self.headers)
        print("Content: " + str(resp.content))
        if resp.status_code < 200 or resp.status_code > 299:
            raise Exception(f"API Error: {resp.status_code}: {resp.content}")
        return resp.json(
        )

    def get(self, url):
        resp = requests.get(self.url_root + url, headers=self.headers)
        if resp.status_code < 200 or resp.status_code > 299:
            raise Exception(f"API Error: {resp.status_code}: {resp.content}")
        return resp.json()

    def get_pipeline_id_by_name(self, name):
        resp = self.get("/pipelines?api-version=7.0")
        found = list(filter(lambda p: p["name"] == name, resp["value"]))
        return found[0]["id"] if len(found) else None

    def run_pipeline(self, repo_ref, pipeline_id, parameters, variables):
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
    if "token" in inputs:
        token = inputs["token"]
    else:
        token = context.getSecret(inputs["pat"])
    backend = Backend(token, inputs["org"], inputs["project"])
    pipeline_id = backend.get_pipeline_id_by_name(pipeline_name)
    if not pipeline_id:
        raise Exception(f"Pipeline {pipeline_name} not found")
    job = backend.run_pipeline(inputs["repoRef"], pipeline_id, inputs.get("parameters", {}),
                               inputs.get("variables", {}))
    result = job.wait_for_completion()
    if result != "succeeded":
        raise Exception("Pipeline execution failed")
