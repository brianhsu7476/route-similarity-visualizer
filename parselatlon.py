import xml.etree.ElementTree as ET
import sys
from math import *
from datetime import datetime
from copy import deepcopy
N=2**19
def toTime(t):
	return datetime.strptime(t, "%Y-%m-%dT%H:%M:%SZ")

def parseGpx(fileName):
    with open(fileName, 'r') as fp:
        fileStr=fp.read()
    namespace=fileStr.split('<gpx')[1].split('>')[0] # remove the namespace
    fileStr=''.join(fileStr.split(namespace))
    fileStr=''.join(fileStr.split('gpxtpx:'))
    root=ET.fromstring(fileStr)

    latlon_list = []
    for pt in root.find('trk').find('trkseg').findall('trkpt'):
        lat = pt.get('lat')
        lon = pt.get('lon')
        latlon_list.append((float(lat),float(lon)))
        
    return latlon_list

def trans(latlon):
    latlon_list = []
    for items in latlon:
        
        tt=list(items)
        lat=tt[0]
        lon=tt[1]
        lat=radians(lat)
        
        latlon_list.append((floor(2*log(abs(1.0/cos(lat)+tan(lat)))/(2*pi)*(N/2)),floor((lon/180.0)*(N/2))))
    #print(len(latlon_list))
    return latlon_list

