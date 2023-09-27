import pandas as pd


def left_merge(df: pd.DataFrame, df_sub: pd.DataFrame, left_on: str, right_on: str, target: str | list[str]):
    """
    左側結合専用のmerge関数
    input
        df: 結合元データ
        df_sub: 結合したいデータ
        left_on: dfの結合キー
        right_on: df_subの結合キー
        target: 使いたい列名 複数の場合リストで指定
    """
    # df_subの使う列抽出
    if type(target) == list:
        target.append(right_on)
    else:
        target = [target, right_on]

    sub_len = len(df_sub)
    df_sub = df_sub[~df_sub[right_on].duplicated()]  # 被りを消す
    if sub_len != len(df_sub):
        print("warning:mergeするデータに被りがありました。一番上のデータのみを利用しています。")
    df = pd.merge(df, df_sub.loc[:, target],
                  how="left", left_on=left_on, right_on=right_on)
    if right_on != left_on:
        df.drop(right_on, axis=1, inplace=True)
    return df
