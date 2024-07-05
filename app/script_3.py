from main import *
import time
from selenium.common.exceptions import ElementNotInteractableException


driver = webdriver.Chrome()

# создаём объект страницы
contacts_page = ContactsPage(driver)
contacts_page.open("https://sbis.ru")

page_url = driver.current_url
finde_link = contacts_page.find_just_link("Скачать локальные версии")

link_for_go = finde_link.get_attribute("href")
contacts_page.open(link_for_go)

time.sleep(2)

new_url = driver.current_url

if new_url == page_url:
    driver.switch_to.window(driver.window_handles[-1])

finde_element = contacts_page.find_element_with_text("Windows")

finde_element2 = contacts_page.find_element_with_text("СБИС Плагин")

try:
    finde_element.click()
except ElementNotInteractableException:
    print("Элемент 'Windows' не кликабелен, просто проверили и мы на верном пути...")

try:
    finde_element2.click()
except ElementNotInteractableException:
    print("Элемент 'СБИС Плагин' не кликабелен, но значит мы точно где надо!")

element_for_download = contacts_page.find_just_link("Скачать (Exe 7.22 МБ)")


url_for_download = element_for_download.get_attribute("href")

contacts_page.download_file(url_for_download)

driver.quit()
