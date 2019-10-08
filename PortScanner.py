import nmap
import optparse
import sys

#using nmap module to scan port
def ScanPort(host, port):
    scanner = nmap.PortScanner()
    scanner.scan(host, port)
    try:
    	return scanner[host]['tcp'][int(port)]['state']
    except Exception as e:
    	print("Error:", e)


if __name__ == "__main__":
    # #parser setting
    # #-h is conflicting help , so use -H
    # parser = optparse.OptionParser("usage%proge" + "-H <target host> -p <target port>")
    # #dest is used to save temp variable
    # parser.add_option("-H", dest = "tgtHost", type = "string", help="specify target host")
    # parser.add_option("-p", dest = "tgtPort", type = "string", help="specify target port.Seperate different ports by ,")
    # #get host and port
    # options, args = parser.parse_args()
    # #the name options.tgtHost comes from the dest variable
    # tgtHost = options.tgtHost
    # #usually we get at least one port
    # tgtPorts = str(options.tgtPort).split(',')
    # if tgtHost == None or tgtPorts == None:
    #     print(parser.usage)
    #     sys.exit()
    tgtHost = "51.24.44.446"
    tgtPorts=["80", "21", "8080"]
    print("-------------------Port Scanner is Running-----------------")
    #in case of extra spaces
    for port in tgtPorts:
        port = port.strip()
        state = ScanPort(tgtHost, port)
        print(" [*] {0} tcp/{1} {2}".format(tgtHost, port, state))
