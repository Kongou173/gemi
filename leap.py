import bs4
import requests


def get_words(part = None):
    url = 'https://ukaru-eigo.com/leap-word-list/'
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')

    def parse(elem):
        index_elem, en_elem, ja_elem = list(elem.children)[1:-1]
        index = int(index_elem.text)
        en = en_elem.text
        ja = ja_elem.text
        return index, en, ja

    def get_part(index: int) -> int:
        if index < 401:
            part = 1
        elif 401 <= index < 1001:
            part = 2
        elif 1001 <= index < 1401:
            part = 3
        else:
            part = 4
        return part

    words = []

    for w in soup.find(attrs={'class': 'row-hover'}).children:
        if not isinstance(w, bs4.element.Tag):
            continue
        index, en, ja = parse(w)
        if part is not None and get_part(index) != part:
            continue
        words.append({'en': en, 'ja': ja})

    return words


for i in [1, 2, 3, 4]:
    words = get_words(i)

    csv_file_path = f'part{i}.csv'
    import csv

    # JSONデータをCSVファイルに書き込む
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=words[0].keys())
        writer.writeheader()
        writer.writerows(words)
