import unittest
import pdhelper as pd
import time
import json

def file_read(file: dict) -> pd.DataFrame:
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
            return pd.read_csv(filename, encoding=conf, header=header, index_col=index)
    elif extention == "xlsx" or extention == "xls":
        if conf == "":
            return pd.read_excel(filename, header=header, index_col=index)
        else:
            return pd.read_excel(filename, sheet_name=conf, header=header, index_col=index)
    else:
        # 拡張子がcsv,xlsx,xls以外だったらこのエラー
        raise ValueError("FileExtentionError")

class TestFunc(unittest.TestCase): # テストのためのクラス
    def test_read(self):
        with open("test_data/parallel/test_input.json") as f:
            files = json.load(f)
        start = time.time()
        arr = pd.parallel_read(files)
        end = time.time()
        print("parallel:"+str(end-start))

        l = dict()
        start = time.time()
        for i in files:
            l[i] = file_read(files[i])
        end = time.time()
        print("single:"+str(end-start))
        for i in arr:
            self.assertEqual(l[i].equals(arr[i]),True)

    def test_merge(self):
        left = pd.read_csv("test_data/merge/left1.csv")
        right = pd.read_csv("test_data/merge/right1.csv")
        ans = pd.read_csv("test_data/merge/out.csv")

        df = pd.left_merge(left,right,"name","named",["age"])
        self.assertEqual(df.equals(ans),True)

if __name__ == '__main__':
    unittest.main()