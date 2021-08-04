import asyncio
import datetime
import freezegun
import pytest

from datatracker.v1.data import datapoints


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
    await datapoints.clear()
    expected_value = bytes(1)
    with freezegun.freeze_time("2021-08-03 00:00:00"):
        expected_score = datetime.datetime.now().timestamp()
        await datapoints.add_and_prune(expected_value)
        points = await datapoints.get_latest()

    retrieved_value, retrieved_score = points[0]

    assert retrieved_value == expected_value
    assert retrieved_score == expected_score


async def test_prune_to_last_24h(event_loop):
    await datapoints.clear()
    value = bytes(1)
    with freezegun.freeze_time("2021-08-03 00:00:00"):
        await datapoints.add_and_prune(value)

    # Note that this is exactly one second after 24h (to make sure it's outside the 24h range)
    with freezegun.freeze_time("2021-08-04 00:00:01"):
        await datapoints.add_and_prune(value)
        points = await datapoints.get_latest()

    assert len(points) == 1


async def test_get_only_last_24h(event_loop):
    await datapoints.clear()
    old_value = bytes(1)
    with freezegun.freeze_time("2021-08-03 00:00:00"):
        await datapoints.add_and_prune(old_value)

    new_value = bytes(2)
    # Note that this is exactly one second after 24h (to make sure it's outside the 24h range)
    with freezegun.freeze_time("2021-08-04 00:00:01"):
        await datapoints.add_and_prune(new_value)
        points = await datapoints.get_latest()

    assert len(points) == 1
    retrieved_value, _ = points[0]
    assert retrieved_value == new_value
