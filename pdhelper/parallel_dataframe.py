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
from typing import (
    Any,
    Callable,
    Literal,
)
from collections.abc import Mapping


if not hasattr(pd.DataFrame, "_pdhelper_apply"):
    pd.DataFrame._pdhelper_apply = pd.DataFrame.apply
if not hasattr(pd.DataFrame, "_pdhelper_map"):
    pd.DataFrame._pdhelper_map = pd.DataFrame.map
if not hasattr(pd.Series, "_pdhelper_map"):
    pd.Series._pdhelper_map = pd.Series.map
if not hasattr(pd.Series, "_pdhelper_apply"):
    pd.Series._pdhelper_apply = pd.Series.apply

pd.DataFrame._apply = pd.DataFrame._pdhelper_apply
pd.DataFrame._map = pd.DataFrame._pdhelper_map
pd.DataFrame._applymap = pd.DataFrame._pdhelper_map
pd.Series._map = pd.Series._pdhelper_map
pd.Series._apply = pd.Series._pdhelper_apply


def initialize(
    nb_workers=max(
        psutil.cpu_count(logical=True)-2,
        psutil.cpu_count(logical=False),
    ),
    progress_bar=False,
):
    pandarallel.initialize(nb_workers=nb_workers, progress_bar=progress_bar)
    return


def df_apply(
    self,
    func: Callable,
    axis: int | str = 0,
    raw: bool = False,
    result_type: Literal["expand", "reduce", "broadcast"] | None = None,
    args: tuple[Any, ...] = (),
    by_row: Literal[False, "compat"] = "compat",
    engine: Callable | Literal["python", "numba"] | None = None,
    engine_kwargs: dict[str, bool] | None = None,
    **kwargs,
):
    axis = self._get_axis_number(axis)
    apply_kwargs = {
        "axis": axis,
        "raw": raw,
        "result_type": result_type,
        "args": args,
        "by_row": by_row,
        "engine": engine,
        "engine_kwargs": engine_kwargs,
        **kwargs,
    }
    if axis == 0:
        process = multiprocessing.current_process()
        if process.daemon:
            return self._apply(func, **apply_kwargs)
        try:
            return self.parallel_apply(func, **apply_kwargs)
        except AttributeError:
            initialize()
            return self.parallel_apply(func, **apply_kwargs)

    # pandarallel processes axis=0 efficiently, so transpose row-wise apply.
    transposed = self.T
    apply_kwargs["axis"] = 0
    if multiprocessing.current_process().daemon:
        return transposed._apply(func, **apply_kwargs)
    try:
        return transposed.parallel_apply(func, **apply_kwargs)
    except AttributeError:
        initialize()
        return transposed.parallel_apply(func, **apply_kwargs)


pd.DataFrame.apply = df_apply


def df_map(
    self,
    func: Callable,
    na_action: Literal["ignore"] | None = None,
    **kwargs,
):
    process = multiprocessing.current_process()
    if process.daemon:
        return self._map(func, na_action=na_action, **kwargs)

    def series_map(series):
        return series._map(func, na_action=na_action, **kwargs)

    try:
        return self.parallel_apply(series_map, axis=0)
    except AttributeError:
        initialize()
        return self.parallel_apply(series_map, axis=0)


pd.DataFrame.map = df_map
pd.DataFrame.applymap = df_map


def s_map(
    self,
    arg: Callable | Mapping | pd.Series | None = None,
    na_action: Literal["ignore"] | None = None,
    engine: Callable | None = None,
    **kwargs,
):
    process = multiprocessing.current_process()
    if process.daemon:
        return self._map(arg, na_action=na_action, engine=engine, **kwargs)
    try:
        return self.parallel_map(
            arg, na_action=na_action, engine=engine, **kwargs
        )
    except AttributeError:
        initialize()
        return self.parallel_map(
            arg, na_action=na_action, engine=engine, **kwargs
        )


pd.Series.map = s_map


def s_apply(
    self,
    func: Callable,
    args: tuple[Any, ...] = (),
    *,
    by_row: Literal[False, "compat"] = "compat",
    **kwargs,
):
    apply_kwargs = {
        "args": args,
        "by_row": by_row,
        **kwargs,
    }
    process = multiprocessing.current_process()
    if process.daemon:
        return self._apply(func, **apply_kwargs)
    try:
        return self.parallel_apply(func, **apply_kwargs)
    except AttributeError:
        initialize()
        return self.parallel_apply(func, **apply_kwargs)


pd.Series.apply = s_apply
