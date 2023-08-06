# CloudFoxy - FoxyProxy

This proxy connects clients implementing simple TCP requests with the CloudFoxy 
RESTful API. You can send any support request via GitLab issues or open a 
support ticket at
[https://cloudfoxy.freshdesk.com](https://cloudfoxy.freshdesk.com/support/tickets/new)

## External dependencies

sudo yum install gcc libffi-devel python-devel openssl-devel

## Install

### Install the application

`pip install foxyproxy`

or 

`pip install --upgrade --no-cache-dir foxyproxy`

and create folder `/opt/cloudfoxy`, where we can store or related files and data

### Install supervisor for automatic restarts

`pip install supervisor`

`mkdir -p /etc/supervisord/conf.d`

`echo_supervisord_conf > /etc/supervisord/supervisord.conf`

`echo [include] >> /etc/supervisord/supervisord.conf`

`echo "files = conf.d/*.conf" >> /etc/supervisord/supervisord.conf`

`nano /etc/supervisord/supervisord.conf`

find a line with _inet_http_server_ and uncomment it (the section name), and the
first line, which is something like "port=127.0.0.1:9001"

`systemctl start supervisord`

`systemctl enable supervisord`   # auto restart after reboot

`nano /etc/supervisord/conf.d/foryproxy.conf`

and fill it with the following contents
```
[program:foxyproxy]
directory=/opt/cloudfoxy
command=foxyproxy -s http://127.0.0.1:8081 -c ica
user=root
autostart=true
autorestart=true
stderr_logfile=/var/log/foxyproxy.log
stdout_logfile=/var/log/foxyproxy.log
```

You can adjust parameters as required.

Restart the supervisor:

`systemctl restart supervisord`

`supervisorctl` - is a client, which shows status of processes - it has commands like:
 - start <name>
 - stop <name>
 - restart <name>
 - reread  # reads configuration files and shows changes
 - reload  # loads the new configuration to use for future commands
 

## TCP Interface

The TCP interface of the proxy starts listening on port 4001. The port can be 
adjusted with a command line parameter `-p<port>`. Similarly, the address of the 
RESTful server can be set with the `-s<url:port>`.

TCP clients can send multiple commands over a period of time as the server keeps 
connections opened until its clients close them.

Each request consists of at least 2 lines:
  - card reader identification
  - one or more commands - each in a separate line

*Example 1 - abstrakt*

```
><card reader name>"|"
><cmd ID1>:<command1>:<data>:<object>"|"
><cmd ID2>:<command2>:<data>:object"|"
```

*with a subsequent response to this request:*

```
<cmd ID1>:<response 1>
<cmd ID2>:<response 2>
@@
```

*Example 2*
```
>OMNIKEY AG 3121 USB|
>1:RESET|
>2:APDU|00 A4 00 0C 02 3F 00|
```

*with a subsequent response*
```
1:6F048400A5009000
2:9000
@@
```

*Example 3*
```
>*|
>1:ENUM|12
```

The first line creates a regular expression for selecting a set of card readers,
the optional numerical parameter of the ENUM command limits the number of terminals
returned to the client.

*with a subsequent response*
```
1:<base64 string of terminal names separated with "|">
```


## TCP Commands

There are currently four commands implemented for the TCP interface:
 - RESET - reset a particular smartcard
 - APDU - send a command according to ISO7816 specifications
 - ENUM - return a list of smart-card readers - names of reaers are base64 
          encoded, separated with "|"
 - ALIASES - return a list of names from certificates in connected smartcards, 
         names are base64 encoded as they may
         contain utf-8 characters; names are separated with "|"
 - CHAIN - return certificate chain for a particular alias
 - SIGN - request a signature from a particular smartcard

The first three are low-level commands, either directly sent to smartcards, or
just return a list of smartcard names. The ALIASES, CHAIN and
SIGN are abstract commands tailored to particular smartcards - eIDAS smartcards
sold by [http://ica.cz](I.CA - a Czech company). They show how the API can be
extended, although the CloudFoxy RESTful API also allows definitions of abstract
commands via protocols defines with a simple JSON notation.

## CloudFoxy Smartcards

CloudFoxy can interface smartcards connected via USB ports - as shown in the
example above, butthe primary reason why we built it was to provide a convenient
interface to the CloudFoxy hardware platform, which can host up to 120 smartcards.

The CloudFoxy RESTful server can connect to a multiple of them and provide access
to thousands of smartcards.

The CloudFoxy smartcards have the following name format:

```
"CloudFoxy " | <IP address> | "@" | <id> - example "CloudFoxy 192.168.42.10@120"
```

which is an enriched format of a geeky `/<IP address> |"@"|<id>`, e.g., `/192.168.42.10@120`


## End-to-End Dataflow Example

While a detailed description of the CloudFoxy RESTful API can be found
[here](https://gitlab.com/cloudfoxy/RESTfulFoxy), it makes sense to demonstrate the
whole dataflow, which compromises:

1. your application / telnet / script / APDUPlay (a Windows PC/SC library)
2. foxyproxy
3. CloudFoxy server

### Request

#### Client -> foxyproxy

```
>CloudFoxy 192.168.42.10@12|
>2342:RESET|
>2343:APDU:00A4040008A00000000300000000|
```

#### foxyproxy -> CloudFoxy RESTful

Assuming the RESTful API is running at the *http://restful.cloudfoxy.com:8081*
address.

`http://restful.cloudfoxy.com:8081/api/v1/basic?reset=1&terminal=%2F192.168.42.10%4012`

`http://restful.cloudfoxy.com:8081/api/v1/basic?apdu=00A4040008A00000000300000000&terminal=%2F192.168.42.10%4012`

*Note: each request to the RESTful API has to hav an X-Auth-Token header. The secrets
are defined in the configuration of each CloudFoxy RESTful server.

### Response

CloudFoxy RESTful returns a response to each of the GET requests, which will be
a simple text response if the `/api/v1/basic` endpoint is used.


#### CloudFoxy RESTful -> foxyproxy

There are two requests above, they may provide separate responses, which look like:

 - response 1: `6F048400A5009000`
 - response 2: `9000`

#### foxyproxy -> client

TCP proxy will combine the responses and send all in one message back to the client:

```
2342:6F048400A5009000
2343:9000
```

### CloudFoxy RESTful - Other Endpoints

This is a side note about other options for using CloudFoxy RESTful. If you use
