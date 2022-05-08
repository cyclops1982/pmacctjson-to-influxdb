#!/usr/bin/env python

import json, argparse
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS, PointSettings, WriteOptions
from datetime import datetime, timezone


def readapitoken():
    data = "FAIED TO READ TOKEN"
    with open('influxapi.token', 'r') as file:
        data = file.read().replace('\n', '')
    return data


def doupload(inputfile):
    bucket = "pmacct"
    with InfluxDBClient(url="http://jubilee.lnd.prof-x.net:8086",
                        token=readapitoken(),
                        org="Prof-X") as client:
        point_settings = PointSettings()
        point_settings.add_default_tag("hostname", "pyro.lnd.prof-x.net")
        with client.write_api(point_settings=point_settings) as write_api:
            # {'event_type': 'purge', 'etype': '800', 'ip_src': '188.39.246.174', 'ip_dst': '85.214.51.245', 'ip_proto': 'tcp', 'stamp_inserted': '2022-04-16 14:25:00', 'stamp_updated': '2022-04-16 14:30:01', 'packets': 9, 'bytes': 6034}

            tags = [
                'etype', 'as_dst', 'as_src', 'ip_proto', 'ip_dst', 'ip_src',
                'label'
            ]
            fields = ['bytes']

            with open(inputfile) as f:
                for line in f:
                    jsonline = json.loads(line)
                    datetime_object = datetime.strptime(
                        jsonline['stamp_inserted'],
                        '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
                    #datetime_object = datetime.strptime(jsonline['stamp_inserted'], '%Y-%m-%d %H:%M:%S')
                    p = Point("pmacct_traffic")
                    for tag in tags:
                        if jsonline.get(tag):
                            p.tag(tag, str(jsonline[tag]))
                    for field in fields:
                        p.field(field, int(jsonline[field]))
                    p.time(datetime_object)
                    print(p)
                    write_api.write(bucket=bucket,
                                    record=p,
                                    time_precision='s')
        client.close()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file",
                        help="The file to parse",
                        type=str,
                        default="./example.json")
    args = parser.parse_args()
    doupload(args.file)


if __name__ == "__main__":
    main()
