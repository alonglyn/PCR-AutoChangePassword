import pandas as pd
from core.data_help import write_to_file



if __name__ == "__main__":
    df = pd.read_excel('data/account.xlsx')
    df1 = df.loc[0:29]
    df2 = df.loc[30:]
    write_to_file([df1],'pcr_farm_mana.txt')
    write_to_file([df2],'pcr_farm_zb.txt')
    write_to_file([df1,df2],'pcr_farm_all.txt')
