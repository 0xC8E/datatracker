# data-tracker
`by JC Coto`

## Overview
The goal of this system is to fetch cryptocurrency price data from `Cryptowatch`, keep the last 24h of data, and provide some metrics queries to support a dashboard-like Web application.

This system has two main components:
- a REST API built with FastAPI (so it's typed, self-documenting, and asynchronous!) with 2 endpoints to query metric data.
- a worker that queries data and updates the data store with metric data.

Here's a simple diagram of the overall architecture:
![System Architecture](https://cdn.zappy.app/4e291cdff5f285d7b513c4273dc2ed1a.png)

The system is versioned at the top level, which is a new pattern I've been trying out - different versions of the system might have slightly different data models, APIs, and utilities. There's a symbolic link to the latest version of the API (`latest`) that's a handy shortcut to the latest and greatest. Finally, the data store is Redis, hosted with Docker Compose.

There are some basic tests of the main data series storage under `tests`, and there's a quality-of-life `scripts` directory with some useful scripts to run the system. See below.


## Running Instructions
There's a really easy-to-use `scripts` directory, with the following scripts:
1. `start-db.sh`: Fetch Redis images and run a Redis instance.
2. `run-tests.sh`: Run a basic set of tests for the datastore with `py.test`.
3. `start-worker.sh`: Start a worker daemon that fetches data from the crypto API and updates the data store.
4. `start-api.sh`: Stand up a `hypercorn` server to host the FastAPI server for the REST API.

## TODOs and Potential Enhancements
Ooof, tons!
- Authentication, or, if this is intended to remain open, then build in some throttling and rate limiting.
- I'd like to add more tests and clean up the test infrastructure, which is currently kind of grafted into the regular infrastructure.
- Improve exception handling.
- Set up proper API routing that follows the versioning scheme in a way that's easy to use and extend.
- Clean things up, in general. More currencies, probably more documentation.
- Get feedback from the team and apply it!

## Open Questions

### Scalability
- What would you change if you needed to track many metrics?
I would first asses how many "many" metrics is - it's important to have some solid data points to make decisions. Assuming it's enough to make Redis unsuitable (RAM limitations, for example), I would reach for a relational database first, or a NoSQL datastore like Dynamo or Cassandra if the data was going to grow significantly more. After a certain inflexion point, though, the data store must be horizontally scalable and to do that we'd need to rely on horizontal partitioning (splitting the data up into multiple tables and, eventually, instances).
- What if you needed to sample them more frequently?
That's fairly simple up to a point: run more workers that handle even subsets of the metric set. This would scale well up to a bottleneck, either the number of workers that can run well concurrently in a single CPU, or IO (meaning saturating the network). In either of those cases, the next step would be scaling worker machines out so their physical resources might be divided between them.
- What if you had many users accessing your dashboard to view metrics?
For querying purposes, probably the best solution is having a sufficiently-up-to-date set of replicas for the databases that track a single writing instance and can spread out read load between them. I'd probably start with a materialized view that's cached, and then eventually scale that up to multiple machines.

If there's no filtering necessary, I would also look at completely static hosting of the data (meaning S3 or a similar block storage) or something like edge-delivered sqlite data (compiled into WASM - this is a really cool pattern!).

### Testing
- How would you extend testing for an application of this kind (beyond what you implemented)?
I tend to favor integration tests over unit tests, except when there are critical parts of the logic that might be complex. I'd set up some CI/CD pipelines with integration tests (meaning a stack is launched and the API is queried).

I would separate API and worker tests at this point - the data store would function as the coordination point between those two components, so I'd be OK with concluding that if the workers update the datastore correctly, and the API serves the data in the store correctly, the system is working correctly.

I'd still set up some monitors and PagerDuty, though ;).

### Feature Request
```
To help the user identify opportunities in real-time, the app will send an alert whenever a metric exceeds 3x the value of its average in the last 1 hour. For example, if the volume of GOLD/BTC averaged 100 in the last hour, the app would send an alert in case a new volume data point exceeds 300. Please write a short proposal on how you would implement this feature request.
```

I would implement it in a very similar way to how the current rank is implemented - while the worker updates data, it would compare the new data point with the standing average (also kept in a sorted set). If there's a significant-enough discrepancy, I'd send an alert (via Twilio, Pushover or some other real-time notification system with a good Python API).

With the current setup, it should provide up-to-the-minute accuracy and still continue working well for a high number of users and metrics, but if we need to support more users or more metrics, it might need to scale out.


## Work Log:
- **(2021-08-02 21:21 - 2021-08-02 21:25; ~20 min)**: Set up API and Redis.
- **(2021-08-03 00:22 - 2021-08-03 01:25; ~60 min)**: Worker scaffold.
- **(2021-08-03 16:18 - 2021-08-03 16:53; ~35 min)**: Redis backend.
- **(2021-08-03 19:05 - 2021-08-03 20:07; ~62 min)**: Set up Redis tests.
- **(2021-08-04 10:10 - 2021-08-04 10:40; ~30 min)**: Complete datapoint storage tests.
- **(2021-08-04 11:00 - 2021-08-04 11:36; ~36 min)**: Complete worker v1.
- **(2021-08-04 16:50 - 2021-08-04 17:51; ~61 min)**: Add multimetrics support and test.
Total: about 5 hours (give or take).
I also spent another ~25 mins writing the README.


### Thanks so much! Looking forward to reviewing with y'all :D!
