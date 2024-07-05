import pytest
from selenium import webdriver
from main import ContactsPage
from loguru import logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

logger.remove()
logger.add("logs/logs.log", level="DEBUG", format="{time} {message}")


url_for_open = "https://sbis.ru/contacts/"


# А вот и сами тесты!
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


def test_find_region(driver):
    contacts_page = ContactsPage(driver)
    contacts_page.open(url_for_open)
    current_url = driver.current_url
    expected_url = f"https://sbis.ru/contacts/{contacts_page.get_region()}?tab=clients"
    if current_url == expected_url:
        logger.info("Проверка на определение региона прошла успешно")
    else:
        logger.error(
            f"Регион не был обнаружен. Ожидаемый URL: {expected_url}, текущий URL: {current_url}"
        )
    assert (
        current_url == expected_url
    ), f"что-то пошло не так и ваш регион установлен как {contacts_page.get_region()}"


def test_check_list_partner(driver):
    contacts_page = ContactsPage(driver)
    contacts_page.open(url_for_open)
    partners = contacts_page.check_list_partners("city-id-2")
    if partners:
        logger.info("Список партнёров обнаружен")
    else:
        logger.error("Список партнёров обнаружен, ошибка, тест провален!")
    assert (
        partners
    ), f"что-то пошло не так и ваш регион установлен как {contacts_page.get_region()}"


def test_change_region_and_check_this(driver):
    contacts_page = ContactsPage(driver)
    contacts_page.open(url_for_open)
    contacts_page.change_region("41-kamchatskij-kraj")
    wait = WebDriverWait(driver, 5)
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//span[@class='sbis_ru-Region-Chooser__text sbis_ru-link']")
        )
    )
    region = contacts_page.check_region("Камчатский край")
    if region:
        logger.info(f"Регион успешно изменен на {region.text}")
    else:
        logger.error(f"Регион не изменился. Текущий регион - {region.text}")
    assert (
        region is not False
    ), f"что-то пошло не так! Регион не изменился. Текущий регион - {region.text}"


def test_check_region_change(driver):
    contacts_page = ContactsPage(driver)
    contacts_page.open(url_for_open)
    partners1 = contacts_page.check_list_partners("city-id-2")
    first_url = driver.current_url
    region1 = contacts_page.find_region_element()
    region1_text = region1.text
    contacts_page.change_region("41-kamchatskij-kraj")
    wait = WebDriverWait(driver, 5)
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//span[@class='sbis_ru-Region-Chooser__text sbis_ru-link']")
        )
    )
    region2 = contacts_page.find_region_element()  # Re-locate the region element
    region2_text = region2.text  # Get the text of the re-located element
    partners2 = contacts_page.check_list_partners("city-id-2")
    second_url = driver.current_url
    if partners1 != partners2 and first_url != second_url:
        logger.info(
            f"Регион точно был успешно изменен на {region2_text}, был {region1_text}"
        )
    else:
        logger.error(f"Регион не изменился. Текущий регион - {region2_text}")
    assert (
        partners1 != partners2 and first_url != second_url
    ), f"что-то пошло не так Регион не изменился. Текущий регион - {region2_text}"


def test_check_partners_again(driver):
    contacts_page = ContactsPage(driver)
    contacts_page.open(url_for_open)
    contacts_page.change_region("41-kamchatskij-kraj")
    wait = WebDriverWait(driver, 5)
    wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "//span[@class='sbis_ru-Region-Chooser__text sbis_ru-link']")
        )
    )
    partners = contacts_page.check_additional_element()
    if partners:
        logger.info(f"Да партнёры теперь во истину с {partners.text}")
    else:
        logger.error("Нет, тест провален и наши партнёры кудато делись")
    assert partners, "что-то пошло не так! Регион не изменился. партнёры сбежали!"
