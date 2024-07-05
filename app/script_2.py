from main import *
import time

driver = webdriver.Chrome()
contacts_page = ContactsPage(driver)
contacts_page.open("https://sbis.ru/contacts/")

region_element = contacts_page.find_region_element()
if region_element:
    print(f"Регион был определён Ваш регион - {region_element.text}")
else:
    print("Регион не был определён!")

contacts_page.change_region("41-kamchatskij-kraj")

time.sleep(2)

contacts_page.check_region("Камчатский край")
title_contact = contacts_page.check_additional_element()
if title_contact.text == "Петропавловск-Камчатский":
    print("Титулка контактов совпадает")

driver.quit()
