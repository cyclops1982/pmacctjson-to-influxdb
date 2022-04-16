#!/usr/bin/env python

import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS, PointSettings
from datetime import datetime


def readapitoken():
    data = "FAIED TO READ TOKEN"
    with open('influxapi.token', 'r') as file:
        data = file.read().replace('\n', '')
    return data


bucket = "pmacct"
client = InfluxDBClient(url="http://jubilee.lnd.prof-x.net:8086",
                        token=readapitoken(),
                        org="Prof-X")

point_settings = PointSettings()
point_settings.add_default_tag("hostname", "pyro.lnd.prof-x.net")
write_api = client.write_api(write_options=SYNCHRONOUS,
                             point_settings=point_settings)

inputfile = "./example.json"

# {'event_type': 'purge', 'etype': '800', 'ip_src': '188.39.246.174', 'ip_dst': '85.214.51.245', 'ip_proto': 'tcp', 'stamp_inserted': '2022-04-16 14:25:00', 'stamp_updated': '2022-04-16 14:30:01', 'packets': 9, 'bytes': 6034}

tags = ['etype', 'ip_src', 'ip_dst', 'ip_proto']
fields = ['bytes', 'packets', 'flows']

with open(inputfile) as f:
    for line in f:
        jsonline = json.loads(line)
        datetime_object = datetime.strptime(jsonline['stamp_updated'],
                                            '%Y-%m-%d %H:%M:%S')
        p = Point("pmacct_traffic")
        for tag in tags:
            p.tag(tag, jsonline[tag])
        for field in fields:
            p.field(fields, jsonline[fields])
        p.time(datetime_object)
        print(p)
        write_api.write(bucket=bucket, record=p)

## using Table structure
# query_api = client.query_api()
# tables = query_api.query('from(bucket:"pmacct") |> range(start: -10m)')

#for table in tables:
#    print(table)
#    for row in table.records:
#        print(row.values)
