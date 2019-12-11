import pandas as pd
import numpy as np
# import tensorflow as tf
# import keras
# from keras.backend import symbolic
import math
from sklearn import preprocessing
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class Initialization:
    def __init__(self, database):
        self.database = database

    def import_data(self, col_names):
        db = pd.read_csv(self.database)
        db.columns = col_names
        symbolic_data = [
            'protocol_type', 'service', 'flag',
            'land', 'logged_in', 'is_host_login', 'is_guest_login'
        ]
        continuous_data = [
            "duration", "src_bytes",
            "dst_bytes", "wrong_fragment", "urgent", "hot", "num_failed_logins", "num_compromised", "root_shell",
            "su_attempted", "num_root",
            "num_file_creations", "num_shells", "num_access_files", "num_outbound_cmds", "count", "srv_count",
            "serror_rate",
            "srv_serror_rate", "rerror_rate", "srv_rerror_rate", "same_srv_rate",
            "diff_srv_rate", "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
            "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
            "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate",
            "dst_host_rerror_rate", "dst_host_srv_rerror_rate"
        ]
        db = self.insert_data(symbolic_data, db)  # Create Dummy Variables
        db = db.iloc[:, :-1]  # Select all data values to db
        dl = db.iloc[:, -1:]  # Select all data labels to dl
        dl = pd.get_dummies(dl)  # Convert data labels to dummy variables
        db = self.scale_data(db)  # Scale all the data in the database
        print(db[:, :5])
        np.savetxt('out.csv', db, encoding='utf-8', delimiter=",")
        np.savetxt('labels.csv', dl, encoding='utf-8', delimiter=",")

    def insert_data(self, needed_replaced_data, full_data):
        for replaced_data in needed_replaced_data:
            dummy_variables = pd.get_dummies(full_data[replaced_data])
            data_location = full_data.columns.get_loc(replaced_data)
            full_data_front = full_data.iloc[:, :data_location]
            full_data_back = full_data.iloc[:, data_location + 1:]
            full_data_front = pd.concat([full_data_front, dummy_variables], axis=1)
            full_data = full_data_front.join(full_data_back)
        return full_data

    def scale_data(self, df):
        data_scaler = preprocessing.MinMaxScaler()
        df = data_scaler.fit_transform(df)
        return df


kdd_col_names = ["duration", "protocol_type", "service", "flag", "src_bytes",
                 "dst_bytes", "land", "wrong_fragment", "urgent", "hot", "num_failed_logins",
                 "logged_in", "num_compromised", "root_shell", "su_attempted", "num_root",
                 "num_file_creations", "num_shells", "num_access_files", "num_outbound_cmds",
                 "is_host_login", "is_guest_login", "count", "srv_count", "serror_rate",
                 "srv_serror_rate", "rerror_rate", "srv_rerror_rate", "same_srv_rate",
                 "diff_srv_rate", "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count",
                 "dst_host_same_srv_rate", "dst_host_diff_srv_rate", "dst_host_same_src_port_rate",
                 "dst_host_srv_diff_host_rate", "dst_host_serror_rate", "dst_host_srv_serror_rate",
                 "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "label"]


# main code #
file = open("kddcup.data.corrected")
kddcup = Initialization(file)
kddcup.import_data(kdd_col_names)
kdd_labels = pd.read_csv(open("labels.csv"))
kdd_data = pd.read_csv(open("out.csv"))
