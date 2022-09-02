import sys
import os
import functions


def main():
    """
    Starts creating empty neural networks for training acoording to the configuration file.
    """
    if len(sys.argv) == 1:

        print("Please input data configuration file.")

    elif len(sys.argv) == 2:

        data_cfg_file = sys.argv[1]

        if os.path.isfile(data_cfg_file):
            data_cfg = functions.load_cfg(data_cfg_file)
            if functions.validate_data_cfg(data_cfg):
                print("Configuration loaded, training sets are now being built using:", data_cfg["training_sets"]["raw_path"])
                functions.build(data_cfg)
                print("OK")
            else:
                print("Invalid configuration file in training_sets section.")
        else:
            print("File or directory not found in training_sets section.")


if __name__ == "__main__":
    main()
