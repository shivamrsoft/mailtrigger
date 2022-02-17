import pandas as pd
import xlsxwriter


def CreateExcel(new_list):

    df = pd.DataFrame(data=new_list)
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter("apistatus.xlsx", engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object.
    df.to_excel(writer, sheet_name='Sheet1')

    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    border_fmt = workbook.add_format(
        {'bottom': 1, 'top': 1, 'left': 1, 'right': 1})
    worksheet.conditional_format(xlsxwriter.utility.xl_range(
        0, 0, len(df), len(df.columns)), {'type': 'no_errors', 'format': border_fmt})

    writer.save()
