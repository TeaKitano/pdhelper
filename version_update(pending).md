# pdhelper ver2の仕様目標
## その1 pandasのオーバーライド
pandasのオーバーライドすることで、
```pyhton
import pdhelper as pd
```
だけでpandas自体も使えるようにする→import文をシンプルに
## その2 並列化
pandarallelをデフォルトで動くようにする
流石に常時並列化だと微妙なので、
```pyhton
from pdhelper import parallel_DataFrame
```
をimportしたときだけ並列化するようにしたい。<br>
とりあえず実装内容は以下。DataFrame.groupbyとSeries.rollingは別実装&使用頻度少なそうなのでとりあえず放置。
```
pandas.DataFrame.apply → pandas.DataFrame.parallel_apply
pandas.DataFrame.applymap → pandas.DataFrame.parallel_applymap
pandas.Series.map → pandas.Series.parallel_map
pandas.Series.apply → pandas.Series.parallel_apply
```