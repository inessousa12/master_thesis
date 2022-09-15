from PredictionBlock import PredictionBlock
from QualityBlock import QualityBlock
from multiprocessing import Queue
from SensorData import SensorData

import statistics, csv, threading
from datetime import datetime, time
import numpy as np

class SensorHandler:
    def __init__(self, period_time, run_periods_self, run_periods_others, approach, cdf_threshold=0.998, skip_period=0, ignore_miss=False):
        """
        Sensor Handler class. Handles all sensor's variables

        Args:
            period_time ([int]): seconds between each measurement
            run_periods_self ([int]): number of values from the target sensor
            run_periods_others ([int]): number of values from neighbor sensors
            approach ([int]): approach to be used for the creation of entry vectors
            cdf_threshold (float, optional): cdf threshold. Defaults to 0.998.
            skip_period (int, optional): minimum tax of sampling. Defaults to 0.
            ignore_miss (bool, optional): Defaults to False.
        """
        # Data Arch
        self.sensors_data = {}
        self.period_time = period_time
        self.run_periods_self = run_periods_self
        self.run_periods_others = run_periods_others
        self.skip_period = skip_period
        self.ignore_miss = ignore_miss
        self.approach = approach
        self.sValues = None
        self.sTimes = None

        # Prediction Block
        self.predictions_data = {}  # {key=sensor, value={key=index, value=[(path, type, p)]}}
        self.prediction_block = PredictionBlock()
        self.prediction_queue = Queue(maxsize=1000)

        # Quality & Failure Detection Block
        self.quality_data = {}  # {key=sensor, value={key=index, value=quality}}
        self.cdf_threshold = cdf_threshold
        self.quality_block = QualityBlock(self.cdf_threshold)
        self.quality_queue = Queue(maxsize=1000)
        
        # Threads
        self.__prediction_thread = threading.Thread(target=self.__prediction_quality_t, args=(self.ignore_miss,))
        self.__prediction_thread.start()

        # self.__quality_thread = threading.Thread(target=self.__quality_t, args=(condition,))
        # self.__quality_thread.start()

    def get_period_time(self):
        return self.period_time
    
    def get_run_periods_self(self):
        return self.run_periods_self

    def get_run_periods_others(self):
        return self.run_periods_others
    
    def get_skip_period(self):
        return self.skip_period

    def get_sensors_data(self):
        return self.sensors_data

    def get_approach(self):
        return self.approach

    def get_prediction_queue(self):
        return self.prediction_queue.get_nowait()

    def __str__(self):
        str = ""
        for sensor in self.sensors_data:
            self.sensors_data[sensor].get_values_in_csv()
            print("outfile values done")

            with open('./data/' + sensor + '/' + sensor + '_out_file_predictions.csv', 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)

                values = []
                times = []
                for key in list(self.predictions_data[sensor]):
                    p = []
                    for i in range(len(self.predictions_data[sensor][key])):
                        p.append(self.predictions_data[sensor][key][i][2])
                    mean_predictions = statistics.mean(p)
                    values.append(mean_predictions)
                    times.append(self.predictions_data[sensor][key][0][3])

                zipped = list(zip(times, values))

                for elem in zipped:
                    writer.writerow(elem)
                print("outfile predictions done")
                print(len(values))
        return str

    def append(self, data):
        """
        Appends data to the prediction queue.

        Args:
            data ([dict]): data to be appended.
        """
        sensor = data["sensor"]
        if sensor not in self.sensors_data:
            self.sensors_data[sensor] = SensorData(sensor, self.run_periods_self, self.period_time)
            self.predictions_data[sensor] = {}
            self.quality_data[sensor] = {}

        appended_indexes = self.sensors_data[data["sensor"]].append(data)

        if len(appended_indexes) > 0:
            self.prediction_queue.put((appended_indexes, sensor))
            
    def __prediction_quality_t(self, ignore_miss):
        while True:
            values = self.prediction_queue.get()
            inserted_values_indexes = values[0]

            sensor = values[1]

            for index in inserted_values_indexes:
                values = self.prediction_block.try_prediction(index, sensor, self.sensors_data,
                                                            self.run_periods_self, self.run_periods_others,
                                                            self.skip_period, ignore_miss)

                if len(values) > 0:
                    if index not in self.predictions_data[sensor]:
                        self.predictions_data[sensor][index] = []
                    self.predictions_data[sensor][index].extend(values)
                    self.quality_queue.put((sensor, index))

                    #quality
                    sensor, index = self.quality_queue.get()
                    predictions = self.predictions_data[sensor][index]
                    actual = self.sensors_data[sensor].get(index)
                    quality = 1
                        
                        
                    if not actual['prediction']:
                        m = actual['value']
                        p = [i[2] for i in predictions]
                        
                        if m is not None:
                            errors = self.quality_block.calculate_error(m, p)
                            faulty, probabilities = self.quality_block.fault_detection(predictions, errors)
                        else:
                            faulty = True

                        to_replace = False
                        if not faulty:
                            quality = self.quality_block.quality_calculation(probabilities)
                        else:
                            quality = 0
                            now = datetime.now()

                            _, true_t = self.sensors_data[sensor].get_values()
                            temp = self.sensors_data[sensor].get(index)['time']
                            true_index = true_t.index(temp)

                            print(f'[{now:%Y-%m-%d %H:%M:%S}] [{sensor} at index: {true_index} FAULT DETECTED]')

                            to_replace = True

                    if to_replace:
                        mean_predictions = statistics.mean(p)
                        self.sensors_data[sensor].put_prediction(mean_predictions, index)
                    else:
                        self.sensors_data[sensor].set_true_value(index)

                    self.quality_data[sensor][index] = quality
                    self.sensors_data[sensor].set_quality(index, quality)
                    self.sensors_data[sensor].insert_into_db(self.sensors_data[sensor].get(index))

    