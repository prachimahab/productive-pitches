import socket
import sys
import json  # way data is being represented

import plotly 
import numpy as np
import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
from plotly.graph_objs import Scatter, Layout

from datetime import datetime, timedelta
import time

from timeit import default_timer as timer

# TCP Echo Client reference: https://pymotw.com/2/socket/tcp.html
# Reference: http://www.unclesax.audio/feed/
# Reference: https://plot.ly/python/streaming-tutorial//

# plotly.tools.set_credentials_file(username='prachim', stream_ids = "aed1rgyebp",
#                                   api_key='xrwXylUxGBZB3Yuj1pnv')

class TGC(object):
    def __init__(self):
        self.port = 13854
        self.hostAddress = "localhost"  # 127.0.0.1

        self.cred_file = tls.get_credentials_file()#['stream_ids']
        self.stream_ids = self.cred_file['stream_ids']
        # Get stream id from stream id list
        self.stream_id_attention = self.stream_ids[0]
        self.stream_id_rawEEG = self.stream_ids[1]
        self.stream_rawEEG = go.Stream(token=self.stream_id_rawEEG,  # link stream id to 'token' key
                     maxpoints=80)
        self.stream_attention = go.Stream(token=self.stream_id_attention,  # link stream id to 'token' key
                     maxpoints=80)     # keep a max of 80 pts on screen
        # Initialize trace of streaming plot by embedding the unique stream_id
        self.trace_attention = go.Scatter(
            x=[],
            y=[],
            mode='lines+markers',
            stream=self.stream_attention) # (!) embed stream id, 1 per trace
        self.trace_rawEEG = go.Scatter(
            x=[],
            y=[],
            mode='lines+markers',
            stream=self.stream_rawEEG)
        data_all = go.Data([self.trace_attention, self.trace_rawEEG])
        layout_all= go.Layout(xaxis = dict(range= [0, 60]), 
                              yaxis = dict(range = [0, 120]),
                              title='Attention and Raw EEG')
        self.fig_all = go.Figure(data=data_all, layout=layout_all)
        self.s_attention = py.Stream(self.stream_id_attention)
        self.s_rawEEG = py.Stream(self.stream_id_rawEEG)
        self.attention = 0

    def connect(self):
        # AF_INET is the addressing stream that is used
        # SOCK_STREAM is TCP (protocal supported by MindWave)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.hostAddress, self.port))  # server address
        print(self.sock)
        formatting = "{\"enableRawOutput\":true,\"format\":\"Json\"}"
        formatting_encoded = formatting.encode()
        self.sock.send(formatting_encoded)
        formatting_sent = self.sock.send(formatting_encoded)
        print(formatting_sent)

        # used to create appKey: http://www.sha1-online.com/

        parameters = "{\"appName\":\"Productive Pitches\",\"appKey\":\"a2685e4803fbe0982bd4d61afdee616a062aa7a5\"}"
        parameters_encoded = parameters.encode()
        self.sock.send(parameters_encoded)
        parameters_sent = self.sock.send(parameters_encoded)
        print(parameters_sent)

    def Graph(self, action):
        if action == "open":
            # Send fig to Plotly, initialize streaming plot, open new tab
            py.iplot(self.fig_all, filename='python-streaming', auto_open=True)
            # We will provide the stream link object the same token that's associated with 
            # the trace we wish to stream to
            self.s_attention.open()
            self.s_rawEEG.open()

        if action == "closed":
            self.s_attention.close()
            self.s_rawEEG.close()


    def timeStr(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

    
    def readData(self):
        BUFFER = 2048
        endTime = datetime.now() + timedelta(minutes = 5)

        self.Graph("open")
        while datetime.now() < endTime:
            data = self.sock.recv(BUFFER)  # number of characters
            data_str = str(data)
            data = data_str.split('\r')

            print("data",data)
            for line in data:
                line = line[2:-5]
                try:
                    json_data = json.loads(line)
                    #print(json_data)
                    if "eSense" in json_data:
                        eSense = json_data["eSense"]
                        if "attention" in eSense:
                            attention = eSense["attention"]
                            x = []
                            for i in range(0, 45):
                                x.append(i)

                            self.attention = attention
                            y = attention
                            #print(attention)
                    if "rawEeg" in json_data:
                        rawEeg = json_data["rawEeg"]
                        x_raw = []
                        for i in range(0, 45):
                            x_raw.append(i)
                        y_raw = rawEeg
                    self.s_attention.write(dict(x= x, y=y))
                    self.s_rawEEG.write(dict(x= x_raw, y= y_raw))

                except:
                    continue
    


