from main import *

driver = webdriver.Chrome()

# создаём объект страницы
contacts_page = ContactsPage(driver)
contacts_page.open("https://sbis.ru/contacts/")

# ищем элемент указаный в ТЗ по селектору со ссылкой и переходим по ней
logo_tensor_link = contacts_page.find_logo_link("sbisru-Contacts__logo-tensor img")
logo_tensor_link.click()

# Перепрыгиваем на новую вкладку, так как какой-то 'уволень' добавил в ссылку атрибут target=_blank
driver.switch_to.window(driver.window_handles[-1])

# Ищем Силу в людях )) и Если находим её, то ищем в том же блоке ссылку и переходим по ней
sila_v_lyudyh_blocks = contacts_page.find_block("Сила в людях")
for block in sila_v_lyudyh_blocks:
    link = contacts_page.find_block_with_link(block, "Подробнее")
    if link and link.get_attribute("text") == "Подробнее":
        print(f'Ссылка найдена Переходим - {link.get_attribute("href")}')
        driver.get(link.get_attribute("href"))
    else:
        print("Ссылка не найдена!")
        exit()

# Поиск элемента с текстом согласно ТЗ
element = contacts_page.find_element_with_text("Работаем")

# Перебераемся по блокам пока не найдём родительский блок того элемента, что мы искали, с картинками
images = contacts_page.find_images(element)

# Достаём нужные нам атрибуты с картинок и чтобы не выдумывать велосипед - засовываем их в сэт
widths = [img.get_attribute("width") for img in images]
heights = [img.get_attribute("height") for img in images]

# Если даже добавятся картинки и если даже изменится хотябы на 1 пиксель размеры некоторых картинок, сэт увеличится (Так проще)
if len(set(widths)) == 1 and len(set(heights)) == 1:
    print("Высота и ширина всех картинок одинаковые")
    driver.execute_script("alert('Высота и ширина всех картинок одинаковые');")
else:
    print("Не одинаковый размер картинок!")
    driver.execute_script("alert('Размер картинок разный!');")


# дадим чуток времени, чтоб скрипт показался ;)
import time

time.sleep(5)

driver.quit()
