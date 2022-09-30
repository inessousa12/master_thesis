Diretoria da framework está dividida em 3 pastas: ann, data e scripts.

ann:
Dividido em duas diretorias: models e training.
    -> models - diretoria onde são guardados os modelos treinados
    -> training - diretoria onde são guardados todos os checkpoints por run de cada tipo de modelo

data:
Diretoria onde os datasets se encontram. As diretorias em ter em consideração são a raw_main, raw_other e processed.
    -> raw_main - Diretoria onde os datasets a serem usados para treinar os modelos se encontram.
                  Ex de estrutura: data/raw_main/<dataset_name>/<metric>/<dataset_files>
    -> raw_other - Diretoria onde os datasets a serem usados como teste (durante a execução da framework) se
                   encontram
    -> processed - Diretoria onde os datasets processados se encontram. Estes datasets são utilizados para a
                   criação das CDFs.

scripts:
Diretoria onde todos os scripts relativos à framework podem ser encontrados.
Os datasets têm de estar organizados com a seguinte estrutura: dd/mm/yyyy HH:MM; <valor>

    -> ann_trainingsets.py - This script is responsible for the processing of data before training. 
                            To execute this script, we need to run the following command: 
                            python ./scripts/ann_trainingsets.py ./scripts/configuration_training.json
    
                            Once executed, the script will start data processing

    -> ann.py - This is where we train neural networks after processing data for training. 
                The script is expecting the same JSON file as the ann_trainingsets.py script. Run command: 
                python ./scripts/ann.py ./scripts/configuration_training.py

    -> app_server.py - This is the main script that starts the framework. It expects the JSON file configuration_processing.json. Run command:
                       python ./scripts/app_server.py ./scripts/configuration_processing.json

    -> app_simulator.py - This script simulates a client that is sending measurements to the framework. Run command:
                          python ./scripts/app_simulator.py ./scripts/configuration_processing.json 0.1
    
                          The last argument passed on the command is the frequency at which the client will send measurements
                          to the framework, in this case, every 0.1 seconds the client sends data to the server

    -> configuration_processing.json - Configuration file for processing

    -> configuration_training.json - Configuration file for training

    -> db_setup.py - This script contains all interactions with the database needed by the framework. 
                     It inserts stations and measurements into the database. If the database suffers alterations, 
                     the user only needs to change this module

    -> entry_vectors.py - Script where entry vectors are created

    -> functions.py - This script contains important functions needed throughout the framework's execution

    -> PredictionBlock.py - This script contains the PredictionBlock class which is responsible for calculating forecasts

    -> QualityBlock.py - This script contains the QualityBlock class which is responsible for calculating a measurement's quality and failure detection

    -> SensorData.py - Contains the SensorData class which stores every measurement received in a Python dictionary

    -> SensorHandler.py - Contains the SensorHandler class which handles all sensor's variables

    -> Server.py - Script that contains the Server class which is used for server-client communication

    -> sock_utils.py - Script containing functions that help with server-client communications


configuration_training.json:
Secção training_sets:
    -> raw_path - directory path where raw data is located
    -> save_path - directory path where processed data will be saved
    -> metrics - list of metrics that will be trained. These metrics need to be the same as the sub-directories of raw_path
    -> n_sensors - number of sensors available for training
    -> run_periods_self - number of measurements from the target sensor considered for entry vector creation within a full tide
    -> run_periods_others - number of measurements from neighbour sensors considered for entry vector creation within a full tide
    -> period_time - period of time in seconds between each measurement
    -> skip_period - minimum tax of sampling

Secção training:
    -> data_train - Percentage of data that will be dedicated to training the model
    -> data_test - Percentage of data that will be dedicated to testing the trained model
    -> epochs - Number of times a network passes backwards and forwards
    -> hidden_layer_1 and hidden_layer_2 - In this case, our neural network is going to have two hidden layers, 
        the first one with 20 neurons and the second one with 15 neurons
    -> output_layer - As this is a neural network that will give as an output one value, we only need one neuron in the last neural network layer
    -> loss_function - Name of the loss function desired to use
    -> sensor - Sensor's name
    -> metric - Metric that corresponds to the dataset's measurements
    -> inputs - Has three different options: all, neighbours and self. Corresponds to the type of model that will be trained
    -> n_other_sensors - Number of sensors without counting the target sensor
    -> input_shape - Total number of measurements considered for training for each sensor
    -> input_target - Total number of measurements considered for training from the target sensor
    -> input_others - Total number of measurements considered for training from the rest of the sensors
    -> runs - Number of neural networks that will be trained


configuration_processing.json:
cdf_threashold is the significance value that will be used to determine if a measurement is an anomaly or not, 
with the help of the CDF function calculated during training. 
approach receives the type of approach the user wants to use. It has three options: 
1 - exponential approach, 2 - linear approach and 3 - last ten approach