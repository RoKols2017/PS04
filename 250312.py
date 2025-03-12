from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

class Browser:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")  # Включение headless-режима
        chrome_options.add_argument("--disable-gpu")   # Отключение использования GPU
        chrome_options.add_argument("--no-sandbox")    # Отключение песочницы
        chrome_options.add_argument("--disable-dev-shm-usage")  # Отключение использования /dev/shm
        self.driver = webdriver.Chrome(service=Service(), options=chrome_options)

    def open_page(self, url):
        self.driver.get(url)

    def find_element(self, by, value):
        return self.driver.find_element(by, value)

    def find_elements(self, by, value):
        return self.driver.find_elements(by, value)

    def quit(self):
        self.driver.quit()

class WikipediaNavigator:
    BASE_URL = "https://ru.wikipedia.org/wiki/"

    def __init__(self, browser):
        self.browser = browser

    def search(self, query):
        search_url = self.BASE_URL + query.replace(' ', '_')
        self.browser.open_page(search_url)

    def get_paragraphs(self):
        paragraphs = self.browser.find_elements(By.TAG_NAME, "p")
        return [p.text for p in paragraphs if p.text.strip()]

    def get_internal_links(self):
        links = self.browser.find_elements(By.XPATH, "//div[@id='bodyContent']//a[starts-with(@href, '/wiki/') and not(contains(@href, ':'))]")
        return {link.text: link.get_attribute('href') for link in links if link.text.strip()}

class WikipediaConsoleApp:
    def __init__(self):
        self.browser = Browser()
        self.navigator = WikipediaNavigator(self.browser)

    def run(self):
        try:
            self.main_menu()
        finally:
            self.browser.quit()

    def main_menu(self):
        query = input("Введите запрос для поиска на Википедии: ")
        self.navigator.search(query)
        while True:
            print("\nВыберите действие:")
            print("1. Читать параграфы текущей статьи")
            print("2. Перейти на связанную страницу")
            print("3. Выйти из программы")
            choice = input("Ваш выбор (1/2/3): ")
            if choice == '1':
                self.read_paragraphs()
            elif choice == '2':
                self.navigate_to_link()
            elif choice == '3':
                print("Выход из программы.")
                break
            else:
                print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")

    def read_paragraphs(self):
        paragraphs = self.navigator.get_paragraphs()
        for i, paragraph in enumerate(paragraphs):
            print(f"\nПараграф {i + 1}:\n{paragraph}")
            cont = input("\nНажмите Enter для продолжения или введите 'q' для выхода: ")
            if cont.lower() == 'q':
                break

    def navigate_to_link(self):
        links = self.navigator.get_internal_links()
        if not links:
            print("Связанных страниц не найдено.")
            return
        print("\nСвязанные страницы:")
        for i, (text, url) in enumerate(links.items()):
            print(f"{i + 1}. {text} ({url})")
        try:
            choice = int(input("Введите номер страницы для перехода или 0 для отмены: "))
            if choice == 0:
                return
            selected_link = list(links.values())[choice - 1]
            self.browser.open_page(selected_link)
            print(f"Перешли на страницу: {selected_link}")
        except (ValueError, IndexError):
            print("Неверный выбор. Пожалуйста, введите корректный номер.")

if __name__ == "__main__":
    app = WikipediaConsoleApp()
    app.run()
