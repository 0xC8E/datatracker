import asyncio
import datetime
import freezegun
import pytest

from datatracker.v1.data import metrics

METRIC = ("Test", "test")


# This marks all tests as async
pytestmark = pytest.mark.asyncio

# We need a module-scoped loop here in our particular case to
# normalize all tests to run on the same event loop.
# TODO: This should be fixed in a more elegant way, though.
loop = None


@pytest.fixture
def event_loop():
    global loop  # yuck!
    if not loop:
        loop = asyncio.get_event_loop()
    yield loop


def pytest_sessionfinish(*_):
    global loop  # double yuck!
    loop.close()


async def test_main_flow_single_item(event_loop):
    await metrics.connect_for_testing_and_clear()
    expected_value = bytes(1)
    with freezegun.freeze_time("2021-08-03 00:00:00"):
        expected_score = datetime.datetime.now().timestamp()
        await metrics.add_and_prune(METRIC, expected_value)
        points = await metrics.get_latest(METRIC)

    retrieved_value, retrieved_score = points[0]

    assert retrieved_value == expected_value
    assert retrieved_score == expected_score


async def test_prune_to_last_24h(event_loop):
    await metrics.connect_for_testing_and_clear()
    value = bytes(1)
    with freezegun.freeze_time("2021-08-03 00:00:00"):
        await metrics.add_and_prune(METRIC, value)

    # Note that this is exactly one second after 24h (to make sure it's outside the 24h range)
    with freezegun.freeze_time("2021-08-04 00:00:01"):
        await metrics.add_and_prune(METRIC, value)
        points = await metrics.get_latest(METRIC)

    assert len(points) == 1


async def test_get_only_last_24h(event_loop):
    await metrics.connect_for_testing_and_clear()
    old_value = bytes(1)
    with freezegun.freeze_time("2021-08-03 00:00:00"):
        await metrics.add_and_prune(METRIC, old_value)

    new_value = bytes(2)
    # Note that this is exactly one second after 24h (to make sure it's outside the 24h range)
    with freezegun.freeze_time("2021-08-04 00:00:01"):
        await metrics.add_and_prune(METRIC, new_value)
        points = await metrics.get_latest(METRIC)

    assert len(points) == 1
    retrieved_value, _ = points[0]
    assert retrieved_value == new_value
