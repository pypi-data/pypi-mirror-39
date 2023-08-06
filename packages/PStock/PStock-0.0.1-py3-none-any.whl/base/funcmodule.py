#Author: lladhibhutall 
import requests
import json
#import pprint
import time

def my_function(args):

	link =  "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={}&interval=5min&outputsize=full&apikey=O45RHWNY6BI3SSGW".format(args)
	r = requests.get(link)
	json_data = r.json()
	return (convert_json_to_dict(json_data))

def convert_json_to_dict(_json):
	stock_data = _json['Time Series (5min)']
	list_of_dict_data = []
	for key,value in stock_data.items():	
		s_data = {}
		s_data['Timestamp'] = key 
		s_data['open'] = value['1. open']
		s_data['high'] = value['2. high']
		s_data['low'] = value['3. low']
		s_data['close'] = value['4. close']
		s_data['volume'] = value['5. volume']
		list_of_dict_data.append(s_data)	
	return list_of_dict_data

def sort_by_time(data_list):
	#pp = pprint.PrettyPrinter(indent=4)
	data_list.sort(key=lambda x:time.mktime(time.strptime(x['Timestamp'], '%Y-%m-%d %H:%M:%S')))
	#pp.pprint(data_list)
	return data_list

def sorted_XY(sorted_list):
	X = []
	Y = []
	count = 1
	for _ in sorted_list:
		Y.append(float(_['open']))
		X.append(count)
		count = count + 1
	return X,Y


