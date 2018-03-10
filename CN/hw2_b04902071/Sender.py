import socket, time, sys
host = 'localhost'
timeout = 0.5
filename = sys.argv[1]
f = open(filename, "rb")
fileExtention = filename[filename.index('.'):]

clientport = 8002
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

serverport = 8001
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((host, serverport))
server.settimeout(0.1)
base = 0
seq = 1
threshold = 16
windowSize = 1
t1 = time.clock()
buffer = []
nextWindow = 1

while True:
    if len(buffer) == 0 and seq == 1:
        buffer.append(bytes(fileExtention.ljust(1004, '\0'), 'utf8'))
    elif len(buffer) < windowSize and not f.closed:
        for i in range(windowSize - len(buffer)):
            tmp = f.read(1000)
            if len(tmp) > 0:
                dlen = len(tmp)
                tmp = tmp.ljust(1000, bytes('\0', 'utf8'))
                buffer.append(bytes(str(dlen).zfill(4), 'utf8') + tmp)
            else:
                buffer.append("finxfin")
                f.close()
                break ;
    if nextWindow:
        nextWindow = 0
        t1 = time.clock()
        for i in range(min(windowSize, len(buffer))):
            seq_str = str(seq + i).zfill(20)
            if buffer[i] == "finxfin":
                print("send    fin")
                client.sendto(bytes(seq_str + buffer[i],'utf8'), (host, clientport))
                break ;
            print("send    data     #%d,   winSize = %d" % (seq + i, windowSize))
            client.sendto(bytes(seq_str,'utf8') + buffer[i], (host, clientport))
    elif (time.clock() - t1) > timeout:
        threshold = max(1, int(windowSize / 2))
        windowSize = 1
        base = seq - 1
        print("time   out,             threshold =", threshold)
        #print(base, seq, windowSize)
        t1 = time.clock()
        for i in range(min(windowSize, len(buffer))):
            seq_str = str(seq + i).zfill(20)
            if buffer[i] == "finxfin":
                print("resend  fin")
                client.sendto(bytes(seq_str + buffer[i],'utf8'), (host, clientport))
                break ;
            print("resend  data     #%d,   winSize = %d" % (seq + i, windowSize))
            client.sendto(bytes(seq_str,'utf8') + buffer[i], (host, clientport))
    try:
        ack, addr= server.recvfrom(20)
        ack = int(ack.decode('utf8'))
        if ack == 99999999999999999999:
            print("recv    finack")
            break ;
        print("recv    ack      #%d" % ack)
        if ack == seq:
            seq += 1
            buffer.pop(0)
            if seq == base + windowSize + 1:
                nextWindow = 1
                base = seq - 1
                if windowSize < threshold:
                    windowSize *= 2
                else:
                    windowSize += 1
        elif ack > seq:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(ack, seq)
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            while ack >= seq:
                seq += 1
                buffer.pop(0)
                if seq == base + windowSize + 1:
                    nextWindow = 1
                    base = seq - 1
                    if windowSize < threshold:
                        windowSize *= 2
                    else:
                        windowSize += 1
    except socket.timeout:
        yolo = 666
    
