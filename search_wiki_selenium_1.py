from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
import textwrap


def initialize_driver():
    """Инициализация Selenium WebDriver с режимом headless (без интерфейса)."""
    options = Options()
    options.add_argument("--headless")  # Запуск без графического интерфейса
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    return webdriver.Chrome(options=options)


def get_wikipedia_article(driver, query):
    """Открывает статью на Википедии по запросу пользователя."""
    url = "https://ru.wikipedia.org/wiki/" + query.replace(" ", "_")
    driver.get(url)

    # Вместо time.sleep() используем WebDriverWait, чтобы дождаться загрузки страницы
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "bodyContent")))
    except:
        print("Ошибка: страница не загрузилась.")  # Обрабатываем ошибку загрузки
    return url


def list_paragraphs(driver):
    """Выводит параграфы статьи по одному с возможностью пролистывания."""
    paragraphs = driver.find_elements(By.TAG_NAME, "p")
    wrapper = textwrap.TextWrapper(width=80)  # Ограничиваем ширину строки для удобного чтения

    for i, paragraph in enumerate(paragraphs):
        text = paragraph.text.strip()
        if not text:
            continue  # Пропускаем пустые параграфы

        print(f"\n🔥 Параграф {i + 1}:\n" + "\n".join(wrapper.wrap(text)))  # Выводим отформатированный текст

        # Предлагаем пользователю продолжить чтение или выйти
        cont = input("\nПоказать следующий параграф? (да/нет): ").strip().lower()
        if cont != "да":
            break


def list_internal_links(driver):
    """Собирает список внутренних ссылок на другие статьи Википедии."""
    links = driver.find_elements(By.XPATH, "//div[@id='bodyContent']//a[@href]")
    internal_links = {}

    current_url = driver.current_url
    current_path = urlparse(current_url).path  # Получаем путь текущей статьи

    print("\n🔗 Связанные страницы:")
    count = 1
    for link in links:
        href = link.get_attribute("href")
        title = link.get_attribute("title")  # Используем title, т.к. он более информативный

        if href and "wikipedia.org/wiki/" in href and ":" not in href:
            # Исключаем ссылки на текущую статью
            if urlparse(href).path != current_path:
                if title and title not in internal_links.values():
                    internal_links[count] = title
                    print(f"{count}. {title}")
                    count += 1
                    if count > 10:  # Ограничение на 10 ссылок для удобства
                        break

    return internal_links


def choose_link_and_navigate(driver, links):
    """Позволяет пользователю выбрать ссылку и перейти на новую статью."""
    while True:
        try:
            link_choice = int(input("\nВведите номер страницы для перехода: ").strip())
            if link_choice in links:
                get_wikipedia_article(driver, links[link_choice])
                break  # Успешный переход - выходим из цикла
            else:
                print("🚨 Некорректный номер. Попробуйте снова.")
        except ValueError:
            print("⚠ Ошибка ввода! Введите число.")  # Предотвращаем падение программы


def main():
    """Основной цикл работы программы."""
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
                    choose_link_and_navigate(driver, links)
                else:
                    print("Нет доступных ссылок.")
            elif choice == "3":
                print("Выход из программы.")
                break
            else:
                print("Некорректный ввод. Попробуйте снова.")
    finally:
        driver.quit()  # Корректно закрываем браузер при выходе


if __name__ == "__main__":
    main()
