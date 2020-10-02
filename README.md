# grpcping
Check tool for communication test with gRPC

## What's this?
Check the following :
- Send grpc requests and responses
- Stream bidirectional communication (file echo back)

## Usage
```shell script
grpcping -s (self address:port) -d (destination address:port) -i (file to echo back))
```
To specify the address/port, connect the IP address and the port with ":" (colon).

### 1. Server
If the -d (dst) option is not specified, it will continue to wait for requests in server mode.

Listening on the IP address "192.168.0.30" and port "8888" :
```shell script
grpcping -s 192.168.0.30:8888
```

There is no problem if output the following:
```
-> receive HELLO from localhost:9999
-> echo start
 --> echo: 0
 --> echo: 1
 --> echo: 2
 --> echo: 3
 --> echo: 4
-> echo end
```

### 2. Client
Sending a request from the IP address "192.168.0.45" port "8888", to the IP address "192.168.0.30" port "8888":
```shell script
grpcping -s 192.168.0.45:8888 -d 192.168.0.30:8888 -i test/test.png
```
=> Save the echoed image with the file name "output.png".

There is no problem if output the following:
```
Hello OK
 read: 0
 read: 1
 read: 2
 read: 3
 read: 4
 resp: 0
 resp: 1
 resp: 2
 resp: 3
 resp: 4
file output OK!
```

## If can't communicate?
If cannot communicate, please check the following:

- Error output to the console
- Port used by the firewall is not closed


## Installation
```shell script
pip install -r requirements.txt
python setup.py install
```
