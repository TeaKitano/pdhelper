# pdhelper ver3の仕様目標
## その1 DataFrameの行・列に対するapplyをinplace化
DataFrameの列に関数を適応する場合、
```python
import pdhelper as pd
df = pd.read_csv("test.csv")
df["a"] = df["a"].apply(abs, axis=1)
```
のようにSeries経由で実装する必要がある。
それを
```python
df.row_apply("a", abs, inplace=True)
```
のようにできるようにする。
また、
```python
s = df.row_apply("a", abs)
```
とすれば、元DataFrameを変更せず関数を適応したシリーズを取得する。
行バージョンはcolumn_applyで実装
## その2 piplineの追加
DataFrameに対する処理のパイプラインを追加する<br>
pipeクラスに引数としてpipelineにしたい内容を登録する。<br>
登録は処理のリスト。処理一つ一つは辞書で記述され、"func"keyが関数、0・1のようなint型のkeyが0~連続で位置引数、文字列keyがキーワード引数を示す。
```python
import pdhelper as pd
df = pd.read_csv("test.csv")
pipe = pd.Pipe([{"func":pd.DataFrame.drop, 0:"name", "axis":1, "inplace":True},
                {"func":pd.DataFrame.row_apply, 0:"a", 1:abs, "inplace":True}])
df.adopt_pipe(pipe, inplace=True)
```
