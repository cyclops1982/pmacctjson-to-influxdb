# PMACCT Json To Influxdb

Simple script that reads PMACCT's JSON format and pushes it to influxdb


Example JSON:
```json
{"event_type": "purge", "etype": "800", "ip_src": "188.39.246.174", "ip_dst": "88.99.84.253", "ip_proto": "tcp", "stamp_inserted": "2022-04-16 13:30:00", "stamp_updated": "2022-04-16 13:35:01", "packets": 18, "bytes": 11882}
{"event_type": "purge", "etype": "800", "ip_src": "188.39.246.174", "ip_dst": "198.51.45.8", "ip_proto": "udp", "stamp_inserted": "2022-04-16 13:30:00", "stamp_updated": "2022-04-16 13:35:01", "packets": 1, "bytes": 67}


```

