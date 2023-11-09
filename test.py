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
        ans = s.map(lambda x: str(x)[0])
        for i in ans:
            self.assertEqual(i, "1")
        ans = s.apply(lambda x: str(x)[0])
        for i in ans:
            self.assertEqual(i, "1")

        def add_a(x, a):
            return x+a
        ans = s.apply(add_a, args=[2])
        for i in range(3):
            self.assertEqual(ans[i], i+17)

    def test_parallelDataframe(self):
        df = pd.read_csv("test_data/dataframe/test_df.csv")
        df1 = df.apply(lambda x: sum(x))
        self.assertEqual(list(df1), [48, 84, 108, 135])
        df2 = df.apply(lambda x: x["a"]+x["b"]-x["c"], axis=1)
        self.assertEqual(list(df2), [7, 8, 9])
        df3 = df.applymap(lambda x: x-2)
        re_list = []
        for i in df3:
            re_list.append(list(df3[i]))
        expend = [[13, 14, 15], [25, 26, 27], [33, 34, 35], [42, 43, 44]]
        self.assertEqual(re_list, expend)


if __name__ == '__main__':
    unittest.main()
