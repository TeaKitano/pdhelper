import pandas as pd

def left_merge(df, df_sub,left_on,right_on,target):
    sub_len = len(df_sub)
    df_sub = df_sub[~df_sub[right_on].duplicated()] # 被りを消す
    if type(target) == list:
        target.append(right_on)
    else:
        target = [target,right_on]
    if sub_len != len(df_sub):
        print("mergeするデータに被りがありました。一番上のデータのみを利用しています。")
    df = pd.merge(df,df_sub.loc[:,target],how="left",left_on=left_on,right_on=right_on)
    if right_on !=left_on:
        df.drop(right_on)
    return df