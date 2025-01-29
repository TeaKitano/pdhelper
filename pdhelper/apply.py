import pandas as pd


def row_apply(self: pd.DataFrame, row: str, func, inplace: bool = False):
    if inplace:
        self[row] = self.row_apply(row, func)
    else:
        return self[row].apply(func)

pd.DataFrame.row_apply = row_apply

def column_apply(self: pd.DataFrame, column: str, func, inplace: bool = False):
    if inplace:
        self.loc[column] = self.column_apply(column, func)
    else:
        return self.loc[column].apply(func)

pd.DataFrame.column_apply = column_apply
