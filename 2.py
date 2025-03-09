from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


def initialize_driver():
    options = Options()
    options.add_argument("--headless")  # Запуск без интерфейса
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(options=options)  # Selenium Manager автоматически управляет драйвером


def get_wikipedia_article(driver, query):
    url = "https://ru.wikipedia.org/wiki/" + query.replace(" ", "_")
    driver.get(url)
    time.sleep(2)
    return url


def list_paragraphs(driver):
    paragraphs = driver.find_elements(By.TAG_NAME, "p")
    for i, paragraph in enumerate(paragraphs):
        text = paragraph.text.strip()
        if text:
            print(f"Параграф {i + 1}: {text[:500]}...")
            cont = input("Показать следующий параграф? (да/нет): ").strip().lower()
            if cont != "да":
                break


def list_internal_links(driver):
    links = driver.find_elements(By.XPATH, "//div[@id='bodyContent']//a[@href]")
    internal_links = {}

    print("Связанные страницы:")
    count = 1
    for link in links:
        href = link.get_attribute("href")
        title = link.text.strip()
        if href and "wikipedia.org/wiki/" in href and ":" not in href and title:
            if title not in internal_links.values():
                internal_links[count] = title
                print(f"{count}. {title}")
                count += 1
                if count > 10:
                    break
    return internal_links


def main():
    driver = initialize_driver()
    try:
        query = input("Введите поисковый запрос: ").strip()
        get_wikipedia_article(driver, query)

        while True:
            print("\nВыберите действие:")
            print("1. Листать параграфы текущей статьи")
            print("2. Перейти на одну из связанных страниц")
            print("3. Выйти")

            choice = input("Введите номер действия: ").strip()

            if choice == "1":
                list_paragraphs(driver)
            elif choice == "2":
                links = list_internal_links(driver)
                if links:
                    try:
                        link_choice = int(input("Введите номер страницы для перехода: ").strip())
                        if link_choice in links:
                            get_wikipedia_article(driver, links[link_choice])
                        else:
                            print("Некорректный номер. Попробуйте снова.")
                    except ValueError:
                        print("Ошибка ввода. Введите число.")
                else:
                    print("Нет доступных ссылок.")
            elif choice == "3":
                print("Выход из программы.")
                break
            else:
                print("Некорректный ввод. Попробуйте снова.")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()

