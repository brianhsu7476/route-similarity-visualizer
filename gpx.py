import xml.etree.ElementTree as ET
import sys
from datetime import datetime
from copy import deepcopy

def toTime(t):
	return datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ")

def parseGpx(fileName):
	with open(fileName, 'r') as fp:
		fileStr=fp.read()
	namespace=fileStr.split('<gpx')[1].split('>')[0] # remove the namespace
	fileStr=''.join(fileStr.split(namespace))
	fileStr=''.join(fileStr.split('gpxtpx:'))
	root=ET.fromstring(fileStr)
	a={}
	a['sttime']=root.find('metadata').find('time').text
	for i in ['name', 'type']:
		a[i]=root.find('trk').find(i).text
	a['seg']=[]
	for pt in root.find('trk').find('trkseg').findall('trkpt'):
		b={}
		for i in ['lat', 'lon']:
			b[i]=pt.get(i)
		for i in ['ele', 'time']:
			b[i]=pt.find(i).text
		ext=pt.find('extensions')
		try:
			b['power']=ext.find('power').text
		except:
			b['power']=None
		try:
			ext=ext.find('TrackPointExtension')
			for i in ['atemp', 'hr', 'cad']:
				try:
					b[i]=ext.find(i).text
				except:
					b[i]=None
		except:
			for i in ['atemp', 'hr', 'cad']:
				b[i]=None
		a['seg'].append(b)
	return a

