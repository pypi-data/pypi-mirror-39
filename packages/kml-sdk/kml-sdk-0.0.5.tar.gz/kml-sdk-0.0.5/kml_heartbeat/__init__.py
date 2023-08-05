import os
import time
import etcd3

etcd_host = ''
etcd_port = 2379
client=etcd3.client(host=etcd_host,ca_cert='/etcd/ca.pem',cert_key='/etcd/etcd-key.pem',cert_cert='/etcd/etcd.pem')

def heartbeat(timeout, operation="alert"):
    client.put('/kml/production/heartbeat/job/'+os.environ['KML_ID'], "%d %d %s" % (time.time(), timeout, operation))
