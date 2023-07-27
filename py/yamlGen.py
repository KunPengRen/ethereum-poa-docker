import yaml
import sys
from collections import OrderedDict 

nodes_path = sys.argv[1]
number_node =  int(sys.argv[2])
chain_id = int(sys.argv[3])
yaml_file = {'version':'3'}
nodes = {}
for i in range(1,number_node+1):
    node={}
    http_port=str(30312+i)
    port=str(8502+i)
    ws_port = str(33444+i)
    node['hostname']='node_'+str(i)
    node['image']='ethereum/client-go:release-1.10'
    worker_node_id = ''
    if i < 9:
        worker_node_id = 'worker-00'+str(i+1)
    elif i < 99:
        worker_node_id = 'worker-0'+str(i+1)
    node['deploy']={'placement':{'constraints':['node.hostname=='+worker_node_id]}}
    node['command']='--datadir  /root/data --nodiscover --syncmode full --nodekey /root/files/priv.key --port '+str(http_port)+' --http --http.addr "0.0.0.0" --http.vhosts="*" --http.corsdomain="*" --http.port '+str(port)+' --http.api db,eth,net,web3,admin,personal,miner,signer:insecure_unlock_protect  --networkid '+str(chain_id)+' --unlock 0 --password /root/files/password --mine --allow-insecure-unlock  --ws --ws.port '+str(ws_port)+' --ws.addr "0.0.0.0" --ws.origins="*" --ws.api eth,net,web3'
    volumes=[]
    volumes.append('./nodes/node_'+str(i)+'/keys/password:/root/files/password:ro')
    volumes.append('./nodes/node_'+str(i)+'/keys/priv.key:/root/files/priv.key:ro')
    volumes.append('./nodes/node_'+str(i)+'/data:/root/data:rw')
    volumes.append('/root/data/geth/nodes/')
    volumes.append('/root/data/geth/triecache/')
    ports=[]
    ports.append(http_port+':'+http_port)
    ports.append(port+':'+port)
    ports.append(ws_port+':'+ws_port)
    node['volumes']=volumes
    node['ports']=ports
    nodes.update({ 'node'+str(i) : node })
yaml_file['services']= nodes
stream = open('docker-compose.yaml', 'w')
yaml.dump(yaml_file, stream)
