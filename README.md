# pdhelper
pandas上で動く便利なツールをまとめたモジュールです。

## Install
```sh
pip install pdhelper
```
※現在pypiへの登録が済んでおらず、こちらの方法でinstallはできません。
```sh
pip install git+https://github.com/TeaKitano/pdhelper.git
```
を使ってください。

## Usage
```python
import pdhelper
```
でimport可能です。この資料においては
```python
import pdhelper as ph
```
とすることで、phとしてimportします。

### parallel_read
複数ファイルを並列処理を使い高速に読み込むための関数です。<br>
input<br>
&emsp;files:ファイル名のリスト<br>
&emsp;conf:追加設定 csvの場合文字コードを(空欄ならutf-8)、excelファイルの場合使うシート(空欄なら1枚目のシート)書く<br>
&emsp;header:ヘッダーついてるかどうか　ついてたらTrue ついてなかったらFalse<br>
&emsp;index:インデックスついてるかどうか　ついてたらTrue ついてなかったらFalse<br>
output<br>
&emsp;読み込んだDataFrameのリスト
```python
ph.paralell_read(files, conf, header, index)
```

### left_merge
左側へのmergeに特化した関数です。<br>
input<br>
&emsp;df: 結合元データ<br>
&emsp;df_sub: 結合したいデータ<br>
&emsp;left_on: dfの結合キー<br>
&emsp;right_on: df_subの結合キー<br>
&emsp;target: 使いたい列名 複数の場合リストで指定<br>
output<br>
&emsp;マージされたDataFrame
```python
ph.left_merge(df, df_sub, left_on, rright_on,target)
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
df_sub
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
ph.left_merge(df, df_sub, name, name,gender)
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
が返ってきます
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
