import pandas as pd

def adopt_pipe(self:pd.DataFrame, pipe: list, inplace: bool = False):
    for process in pipe:
        func = process["func"]
        
    return