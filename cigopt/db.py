from couchbase import LOCKMODE_WAIT
from couchbase.bucket import Bucket
from couchbase.cluster import Cluster, PasswordAuthenticator

from cigopt.types import Experiment, ExperimentInDB


class Controller:

    def __init__(self, bucket: Bucket):
        self.bucket = bucket

    def read_experiment(self, experiment_id: str):
        doc_id = f"experiment::{experiment_id}"
        result = self.bucket.get(doc_id, quiet=True)
        if not result.value:
            return None
        return ExperimentInDB(**result.value)

    def create_experiment(self, experiment: Experiment):
        doc_id = f"experiment::{experiment.experiment_id}"
        result = self.bucket.insert(doc_id, ExperimentInDB(**experiment.dict()).dict())
        if not result.success:
            raise RuntimeError(f'Error creating experiment: {experiment}')
        return experiment

    def delete_experiment(self, experiment_id: str):
        doc_id = f"experiment::{experiment_id}"
        result = self.bucket.delete(doc_id, quiet=True)
        if not result.success:
            raise RuntimeError(f'Error deleting experiment: {experiment_id}')


def get_bucket():
    cluster = Cluster(
        "couchbase://localhost:8091?fetch_mutation_tokens=1&operation_timeout=30&n1ql_timeout=300"
    )
    authenticator = PasswordAuthenticator("admin", "password")
    cluster.authenticate(authenticator)
    bucket: Bucket = cluster.open_bucket("experiments", lockmode=LOCKMODE_WAIT)
    bucket.timeout = 30
    bucket.n1ql_timeout = 300
    return bucket


def get_controller():
    bucket = get_bucket()
    return Controller(bucket)
