import pandas as pd
from concurrent.futures import ProcessPoolExecutor


def _file_read(file: dict) -> pd.DataFrame:
    # ファイル読み込みのための内部関数
    filename = file["filename"]
    conf = file["conf"]
    header = file["header"]
    index = file["index"]
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
            return pd.read_csv(filename, encoding=conf, header=header,
                               index_col=index)
    elif extention == "xlsx" or extention == "xls":
        if conf == "":
            return pd.read_excel(filename, header=header, index_col=index)
        else:
            return pd.read_excel(filename, sheet_name=conf,
                                 header=header, index_col=index)
    else:
        # 拡張子がcsv,xlsx,xls以外だったらこのエラー
        raise ValueError("FileExtentionError")


def parallel_read(files: dict):
    """
    並列処理でファイルを読み込む関数\n
    input:\n
        files  読み込むファイルのdict\n
            key:出力のdictのkeyにしたい名前
            value:各種設定のdict
                filename:ファイルへのパス
                conf:追加設定 csvの場合文字コードを(空欄ならutf-8)、excelファイルの場合
                使うシート名を(空欄なら1枚目のシート)書く\n
                header:ヘッダーついてるかどうか　ついてたらTrue ついてなかったらFalse\n
                index:インデックスついてるかどうか　ついてたらTrue ついてなかったらFalse\n
    outout:\n
        読み込んだDataFrameの辞書
        key:inputのkey
        value:読み込んだDataFrame
    """
    df_dict = dict()
    with ProcessPoolExecutor() as executor:
        for i in files:
            df_dict[i] = executor.submit(_file_read, files[i])
    for i in df_dict:
        df_dict[i] = df_dict[i].result()
    return df_dict
