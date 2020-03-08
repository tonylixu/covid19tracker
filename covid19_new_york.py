from lxml import html
import os
import requests
import slack

url = f'https://coronavirus.1point3acres.com/en'

page = requests.get(url)
tree = html.fromstring(page.content)

# Convert full data into list
us_data = tree.xpath('//span[@class="jsx-2915694336"]/text()')
# Skip the first four lines:
# Location, Confirmed, Recovered, Deaths
us_data = us_data[4:]
encoded_str = us_data[0].encode('unicode-escape')

# Define New York Unicode String
new_york_code = b'\\u7ebd\\u7ea6'
for i in range(len(us_data)):
    if us_data[i].encode('unicode-escape') == b'\\u7ebd\\u7ea6':
        location = 'New York'
        confirmed = us_data[i+1]
        recovered = us_data[i+2]
        deaths = us_data[i+3]
        msg_to_slack = (
            f"COVID-19 New York Hourly Update\n"
            f'{location}, Confirmed: {confirmed}, Recovered:{recovered}, Deaths: {deaths}'
        )
        break

client = slack.WebClient(token=os.environ['SLACK_API_TOKEN'])

response = client.chat_postMessage(
    channel='#covid-19',
    text=msg_to_slack )
assert response["ok"]
