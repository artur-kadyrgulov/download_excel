import download_excel
import parse

directory_for_download = "/Users/kadyrgulovartur/python_learn/test_folder"
download_excel.download_excel(directory_for_download)
print(parse.parse(directory_for_download))
