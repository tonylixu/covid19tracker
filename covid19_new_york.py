from lxml import html
import os
import requests
import slack
from datetime import datetime

def get_us_data(_us_data_number) -> str:
    _us_confirmed = _us_data_number[0]
    _us_recovered = _us_data_number[1]
    _us_deaths = _us_data_number[2]
    _ca_confirmed = _us_data_number[3]
    _ca_recovered = _us_data_number[4]
    _ca_deaths = _us_data_number[5]
    _msg = (
        f"US Confirmed: `{_us_confirmed}`, Recovered: `{_us_recovered}, Deaths: `{_us_deaths}`\n"
        f"CA Confirmed: `{_ca_confirmed}`, Recovered: `{_ca_recovered}`, Deaths: {_ca_deaths}"
        f"\n======\n"
    )
    return _msg


def get_new_york_data(_us_detailed_data):
    # Define New York Unicode String
    new_york_code = b'\\u7ebd\\u7ea6'
    for i in range(len(_us_detailed_data)):
        if _us_detailed_data[i].encode('unicode-escape') == new_york_code:
            location = 'New York'
            confirmed = _us_detailed_data[i + 1]
            new_cases = _us_detailed_data[i + 2]
            deaths = _us_detailed_data[i + 3]
            _msg = (
                f'{location}, Confirmed: `{confirmed}`, NewCases: `{new_cases}`, Deaths: `{deaths}`'
            )
            break
    return _msg


def send_msg_to_slack(_msg: str):
    client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])
    response = client.chat_postMessage(
        channel='#covid-19',
        text=_msg)
    assert response["ok"]


if __name__ == '__main__':
    now = datetime.now()
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    url = f'https://coronavirus.1point3acres.com/en'
    page = requests.get(url)
    tree = html.fromstring(page.content)

    # Convert full data into list
    us_data_title = tree.xpath('//dt[@class="jsx-4193741142"]/text()')
    us_data_number = tree.xpath('//dd[@class="jsx-4193741142"]/text()')
    us_detailed_data = tree.xpath('//span[@class="jsx-153966605"]/text()')

    # Skip the first four lines:
    # Location, Confirmed, Recovered, Deaths
    us_detailed_data = us_detailed_data[4:]

    msg_to_slack = f"`*COVID-19 Hourly Update {dt_string}*` \n"
    msg_to_slack += get_us_data(us_data_number)
    msg_to_slack += get_new_york_data(us_detailed_data)
    print(msg_to_slack)
    send_msg_to_slack(msg_to_slack)
