import tensorflow as tf
from tensorflow import keras
import numpy as np
import os
import json
import functions, time

class PredictionBlock:
    """
    Prediction Block class.
    """
    def __init__(self):
        """
        Initializes Prediction Block class
        """
        self.models = self.startup_models()
        pass

    def get_model(self, sensor, typeM, size):
        """
        Gets the best model for the prediction
        """
        if size == "others":
            sizeM = "neighbours"
        else:
            sizeM = size

        if sensor in self.models:
            models = [i for i in self.models[sensor] if sizeM == i['sizeM'] and typeM == i['typeM']]

            if len(models) != 0:
                best_model = models[0]
                for model in models:
                    if model['loss'] < model['loss']:
                        best_model = model

                return best_model
        return None

    def try_prediction(self, appended_index, sensor, sensors, run_periods_self,
                       run_periods_others, skip_period, ignore_miss):
        """
        Tries o make a prediction.

        Args:
            appended_index ([int]): target index
            sensor ([str]): sensor's name
            sensors ([list]): list of sensors available
            run_periods_self ([int]): number of values sent from the target sensor
            run_periods_others ([int]): number of values sent from neighbor sensors
            skip_period ([int]): minimum tax of sampling
            ignora_miss ([bool]): flag that ignores missing data

        Returns:
            [list]: list of predictions
        """
        # Check if we have atleast 750min of data (1tide period)
        sensor_names = list(sensors.keys())
        min_time = sensors[sensor].get(0)["time"] + ((720) * 60)
        target_time = sensors[sensor].get(appended_index)["time"]
        diff = target_time - min_time
        # print("min_time:", min_time, flush=True)
        # print("target_time:", target_time, flush=True)
        # print("diff: ", diff, flush=True)

        if diff > 0:
            diffs = []
            
            for sn in sensor_names:
                current_min_time = sensors[sn].get(0)["time"] + ((720) * 60)
                current_diff = target_time - current_min_time
                # print("current_diff: ", current_diff, flush=True)
                diffs.append(current_diff)
            diffs = [i for i in diffs if i > 0]

            if len(diffs) != len(sensor_names):
                return []
        else:
            return []

        # Order by name
        sensor_names.sort()

        main_sensor_index = sensor_names.index(sensor)
        values = []
        times = []
        

        for sensor_name in sensor_names:
            if not ignore_miss:
                temp_v, temp_t = sensors[sensor_name].get_values()
                values.append(temp_v)
                times.append(temp_t)
            else:
                temp_v, temp_t = sensors[sensor_name].get_raw_values()
                values.append(temp_v)
                times.append(temp_t)
        
        # Switch sensor[0] to the main sensor
        tmp = np.copy(values[0])
        values[0] = values[main_sensor_index]
        values[main_sensor_index] = tmp

        tmp = np.copy(times[0])
        times[0] = times[main_sensor_index]
        times[main_sensor_index] = tmp

        # Convert to numpy array
        for i in range(len(values)):
            values[i] = np.asarray(values[i])
            times[i] = np.asarray(times[i])

        values = np.asarray(values)
        times = np.asarray(times)

        sizes = [len(i) for i in values]
        
        input_values, input_times = functions.generate1(target_time, sizes, times, values, skip_period, run_periods_self, run_periods_others)

        predictions = []

        if input_values is not None:
            inputs = input_values
            inputs_self = inputs[:run_periods_self]
            inputs_others = inputs[run_periods_self:]
            models = []
            to_input = []

            ann_type = []
            if None in inputs: #a missing value is detected
                if None not in inputs_self: #only enters if there is no omission
                    self_model = self.get_model(sensor, sensors[sensor].type, 'self')
                    if self_model is not None:
                        models.append(self_model)
                        to_input.append(inputs_self)
                        ann_type = ['self']
                elif None not in inputs_others: #only enters if there is no omission
                    others_model = self.get_model(sensor, sensors[sensor].type, 'neighbours')
                    if others_model is not None:
                        models.append(others_model)
                        to_input.append(inputs_others)
                        ann_type = ['neighbours']
            else:
                all_model = self.get_model(sensor, sensors[sensor].type, 'all')
                self_model = self.get_model(sensor, sensors[sensor].type, 'self')
                others_model = self.get_model(sensor, sensors[sensor].type, 'neighbours')

                if all_model is not None:
                    to_input.append(inputs)
                    models.append(all_model)
                    ann_type.append('all')
                if self_model is not None:
                    to_input.append(inputs_self)
                    models.append(self_model)
                    ann_type.append('self')
                if others_model is not None:
                    to_input.append(inputs_others)
                    models.append(others_model)
                    ann_type.append('neighbours')
            if len(models) > 0:
                for i in range(len(models)):
                    path = models[i]['path']
                    model = models[i]['model']
                    model.compile(optimizer = 'adam', loss = "mean_squared_error", metrics = [])
                    inpt = to_input[i]
                    p = model.predict((inpt,))[0][0]
                    predictions.append((path, ann_type[i], p, target_time))

                del models
                tf.keras.backend.clear_session()

        if len(predictions) > 0:
            print(f"{len(predictions)} predictions calculated for {sensor} at {target_time}")
        return predictions

    @staticmethod
    def startup_models():
        """
        Gets models using keras.
        """
        models = {}

        models_folder = f'./ann/models/'
        folders_found = os.listdir(models_folder)

        if folders_found == 0:
            print("No ann models found, exiting...")
            exit(-1)

        sensor_names = [i.split('_')[0] for i in folders_found]
        folders_found = [models_folder + i for i in folders_found]

        for i in range(len(folders_found)):
            folder = folders_found[i]
            loss_file = f'{folders_found[i]}/loss.json'
            with open(loss_file) as file:
                current_loss = json.load(file)['loss']
            sensor_name = sensor_names[i]
            typeM = folder.split('_')[1]
            sizeM = folder.split('_')[2]

            model = keras.models.load_model(folder +"/saved_model.h5", compile=False)

            if sensor_name not in models:
                models[sensor_name] = []

            models[sensor_name].append({'path': folder,
                                        'typeM': typeM,
                                        'sizeM': sizeM,
                                        'loss': current_loss,
                                        'model': model})

        return models