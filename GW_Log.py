import serial
import time
import datetime
import serial.tools.list_ports



port = 'COM16'
baudrate = 115200
databits = 8
stopbits = 1
prioty = None

t = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
logName = 'GW_LOG_{}.txt'.format(t)

sp = serial.Serial(port=port, baudrate=baudrate)

# l = list(serial.tools.list_ports.comports())
# print(l)

# print(len(list(l[0])))
# for i in range(len(list(l[0]))):
#     print(l[0][i])
# # print(l[0][0])

# exit()

line = ''
f = open(logName, 'a+')
snr = 0
rssi = 0
have_snr = 0
have_rssi = 0
pktrssi = 0
have_pktrssi = 0
currssi = 0
have_currssi = 0
while True:
    try:
        re = sp.readline()
        try:
            line = ''
            line = re.decode('gbk')
            t = datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')
            print('['+t+']'+'\t'+line)
            f.write('['+t+']'+'\t'+line+'\n')
            if '"rssi"' in line:
                rssi = eval(line[:-2])['rssi']
                have_rssi = 1
            if 'snr' in line:
                key = eval(line[:-2])
                snr = key['snr']
                pktrssi = key['pktrssi']
                currssi = key['currssi']
                have_currssi = 1
            if have_rssi == 1 and have_currssi == 1:
                t = datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')
                record = '{},{},{},{},{}\n'.format(t, rssi, snr, pktrssi, currssi)
                fr = open('rssi_record.csv', 'a+')
                fr.write(record)
                fr.close()
                rssi = 0
                have_rssi = 0
                snr = 0
                have_snr = 0
                pktrssi = 0
                have_pktrssi = 0
                currssi = 0
                have_currssi = 0
        except:
            pass
    except KeyboardInterrupt as e:
        print(e)
        f.close()
        exit()



