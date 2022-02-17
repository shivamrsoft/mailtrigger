import pandas as pd


def CreateExcel(new_list):

    df = pd.DataFrame(data=new_list)
    df.to_excel('apistatus.xlsx')
