import socket, time
host = 'localhost'
def seq_data(b):
    string = b
    return (int(string[:20]), string[20:])
def flush(file_obj, buffer):
    for i in buffer:
        l = int(i[:4])
        file_obj.write(i[4:4 + l])
    buffer.__init__([])
    
clientport = 8008
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serverport = 8007
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((host, serverport))

seq = 1
bufferSize = 32
buffer = []
while True:
    global f
    buf, addr = server.recvfrom(1024)
    s, d = seq_data(buf)
    #print(s, d)
    if s == seq :
        if d == bytes("finxfin", 'utf8'):
            print("recv    fin      ")
            print("send    finack   ")
            client.sendto(bytes(("9")*20,'utf8'), (host, clientport))
            flush(f, buffer)
            f.close();
            break ;
        if len(buffer) == 32:
            print("drop    data    #%d" % s)
            print("send    ack     #%d" % (seq - 1))
            client.sendto(bytes(str(seq - 1).zfill(20),'utf8'), (host, clientport))
            print("flush")
            flush(f, buffer)
        else:
            print("recv    data    #%d" % s)
            print("send    ack     #%d" % s)
            client.sendto(bytes(str(s).zfill(20),'utf8'), (host, clientport))
            seq += 1
            if s == 1:
                d = d.decode('utf8')
                resultFile = "result" + d[:d.index('\0')]
                f = open(resultFile, 'wb')
                print(resultFile)
            else:
                buffer.append(d)
    else :
        print("drop    data    #%d" % s)
        print("send    ack     #%d" % (seq - 1))
        client.sendto(bytes(str(seq - 1).zfill(20),'utf8'), (host, clientport))