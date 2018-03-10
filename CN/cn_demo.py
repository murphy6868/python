import socket, time, threading

botnick = "iirobot "
hexset = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','F']
def send(msg):
    IRCSocket.send( bytes("PRIVMSG #CN_DEMO :%s\r\n" % msg, 'utf8'))
    time.sleep(0.2)
def ping(): # respond to server Pings.
    IRCSocket.send(bytes("PONG :pingis\r\n", "UTF-8"))
def notIP(seg):
    intseg = int(seg)
    if intseg > 255 : return 1
    if len(seg) > 1 and seg[0] == '0': return 1
    return 0
def robot():
    while True :
        msg = IRCSocket.recv( 4096 )
        mstr = str(msg)
        if len(msg) > 10 :
            print (msg)
        if "PING" in mstr :
            ping()
            print("ping me? I'm still alive haha")
        if "@repeat " in mstr :
            pos = mstr.index("@repeat ") + 8
            end = len(mstr) - 5
            send(mstr[pos:end])
        if "@ip " in mstr :
            pos = mstr.index("@ip ") + 4
            end = len(mstr) - 5
            ip = mstr[pos:end]
            l = len(ip)
            if l < 4 or l > 12 or not ip.isdigit(): continue
            ipnum = 0
            iplist = []
            for a in range(1, l-2) :
                for b in range(a+1, l-1) :
                    for c in range(b+1, l) :
                        if notIP(ip[:a]) or notIP(ip[a:b]) or notIP(ip[b:c]) or notIP(ip[c:]) :
                            continue
                        ips = ip[:a] + '.' + ip[a:b] + '.' + ip[b:c] + '.' + ip[c:]
                        ipnum += 1
                        iplist.append(ips)
                        #send(ips)
            send(ipnum)
            for i in range(ipnum):
                send(iplist[i])
        if "@convert " in mstr :
            pos = mstr.index("@convert ") + 9
            end = len(mstr) - 5
            num = mstr[pos:end]
            if num[0:2] == "0x":
                ok = 1
                for idx in num[2:]:
                    if not idx in hexset:
                        ok = 0
                        break
                if ok:
                    send(int(num,0))
            elif num.isdigit():
                send(hex(int(num)))
        if "@help" in mstr :
            send("@repeat <Message>");
            send("@convert <Number>");
            send("@ip <String>");
class myThread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        print ("开始线程：")
        robot()
        print ("退出线程：")

IRCSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
IRCSocket.connect( ( "irc.freenode.net", 6667 ) )
IRCSocket.send( bytes("USER "+ botnick +" "+ botnick +" "+ botnick + " " + botnick + "\r\n", 'UTF-8') )
IRCSocket.send( bytes("NICK "+ botnick +"\r\n", 'utf8') )
IRCSocket.send( bytes("JOIN #CN_DEMO \r\n", 'utf8') )
send("Hello! I am robot.")

robotThread = myThread()
robotThread.start()
while True:
    robotalk = input()
    send(robotalk)





