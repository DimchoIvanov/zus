# ZUS
Zilogic USB switch control

Simple script sending commands to the Zilogic's USB switch box.
See the usage :
```
#zus.py -h
Usage:
      zus.py [N|f] : connect / disconnect port;
               N: the port number going be connected, [0-7];
               f: disconnect any port;
      zus.py -s    : get box F/W version & available ports;
      zus.py -p    : get connected port, [0-7] if connected, none if no port connected;
      zus.py -h    : help - this message;
```
