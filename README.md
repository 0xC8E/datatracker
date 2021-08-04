# data-tracker

```
- Users will select one of the collected metrics (e.g. BTC/USD price) from a combo box or list. 

- The selected metric will be presented in a chart over time (so as to show the user how it changed throughout the last 24 hours). 

- In addition, the application will present the selected metric's "rank". The "rank" of the metric helps the user understand how the metric is changing relative to other similar metrics, as measured by the standard deviation of the metric over the last 24 hours. For example in the crypto data source, if the standard deviations of the volume of BNT/BTC, GOLD/BTC and CBC/ETH were 100, 200 and 300 respectively, then rank(CBC/ETH)=1/3, rank(GOLD/BTC)=2/3 and rank(BNT/BTC)=3/3.
```

```
Scalability: what would you change if you needed to track many metrics? What if you needed to sample them more frequently? what if you had many users accessing your dashboard to view metrics?

Testing: how would you extend testing for an application of this kind (beyond what you implemented)?

Feature request: to help the user identify opportunities in real-time, the app will send an alert whenever a metric exceeds 3x the value of its average in the last 1 hour. For example, if the volume of GOLD/BTC averaged 100 in the last hour, the app would send an alert in case a new volume data point exceeds 300. Please write a short proposal on how you would implement this feature request.
```

## Work Log:
- **(2021-08-02 21:21 - 2021-08-02 21:25; ~20 min)**: Set up API and Redis.
- **(2021-08-03 00:22 - 2021-08-03 01:25; ~60 min)**: Worker scaffold.
- **(2021-08-03 16:18 - 2021-08-03 16:53; ~35 min)**: Redis backend.
- **(2021-08-03 19:05 - 2021-08-03 20:07; ~62 min)**: Set up Redis tests.
- **(2021-08-04 10:10 - 2021-08-04 10:40; ~30 min)**: Complete datapoint storage tests.
- **(2021-08-04 11:00 - 2021-08-04 11:36; ~36 min)**: Complete worker.
