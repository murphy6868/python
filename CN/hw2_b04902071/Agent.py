import socket, time, threading, random
lossrate = 0.01
host = 'localhost'
timeout = 1
stopdrop = 0

def seq_data(b):
    string = b
    return (int(string[:20]), string[20:])

Aserverport = 8002
Aserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Aserver.bind((host, Aserverport))
#Aserver.settimeout(timeout)

Aclientport = 8001
Aclient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

Cserverport = 8008
Cserver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
Cserver.bind((host, Cserverport))

Cclientport = 8007
Cclient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
total = 0
loss = 0

def is_loss():
    if random.uniform(0, 1) > lossrate :
        return 0
    else:
        return 1
def drop_loop():
    global total, loss, buf
    while True:     
        buf, addr = Aserver.recvfrom(1024)
        s, d = seq_data(buf)
        if d == bytes("finxfin", 'utf8'):
            print("get     fin     ")      
        else:
            print("get     data    #%d" % s)
        if is_loss():
            total += 1
            loss += 1
            if d == bytes("finxfin", 'utf8'):
                print("drop    fin     #%d,    loss rate = %f" % (s, loss/total))
            else:
                print("drop    data    #%d,    loss rate = %f" % (s, loss/total))
        else:
            total += 1
            Cclient.sendto(buf, (host, Cclientport))
            if d == bytes("finxfin", 'utf8'):
                print("fwd     fin")
                break ;
            else:
                print("fwd     data    #%d,    loss rate = %f" % (s, loss/total))
    Aserver.close()
class my_drop_Thread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        print ("my_drop_Thread start：")
        drop_loop()
        print ("my_drop_Thread stop")

def ack_loop():
    while True:
        buf, addr = Cserver.recvfrom(1024)
        s, d = seq_data(buf)
        Aclient.sendto(buf, (host, Aclientport))
        if s == 99999999999999999999:
            print("get     finack     ")
            print("fwd     finack     ")
            break ;
        print("get     ack     #%d" % s)
        print("fwd     ack     #%d" % s)
    Cserver.close()
class my_ack_Thread (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        print ("my_ack_Thread start：")
        ack_loop()
        print ("my_ack_Thread stop")
        
dropThread = my_drop_Thread()
dropThread.start()
ackThread = my_ack_Thread()
ackThread.start()
print("main_Thread stop")
