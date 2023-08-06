import json
import socket

import mjlib.config as config

import select



# stream OpenBCI data over UDP to algorithm
def udp_socket(main_win,cfg):
    print("streaming udp")

    vars.done_streaming = False

    ADDRESS = "127.0.0.1"
    PORT = 12345

    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind((ADDRESS, PORT))

    print("receiving data")
    while vars.stream:
        ready = select.select([sock], [], [], 1)
        if ready[0]:
            data, addr = sock.recvfrom(20000)
            try:
                modified_sentance = data.strip().decode('utf-8') #  'ISO-8859-1'

                modified_sentance = modified_sentance.rsplit('}', 1)[0] + '}'

                m = json.loads(modified_sentance)

                if main_win.RESET_CHANNELS:
                    config.reset_channels(*main_win.channel_reset_vars,main_win)
                    main_win.RESET_CHANNELS = False

                for i in config.channels:

                    chan1_eeg = m['data'][i]
                    main_win.data_in(chan1_eeg,cfg,i)


            except UnicodeDecodeError:
                print('got UnicodeDecodeError, skipping data')

    print('closing UDP listener')
    vars.done_streaming = True
    print("done streaming udp")
