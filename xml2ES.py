import xmltodict
import json
from elasticsearch import Elasticsearch
from elasticsearch.connection import create_ssl_context
import sys
##By: Milad Fadavvi

def Connect2ES(ip='127.0.0.1',port='9200',user="",password="",https=False,CertPath="",ES_Index='reports',Data=""):
    ## Connection to Elastic Search (http/https)
    raiseFieldLimit = '''
{  
  "index.mapping.total_fields.limit": 500000
}'''

    if https :
        context = create_ssl_context(cafile=CertPath)
        es = Elasticsearch(
                [ip],
                http_auth=(user, password),
                scheme="https",
                port=int(port),
                ssl_context=context,
        )
    else :
        es = Elasticsearch(
        [ip],
        scheme="http",
        port=int(port),
    )      

    if not es.indices.exists(index=ES_Index):
        es.indices.create(index=ES_Index, ignore=400,body=raiseFieldLimit) 
    es.index(index=ES_Index, doc_type='Report', body=Data)


def XML2JSON(address):
    # Any XML 2 JSON (tested on: ZAP, Nesus v2 and higher, acunetix 11, Openvas, Arachni , Nikto, NMAP) 
        file = open(address,"r")
        return (json.dumps(xmltodict.parse(file.read())))


if (sys.argv[1] == 'http'):
    Connect2ES (ip=sys.argv[2],port=sys.argv[3],https=False,ES_Index=(sys.argv[5]),Data=XML2JSON(sys.argv[4]))
elif (sys.argv[1] == 'https'):
    Connect2ES (ip=sys.argv[2],port=sys.argv[3],https=True,user=sys.argv[6],password=sys.argv[7],CertPath=sys.argv[8],ES_Index=(sys.argv[5]),Data=XML2JSON(sys.argv[4]))
else:
    print ('Did not support on this version')

# Usage: python3 scanner.py [HTTP] [ES IP] [ES Port] [XML Path] [ES Index name]
#        python3 scanner.py [HTTPs] [ES IP] [ES Port] [XML Path] [ES Index name] [User Name] [Password] [Cert Path]


