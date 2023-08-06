import pandas as pd
import numpy as np

class Wcsv:
    def missing_value(csv, frequency):
        df = pd.read_csv(csv, header=None)
        df = df[df[1] <= frequency]
        df.dropna(inplace=True)
        df.reset_index(inplace=True)
        return df

    def convert_string(df):
        csv_str = "" 
        words = []
        for i in range(0, len(df[0])):
            # 頻出回数分の単語を再生する
            for j in range(0, df[1][i]):
                words.append(df[0][i])
        
        np.random.shuffle(words)
        for word in words:
            csv_str += word + " "
        return csv_str