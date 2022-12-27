import requests
from bs4 import BeautifulSoup as bs
from datetime import date
import warnings
import os
import parse

def download_excel(directory_for_download: str):

    #Отключение сообщение о том что требуется сертификат
    warnings.filterwarnings('ignore', message='Unverified HTTPS request')
    
    #Получаю текущую дату
    today = date.today()
    today_y_m_d = today.strftime('%Y%m%d')
    
    if os.path.isdir(directory_for_download):
        directory_for_download = directory_for_download + '/' + today_y_m_d
        if os.path.isdir(directory_for_download) == False:
            os.mkdir(directory_for_download)
    else:
        os.mkdir(directory_for_download)
        directory_for_download = directory_for_download + '/' + today_y_m_d
        os.mkdir(directory_for_download)

    regions = ['eur']
    
    #Адресс сайта где лежат excel без указания региона. Их два sib и eur
    URL_TEMPLATE = "https://www.atsenergo.ru/nreport?access=public&rname=carana_sell_units&rdate=" + today_y_m_d + "&region="
    #Адресс сайта для для скачивания excel
    site_for_download_excel = 'https://www.atsenergo.ru/nreport'
    filename_pattern = 'KUZBAS'

    for reg in regions:
        URL = URL_TEMPLATE + reg
        r = requests.get(URL, verify=False)
        soup = bs(r.text, "html.parser")
        reports_files = soup.find_all('div', class_='reports_files')
        table_with_href_and_names = []
        pattern = 'Опубликовано'
        for report in reports_files:
            for r in report:
                for cont in r:
                    for c in cont:
                        for a in c:
                            keys = a.attrs
                            title = str(keys.get('title'))
                            if pattern in title:
                                #Получаю ссылку на для скачивания excel
                                url_for_download_excel = keys.get('href')
                                #Получаю имя файла
                                file_name = a.text
                                tup = (url_for_download_excel, file_name)
                                table_with_href_and_names.append(tup)
        
        for index, row in enumerate(table_with_href_and_names):
            site_url_for_get_data = site_for_download_excel + row[0]
            #print(site_url_for_get_data)
            r = requests.get(site_url_for_get_data, verify=False)
            file_name = row[1]
            #Для примера беру два значения и и чтобы был точно Кузбас
            if index <= 1 or file_name.find(filename_pattern) != -1:
                print(file_name)
                file_fill_path = os.path.join(directory_for_download, file_name)
                with open(file_fill_path, 'wb') as f:
                    f.write(r.content)
                #if index == 1:
                     #break

        print(f"Количество записей {len(table_with_href_and_names)} для {reg} региона")

        

directory_for_download = "/Users/kadyrgulovartur/python_learn/test_folder"
download_excel(directory_for_download)
data = parse.parse(directory_for_download)
print(data)
