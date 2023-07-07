import unittest

import common


class TestCreate(unittest.TestCase):
    def test_simple(self):
        op = common.Backend("mpk5tkon2hwvafqeo4gslnkzlexzsf3y367ojoexkwsfywms2ioq", "prydin", "prydin")
        job = op.run_pipeline("refs/heads/main", "1", {"target": "Pontus", "time": "evening"}, {})
        print(job)
        print(job.wait_for_completion())

    def test_lookup(self):
        op = common.Backend("mpk5tkon2hwvafqeo4gslnkzlexzsf3y367ojoexkwsfywms2ioq", "prydin", "terraform-poc")
        pipeline = op.get_pipeline_id_by_name("Terraform Apply")
        print(pipeline)
