import pandas as pd
import sys
import multiprocessing
try:
    from pandarallel import pandarallel
except:
    print("並列で処理を行いたい場合はpandarallelインストールする必要があります。")
    print("pip install pandarallel でインストールしてください。")
    sys.exit(1)
from pandas._typing import (
    AggFuncType,
    Axis,
    NaAction,
    PythonFuncType,
)
from typing import (
    Any,
    Callable,
    Literal,
)
from collections.abc import Mapping
from pandas._libs import lib

pandarallel.initialize(progress_bar=True)

pd.DataFrame._apply = pd.DataFrame.apply
pd.DataFrame._applymap = pd.DataFrame.applymap
pd.Series._map = pd.Series.map
pd.Series._apply = pd.Series.apply

def df_apply(
    self,
    func: AggFuncType,
    axis: Axis = 0,
    raw: bool = False,
    result_type: Literal["expand", "reduce", "broadcast"] | None = None,
    **kwargs,
):
    process = multiprocessing.current_process()
    if process.daemon:
        if kwargs == dict():
            return self._apply(func, axis, raw, result_type)
        else:
            return self._apply(func, axis, raw, result_type, kwargs)
    if kwargs == dict():
        return self.parallel_apply(func, axis, raw, result_type)
    else:
        return self.parallel_apply(func, axis, raw, result_type, kwargs)


pd.DataFrame.apply = df_apply


def df_applymap(
    self, func: PythonFuncType, na_action: NaAction | None = None, **kwargs
):
    process = multiprocessing.current_process()
    if process.daemon:
        if kwargs == dict():
            return self._applymap(func)
        else:
            return self._applymap(func, kwargs)
    if kwargs == dict():
        print(func)
        return self.parallel_applymap(func)
    else:
        return self.parallel_applymap(func, na_action, kwargs)


pd.DataFrame.applymap = df_applymap