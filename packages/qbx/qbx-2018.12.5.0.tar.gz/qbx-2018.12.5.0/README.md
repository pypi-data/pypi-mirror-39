
# usage
## Register Websocket

qbx register_ws --name /$endpoint --uri $uri --port $port

client will connect to api.qbtrade.org/wsv2/$endpoint

the proxy will to connect to $container:${port}/${uri}


## Example

qbx register_ws --name /candle --uri ws --port 3000

### Python Server Pesudo Code
server.listen('/ws', port=3000)

### Python Client Pesudo Code
ws_connect('ws://api.qbtrade.org/wsv2/candle')



# Developer

需要pip install pyinvoke

## Upload

inv add-version

watch build status
http://gitlab.qbtrade.org/root/qbx/pipelines
