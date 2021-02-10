import csv
import os
import datetime as dt
import urllib.request

from ip2geotools.databases.noncommercial import DbIpCity

def get_datetime():
    return dt.datetime.now()

def get_location():
    #get and return location of rpi if available, return none so null values are recorded if location data is unavailable
    try:
        ##### replace with gps location info once gps reciever has ben integrated
        external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
        response = DbIpCity.get(external_ip, api_key='free')
        return response.latitude, response.longitude
    except:
        return None, None

def get_img_name(datetime):
    #label image name with date
    return f'{datetime.strftime("%Y%m%d%H%M%S")}_rpilog_img.png'

def collect(datetime, latitude, longitude, img_filename):
    #write and/or append data files (based on whether or not data is recorded on a new day)
    doc_name = f'/home/pi/gui_apps/output/{datetime.strftime("%Y")}{datetime.strftime("%m")}{datetime.strftime("%d")}_rpilog.csv'
    fields = ['datetime', 'latitude', 'longitude', 'img_filename']
    row = [datetime.strftime("%Y-%m-%d %H:%M:%S"), latitude, longitude, img_filename]

    FILE_EXISTS = os.path.isfile(doc_name)

    with open(doc_name, 'a', newline='') as doc:
        writer = csv.writer(doc)
        if not FILE_EXISTS:
            writer.writerow(fields)
        writer.writerow(row)

