import unittest
import pdhelper as pd
import time
import json

from pdhelper import parallel_dataframe


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


class TestFunc(unittest.TestCase):  # テストのためのクラス
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
            self.assertEqual(l[i].equals(arr[i]), True)

    def test_merge(self):
        left = pd.read_csv("test_data/merge/left1.csv")
        right = pd.read_csv("test_data/merge/right1.csv")
        ans = pd.read_csv("test_data/merge/out.csv")

        df = pd.left_merge(left, right, "name", "named", ["age"])
        self.assertEqual(df.equals(ans), True)

    def test_parallelSeries(self):
        df = pd.read_csv("test_data/dataframe/test_df.csv")
        s = df["a"]
        self.assertEqual(s.map(lambda x: str(x)[0]).equals(
            s._map(lambda x: str(x)[0])), True)
        self.assertEqual(s.apply(lambda x: str(x)[0]).equals(
            s._apply(lambda x: str(x)[0])), True)

        def add_a(x, a):
            return x+a
        self.assertEqual(s.apply(add_a, args=[2]).equals(
            s._apply(add_a, args=[2])), True)

    def test_parallelDataframe(self):
        df = pd.read_csv("test_data/dataframe/test_df.csv")
        self.assertEqual(df.apply(lambda x: sum(x)).equals(
            df._apply(lambda x: sum(x))), True)
        self.assertEqual(df.apply(lambda x: x["a"]+x["b"]-x["c"], axis=1).equals(
            df._apply(lambda x: x["a"]+x["b"]-x["c"], axis=1)), True)
        self.assertEqual(df.applymap(
            lambda x: x-2).equals(df._applymap(lambda x: x-2)), True)


if __name__ == '__main__':
    unittest.main()
