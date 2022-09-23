import json
import os
import socket as s
import struct
import pickle
import sock_utils
import sys
from datetime import datetime
from multiprocessing import Condition, Queue
import threading
import time, functions
import codecs

from SensorHandler import SensorHandler
import db_setup

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

dataQueue = Queue()
 
def communicate(cond):
    """
    Thread that communicates with the socket and receives data.

    Args:
        cond ([Condition]): lock condition
    """
    while True:
        try:
            
            # connbuf = sock_utils.buffer(conn_sock)
            # data = connbuf.get_bytes(4) #9 fields X 8 bytes of each float 
            # size = struct.unpack('!i', data)[0]
            # print(size)
            
            # data_to_unpack = connbuf.get_bytes(size) #9 fields X 8 bytes of each float 
            # print(data_to_unpack)    
    
            #Received data from client
            size_bytes = sock_utils.receive_all(conn_sock, 4)
            size = struct.unpack('!i', size_bytes)[0]

            msg_bytes = sock_utils.receive_all(conn_sock, size)
            recvCmd = pickle.loads(msg_bytes)
            # print(msg_bytes)
            # try:
            #     # recvCmd = pickle.loads(data_to_unpack)
            #     data = json.loads(codecs.decode(msg_bytes))
            # except Exception as e:
            #     print(e)
            cond.acquire()

            data = json.loads(recvCmd)
            dataQueue.put(data)
            
            # print(data, flush=True)
            

            cond.notify()
            cond.release()
        except:
            print("waiting for data")
            print(sensor_handler)
            time.sleep(5)
            continue

def processing(cond, sensor_handler):
    """
    Threads that processes received data.
    For each value received:
    aligns times -> creates entry vectors -> tries making predictions -> checks its quality -> output

    Args:
        cond ([Condition]): lock condition
        sensor_handler ([SensorHandler]): SensorHandler object
    """
    while True:
        cond.acquire()
        while dataQueue.qsize() == 0: 
            val = cond.wait(timeout=10)

            if not val:
                print(sensor_handler)
                # break
        
        data = dataQueue.get()
        # print("data:", data, flush=True)

        sensor_handler.append(data)
            
        cond.release()

        #output
        msg = ''

        count = 0
        for i in sensor_handler.sensors_data.keys():
            if count == 0:
                now = datetime.now()
                msg = f'[{now:%Y-%m-%d %H:%M:%S}]'
            sensor = sensor_handler.sensors_data[i]
            msg += f'[{i} -> M: [{len(sensor.get_values()[1])}]]   '
            count += 1

        if len(msg) > 0:
            print(msg, flush=True)
            print(f'Entry Queue Size: {dataQueue.qsize()}, Prediction Queue: {sensor_handler.prediction_queue.qsize()}', flush=True)


if __name__ == "__main__":
    """
    Starts server. Receives configuration file, a json file, with the necessary information to process data.
    This information is given to the SensorHandler class and it is also used to create a socket communication. 
    """
    if len(sys.argv) == 2:
        json_path = sys.argv[1]

        data = functions.load_cfg(json_path)
        
        if functions.validate_config_file(data):
            sensor_handler_data = data["sensor_handler"]
            communication_data = data["communication"]
            sensors = data["sensors"]

            HOST = communication_data["host"]
            PORT = int(communication_data["port"])

            server = sock_utils.create_tcp_server_socket(HOST, PORT, 1024)
            

            sensor_handler = SensorHandler(int(sensor_handler_data["period_time"]), 
                                        int(sensor_handler_data["run_periods_self"]), 
                                        int(sensor_handler_data["run_periods_others"]), 
                                        int(sensor_handler_data["approach"]), 
                                        float(sensor_handler_data["cdf_threshold"]),
                                        int(sensor_handler_data["skip_period"]),
                                        False)

            condition = threading.Condition()            
            
            processingThread = threading.Thread(name="processingThread", target=processing, args=(condition, sensor_handler,))
            processingThread.start()
            commThread = threading.Thread(name="communicationThread", target=communicate, args=(condition,))
            commThread.start()

            while True:
                (conn_sock, addr) = server.accept()
            
        else:
            raise Exception("Error cfg")
