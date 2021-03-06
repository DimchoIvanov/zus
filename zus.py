'''
Created on Apr 3, 2020

@author: Dimcho Ivanov
'''

'''
Doc excerpt:

1. Serial Port setting
    Parameter     Value
    Baud Rate     9600
    No. Bits      8
    Stop bit      1
    Parity        No
    Flow Control  No
    
2. Command Basics
    The device is designed to accept serial commands. Each command should end with CR (\r).
    The device will respond back with the reply appended with CR (\r) and prompt symbol >.
    Commands are not case sensitive.
    
3. Command List

    Version. Version command is used to check the device version.
    Command V\r
    Response OK:101\r>
    
    Information. Information command list the available USB ports, with the corresponding numbers.
    Command I\r
    Response OK:<port no> <port no> <port no> <port no> <port no> <port no> <port no> <port no> \r>
    
    Status. Status command returns the USB port number which is ON currently.
    Command S\r
    Response OK:<port no>\r>
    
    ON. ON command enables the given port. The port number is a two digit number from 00 - 55
    Command O<port no>\r
    Response OK:\r>
    
    OFF. OFF command disables the given port. The port number is a two digit number from 00 - 55
    Command F<port no>\r
    Response OK:\r>
    
    Any. Any command will disable which ever port is currently ON. This command does not need port number.
    Command A\r
    Response OK:\r>
'''

import sys
import serial
import time

def connectToBox(com):
    #try:
        ser = serial.Serial(com, 9600, timeout=1.0, inter_byte_timeout=0.1)
        ser.flushInput()
        ser.flushOutput()
        #time.sleep(3)
        #print("Connected to " + com)
        #read_val = ser.read(size=64)
        #print(read_val)
        return ser
    #except serial.SerialException as e:
    #    print("connectToBox failed with " + str(e))
    #    return None

def disconnectFromBox(ser):
    try:
        if (ser is not None):
            ser.close()
        #print("Disconnected") 
    except serial.SerialException as e:
        print("disconnectFromBox failed with " + str(e))

def connectUSB(ser, timeout, usb):
    try:
        print("Connecting " + str(usb))
        cmdStr = "O0" + str(usb) + "\r"
        cmdBytes = bytearray(cmdStr, "ascii")
        ser.write(cmdBytes)
        time.sleep(timeout)
        read_val = ser.read(size=64)
        print(read_val)
    except serial.SerialException as e:
        print("connectUSB failed with " + str(e))

def disConnectUSB(ser, timeout, usb):
    try:
        print("Disconnecting " + str(usb))
        cmdStr = "F0" + str(usb) + "\r"
        cmdBytes = bytearray(cmdStr, "ascii")
        ser.write(cmdBytes)
        time.sleep(timeout)
        read_val = ser.read(size=32) #
        print(read_val)
    except serial.SerialException as e:
        print("disConnectUSB failed with " + str(e))

def disConnAnyUSB(ser, timeout):
    try:
        print("Disconnecting Any Port")
        cmdStr = "A\r"
        cmdBytes = bytearray(cmdStr, "ascii")
        ser.write(cmdBytes)
        time.sleep(timeout + 0.5) #
        read_val = ser.read(size=32)
        print(read_val)
    except serial.SerialException as e:
        print("disConnectUSB failed with " + str(e))

def version(ser, timeout):
    try:
        print("ZUS Version :")
        cmdStr = "V" + "\r"
        cmdBytes = bytearray(cmdStr, "ascii")
        ser.write(cmdBytes)
        time.sleep(timeout)
        read_val = ser.read(size=32)
        print(repr(read_val))
    except serial.SerialException as e:
        print("Version failed with " + str(e))

def info(ser, timeout):
    try:
        print("Info :")
        cmdStr = "I" + "\r"
        cmdBytes = bytearray(cmdStr, "ascii")
        ser.write(cmdBytes)
        time.sleep(timeout)
        read_val = ser.read(size=32)
        print(str(read_val))
    except serial.SerialException as e:
        print("Status failed with " + str(e))

def status(ser, tmout):
    try:
        print("Conn.port :")
        cmdStr = "S" + "\r"
        cmdBytes = bytearray(cmdStr, "ascii")
        ser.write(cmdBytes)
        time.sleep(tmout)
        read_val = ser.read(size=32)
        print(str(read_val))
    except serial.SerialException as e:
        print("Status failed with " + str(e))

def usage():
    print("Usage: ")
    print("      zus.py [N|f] : connect / disconnect port;")
    print("               N: the port number going be connected, [0-7];")
    print("               f: disconnect any port; ")
    print("      zus.py -s    : get box F/W version & available ports; ")
    print("      zus.py -p    : get connected port, [0-7] if connected, none if no port connected; ")
    print("      zus.py -h    : help - this message; ")

#MAIN is HERE!!!


def main(argv):
    #
    comport = "COM7"
    usbport = -1
    timeout = 0.5
    #discTimeout = 1
    ser = None
    cmd_p_on = False;
    cmd_poff = False;
    cmd_psts = False;
    cmd_help = False;
    cmd_stat = False;
    #
    #print("args[" + str(len(argv)) + "]: " + str(argv[0]) + ":" + str(argv[1]) + ":" + str(argv[2]) + ":" + str(argv[3]))
    if (len(argv) > 1):
        #print("args[" + str(len(argv)) + "]:<" + str(argv[0]) + ":" + str(argv[1]) + ">")
        if (argv[1].isdigit()):
            usbport = int(argv[1], 10)
            cmd_p_on = True
        elif (argv[1].lower() == 'f'):
            cmd_poff = True
        elif (argv[1].lower() == '-p'):
            cmd_psts = True
        elif (argv[1].lower() == '-s'):
            cmd_stat = True
        elif (argv[1].lower() == '-h'):
            cmd_help = True
        else:
            print("unsupported option :" + str(argv[1]))
            cmd_help = True
    elif (len(argv) > 0):
        #print("args[" + str(len(argv)) + "]:<" + str(argv[0])  + ">")
        cmd_help = True
    else: #(len(argv) == 0):
        print("args[" + str(len(argv)) + "]")
    #
    ##########################################################
    #try:
    #    (opts, args) = getopt.getopt(sys.argv[1:], "hsf", ["help", "status", "off"])
    #except getopt.GetoptError as err:
    #    # print help information and exit:
    #    print(err)  # will print something like "option -a not recognized"
    #    usage()
    #    sys.exit(2)
    #cmd_off = False
    #cmd_status = False
    #for o, a in opts:
    #    if o == "-s":
    #        cmd_status = True
    #    elif o in ("-h", "--help"):
    #        usage()
    #        sys.exit()
    #    elif o in ("-f", "--off"):
    #        cmd_off = True
    #    else:
    #        assert False, "unhandled option"
    #
    #if (len(args) > 0):
    #    usbport = int(args[0], 10)
    ##########################################################
    if (cmd_help):
        usage()
        sys.exit(2)
    
    if (cmd_p_on or cmd_poff or cmd_psts or cmd_stat):
        try:
            ser = connectToBox(comport)
            if (cmd_p_on):
                connectUSB(ser, timeout, usbport)
            elif (cmd_poff):
                disConnAnyUSB(ser, timeout)
            elif (cmd_psts):
                status(ser, tmout=timeout)
            elif (cmd_stat):
                version(ser, timeout)
                info(ser, timeout)
            else:
                print ("Error!")
        except serial.SerialException as e:
            print("Failed with exception: " + str(e))
        except ValueError as e:
            print("Failed with exception: " + str(e))
        except KeyboardInterrupt:
            print("Bye!")
        finally:
            disconnectFromBox(ser)
    ##########################################################


if __name__ == '__main__':
    main(sys.argv)
