import pandas as pd

def TransPandas(data) :
    df = pd.DataFrame(data[1:], columns=data[0])
    return df



