# sp-analytics-email

SparkPost sending platform and stored templates are used to send an email with an in-line image of the performance metrics.  First, the SparkPost [Metrics API](https://developers.sparkpost.com/api/metrics/#metrics-get-time-series-metrics) is used to retrieve the specified sending metrics.  Then a plot of the metrics data are recreated using `Plotly` and embedded within an email which is then sent to a recipient using SparkPost.  

The Analytics report image is embedded in-line using the ["inline_images"](https://developers.sparkpost.com/api/transmissions/#header-inline-image-object) field within the SparkPost Transmissions API.  Additionally, the email can be branded by including a URL to a logo using the optional `logo_url` parameter within the main `send_analytics_report` function.

[Taxi For Email](https://taxiforemail.com/) was used to create the email template and export into SparkPost with their pre-built connector.

## How To Use

The script was designed to integrate with your, where you can use the function `send_analytics_report` to pass the necessary information (such as recipient address, the metrics to display, and a logo for custom branding) and generate a customized email with the analytics embedded.  

There is an optional parameter `logo_url` which can be used to include a logo in the Analytics Report for custom branding.  To use this parameter, pass the URL to the image location on your CDN.

An example of using the function can be found below:

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
