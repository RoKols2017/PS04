import wikipediaapi
import textwrap

# Указываем корректный User-Agent
USER_AGENT = "MyWikiSearcher/1.0 (contact: your-email@example.com)"


def get_wiki_page(title, lang="ru"):
    """Запрашивает статью из Википедии и обрабатывает ошибки."""
    wiki = wikipediaapi.Wikipedia(language=lang, user_agent=USER_AGENT)
    
    while True:
        page = wiki.page(title)
        if page.exists():
            return page  # Если статья найдена – возвращаем её
        
        print(f"🚨 Ошибка: Статья '{title}' не найдена.")
        title = input("Введите другой запрос или 'выход' для выхода: ").strip()
        if title.lower() == "выход":
            return None


def display_paragraphs(page):
    """Выводит текст статьи по абзацам, ожидая нажатия Enter перед каждым."""
    wrapper = textwrap.TextWrapper(width=80)

    paragraphs = [p.strip() for p in page.text.split("\n") if p.strip()]
    for i, paragraph in enumerate(paragraphs, 1):
        input(f"\n🔹 Параграф {i} (Нажмите Enter для продолжения)...")
        print("\n".join(wrapper.wrap(paragraph)))  # Форматируем текст


def list_links(page):
    """Выводит список связанных страниц, удаляя дубликаты."""
    links = list(set(page.links.keys()))
    if not links:
        print("Нет связанных статей.")
        return None

    print("\n🔗 Связанные статьи:")
    for i, link in enumerate(links[:10], 1):
        print(f"{i}. {link}")
    return links[:10]  # Ограничение 10 ссылок


def choose_link(links):
    """Позволяет выбрать связанную статью и обрабатывает ошибки ввода."""
    while True:
        link_choice = input("Введите номер связанной статьи или 'назад': ").strip().lower()
        if link_choice == "назад":
            return None
        if link_choice.isdigit():
            link_choice = int(link_choice)
            if 1 <= link_choice <= len(links):
                return links[link_choice - 1]
        print("🚨 Ошибка: Введите корректный номер или 'назад'.")


def main():
    lang = "ru"
    query = input("Введите запрос для поиска на Википедии: ")
    page = get_wiki_page(query, lang)

    if not page:
        return

    while True:
        choice = input("\n1. Листать параграфы\n2. Перейти на связанную страницу\n3. Выйти\nВыбор: ")
        if choice == "1":
            display_paragraphs(page)
        elif choice == "2":
            links = list_links(page)
            if links:
                new_query = choose_link(links)
                if new_query:
                    page = get_wiki_page(new_query, lang)
        elif choice == "3":
            print("Выход.")
            break


if __name__ == "__main__":
    main()
