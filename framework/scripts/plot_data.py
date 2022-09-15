from datetime import datetime, timedelta

from matplotlib import pyplot as plt
import functions

# times, values = load_raw("data\\raw_main\\21jul_2009-18oct_2009\\temp\\dsdma_temp_21jul_18oct2009.mat")
# times, values = functions.load_raw("data\\dsdma_missing\\dsdma_out_file.csv")
# counter, values = functions.loadtime_diff("diff_ms_training.csv")
# times, values = functions.load_raw("data\\lnec\\lnec_out_file.csv")
times_p1, values_p1 = functions.load_raw("data\\lnec\\lnec_out_file_predictions_exp.csv")
times_p2, values_p2 = functions.load_raw("data\\lnec\\lnec_out_file_predictions_linear.csv")
times_p3, values_p3 = functions.load_raw("data\\lnec\\lnec_out_file_predictions_last.csv")
# times_r, values_r = functions.load_raw_saturn("data\\raw_other\\lnec\\temp\\lnec_data_set01_set08.csv")
# times_o, values_o = functions.load_raw("data\\lnec\\lnec_outliers_file.csv")
# times, values = load_raw("data\processed\\21jul_2009-18oct_2009\\temp\dsdma.npz")


# times = [datetime.fromordinal(int(i)) + timedelta(days=i % 1) - timedelta(days=366) for i in times]
# print(times)

# times = [datetime.fromtimestamp(float(i)) for i in times]
times_p1 = [datetime.fromtimestamp(float(i)) for i in times_p1]
times_p2 = [datetime.fromtimestamp(float(i)) for i in times_p2]
times_p3 = [datetime.fromtimestamp(float(i)) for i in times_p3]
# times_r = [datetime.fromtimestamp(float(i)) for i in times_r]
# times_r = [i for i in times_r]
# times_o = [datetime.fromtimestamp(float(i)) for i in times_o]
# print(values)

# start = datetime.strptime("2013-10-01 00:00", "%Y-%m-%d %H:%M")
# end = datetime.strptime("2013-12-31 00:00", "%Y-%m-%d %H:%M")

sensor_name = "LNEC Temperature Sensor"
# values_x = times
# values_y = values
# print(values_y)
values_x_p1 = times_p1
values_y_p1 = values_p1
values_x_p2 = times_p2
values_y_p2 = values_p2
values_x_p3 = times_p3
values_y_p3 = values_p3
# values_x_r = times_r
# values_y_r = values_r
# values_x_o = times_o
# values_y_o = values_o

# xticks = [start, values_x[int(len(values_x) / 2)], end]
yticks = [0, 15, 20, 25, 30, 35, 40]
f = plt.figure(figsize=(12.0, 3.7))
plt.ylabel('Temperature', fontsize=16)
plt.title(sensor_name, fontsize=20)
# plt.plot(values_x, values_y, color='royalblue', label='Corrected Values', linewidth=1.1)
plt.plot(values_x_p1, values_y_p1, color='black', label='Exponential Predictions', linewidth=1.1)
plt.plot(values_x_p2, values_y_p2, color='royalblue', label='Linear Predictions', linewidth=1.1)
plt.plot(values_x_p3, values_y_p3, color='red', label='Last Ten Predictions', linewidth=1.1)
# plt.plot(values_x_r, values_y_r, '.r', color='black', label='Raw Values', linewidth=1.1)
# plt.plot(values_x_o, values_y_o, 'r.', color='red', label='Outliers', linewidth=1.1)
# plt.xticks(xticks, fontsize=14)
plt.yticks(yticks, fontsize=14)
plt.ylim(0, 45)
plt.legend(loc='best')
#plt.xlim(start, end)
plt.tight_layout()
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
f.savefig("lnec_approaches.pdf", bbox_inches='tight')
plt.show()
