import pandas as pd
from multiprocessing import Pool


def _file_read(filename: str, conf: str, header: bool, index: bool) -> pd.DataFrame:
    # ファイル読み込みのための内部関数
    if header:
        header = 0
    else:
        header = None
    if index:
        index = 0
    else:
        index = None
    extention = filename.split(".")[-1].lower()  # 拡張子入手
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
        # 拡張子がcsv,xlsx,xls以外だったらこのエラー
        raise ValueError("FileExtentionError")


def parallel_read(files: list[str], conf: list[str], header: list[bool], index: list[bool]):
    """
    並列処理でファイルを読み込む関数\n
    input:\n
        files  ファイル名のリスト\n
        conf   追加設定 csvの場合文字コードを(空欄ならutf-8)、excelファイルの場合使うシート名を(空欄なら1枚目のシート)書く\n
        header ヘッダーついてるかどうか　ついてたらTrue ついてなかったらFalse\n
        index  インデックスついてるかどうか　ついてたらTrue ついてなかったらFalse\n
    outout:\n
        読み込んだDataFrameのリスト
    """
    args = list(zip(files, conf, header, index))
    with Pool() as pool:
        df_list = pool.starmap(_file_read, args)
    return df_list
