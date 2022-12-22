#from datetime import date
import datetime
import pandas as pd
import os, sys

def parse(path: str):
    #Получаю текущую дату
    today = datetime.date.today()
    today_y_m_d = today.strftime('%Y%m%d')
    
    path = path + '/' + today_y_m_d

    dirs = os.listdir( path )
    row_counter = 0
    invert_df = pd.DataFrame(columns = ['Дата', 'Субъект ОРЭ', 'Номер', 'Наименование', 'Номер.1', 'Наименование.1', 'Тип показателя', 'Unnamed3', 'Период (ч)', 'Показатель'])
    print(dirs)

    # Вывести все файлы и папки
    for file in dirs:
        excel_path = path + '/' + file
        df = pd.read_excel(excel_path, sheet_name='Торговый график', skiprows=6)    
        df_head = pd.read_excel(excel_path, sheet_name='Торговый график', nrows = 3)
        date = df_head['Unnamed: 2'].iloc[1]
        name = df_head['Unnamed: 2'].iloc[0]
        period = 1
        period_counter = 0

        row = {}
        for j in range(len(df)-1):
            period = 1
            counter = 0 #нужен чтобы взять первые четыре колонки
            column_counter = 0 #нужен чтобы считать колонки с показателями
            for i in df.columns:
                if counter < 5:
                   # 
                    counter+=1
                if counter == 5:

                    row_series = [date, name, df['Номер'].loc[j], df['Наименование'].loc[j], df['Номер.1'].loc[j],df['Наименование.1'].loc[j]]
                    if column_counter == 0:
                        row_series.append('TCMIN')
                        row_series.append('Технический минимум, МВтЧ') 
                    elif column_counter == 1:
                        row_series.append('TLMIN')
                        row_series.append('Технологический минимум, МВтЧ')
                    elif column_counter == 2:
                        row_series.append('NPREG')
                        row_series.append('Нижний предел регулирования, МВтЧ')
                    elif column_counter == 3:
                        row_series.append('POBPR')
                        row_series.append('Плановый объем производства, МВтЧ') 
                    elif column_counter == 4:
                        row_series.append('VPREG')
                        row_series.append('Верхний предел регулирования, МВтЧ')
                    elif column_counter == 5:
                        row_series.append('TCMAX')
                        row_series.append('Технический максимум, МВтЧ') 
                    elif column_counter == 6:
                        row_series.append('TLMAX')
                        row_series.append('Технологический максимум, МВтЧ.')
                    row_series.append(period)
                    row_series.append(df[i].loc[j])
                    invert_df.loc[row_counter] = row_series
                    column_counter+=1                
                    row_counter += 1
                if column_counter == 7:
                    period+=1
                    column_counter = 0

    return invert_df.to_dict('split')['data']
