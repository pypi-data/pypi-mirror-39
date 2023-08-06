import sys
import pandas as pd


class DataCut:
    df = None
    x_axis = None

    __log_file_path = list()
    __x_col = None

    def __init__(self):
        pass

    def dispose(self):
        self.__log_file_path = None
        self.df = None
        self.x_axis = None

    def import_file(self, path, header=0, sep=","):
        try:
            self.df = pd.read_csv(path, header=header, sep=sep)
        except:
            print(path, "is cannot imported:", sys.exc_info()[0])
            return False
        if len(self.df.index) == 0:
            print(path, "is empty.")
            return False
        return True

    def set_x_axis(self, x_col):
        self.x_axis = self.df.loc[:, x_col] if x_col in self.df.columns else self.df.iloc[:, x_col]
        self.__x_col = x_col

    def shift(self, trig_col, trig_val):
        trig_df = self.df.loc[:,
                              trig_col] if trig_col in self.df.columns else self.df.iloc[:, trig_col]
        idx = [0, None]
        while trig_val[0] < float(trig_df[idx[0]+1]) < trig_val[1]:
            idx[0] += 1
        shift_start_time = self.x_axis[idx[0]]
        shift_df = self.df.iloc[idx[0]:idx[1], :].reset_index(drop=True)
        if self.__x_col in shift_df:
            shift_df.loc[:, self.__x_col] -= shift_start_time
        else:
            shift_df.iloc[:, self.__x_col] -= shift_start_time
        self.df = shift_df
        self.set_x_axis(self.__x_col)

    def slice(self, time):
        idx = [0, None]
        while float(self.x_axis[idx[0]]) < float(time[0]):
            idx[0] += 1
        idx[1] = idx[0]
        while float(self.x_axis[idx[1]]) <= float(time[1]):
            idx[1] += 1
        slice_df = self.df.iloc[idx[0]:idx[1], :]
        self.df = slice_df.reset_index(drop=True)
        self.set_x_axis(self.__x_col)
