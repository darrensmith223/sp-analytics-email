# sp-analytics-email

SparkPost sending platform and stored templates are used to send an email with an in-line image of the performance metrics.  First, the SparkPost [Metrics API](https://developers.sparkpost.com/api/metrics/#metrics-get-time-series-metrics) is used to retrieve the specified sending metrics.  Then a plot of the metrics data are recreated and embedded within an email which is then sent to a recipient using SparkPost.  

