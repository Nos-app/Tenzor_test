from selenium import webdriver
from selenium.webdriver.common.by import By
import os
import requests


class ContactsPage:
    """Объект страницы"""

    def __init__(self, driver):
        """инициализация и Запуск сразу с контактов, с Вашего позволения"""
        self.driver = driver
        # self.url = "https://sbis.ru/contacts/"

    # метод запуска драйвера / открытие браузера
    def open(self, url):
        """Функция открытия сраницы с прокидывнием в неё url"""
        self.driver.get(url)

    def find_logo_link(self, selector):
        """метод поиска лого"""
        return self.driver.find_element(By.CSS_SELECTOR, f".{selector}")

    def find_block(self, text):
        """метод поиска блока с текстом в тэге p"""
        return self.driver.find_elements(By.XPATH, f"//div[contains(p, '{text}')]")

    def find_block_with_link(self, block, text):
        """метод поиска блока со ccылкой по тексту"""
        return block.find_element(By.XPATH, f".//a[contains(text(), '{text}')]")

    def find_just_link(self, text):
        """Метод поиска просто ссылки по тексту"""
        link = self.driver.find_element(By.XPATH, f".//a[contains(text(), '{text}')]")
        return link

    def find_element_with_text(self, text):
        """метод поиска элемента по тексту"""
        return self.driver.find_element(By.XPATH, f"//*[contains(text(), '{text}')]")

    def find_images(self, element):
        """метод поиска картинок в родительском блоке запрашиваемого элемента с определённым текстом"""
        parent_element = element.find_element(By.XPATH, "..")
        images = parent_element.find_elements(By.TAG_NAME, "img")
        while not images:
            parent_element = parent_element.find_element(By.XPATH, "..")
            images = parent_element.find_elements(By.TAG_NAME, "img")
        return images

    def get_region(self):
        """Метод вытягивания части эндпоинта с регионом"""
        url = self.driver.current_url
        location = url.split("?")[0].split("/")[-1]
        return location

    def find_region_element(self):
        """Поиск названия региона"""
        return self.driver.find_element(
            By.XPATH, "//span[@class='sbis_ru-Region-Chooser__text sbis_ru-link']"
        )

    def change_region(self, region):
        """Метод изменения региона"""
        new_region = f"https://sbis.ru/contacts/{region}?tab=clients"
        self.driver.get(new_region)
        return new_region

    def check_region(self, region):
        """Метод проверки региона"""
        region_element = self.find_region_element()
        if region_element.text == region:
            print(f"регион успешно изменён! на {region}")
            return region_element
        else:
            print("Регион не поменялся, что-то пошло не так!")
            return False

    def check_list_partners(self, id):
        """Проверка присутствия на странице списка партнёров"""
        partners = self.driver.find_element(By.ID, id)
        return partners

    def check_additional_element(self):
        """Дополнительная проверка при изменении региона (пусть будет...)"""
        return self.driver.find_element(
            By.XPATH, "//div[contains(text(), 'Петропавловск-Камчатский')]"
        )

    def download_file(self, download_url):
        """Метод загрузки файлов"""
        download_folder = "downloads"

        if not os.path.exists(download_folder):
            os.makedirs(download_folder)

        filename = os.path.join(download_folder, os.path.basename(download_url))

        try:
            response = requests.get(download_url)
            response.raise_for_status()

            with open(filename, "wb") as file:
                file.write(response.content)

                expected_size = 7.22
                actual_size = round(os.path.getsize(filename) / 1024 / 1024, 2)

                if actual_size == expected_size:
                    print(
                        f"Файл успешно скачан и размер в мегабайтах совпадает ({actual_size} Мбайт)."
                    )
                else:
                    print(
                        f"Внимание: размер файла ({actual_size} Мбайт) не совпадает с ожидаемым ({expected_size} Мбайт)."
                    )
        except requests.RequestException as e:
            print(
                f"Ошибка при запросе на скачивание, ссылка куда-то подевалась или проверьте введенные данные: {e}"
            )
