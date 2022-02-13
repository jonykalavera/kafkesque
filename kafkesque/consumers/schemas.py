from djantic import ModelSchema

from consumers.models import Consumer, ConsumerStatus, SerializationFormat


class ConsumerSchema(ModelSchema):
    status: ConsumerStatus
    serialization_format: SerializationFormat

    class Config:
        model = Consumer


class CreateConsumerSchema(ModelSchema):
    serialization_format: str = SerializationFormat.JSON.value

    class Config:
        model = Consumer
        exclude = ["id", "ts_created", "ts_updated", "status"]


class StartConsumerSchema(ModelSchema):
    serialization_format: str = SerializationFormat.JSON.value

    class Config:
        model = Consumer
        exclude = ["id", "ts_created", "ts_updated", "status"]
