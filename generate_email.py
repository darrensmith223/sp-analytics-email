from sparkpost import SparkPost
import json
import os
import requests
import pandas as pd
from pathlib import Path
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dateutil import parser
from datetime import datetime
from datetime import timedelta
import base64


class Template(object):
    subject_line = ""
    from_name = ""
    from_email = ""
    html = ""
    text = ""

    def __init__(self, template_data):
        self.subject_line = template_data.get("content").get("subject")
        self.from_name = template_data.get("content").get("from").get("name")
        self.from_email = template_data.get("content").get("from").get("email")
        self.html = template_data.get("content").get("html")
        self.text = template_data.get("content").get("text")


def map_metrics():
    pass


def get_metrics(api_key, start_dt, end_dt, metrics_csv):
    url = "https://api.sparkpost.com/api/v1/metrics/deliverability/time-series?from=" + start_dt + "&to=" + end_dt + "&metrics=" + metrics_csv
    headers = {"Authorization": api_key, "Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    result_obj = json.loads(response.text)

    return result_obj.get("results")


def generate_plot(metrics_list, metrics_data):
    metrics_df = pd.DataFrame.from_records(metrics_data)  # Convert SP data into dataframe

    # Convert SparkPost ts to datetime
    metrics_df["ts"] = [parser.parse(dt_str) for dt_str in metrics_df["ts"]]

    # Map metrics back to input

    # Create plot
    fig = make_subplots(rows=1, cols=1, specs=[[{"secondary_y": True}], [{"secondary_y": False}]],
                        row_width=[0.2, 0.8], shared_xaxes=True)
    fig.update_layout(title="Email Metrics", xaxis_rangeslider_visible=False)

    for metric in metrics_list:
        # Map metric from SP metric(s)
        metric_array = metrics_df[metric]
        metric_color = get_color(metrics_list.index(metric))

        fig.add_trace(
            go.Scatter(x=metrics_df["ts"], y=metric_array, line=dict(color=metric_color, width=1.5)
                       , opacity=0.4, name=metric), secondary_y=False, row=1, col=1)

    # Store plot for email
    file_name = "sp_plot.png"
    file_path = os.path.join(Path(os.getcwd()), "img", file_name)
    fig.write_image(file_path)

    return file_path


def get_color(index):
    colors = [
        "orange",
        "darkblue",
        "darkgreen",
        "cyan",
        "mintcream",
        "salmon",
        "teal"
    ]

    if index <= len(colors) - 1:
        color = colors[index]
    else:
        color = colors[0]

    return color


def send_email(api_key, template_id, recipient_address, file_path, substitution_data=None):

    # Retrieve Template Content
    template_data = get_template(api_key, template_id)
    template_obj = Template(template_data)

    # Set Defaults
    if substitution_data is None:
        substitution_data = {}

    # Send Message
    sp = SparkPost(api_key)
    img_obj = base64_img(file_path)  # Convert image into base64
    sp.transmissions.send(
        recipients=[{'address': {'name': "name", 'email': recipient_address}}],
        subject=template_obj.subject_line,
        html=template_obj.html,
        text=template_obj.text,
        from_email=template_obj.from_email,
        from_name=template_obj.from_name,
        inline_images=[{
            "name": os.path.basename(file_path),
            "type": "image/png",
            "data": img_obj
        }],
        substitution_data=substitution_data
    )


def get_template(api_key, template_id):
    url = "https://api.sparkpost.com/api/v1/templates/" + template_id
    headers = {"Authorization": api_key, "Content-Type": "application/json"}
    response = requests.get(url, headers=headers)
    result_obj = json.loads(response.text)

    return result_obj.get("results")


def base64_img(file_path):
    with open(file_path, "rb") as img_file:
        base64Bytes = base64.b64encode(img_file.read())

    img_obj = base64Bytes.decode('ascii')  # Convert encode back into ASCII

    return img_obj


def send_analytics_report(**kwargs):
    """
    Generate Analytics Report Email

    :param str api_key:  SparkPost API Key
    :param str recipient_address:  Recipient address to send email to
    :param str template_id:  SparkPost Stored Template ID
    :param str logo_url:  URL of logo to include in the email body
    :param metrics_list:  List of strings
    :param filters:  List of strings
    :param comparisons:  List of strings
    :return: None
    """

    api_key = kwargs.get("api_key")
    recipient_address = kwargs.get("recipient_address")
    template_id = kwargs.get("template_id")
    logo_url = kwargs.get("logo_url")
    metrics_list = kwargs.get("metrics_list")
    filters = kwargs.get("filters")
    comparisons = kwargs.get("comparisons")

    # Map Metrics to determine which raw metrics are needed
    metrics_csv = ",".join(metrics_list)

    # Define and formate date range
    start_dt = str(parser.parse(str(datetime.now() - timedelta(days=180))))
    end_dt = str(parser.parse(str(datetime.now())))

    # Retrieve metrics from SP
    metrics_data = get_metrics(api_key, start_dt, end_dt, metrics_csv)

    # Generate Plot
    file_path = generate_plot(metrics_list, metrics_data)

    # Send Email
    substitution_data = {
        "logo_img": logo_url
    }
    send_email(api_key, template_id, recipient_address, file_path, substitution_data)


if __name__ == "__main__":
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
