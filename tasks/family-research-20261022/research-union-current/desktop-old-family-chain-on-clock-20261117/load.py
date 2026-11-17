import glob, numpy as np, pandas as pd
pd.set_option("display.width",250); pd.set_option("display.max_columns",80)
DATA="/home/claude/work/data/"
DAYS=["20231002","20231003","20231017","20231018"]
NAME={"20231002":"Mon Oct 2","20231003":"Tue Oct 3","20231017":"Tue Oct 17","20231018":"Wed Oct 18"}
def rd(day,stem,cols=None):
    fs=sorted(glob.glob(f"{DATA}{day}/{stem}-{day}-part*.parquet"))
    assert fs,(day,stem)
    return pd.concat([pd.read_parquet(f,columns=cols) for f in fs],ignore_index=True)
