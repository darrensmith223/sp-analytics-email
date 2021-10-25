# sp-analytics-email

SparkPost sending platform and stored templates are used to send an email with an in-line image of the performance metrics.  First, the SparkPost [Metrics API](https://developers.sparkpost.com/api/metrics/#metrics-get-time-series-metrics) is used to retrieve the specified sending metrics.  Then a plot of the metrics data are recreated and embedded within an email which is then sent to a recipient using SparkPost.  

## How To Use

You can use the function `send_analytics_report` to pass the necessary information.  

For example:

```python
# Initialize Variables
    api_key = os.environ.get("API_KEY")
    recipient_address = os.environ.get("RECIPIENT_ADDRESS")
    template_id = os.environ.get("TEMPLATE_ID")
    logo_url = os.environ.get("LOGO_URL")

    metrics_list = [
        "count_injected",
        "count_delivered",
        "count_rendered"
    ]
    filters = []
    comparisons = []

    # Send Report Email
    send_analytics_report(
        api_key=api_key,
        recipient_address=recipient_address,
        template_id=template_id,
        logo_url=logo_url,
        metrics_list=metrics_list
    )
```
