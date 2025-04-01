# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 15:43:15 2023

@author: 11107045
"""

import requests


def get_access_token(url, client_id, client_secret):
    response = requests.post(
        url,
        data={"grant_type": "client_credentials"},
        auth=(client_id, client_secret),
    )
    return response.json()["access_token"]

url="https://login.microsoftonline.com/4908fa00-a99f-47f5-ad64-86bd2e41f3dd/oauth2/token"
client_id="4ea9c2a8-eb98-4f90-ac00-2cb569eee612"
client_secret="GxC8Q~An_e25ww3rpWax7tJtza1RyhWh9wiZ~bGT"
print(get_access_token(url,client_id ,client_secret))
access_token=get_access_token(url,client_id ,client_secret)