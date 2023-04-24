___________Download Files Notes___________

import os.path
from time import sleep

import requests

'''Создание webdriver с кастомными настройками: изменение пути для скачиваемых файлов в браузере.
Без них файл скачивается в дирректорию по умолчанию (Например, в папку Загрузки).
Необходимы, если файл скачивается не по прямой ссылке, а при использовании действий в браузере (например, нужно нажать кнопку Загрузить)'''

from selene.support.shared import browser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": 'C:\\Users\\Hanna\\PycharmProjects\\qa_guru_python_4_7\\resources',
    "download.prompt_for_download": False
}
options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

browser.config.driver = driver

'''Настройки для скачивания напрямую с web. Файлы сохраняются в проект в папку с файлом теста'''

url_pdf = "https://file-examples.com/storage/fef89aabc36429826928b9c/2017/10/file-example_PDF_1MB.pdf"
url_xlsx = "https://go.microsoft.com/fwlink/?LinkID=521962"
url_csv = "https://support.staffbase.com/hc/en-us/articles/360007108391-CSV-File-Examples"

response_pdf = requests.get(url_pdf, allow_redirects=True)
response_xlsx = requests.get(url_xlsx, allow_redirects=True)
response_csv = requests.get(url_csv, allow_redirects=True)


def test_download_pdf():
    with open('..\\resources\\dummy.pdf', 'wb') as file_pdf:
        file_pdf.write(response_pdf.content)


def test_download_xlsx():
    with open('Financial Sample.xlsx', 'wb') as file_xlsx:
        file_xlsx.write(response_xlsx.content)


def test_download_csv():
    browser.open(url_csv)
    browser.element('//a[contains(text(),"Data Set for Username Onboarding")]').click()
    sleep(5)
    print(os.path.abspath(__file__))

''' Удаление файлов '''
# def test_remove_files():
#     remove_pdf = os.remove('..\\resources\\dummy.pdf')


_______ Zip Files Notes________

import os
import zipfile
from os.path import basename

# current_dir = os.path.dirname(os.path.abspath(__file__))
current_dir = os.path.dirname(__file__)
# path_csv = os.path.join(current_dir, '..', 'resources', 'username.csv')
path_xlsx = os.path.abspath('Financial Sample.xlsx')
# path_pdf = os.path.abspath(current_dir, '..', 'dummy.pdf')

path_files = os.path.join(current_dir, '..', 'resources')
file_dir = os.listdir(path_files)


# with zipfile.ZipFile('myZip.zip', mode='w', compression=zipfile.ZIP_DEFLATED) as my_zip:
#     my_zip.write(path_csv, basename(path_csv))

with zipfile.ZipFile('..\\resources\\myZip.zip', mode='w', compression=zipfile.ZIP_DEFLATED) as my_zip:
    for files in file_dir:
        add_files = os.path.join(path_files, files)
        my_zip.write(add_files, basename(add_files))

with zipfile.ZipFile('..\\resources\\myZip.zip', mode='a', compression=zipfile.ZIP_DEFLATED) as add_zip:
    add_zip.write(path_xlsx, basename(path_xlsx))
    # add_zip.write(path_pdf, basename(path_pdf))

# path_pdf = 'C:\\Users\\Hanna\\PycharmProjects\\qa_guru_python_4_7\\tests'
# pdf_file_dir = os.listdir(path_pdf)
#
# path_xlsx = 'C:\\Users\\Hanna\\PycharmProjects\\qa_guru_python_4_7\\tests\\..xlsx'
# xlsx_file_dir = os.listdir(path_xlsx)
#
# with zipfile.ZipFile('myZip.zip', mode='w', compression=zipfile.ZIP_DEFLATED) as add_to_zip:
#     # add_to_zip.write(pdf_file_dir, filename='../resources/dummy(1).pdf')
#     # for file_xlsx in xlsx_file_dir:
#         add_xlsx = os.path.join(path_xlsx)
#         add_to_zip.write(add_xlsx)


current_dir = os.path.dirname(os.path.abspath(__file__))
create_sours = os.path.abspath(os.path.join(current_dir, '..', 'resources'))

