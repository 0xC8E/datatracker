import typing

import pydantic


class MetricMetadata(pydantic.BaseModel):
    human_readable_name: str
    metric_id: str


class Metric(pydantic.BaseModel):
    values: typing.List[float]
    rank: float
