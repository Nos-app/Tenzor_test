import pytest
from selenium import webdriver
from main import ContactsPage
import selenium
from loguru import logger


logger.add("logs/logs.log", level="DEBUG", format="{time} {message}")

url_for_open = "https://sbis.ru/contacts/"


# А вот и сами тесты!
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()


# Тесты метода open
def test_contacts_page_open_positive_1(driver):
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


def test_contacts_page_open_negative_1(driver):
    with pytest.raises(AssertionError):
        contacts_page = ContactsPage(driver)
        contacts_page.open(url_for_open)
        assert (
            driver.current_url == "https://sbis.ru/contacts/"
        ), f"место положения не определилось и получен адрес {driver.current_url}"
        logger.error(
            f"Регион не был обнаружен. Ожидаемый URL: https://sbis.ru/contacts/, текущий URL: {driver.current_url}"
        )
    logger.info(f"Проверка негативного сценария для региона пройдена!")


def test_contacts_page_open_negative_2(driver):
    contacts_page = ContactsPage(driver)
    contacts_page.open(url_for_open)
    current_url = driver.current_url
    expected_url = f"https://sbis.ru/contacts/{contacts_page.get_region()}"
    if current_url != expected_url:
        logger.info(
            "Проверка №2 на определение региона в случае негативного сценария пройдена"
        )
    else:
        logger.error(
            f"Регион не был обнаружен. Ожидаемый URL: {expected_url}, текущий URL: {current_url} Проверка негативного сценария №2 не пройдена"
        )
    assert (
        current_url != expected_url
    ), f"Текущий URL: {current_url}, ожидался: {expected_url}"


# Тестим поиск по логo и переход по ссылке
def test_find_logo_link_positive(driver):
    contacts_page = ContactsPage(driver)
    contacts_page.open(url_for_open)
    # current_url = driver.current_url
    logo_link = contacts_page.find_logo_link("sbisru-Contacts__logo-tensor img")
    if logo_link is not None:
        logger.info("Тест поиска лого Тензор прошёл успешно")
    else:
        logger.error("Лого Тензор не найдено тест по поиску лого провален")
    assert logo_link is not None


def test_find_logo_link_negative(driver):
    contacts_page = ContactsPage(driver)
    contacts_page.open(url_for_open)
    logo_tensor_link = contacts_page.find_logo_link("sbisru-text--gray br")
    with pytest.raises(selenium.common.exceptions.ElementNotInteractableException):
        logo_tensor_link.click()
        logger.error("Тест негативного сценария перехода по ссылке провален!")
    logger.info("Тест негативного сценария перехода по ссылке прошел успешно")


def test_find_block_positive(driver):
    contacts_page = ContactsPage(driver)
    contacts_page.open(url_for_open)
    block = contacts_page.find_block("Сила в людях")
    if block is not None:
        logger.info(
            "Тест поиск блока с текстом 'Сила в людях' прошёл успешно, блок найден"
        )
    else:
        logger.error(
            "Тест поиск блока с текстом 'Сила в людях' успешно провален!, блок не найден!"
        )
    assert block is not None


def test_find_and_open_link(driver):
    contacts_page = ContactsPage(driver)
    contacts_page.open(url_for_open)
    logo_tensor_link = contacts_page.find_logo_link("sbisru-Contacts__logo-tensor img")
    logo_tensor_link.click()
    driver.switch_to.window(driver.window_handles[-1])
    blocks = contacts_page.find_block("Сила в людях")
    for block in blocks:
        link = contacts_page.find_block_with_link(block, "Подробнее")
        if link.get_attribute("text") == "Подробнее":
            logger.info(
                "Тест перехода по ссылке 'подробнее' в блоке с текстом 'Сила в людях' пройден успешно!"
            )
        else:
            logger.error(
                "Тест перехода по ссылке 'подробнее' в блоке с текстом 'Сила в людях' успешно провален!, что-то снова пошло не так!"
            )
    assert link is not None


def test_find_element_with_text(driver):
    contacts_page = ContactsPage(driver)
    contacts_page.open(url_for_open)
    logo_tensor_link = contacts_page.find_logo_link("sbisru-Contacts__logo-tensor img")
    logo_tensor_link.click()
    import time

    time.sleep(2)
    driver.switch_to.window(driver.window_handles[-1])
    blocks = contacts_page.find_block("Сила в людях")
    for block in blocks:
        link = contacts_page.find_block_with_link(block, "Подробнее")
    driver.get(link.get_attribute("href"))
    element = contacts_page.find_element_with_text("Работаем")
    if element.text == "Работаем":
        logger.info(
            "Тест поиска блока с текстом 'Работаем' успешно пройден, блок найден"
        )
    else:
        logger.error("Тест поиска блока с текстом 'Работаем' успешно провален!")
    assert element is not None, "Элемент не найден"
    assert element.text == "Работаем", "Текст элемента не соответствует ожидаемому"


def test_find_images(driver):
    contacts_page = ContactsPage(driver)
    contacts_page.open(url_for_open)
    logo_tensor_link = contacts_page.find_logo_link("sbisru-Contacts__logo-tensor img")
    logo_tensor_link.click()
    driver.switch_to.window(driver.window_handles[-1])
    blocks = contacts_page.find_block("Сила в людях")
    for block in blocks:
        link = contacts_page.find_block_with_link(block, "Подробнее")
    driver.get(link.get_attribute("href"))
    element = contacts_page.find_element_with_text("Работаем")
    images = contacts_page.find_images(element)
    widths = [img.get_attribute("width") for img in images]
    heights = [img.get_attribute("height") for img in images]
    if len(set(widths)) == 1 and len(set(heights)) == 1:
        logger.info(
            "Тест на поиск картинок и определение размеров пройден успешно - Высота и ширина всех картинок одинаковые"
        )

    else:
        logger.error(
            "ТТест на поиск картинок и определение размеров провален! - Размер картинок разный!"
        )
    assert len(set(widths)) == 1 and len(set(heights)) == 1, "Размер картинок разный!"
