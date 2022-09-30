Diretoria onde se encontra a API. Para adicionar uma nova route é no ficheiro app.py que se adiciona.

/api/<sensor_name>/<variable>/<begin_date>/<period>/<method>

    -> <sensor_name> is the name of the sensor
    -> <variable> is the type of metric
    -> <begin_date> is the date the user wishes to start in dd/mm/yyyy format
    -> <period> is the number of days after <begin\_date> 
    -> <method> is the method that will define which type of data is going to be fetched

For <method>:
    -> /raw_measurements - only returns raw measurements
    -> /corrected_measurements - only returns measurements that are correct. 
        This includes measurements that were defined as anomalies and were replaced by their forecasts
    -> /quality - returns the quality average
    -> /outliers - returns all measurements that were considered to be outliers
    -> /omissions - returns all measurements that were considered to be omissions
    -> /anomalies - returns all anomalies (outliers and omissions)