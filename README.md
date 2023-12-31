# pdhelper
pandas上で動く便利なツールをまとめたモジュールです。

## Install
```sh
pip install pandashelper
```
でインストールできます。
## Usage
```python
import pdhelper
```
でimport可能です。この資料においては
```python
import pdhelper as pd
```
とすることで、pdとしてimportします。
(PyPiへの登録の関係上、install時はpandashelper、import時はpdhelperとなっていますので、気を付けてください。)<br>
また、このモジュールはpandasをオーバーライドしているため、pandasに実装されているすべての関数を利用できます。<br>
詳細は、[test.py](test.py)で確認できます。
### parallel_read
複数ファイルを並列処理を使い高速に読み込むための関数です。入力例は[test_input.json](test_data/parallel/test_input.json)を確認してください。<br>
```text
input
    files:読み込むファイルのdict
        key:ファイル名
        value:各種設定のdict
            conf:追加設定 csvの場合文字コードを(空欄ならutf-8)、excelファイルの場合使うシート名を(空欄なら1枚目のシート)書く
            header:ヘッダーついてるかどうか　ついてたらTrue ついてなかったらFalse
            index:インデックスついてるかどうか　ついてたらTrue ついてなかったらFalse
output
    読み込んだDataFrameのリスト
```
```python
pd.paralell_read(files, conf, header, index)
```

### left_merge
左側へのmergeに特化した関数です。<br>
```text
input<br>
    df: 結合元データ<br>
    df_sub: 結合したいデータ<br>
    left_on: dfの結合キー<br>
    right_on: df_subの結合キー<br>
    target: 使いたい列名 複数の場合リストで指定<br>
output<br>
    マージされたDataFrame
```
```python
pd.left_merge(df, df_sub, left_on, rright_on,target)
```
example:<br>
df
| id  | name |     
| --- | ---- | 
| 0   | a    |
| 1   | b    |     
| 2   | c    |     
| 3   | d    |
| 4   | e    |
| 5   | f    |

df_sub<br>
| name | gender | age | 
| ---- | ------ | --- | 
| a    | 1      | 5   | 
| b    | 2      | 12  | 
| c    | 1      | 31  | 
| d    | 1      | 16  | 
| e    | 1      | 27  | 
| f    | 2      | 19  | 

として
```python
pd.left_merge(df, df_sub, name, name,gender)
```
とした場合、
| id  | name | gender | 
| --- | ---- | ------ | 
| 0   | a    | 1      | 
| 1   | b    | 2      | 
| 2   | c    | 1      | 
| 3   | d    | 1      | 
| 4   | e    | 1      | 
| 5   | f    | 2      | 

が返ってきます。

### 並列処理
```python
from pdhelper import parallel_dataframe
```
をimportすることにより、DataFrameとSeriesに適用するapply等を常時並列で処理します。
この機能を使う場合、
```bash
pip install pandarallel
```
でpandarallelをインストールしてください。<br>
現在対応している関数は
```
pandas.DataFrame.apply
pandas.DataFrame.applymap
pandas.Series.map
pandas.Series.apply
```
の4つです。<br>
詳細設定のためにinitialize関数が用意されています。
```python
parallel_dataframe.initialize(nb_workers=10, progress_bar=False)
```
のように利用します。
```text
input
    nb_workers : どれだけ並列にするかを設定します。デフォルトではCPUのスレッド数-2です。
    progress_bar : どれだけ処理したかを標準出力にバーで表すかどうかです。デフォルトではFalseとなっています。表示したい場合はTrueにしてください。
output
    なし(並列処理用のシステムの初期化が行われます。)
```
## Requrements
```python
pandas
```
## Licence
BSD 3-Clause License (LICENSEファイルも参照して下さい)
## Author
name: Tea Kitano<br>
e-mail: chachamusics@outlook.com<br>
twitter: https://twitter.com/ChachaLepracaun
