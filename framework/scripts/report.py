import json
import os
import statistics
import sys
from os import listdir
from os.path import isfile, join, isdir
import copy
import matplotlib.pyplot as plt
import numpy as np
from functions import load_raw_saturn
# from .functions import load_raw_saturn

import functions
from SensorHandler import SensorHandler
from PredictionBlock import PredictionBlock
from functions import generate1
from functions import load_processed, load_raw
from datetime import datetime, timedelta

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


def start_report(report_data, threshold):
    times, values, snames = report_data[0], report_data[1], report_data[2]
    corrected_values = copy.deepcopy(values)
    sizes = [len(i) for i in times]
    count = {}
    for n in snames:
        count[n] = 0
    quality = {}
    predictions = {}

    start = datetime.strptime("2021-08-18 00:00", "%Y-%m-%d %H:%M").timestamp()
    end = datetime.strptime("2021-10-18 23:45", "%Y-%m-%d %H:%M").timestamp()

    os.makedirs(f"./framework/report/{int(threshold * 10000)}/", exist_ok=True)
    files = listdir(f"./framework/report/{int(threshold * 10000)}/")

    models = PredictionBlock.startup_models()
    new_times = []

    for i in range(len(snames)):
        print(snames[i])
        quality[snames[i]] = {}
        predictions[snames[i]] = {}
        sensor_name = snames[i]
        current_models = models[sensor_name]

        predictions_file = f"./framework/report/{snames[i]}_predictions.npy"
        if isfile(predictions_file):
            predictions = np.load(predictions_file, allow_pickle=True).item()

            for key in predictions[sensor_name].keys():
                # 3 predictions example [dsdma][index] = {p,model_path},{p,model_path},{p,model_path}
                index = key
                print(f'{snames[i]}: [{index}]')
                count[sensor_name] += 1
                prediction = predictions[sensor_name][key]
                qs = []
                ps = []
                for p in prediction:
                    model_path = p['model_path']
                    p = p['p']
                    ps.append(p)
                    q_error = pow(values[snames.index(sensor_name)][index] - p, 2)
                    cdf = load_cdf(model_path)
                    q = cdf_eval(cdf, q_error, threshold)
                    qs.append(q)

                current_quality = qs
                if max(current_quality) == 0:
                    quality[sensor_name][index] = 0
                    new_value = statistics.mean(ps)
                    corrected_values[snames.index(sensor_name)][index] = new_value
                else:
                    quality[sensor_name][index] = 1 - statistics.mean(current_quality)

        else:
            copy_times = copy.copy(times)
            copy_values = copy.copy(corrected_values)
            copy_sizes = copy.copy(sizes)
            copy_names = copy.copy(snames)
            
            for j in range(len(copy_values)):
                copy_values[j] = np.asarray(copy_values[j])
                copy_times[j] = np.asarray(copy_times[j])
                copy_sizes[j] = np.asarray(copy_sizes[j])
                copy_names[j] = np.asarray(copy_names[j])
            
            if i > 0:
                # Switch first sensor to the sensor we want to target
                tmp = copy.copy(copy_values[0])
                copy_values[0] = copy_values[i]
                copy_values[i] = tmp

                tmp = copy.copy(copy_times[0])
                copy_times[0] = copy_times[i]
                copy_times[i] = tmp

                tmp = copy.copy(copy_sizes[0])
                copy_sizes[0] = copy_sizes[i]
                copy_sizes[i] = tmp

                tmp = copy.copy(copy_names[0])
                copy_names[0] = copy_names[i]
                copy_names[i] = tmp

            new_times.append(functions.build_new_times(copy_times, copy_sizes, 0))

            for nt in new_times[i]:
                if nt[0][0] < start:
                    continue
                if nt[0][0] > end:
                    break
                if sensor_name not in count:
                    count[sensor_name] = 1
                else:
                    count[sensor_name] += 1

                index = nt[0][2]
                print(f'{snames[i]}: [{index}]')
                real = copy_values[0][index]
                input, input_times = generate1(nt[0][0], copy_sizes, copy_times, copy_values, 0, 10, 0,
                                               new_times[i])
                
                qs = []
                ps = []
                for m in current_models:
                    model = m['model']
                    model.compile(optimizer='adam', loss="mean_squared_error", metrics=[], )
                    if m['sizeM'] == 'all':
                        prediction = model.predict((input,))[0][0]
                    elif m['sizeM'] == 'self':
                        input_self = input[:10]
                        prediction = model.predict((input_self,))[0][0]
                    else:
                        input_others = input[10:]
                        prediction = model.predict((input_others,))[0][0]
                    ps.append({'p':prediction, 'model_path':m['path']})

                    cdf = load_cdf(m['path'])
                    q_error = pow(real - prediction, 2)
                    q = cdf_eval(cdf, q_error, threshold)
                    qs.append(q)

                current_quality = qs

                predictions[sensor_name][index] = ps
                if max(current_quality) == 0:
                    quality[sensor_name][index] = 0

                    new_value = statistics.mean([p['p'] for p in ps])

                    corrected_values[snames.index(sensor_name)][index] = new_value
                    copy_values[copy_names.index(sensor_name)][index] = new_value
                else:
                    quality[sensor_name][index] = 1 - statistics.mean(current_quality)

            np.save(predictions_file, predictions)

        np.save(f"./framework/report/{int(threshold * 10000)}/{snames[i]}_faults{int(threshold * 10000)}.npy",
                quality[snames[i]])

    for i in range(len(snames)):
        values_y, values_x = values[i], times[i]
        corrected_values_y = corrected_values[i]
        values_x = [datetime.utcfromtimestamp(i).strftime('%Y-%m-%d %H:%M') for i in values_x]

        # start = datetime.utcfromtimestamp(i).strptime("2013-10-03 00:00", "%Y-%m-%d %H:%M")
        # end = datetime.utcfromtimestamp(i).strptime("2013-12-22 00:00", "%Y-%m-%d %H:%M")

        sensor_name = snames[i]
        q = quality[sensor_name]

        # OUTLIERS -------------------------------------------------------------------

        qualities_index = q.keys()
        outliers_y = [values_y[i] for i in qualities_index if q[i] == 0]
        outliers_x = [values_x[i] for i in qualities_index if q[i] == 0]

        for e in range(len(outliers_y)):
            current = outliers_y[e]
            if current < 0:
                outliers_y[e] = 0
            elif current > 20:
                outliers_y[e] = 20

        # xticks = [start, values_x[int(len(values_x) / 2)], end]
        yticks = [0, 5, 10, 15, 20, 25, 30, 35]
        plt.figure(figsize=(12.0, 3.2))
        plt.ylabel('Temperature (ºC)', fontsize=16)
        plt.title(sensor_name, fontsize=20)
        plt.plot(values_x, values_y, color='royalblue', linewidth=1.1, zorder=0, label="Measurements")
        plt.plot(outliers_x, outliers_y, 'r.', color='red', label='Outliers', zorder=10)
        # plt.xticks(xticks, fontsize=14)
        plt.yticks(yticks, fontsize=14)
        # plt.xticks(xticks)
        plt.ylim(0, 40)
        # plt.xlim("2021-08-18", "2021-10-18")
        plt.legend(loc='best')
        plt.tight_layout()
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.savefig(f'./framework/report/{int(threshold * 10000)}/{snames[i]}.png',
                    bbox_inches='tight', dpi=150, block=False)
        plt.clf()

        # PREDICTIONS ---------------------------------------------------------------

        # xticks = [start, values_x[int(len(values_x) / 2)], end]
        yticks = [0, 5, 10, 15, 20, 25, 30, 35]
        plt.figure(figsize=(12.0, 3.2))
        plt.ylabel('Temperature (ºC)', fontsize=16)
        plt.title(sensor_name, fontsize=20)
        plt.plot(values_x, values_y, color='royalblue', linewidth=1, label="Measurements")
        plt.plot(values_x, corrected_values_y, color='black', linewidth=1.1, label="Corrected Measurements")
        plt.plot(outliers_x, outliers_y, 'r.', color='red', label='Outliers')
        # plt.xticks(xticks, fontsize=14)
        plt.yticks(yticks, fontsize=14)
        # plt.xticks(xticks)
        plt.ylim(0, 40)
        # plt.xlim(start, end)
        # plt.xlim("2021-08-18", "2021-10-18")
        plt.legend(loc='best')
        plt.tight_layout()
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.savefig(f'./framework/report/{int(threshold * 10000)}/{snames[i]}_corrected.png',
                    bbox_inches='tight', dpi=150, block=False)
        plt.clf()

        # QUALITY -------------------------------------------------------------------

        qualities_index = q.keys()
        qualities_y = [q[i] for i in qualities_index]
        qualities_x = [values_x[i] for i in qualities_index]

        outliers2_y = [q[i] for i in qualities_index if q[i] == 0]
        outliers2_x = [values_x[i] for i in qualities_index if q[i] == 0]

        yticks = [0, 0.2, 0.4, 0.6, 0.8, 1]
        plt.figure(figsize=(12.0, 3.2))
        plt.ylabel('Quality Coefficient', fontsize=16)
        plt.title(sensor_name, fontsize=20)
        plt.plot(qualities_x, qualities_y, color='royalblue', linewidth=1, label="Measurements")
        plt.plot(outliers2_x, outliers2_y, 'r.', color='red', label="Outliers")
        # plt.xticks(xticks, fontsize=14)
        plt.yticks(yticks, fontsize=14)
        plt.ylim(0, 1)
        # plt.xlim("2013-10-03", "2013-10-17")
        # plt.legend(loc='best')
        plt.tight_layout()
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.savefig(f'./framework/report/{int(threshold * 10000)}/{snames[i]}_quality.png',
                    bbox_inches='tight', dpi=150, block=False)
        plt.clf()

    report = {'Detected': {}, 'RD': {}, 'RFP': {}}
    for i in range(len(snames)):
        current_name = snames[i]

        q = quality[current_name]
        qualities_index = q.keys()
        current_detected = len([k for k in qualities_index if q[k] == 0])

        report['Detected'][current_name] = current_detected

        if current_name == 'dsdma':
            if current_detected < 44:
                report['RD'][current_name] = f'{(current_detected / 44) * 100:.5f}%'
                report['RFP'][current_name] = '0.00%'
            else:
                report['RD'][current_name] = '100.00%'
                report['RFP'][current_name] = f'{((current_detected - 44) / (count[current_name] - 44)) * 100:.5f}%'
        elif current_name == 'jettya':
            if current_detected == 0:
                report['RD'][current_name] = '100.00%'
                report['RFP'][current_name] = '0.00%'
            else:
                report['RD'][current_name] = '100.00%'
                report['RFP'][current_name] = f'{(current_detected / count[current_name]) * 100:.5f}%'
        elif current_name == 'sandi':
            if current_detected < 1:
                report['RD'][current_name] = '0.00%'
                report['RFP'][current_name] = '0.00%'
            else:
                report['RD'][current_name] = '100.00%'
                report['RFP'][current_name] = f'{((current_detected - 1) / (count[current_name] - 1)) * 100:.5f}%'
        elif current_name == 'tansy':
            if current_detected < 11:
                report['RD'][current_name] = f'{(current_detected / 11) * 100:.5f}%'
            else:
                report['RD'][current_name] = '100.00%'
                report['RFP'][current_name] = f'{((current_detected - 11) / (count[current_name] - 11)) * 100:.5f}%'
        elif current_name == 'lnec':
            if current_detected < 5:
                report['RD'][current_name] = f'{(current_detected / 3) * 100:.5f}%'
            else:
                report['RD'][current_name] = '100.00%'
                report['RFP'][current_name] = f'{((current_detected - 3) / (count[current_name] - 3)) * 100:.5f}%'

    with open(f'./framework/report/{int(threshold * 10000)}/report{int(threshold * 10000)}.json', 'w') as file:
        file.write(json.dumps(report, indent=4, sort_keys=True))
    exit('DONE')


def validate(path):
    times, values, snames = None, None, None
    if isdir(path):
        files_names = [f for f in listdir(path) if isfile(join(path, f))]
        files_names.sort()
        if len(files_names) == 0:
            return times, values, snames
        for file_name in files_names:
            if not len(file_name) > 4:
                return times, values, snames
            str_end = file_name[-4:]
            if not str_end == ".mat" and not str_end == ".npz" and not ".csv" and not "json":
                return times, values, snames

        times, values, snames = build_data(path)

    return times, values, snames


def build_data(path):
    if "/" in path and path[-1] != "/":
        path += "/"
    elif path[-1] != "\\":
        path += "\\"

    files_names = [f for f in listdir(path) if isfile(join(path, f))]

    times = []
    values = []
    sensor_names = []
    for file_name in files_names:
        file_path = path + file_name
        sensor_name = file_name.split('_')[0]

        if ".mat" in file_name or ".csv" in file_name or ".json" in file_name:
            data_times, data_values = load_raw_saturn(file_path)
        else:
            result = load_processed([file_path])
            data_times, data_values = result[0], result[1]

        times.append(data_times)
        values.append(data_values)
        sensor_names.append(sensor_name)

    return times, values, sensor_names


def cdf_eval(cdf, x, threshold):
    x_index = np.searchsorted(cdf['x'], x, side="left")

    if x_index == len(cdf['y']):
        v = 1
    else:
        v = cdf['y'][x_index]

    if v >= threshold:
        return 0
    else:
        return v


def load_cdf(path):
    return load_processed([path + "\\cdf.npz"])


def datetime2matlabdn(dt):
    mdn = dt + timedelta(days=366)
    frac_seconds = (dt - datetime(dt.year, dt.month, dt.day, 0, 0, 0)).seconds / (24.0 * 60.0 * 60.0)
    frac_microseconds = dt.microsecond / (24.0 * 60.0 * 60.0 * 1000000.0)
    return mdn.toordinal() + frac_seconds + frac_microseconds


if __name__ == "__main__":
    times, values, sensor_names = validate(sys.argv[1])

    start = datetime2matlabdn(datetime.strptime("2021-08-18 00:00", "%Y-%m-%d %H:%M"))
    end = datetime2matlabdn(datetime.strptime("2021-10-18 23:45", "%Y-%m-%d %H:%M"))

    for i in range(len(times)):
        count = 0
        for t in times[i]:
            if t > start:
                count += 1
            if t > end:
                break

        print(f'{sensor_names[i]}: {count}')

    threshold = eval(sys.argv[2])
    if type(threshold) is float:
        start_report([times, values, sensor_names], threshold)
    else:
        print("Bad Threshold value")
