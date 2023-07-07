import os
import unittest

import common

pat = os.environ["ADO_KEY"]


class TestCreate(unittest.TestCase):
    def test_simple(self):
        op = common.Backend(pat, "prydin", "prydin")
        job = op.run_pipeline("refs/heads/main", "1", {"target": "Pontus", "time": "evening"}, {})
        print(job)
        print(job.wait_for_completion())

    def test_lookup(self):
        op = common.Backend(pat, "prydin", "terraform-poc")
        pipeline = op.get_pipeline_id_by_name("Terraform Apply")
        print(pipeline)
