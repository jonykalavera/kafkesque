from djantic import ModelSchema

from clusters.models import Cluster


class ClusterSchema(ModelSchema):
    class Config:
        model = Cluster
