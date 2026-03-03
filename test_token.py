#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import datetime

token = "eyJhbGciOiJIUzI1NiJ9.eyJhY2NvdW50SWQiOiI3MDQ2ODk3NjJAcXEuY29tIiwic3ViIjoiYm9zcyIsInNvdXJjZSI6InRoaXJkX2xvZ2luX3NvdXJjZV8wIiwiZXhwIjoxNzc1MDE1OTgxfQ.WvaFZSD_3CEVitxkjohE4xS2sYzS5Fjq-yJhFZSfHho"
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'login-token': token
}
today = datetime.datetime.now().strftime('%Y-%m-%d')
payload = {
    'sortType': 'createTimeDesc',
    'pageNo': 1,
    'pageSize': 10,
    'searchType': 10,
    'current': 1,
    'startTime': f'{today} 00:00:00',
    'endTime': f'{today} 23:59:59',
    'isTouchNone': 0
}
try:
    resp = requests.post('https://admin.avatr.com/crm/v2/clue/search/pageEsClue', headers=headers, json=payload, timeout=30)
    print('Status:', resp.status_code)
    print('Response:', resp.text[:1000])
except Exception as e:
    print('Error:', e)
