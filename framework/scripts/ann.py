import json
import os
import re
import sys
from timeit import default_timer

import distfit
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from numpy.random import randint
from tensorflow import keras

import functions, time


def main():
    # No args -> Error

    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
    os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"  # see issue #152
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    
    if len(sys.argv) == 1:
        print("Please input data configuration file.")

    # 1 Args -> Create model & train it
    elif len(sys.argv) == 2:
        try:
            ann_cfg = get_cfg(sys.argv[1])
        except Exception as inst:
            print(inst)
            sys.exit(1)

        data_path = ann_cfg["data_path"]

        if os.path.isfile(data_path[0]):
            try:
                data = functions.load_processed(data_path)
            except IOError or ValueError:
                print("Error loading file.")
                sys.exit(1)
        else:
            print("Error invalid path.")
            sys.exit(1)

        inputs = data[0]
        if ann_cfg["inputs"] == "self":
            inputs = [values[:ann_cfg["input_target"]] for values in inputs]
        elif ann_cfg["inputs"] == "neighbours":
            inputs = [values[ann_cfg["input_target"]:] for values in inputs]
        elif ann_cfg["inputs"] == "all":
            end = int(ann_cfg["input_target"]) + int(ann_cfg["input_others"]) * int(ann_cfg["n_other_sensors"])
            inputs = [values[:end] for values in inputs]
        
        targets = data[1]

        random_ints1 = randint(0, 9999999, 10)
        random_ints2 = randint(0, 9999999, 10)

        for i in range(ann_cfg["runs"]):
            weights_seed = random_ints1[i]
            bias_seed = random_ints2[i]

            model = create_model(ann_cfg, weights_seed, bias_seed)
            train_model(model, [inputs, targets], ann_cfg)

        save_models(ann_cfg)


def get_cfg(ann_cfg_path):
    if os.path.isfile(ann_cfg_path):
        ann_cfg = functions.load_cfg(ann_cfg_path)
        ann_cfg = ann_cfg["training"]
        if functions.validate_ann_cfg(ann_cfg):
            return ann_cfg
        else:
            print("Invalid cfg.")
            raise Exception("Error cfg")
    else:
        print("Invalid cfg path.")
        raise Exception("Error cfg")


def create(ann_cfg, seed1, seed2):
    array_size = ann_cfg["input_shape"]
    my_initializer1 = keras.initializers.TruncatedNormal(seed=seed1)
    my_initializer2 = keras.initializers.TruncatedNormal(seed=seed2)

    model = keras.Sequential()
    model.add(keras.layers.Flatten(input_shape=(array_size,)))
    model.add(keras.layers.Dense(ann_cfg["hidden_layer_1"],
                                 activation="tanh",
                                 kernel_initializer=my_initializer1))
    model.add(keras.layers.Dense(ann_cfg["hidden_layer_2"],
                                 activation="tanh",
                                 kernel_initializer=my_initializer2))
    model.add(keras.layers.Dense(ann_cfg["output_layer"], activation="linear"))

    return model


def create_model(ann_cfg, seed1=0, seed2=0):
    model = create(ann_cfg, seed1, seed2)
    model.compile(optimizer='adam', loss=ann_cfg["loss_function"], metrics=[], )
    return model


def calculate_cdf(model, ann_cfg, i):
    if ann_cfg["cdf_data_path"] is not None:
        if os.path.isfile(ann_cfg["cdf_data_path"]):
            try:
                data = functions.load_processed([ann_cfg["cdf_data_path"]])
            except IOError or ValueError:
                print("Error loading cdf data file.")
                return None
        else:
            print("Error invalid cdf data path.")
            return None

        save_folder = ann_cfg['model_save_path'] + \
                      f"/{ann_cfg['sensor']}_{ann_cfg['metric']}_{ann_cfg['inputs']}_{ann_cfg['id']}_r{i}/stats/"

        inputs = data[0]

        if ann_cfg["inputs"] == "self":
            inputs = [values[:ann_cfg["input_target"]] for values in inputs]
        elif ann_cfg["inputs"] == "neighbours":
            inputs = [values[ann_cfg["input_target"]:] for values in inputs]
        elif ann_cfg["inputs"].isdigit():
            start = int(ann_cfg["input_target"])
            end = int(ann_cfg["input_target"]) + int(ann_cfg["input_others"]) * int(ann_cfg["inputs"])
            inputs = [values[start:end] for values in inputs]

        targets = data[1]

        predictions = [p[0] for p in model.predict(inputs)]
        quadratic_errors = [pow(predictions[i] - targets[i], 2) for i in range(len(predictions))]
        quadratic_errors.sort()

        dist = distfit.distfit(distr='fisk', bins=len(quadratic_errors))
        dist.fit_transform(np.array(quadratic_errors))

        ln = np.linspace(min(quadratic_errors), max(quadratic_errors), len(quadratic_errors))
        pdf = dist.predict(ln)['y_proba']

        param = dist.model

        counts, bin_edges = dist.histdata
        cs = np.cumsum(counts)
        x, y = bin_edges[:], cs / cs[-1]
        cdf = dict(x=x, y=y)

        
        # -----------------------------------HISTOGRAM------------------------------------------
        plt.figure(figsize=(12.0, 3.2))
        plt.ylabel('Density')
        plt.title('Square errors Histogram')
        plt.hist(quadratic_errors, bins=200)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.savefig(save_folder + "hist.pdf", bbox_inches='tight', dpi=150, block=False)
        plt.clf()

        # ------------------------------------PDF FIT-------------------------------------------
        plt.figure(figsize=(12.0, 3.2))
        plt.ylabel('Probability')
        plt.title('Log-Logistic Probability Distribution of the square errors')
        plt.plot(pdf, color='red', label='Log-Logistic Fit', linewidth=1.5)
        plt.legend(loc='best')
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.savefig(save_folder + "pdf.pdf", bbox_inches='tight', dpi=150, block=False)
        plt.clf()

        # ------------------------------------CDF FIT-------------------------------------------
        plt.figure(figsize=(12.0, 3.2))
        plt.ylabel('Cumulative Probability')
        plt.title('Cumulative Density Function of the Probability Distribution of the square errors')
        plt.plot(quadratic_errors, cdf['y'], color='purple', alpha=0.8, label='Square Errors', linewidth=0.9)
        plt.plot(cdf['x'], cdf['y'], color='red', label='Log-Logistic Fit', linewidth=1.5)
        plt.legend(loc='best')
        plt.tight_layout()
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.savefig(save_folder + "cdf.pdf", bbox_inches='tight', dpi=150, block=False)        

        return cdf

    return None


def train_model(model, data, ann_cfg):
    inputs = data[0]
    targets = data[1]

    # TEST
    inputs, targets = unison_shuffled_copies(inputs, targets)

    # 90% of the data used for training 10% used for testing
    train_percentage = ann_cfg["data_train"]
    n_train_total = int(len(inputs) * train_percentage)

    train_inputs = inputs[:n_train_total]
    train_targets = targets[:n_train_total]

    test_inputs = inputs[n_train_total:len(inputs)]
    test_targets = targets[n_train_total:len(targets)]

    epochs = ann_cfg["epochs"]

    run_n = 0
    latest_epoch = 0
    continuing_train = False
    while True:
        checkpoint_path = ann_cfg["checkpoint_path"] + functions.get_model_name(ann_cfg) + "/run_" + str(run_n) + "/"
        try:
            os.makedirs(checkpoint_path)
            functions.save_train_cfg(ann_cfg, checkpoint_path + "train.json")
            break
        except OSError:
            train_cfg = functions.load_cfg(checkpoint_path + "train.json")
            latest_checkpoint = tf.train.latest_checkpoint(checkpoint_path)
            latest_epoch = int(re.findall(r'\b\d+\b', latest_checkpoint)[0])

            if latest_epoch == train_cfg["epochs"]:
                if run_n + 1 >= ann_cfg['runs']:
                    return
                run_n += 1
                latest_epoch = 0
                latest_checkpoint = 0
                continue
            else:
                if train_cfg["data_path"] == ann_cfg["data_path"]:
                    continuing_train = True
                    break
                else:
                    print("Previous training is unfinished or / and user gave different data.")
                    sys.exit(1)

    if continuing_train:
        latest_checkpoint = tf.train.latest_checkpoint(checkpoint_path)
        latest_epoch = int(re.findall(r'\b\d+\b', latest_checkpoint)[0])
        model.load_weights(latest_checkpoint)

    checkpoint_folder = str(checkpoint_path)
    checkpoint_path += "cp-{epoch:04d}.ckpt"

    if not continuing_train:
        model.save_weights(checkpoint_path.format(epoch=0))

    cp_callback = keras.callbacks.ModelCheckpoint(
        filepath=checkpoint_path,
        verbose=1,
        save_weights_only=True,
        period=ann_cfg["checkpoint_epochs"],
    )

    model_path = ann_cfg["model_save_path"] + functions.get_model_name(ann_cfg) + "/"

    t_start = default_timer()

    model.fit(
        train_inputs,
        train_targets,
        epochs=epochs,
        callbacks=[cp_callback],
        initial_epoch=latest_epoch,
        verbose=2
    )

    model.save_weights(checkpoint_path.format(epoch=epochs))

    time_elapsed = (default_timer() - t_start)
    hours, seconds = divmod(time_elapsed, 3600)
    minutes, seconds = divmod(seconds, 60)
    result = "{:02.0f}:{:02.0f}:{:02.0f}".format(hours, minutes, seconds)

    print("Training took:", result)

    results = model.evaluate(test_inputs, test_targets)

    print("Loss on test data:", results)

    functions.save_loss(results, checkpoint_folder + "/loss.json")


def save_models(ann_cfg):
    print("Saving models...")

    checkpoint_path = ann_cfg['checkpoint_path']
    folders_found = [x[0] for x in os.walk(checkpoint_path)]
    folders_found = [x for x in folders_found
                     if ann_cfg['sensor'] in x
                     and ann_cfg['metric'] in x
                     and ann_cfg['inputs'] in x
                     and str(ann_cfg['id']) in x
                     and 'run' in x]

    for i in range(len(folders_found)):
        model_folder = folders_found[i]

        loss_file = f'{folders_found[i]}/loss.json'

        model = create_model(ann_cfg)
        latest_checkpoint = tf.train.latest_checkpoint(model_folder)
        model.load_weights(latest_checkpoint).expect_partial()

        save_folder = ann_cfg['model_save_path'] + \
                      f"/{ann_cfg['sensor']}_{ann_cfg['metric']}_{ann_cfg['inputs']}_{ann_cfg['id']}_r{i}/"
        try:
            os.makedirs(save_folder, exist_ok=False)
            os.makedirs(save_folder + "stats", exist_ok=True)
        except OSError:
            print("Model Already Trained.")
            continue

        print("Calculating cdf...")
        cdf = calculate_cdf(model, ann_cfg, i)

        with open(loss_file) as f:
            loss = json.load(f)['loss']
        print("SAVE FOLDER", save_folder)
        functions.save_data(cdf, save_folder + "/cdf.npz")
        functions.save_loss(loss, save_folder + "/loss.json")
        model.save(save_folder + "saved_model.h5")

    print("Models Saved...")


def unison_shuffled_copies(inputs, targets):
    assert len(inputs) == len(targets)
    p = np.random.permutation(len(inputs))
    return [inputs[i] for i in p], [targets[i] for i in p]


if __name__ == "__main__":
    main()
