import os
import time
import etcd

etcd_host = 'paas-etcd-yz.internal'
etcd_port = 2379
etcd_client = etcd.Client(host=etcd_host, port=etcd_port)

def heartbeat(timeout, operation="alert"):
    etcd_client.write('/kml/production/heartbeat/job/'+os.environ['KML_ID'], "%d %d %s" % (time.time(), timeout, operation))
