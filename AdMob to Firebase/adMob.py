import os
import csv
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import pandas as pd


# Authenticate using the client_secrets file.
from pandas._libs import json

client_secrets = os.path.join(
    os.path.dirname(__file__), 'client_secrets.json')
flow = Flow.from_client_secrets_file(
    client_secrets,
    scopes=['https://www.googleapis.com/auth/admob.report'],
    redirect_uri='urn:ietf:wg:oauth:2.0:oob')

# Redirect the user to auth_url on your platform.
auth_url, _ = flow.authorization_url()
print('Please go to this URL: {}\n'.format(auth_url))

# The user will get an authorization code. This code is used to get the
# access token.
code = input('Enter the authorization code: ')
flow.fetch_token(code=code)
credentials = flow.credentials

# Create an AdMob service object on which to run the requests.
admob = build('admob', 'v1', credentials=credentials)

# Get AdMob account information by replacing publisher_id,
# which follows the format "pub-XXXXXXXXXXXXXXXX".
# See https://support.google.com/admob/answer/2784578
# for instructions on how to find your publisher ID.
result = admob.accounts().get(
name = 'accounts/{}'.format("pub-9899159862856473")).execute()

# Print the result.
print('Name: ' + result['name'])
print('Publisher ID: ' + result['publisherId'])
print('Currency code: ' + result['currencyCode'])
print('Reporting time zone: ' + result['reportingTimeZone'])


# Set date range.
# AdMob API only supports the account default timezone and "America/Los_Angeles", see
# https://developers.google.com/admob/api/v1/reference/rest/v1/accounts.networkReport/generate
# for more information.
date_range = {
    'startDate': {'year': 2020, 'month': 1, 'day': 1},
    'endDate': {'year': 2020, 'month': 1, 'day': 30}
}

# Set metrics.
metrics = ['ESTIMATED_EARNINGS', 'IMPRESSIONS', 'SHOW_RATE', 'MATCH_RATE', 'MATCHED_REQUESTS', 'CLICKS']

# Set dimensions.
dimensions = ['DATE', 'APP', 'PLATFORM','FORMAT', 'AD_UNIT', 'COUNTRY']

# Set sort conditions.
sort_conditions = {'dimension': 'MATCH_RATE', 'order': 'DESCENDING'}


# Set dimension filters.
dimension_filters = {
    'dimension': 'COUNTRY',
    'matchesAny': {
        'values': ['US', 'CA']
    }
}

# Create network report specifications.
report_spec = {
    'dateRange': date_range,
    'dimensions': dimensions,
    'metrics': metrics,
    #'sortConditions': [sort_conditions],
    'dimensionFilters': [dimension_filters]
}



# Create network report request.
request = {'reportSpec': report_spec}

# Execute network report request.
# Get AdMob account information by replacing publisher_id,
# which follows the format "pub-XXXXXXXXXXXXXXXX".
# See https://support.google.com/admob/answer/2784578
# for instructions on how to find your publisher ID.
result = admob.accounts().networkReport().generate(
    #"pub-2230335825119050"
    parent='accounts/{}'.format("pub-9899159862856473"), body=request).execute()

# Display results.
for report_line in result:
  print(report_line)

print(type(report_line))


with open('datas.json', 'w') as outfile:
    json.dump(result, outfile)


pdObj = pd.read_json('datas.json', orient='index')
print(pdObj)