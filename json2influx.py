#!/usr/bin/env python

import json
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS, PointSettings, WriteOptions
from datetime import datetime, timezone


def readapitoken():
    data = "FAILED TO READ TOKEN"
    with open('influxapi.token', 'r') as file:
        data = file.read().replace('\n', '')
    return data


bucket = "pmacct"
inputfile = "./example.json"
with InfluxDBClient(url="http://jubilee.lnd.prof-x.net:8086",
                    token=readapitoken(),
                    org="Prof-X") as client:
    point_settings = PointSettings()
    point_settings.add_default_tag("hostname", "pyro.lnd.prof-x.net")
    with client.write_api(point_settings=point_settings) as write_api:
        tags = ['etype', 'as_dst', 'as_src', 'ip_proto', 'ip_dst', 'ip_src']
        fields = ['bytes']

        with open(inputfile) as f:
            for line in f:
                jsonline = json.loads(line)
                datetime_object = datetime.strptime(
                    jsonline['stamp_inserted'],
                    '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
                p = Point("pmacct_traffic")
                for tag in tags:
                    p.tag(tag, str(jsonline[tag]))
                for field in fields:
                    p.field(field, int(jsonline[field]))
                p.time(datetime_object)
                write_api.write(bucket=bucket, record=p, time_precision='s')
    client.close()

## using Table structure
# query_api = client.query_api()
# tables = query_api.query('from(bucket:"pmacct") |> range(start: -10m)')

#for table in tables:
#    print(table)
#    for row in table.records:
#        print(row.values)
