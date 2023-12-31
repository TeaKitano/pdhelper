import pandas as pd
import sys
import multiprocessing
import psutil
try:
    from pandarallel import pandarallel
except ModuleNotFoundError:
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


pd.DataFrame._apply = pd.DataFrame.apply
pd.DataFrame._applymap = pd.DataFrame.applymap
pd.Series._map = pd.Series.map
pd.Series._apply = pd.Series.apply


def initialize(nb_workers=max(psutil.cpu_count(logical=True)-2,
                              psutil.cpu_count(logical=False)), progress_bar=False):
    pandarallel.initialize(nb_workers=nb_workers, progress_bar=progress_bar)
    return


def df_apply(
    self,
    func: AggFuncType,
    axis: Axis = 0,
    raw: bool = False,
    result_type: Literal["expand", "reduce", "broadcast"] | None = None,
    **kwargs,
):
    if axis == 0:
        process = multiprocessing.current_process()
        if process.daemon:
            if kwargs == dict():
                return self._apply(func, axis, raw, result_type)
            else:
                return self._apply(func, axis, raw, result_type, kwargs)
        if kwargs == dict():
            try:
                return self.parallel_apply(func, axis, raw, result_type)
            except AttributeError:
                initialize()
                return self.parallel_apply(func, axis, raw, result_type)
        else:
            try:
                return self.parallel_apply(func, axis, raw, result_type, kwargs)
            except AttributeError:
                initialize()
                return self.parallel_apply(func, axis, raw, result_type, kwargs)
    else:
        process = multiprocessing.current_process()
        self = self.T
        axis = 0
        if process.daemon:
            if kwargs == dict():
                try:
                    return self._apply(func, axis, raw, result_type)
                except AttributeError:
                    initialize()
                    return self._apply(func, axis, raw, result_type)
            else:
                try:
                    return self._apply(func, axis, raw, result_type, kwargs)
                except AttributeError:
                    initialize()
                    return self._apply(func, axis, raw, result_type, kwargs)
        if kwargs == dict():
            try:
                return self.parallel_apply(func, axis, raw, result_type)
            except AttributeError:
                initialize()
                return self.parallel_apply(func, axis, raw, result_type)
        else:
            try:
                return self.parallel_apply(func, axis, raw, result_type, kwargs)
            except AttributeError:
                initialize()
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
        try:
            return self.parallel_applymap(func)
        except AttributeError:
            initialize()
            return self.parallel_applymap(func)
    else:
        try:
            return self.parallel_applymap(func, na_action, kwargs)
        except AttributeError:
            initialize()
            return self.parallel_applymap(func, na_action, kwargs)


pd.DataFrame.applymap = df_applymap


def s_map(
    self,
    arg: Callable | Mapping | pd.Series,
    na_action: Literal["ignore"] | None = None,
):
    process = multiprocessing.current_process()
    if process.daemon:
        return self._map(arg, na_action)
    try:
        return self.parallel_map(arg, na_action)
    except AttributeError:
        initialize()
        return self.parallel_map(arg, na_action)


pd.Series.map = s_map


def s_apply(
    self,
    func: AggFuncType,
    convert_dtype: bool | lib.NoDefault = lib.no_default,
    args: tuple[Any, ...] = (),
    **kwargs,
):
    process = multiprocessing.current_process()
    if process.daemon:
        if kwargs == dict():
            return self._apply(func, convert_dtype, args)
        else:
            return self._apply(func, convert_dtype, args, kwargs)
    if kwargs == dict():
        try:
            return self.parallel_apply(func, convert_dtype, args)
        except AttributeError:
            initialize()
            return self.parallel_apply(func, convert_dtype, args)
    else:
        try:
            return self.parallel_apply(func, convert_dtype, args, kwargs)
        except AttributeError:
            initialize()
            return self.parallel_apply(func, convert_dtype, args, kwargs)


pd.Series.apply = s_apply
