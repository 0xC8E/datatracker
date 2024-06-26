import fastapi
import typing

from datatracker.v1.api import models
from datatracker.v1.data import metrics

app = fastapi.FastAPI()


@app.get("/api/v1/metrics", response_model=typing.List[models.MetricMetadata])
async def get_metrics():
    """
    Retrieve all the currently defined metrics in the system.
    """
    all_metrics = metrics.get_all_metrics()
    return [
        models.MetricMetadata(
            human_readable_name=metrics.get_readable_name(m),
            metric_id=metrics.get_metric_id(m),
        )
        for m in all_metrics
    ]


@app.get("/api/v1/metrics/{metric_id}", response_model=models.Metric)
async def get_metric(metric_id):
    """
    Retrieve details related to a specific metric in the system.
    """
    data_points = await metrics.get_latest(metric_id)
    rank = await metrics.get_rank(metric_id)
    response = models.Metric(values=[float(dp[0]) for dp in data_points], rank=rank)
    return response
