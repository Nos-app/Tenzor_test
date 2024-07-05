import pytest
from selenium import webdriver
from main import ContactsPage
from loguru import logger
import os

logger.remove()
logger.add("logs/logs.log", level="DEBUG", format="{time} {message}")

url_for_open = "https://sbis.ru/contacts/"


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_download_plugin(driver):
    contacts_page = ContactsPage(driver)
    contacts_page.open("https://sbis.ru")
    finde_link = contacts_page.find_just_link("Скачать локальные версии")
    link_for_go = finde_link.get_attribute("href")
    contacts_page.open(link_for_go)
    element_for_download = contacts_page.find_just_link("Скачать (Exe 7.22 МБ)")
    url_for_download = element_for_download.get_attribute("href")
    contacts_page.download_file(url_for_download)
    download_folder = "downloads"
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
    filename = os.path.join(download_folder, os.path.basename(url_for_download))
    if filename:
        logger.info("Файл найден и готов к скачиванию")
    else:
        logger.error("Файл для скачивания не найден")
    assert os.path.exists(filename)
    expected_size = 7.22
    actual_size = round(os.path.getsize(filename) / 1024 / 1024, 2)
    if actual_size == expected_size:
        logger.info(
            "Размер скачанного файла совпадает с размером файла на сайте! Тест пройден Успешно!"
        )
    else:
        logger.error("Тест провален, размеры файлов не совпадают!")
    assert actual_size == expected_size
    os.remove(filename)
