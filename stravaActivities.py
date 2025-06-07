import os
import requests
import urllib3
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
import folium
import polyline
import base64
import webbrowser
from tqdm import tqdm
from transfer import *
# disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def getPolylines():
	def open_file():
		with open('.token', 'r') as fp:
			client_id, client_secret, refresh_token=fp.read().split('\n')[:3]

		print('Authorization url')
		s='https://www.strava.com/oauth/authorize?client_id='+str(client_id)+'&redirect_uri=http://localhost&response_type=code&scope='
		print(s+'read_all,profile:read_all,activity:read_all')
		return (client_id, client_secret, refresh_token)

	def get_access_token2(client_id, client_secret, code):
		oauth_url = 'https://www.strava.com/oauth/token'
		payload={
			'client_id': client_id,
			'client_secret': client_secret,
			'code': code,
			'grant_type': 'authorization_code',
			'f': 'json'
		}
		r = requests.post(oauth_url, data=payload, verify=False)
		access_token = r.json()['access_token']
		return access_token

	client_id, client_secret, refresh_token = open_file()
	code=input('The result url: ').split('code=')[1].split('&')[0]
	print(code)
	access_token=get_access_token2(client_id, client_secret, code)

	def get_data(access_token, per_page=200, page=1):
		url='https://www.strava.com/api/v3/athlete/activities'
		headers={'Authorization': 'Bearer '+access_token}
		params={'activity': 'read', 'per_page': per_page, 'page': page}
		data=requests.get(
			url,
			headers=headers,
			params=params
		).json()
		return data

	def get_segment(access_token, per_page=200, page=1):
		url='https://www.strava.com/api/v3/segments/starred'
		headers={'Authorization': 'Bearer '+access_token}
		params={'per_page': per_page, 'page': page}
		data=requests.get(url, headers=headers, params=params).json()
		return data

	max_number_of_pages = 10
	data = list()
	for page_number in tqdm(range(1, max_number_of_pages + 1)):
		page_data = get_data(access_token, page=page_number)
		if page_data == []:
			break
		data.append(page_data)

	data_dictionaries = []
	for page in data:
		data_dictionaries.extend(page)

	print('Number of activities downloaded: {}'.format(len(data_dictionaries)))

	activities = pd.json_normalize(data_dictionaries)

	activities['map.polyline'] = activities['map.summary_polyline'].apply(polyline.decode)

	activities.loc[:, 'start_date'] = pd.to_datetime(activities['start_date']).dt.tz_localize(None)
	activities.loc[:, 'start_date_local'] = pd.to_datetime(activities['start_date_local']).dt.tz_localize(None)
	activities.loc[:, 'distance'] /= 1000 # convert from m to km
	activities.loc[:, 'average_speed'] *= 3.6 # convert from m/s to km/h
	activities.loc[:, 'max_speed'] *= 3.6 # convert from m/s to km/h
	activities.set_index('start_date_local', inplace=True)
	activities.drop(
		[
			'map.summary_polyline',
			'resource_state',
			'external_id',
			'upload_id',
			'location_city',
			'location_state',
			'has_kudoed',
			'start_date',
			'athlete.resource_state',
			'utc_offset',
			'map.resource_state',
			'athlete.id',
			'visibility',
			'heartrate_opt_out',
			'upload_id_str',
			'from_accepted_tag',
			'map.id',
			'manual',
			'private',
			'flagged',
		],
		axis=1,
		inplace=True
	)

	polylines = []
	for i in range(len(data_dictionaries)):
		my_ride = activities.iloc[i, :]
		polylines.append(my_ride['map.polyline'])
	return polylines

def main():
	print('The index of the routes (0-base), and the number of similar routes to plot:')
	index, K=input().split(' ')
	index, K=int(index), int(K)
	paintpath(getPolylines(), index, K)

if __name__=='__main__':
	main()
