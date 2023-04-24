'''Создание webdriver с кастомными настройками: изменение пути для скачиваемых файлов в браузере.
Без них файл скачивается в дирректорию по умолчанию (Например, в папку Загрузки).
Необходимы, если файл скачивается не по прямой ссылке, а при использовании действий в браузере (например, нужно нажать кнопку Загрузить)'''
import os
import zipfile
from os.path import basename

import pytest
from time import sleep
from pathlib import Path

import requests

from selene.support.shared import browser
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

import tests


project = Path(__file__).parent  #Nata
resources = str(project.joinpath(f'resources/')) #Nata

resources1 = os.path.abspath(os.path.join(os.path.dirname(tests.__file__), f'../resources/')) #Nata  2 вариант

@pytest.fixture
def set_browser():
    # current_dir = os.path.dirname(__file__)
    # download_sours = os.path.abspath(os.path.join(current_dir, 'resources'))
    options = webdriver.ChromeOptions()
    prefs = {
        #"download.default_directory": resources(),
        "download.default_directory": resources,
        "download.prompt_for_download": False
    }
    options.add_experimental_option("prefs", prefs)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    browser.config.driver = driver


'''Настройки для скачивания напрямую с web. Файлы сохраняются в проект в папку с файлом теста'''

url_pdf = "https://bugs.python.org/file47781/Tutorial_EDIT.pdf"
url_xlsx = "https://go.microsoft.com/fwlink/?LinkID=521962"
url_csv = "https://support.staffbase.com/hc/en-us/articles/360007108391-CSV-File-Examples"

response_pdf = requests.get(url_pdf, allow_redirects=True)
response_xlsx = requests.get(url_xlsx, allow_redirects=True)
response_csv = requests.get(url_csv, allow_redirects=True)


@pytest.fixture
def download_files(set_browser):
    ''' download_pdf'''
    # current_dir = os.path.dirname(__file__)
    # download_sours = os.path.abspath(os.path.join(current_dir, 'resources'))
    # with open(os.path.join(resources(), 'dummy.pdf'), 'wb') as file_pdf:
    with open(os.path.join(resources, 'dummy.pdf'), 'wb') as file_pdf:
        file_pdf.write(response_pdf.content)

    ''' download_xlsx'''
    #with open('Financial Sample.xlsx', 'wb') as file_xlsx:
    with open(os.path.join(resources, 'Financial Sample.xlsx'), 'wb') as file_xlsx:
        file_xlsx.write(response_xlsx.content)

    ''' download_csv'''
    browser.open(url_csv)
    browser.element('//a[contains(text(),"Data Set for Username Onboarding")]').click()
    sleep(5)


@pytest.fixture
def zip_files(download_files):
    # current_dir = os.path.dirname(__file__)
    # path_xlsx = os.path.abspath('Financial Sample.xlsx')
    # path_files = os.path.join(current_dir, 'resources')
    # file_dir = os.listdir(path_files)
    file_dir = os.listdir(resources)

    #with zipfile.ZipFile(f'{resources()}/myZip.zip', mode='w', compression=zipfile.ZIP_DEFLATED) as my_zip:
    with zipfile.ZipFile(f'{resources}/myZip.zip', mode='w', compression=zipfile.ZIP_DEFLATED) as my_zip:
        for files in file_dir:
            #add_files = os.path.join(resources(), files)
            add_files = os.path.join(resources, files)
            my_zip.write(add_files, basename(add_files))

    # with zipfile.ZipFile(f'{resources()}/myZip.zip', mode='a', compression=zipfile.ZIP_DEFLATED) as add_zip:
    #     add_zip.write(path_xlsx, basename(path_xlsx))

    yield zip_files
    file_dir = os.listdir(resources)
    for files in file_dir:
        os.remove(f'{resources}/{files}')
    # os.remove(f'{resources()}/myZip.zip')
    # os.remove(f'{resources()}/dummy.pdf')
    # os.remove(f'{resources()}/username.csv')
    # os.remove(f'{project()}\\tests\\Financial Sample.xlsx')

