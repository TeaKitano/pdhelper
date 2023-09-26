import pandas as pd
from multiprocessing import Pool

def _file_read(filename, conf, header, index):
    if header:
        header = 0
    else:
        header = None
    if index:
        index = 0
    else:
        index = None
    extention = filename.split(".")[-1].lower()
    if extention == "csv":
        if conf == "":
            return pd.read_csv(filename, header=header, index_col=index)
        else:
            return pd.read_csv(filename, encoding=conf, header=header, index_col=index)
    elif extention == "xlsx" or extention == "xls":
        if conf == "":
            return pd.read_excel(filename, header=header, index_col=index)
        else:
            return pd.read_excel(filename, sheet_name=conf, header=header, index_col=index)
    else:
        raise ValueError("FileExtentionError")

def parallel_read(files, conf, header, index):
    args = list(zip(files, conf, header, index))
    with Pool(3) as pool:
        df_list = pool.starmap(_file_read, args)
    return df_list