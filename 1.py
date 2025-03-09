import wikipediaapi

# Указываем корректный User-Agent
USER_AGENT = "MyWikiSearcher/1.0 (contact: your-email@example.com)"


def get_wiki_page(title, lang="ru"):
    wiki = wikipediaapi.Wikipedia(language=lang, user_agent=USER_AGENT)
    page = wiki.page(title)
    if not page.exists():
        print(f"Статья '{title}' не найдена.")
        return None
    return page


def display_paragraphs(page):
    paragraphs = page.text.split("\n")
    for i, paragraph in enumerate(paragraphs):
        if paragraph.strip():
            input("Нажмите Enter для продолжения...")
            print(f"\nПараграф {i + 1}:\n{paragraph}")


def list_links(page):
    links = list(page.links.keys())
    if not links:
        print("Нет связанных статей.")
        return None
    print("\nСвязанные статьи:")
    for i, link in enumerate(links[:10], 1):
        print(f"{i}. {link}")
    return links


def main():
    lang = "ru"
    query = input("Введите запрос для поиска на Википедии: ")
    page = get_wiki_page(query, lang)

    if not page:
        return

    while True:
        print("\nВыберите действие:")
        print("1. Листать параграфы текущей статьи")
        print("2. Перейти на связанную страницу")
        print("3. Выйти из программы")

        choice = input("Введите номер действия: ")

        if choice == "1":
            display_paragraphs(page)
        elif choice == "2":
            links = list_links(page)
            if links:
                link_choice = input("Введите номер связанной статьи или 'назад': ")
                if link_choice.isdigit() and 1 <= int(link_choice) <= len(links):
                    page = get_wiki_page(links[int(link_choice) - 1], lang)
                    if not page:
                        continue
                elif link_choice.lower() == "назад":
                    continue
                else:
                    print("Неверный ввод.")
        elif choice == "3":
            print("Выход из программы.")
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")


if __name__ == "__main__":
    main()
