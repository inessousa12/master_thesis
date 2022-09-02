import copy
import numpy as np
import tensorflow as tf
from tensorflow import keras
import csv
# import db_setup

class SensorData:
    """
    SensorData class. Stores raw data from a sensor.
    """

    def __init__(self, sensor, run_periods_self, period_time):
        """
        Initializes the SensorData class.

        Args:
            sensor ([str]): Sensor's name
            run_periods_self ([int]): number of values sent from the target sensor
            period_time ([int]): seconds between each measurement
        """
        self.sensor_name = sensor
        self.type = ""
        self.run_periods_self = run_periods_self
        self.period_time = period_time

        self.frequency = -1

        # {"value", "time", "type", "sensor"}
        self.__raw_data = []
        self.__data = []
        self.__last_pointer = -1

        self.__init_buffer = []
        self._init_ok = False

    def __populate(self):
        """
        Populates list according to the initial buffer.

        Returns:
            [list]: list of appended indexes
        """
        intervals = {}
        for i in range(len(self.__init_buffer) - 1):
            a_time = self.__init_buffer[i]["time"]
            b_time = self.__init_buffer[i + 1]["time"]

            interval = float(b_time) - float(a_time)
            interval = round(int(interval), -1)
            if str(interval) in intervals:
                intervals[str(interval)] += 1
            else:
                intervals[str(interval)] = 1

        best_interval = int(max(intervals, key=intervals.get))

        start_idx = -1
        for i in range(len(self.__init_buffer) - 1):
            a_time = self.__init_buffer[i]["time"]
            b_time = self.__init_buffer[i + 1]["time"]

            interval = b_time - a_time
            interval = round(int(interval), -1)

            if interval == best_interval:
                start_idx = i
                break

        self._init_ok = True

        appended_indexes = []
        for i in range(start_idx, 10):
            appended_indexes.extend(self.append(self.__init_buffer[i]))

        return appended_indexes

    def append_raw(self, new_entry):
        """
        Appends raw measurement.

        Args:
            new_entry ([dict]): new raw measurement
        """
        self.__raw_data.append(new_entry)

    def append(self, new_entry):
        """Appends new entry.

        Args:
            new_entry ([dict]): new raw measurement

        Returns:
            [list]: list of appended indexes
        """
        appended_indexes = []
        
        new_entry["prediction"] = False
        new_entry["failure"] = False
        new_entry["failure_type"] = ""
        new_entry["quality"] = 0

        if self.type == "":
            self.type = new_entry["type"]

        if not self._init_ok:
            self.__init_buffer.append(new_entry)
            if len(self.__init_buffer) == 10:
                appended_indexes.extend(self.__populate())
        else:
            last_measurement = self.getLast()

            if last_measurement is not None:
                current_measurement_time = new_entry["time"]
                last_measurement_time = last_measurement["time"]
                jitter = 1 #seconds

                if current_measurement_time > last_measurement_time + float(self.period_time) + jitter:

                    while current_measurement_time > last_measurement_time + self.period_time + jitter:
                        self.__data.append({'time': last_measurement_time + self.period_time, 'value': None, 'type': 'temp', 'sensor': self.sensor_name, "prediction": False, "failure": True, "failure_type": "omission"})
                        last_measurement_time = last_measurement_time + self.period_time
                        appended_indexes.append(len(self.__data) - 1)
                        print("omission detected at ", len(self.__data) - 1)
                    to_append = True
                else:
                    to_append = True
            else:
                to_append = True

            if to_append:
                self.__data.append(new_entry)
                self.__last_pointer = len(self.__data) - 1
                appended_indexes.append(len(self.__data) - 1)

            self.append_raw(new_entry)

        return appended_indexes

    def getLast(self):
        """
        Gets last measurement
        """
        if len(self.__data) == 0:
            return None
        else:
            return self.__data[self.__last_pointer]

    def get(self, idx):
        """
        Gets value in a certain index
        """
        if idx <= len(self.__data) - 1:
            return self.__data[idx]
        else:
            return None

    def put_prediction(self, value, index):
        """
        Adds prediction to data dict.

        Args:
            value ([float]): prediction's value
            index ([int]): prediction's index
        """
        if index < len(self.__data):
            self.__data[index]["prediction"] = True
            if self.__data[index]["failure"] != True:
                self.__data[index]["failure"] = True
                self.__data[index]["failure_type"] = "outlier"
            self.__data[index]["true_value"] = copy.deepcopy(self.__data[index]["value"]) #raw value
            self.__data[index]["value"] = np.float32(round(value, 2)) #corrected value

    def set_true_value(self, index):
        self.__data[index]["true_value"] = copy.deepcopy(self.__data[index]["value"])
        
    def get_values(self):
        """
        Gets all values and times received.
        """
        return [i["value"] for i in self.__data], [i["time"] for i in self.__data]

    def get_raw_values(self):
        """
        Gets all raw measurements and times.
        """
        return [i["value"] for i in self.__raw_data], [i["time"] for i in self.__raw_data]

    def get_raw_values_w_predictions(self):
        """
        Gets all values and times with predictions.
        """
        return [i["value"] for i in self.__data if i["value"] is not None], \
            [i["time"] for i in self.__data if i["value"] is not None]

    def get_values_without_predictions(self):
        """
        Gets all values and times without predictions.
        """
        values = []
        times = []
        for i in self.__data:
            if i["prediction"] is False:
                values.append(i["value"])
                times.append(i["time"])
            else:
                values.append(None)
                times.append(i["time"])

        return values, times

    def get_values_in_csv(self):
        """
        Puts values and times in a csv
        """
        with open('./aquaIoT/framework/data/' + self.sensor_name + '/' + self.sensor_name + '_out_file.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            values = [i["value"] for i in self.__data]
            time = [i["time"] for i in self.__data]

            zipped = list(zip(time, values))

            for elem in zipped:
                writer.writerow(elem)

        # with open('./data/' + self.sensor_name + '/' + self.sensor_name + '_raw_file.csv', 'w', encoding='UTF8', newline='') as f:
        #     writer = csv.writer(f)

        #     values, time = self.get_raw_values()

        #     zipped = list(zip(time, values))

        #     for elem in zipped:
        #         writer.writerow(elem)

        with open('./aquaIoT/framework/data/' + self.sensor_name + '/' + self.sensor_name + '_outliers_file.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            values, time = [i["true_value"] for i in self.__raw_data if i["failure_type"] == "outlier"], [i["time"] for i in self.__raw_data if i["failure_type"] == "outlier"]

            zipped = list(zip(time, values))

            for elem in zipped:
                writer.writerow(elem)

    def insert_into_db(self, message):
        db_setup.insert_data(message)

    def set_quality(self, index, quality):
        self.__data[index]["quality"] = quality