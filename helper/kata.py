from bs4 import BeautifulSoup


class Kata:
    def __init__(self, soup):
        self.soup = soup

    def source_codes(self):
        codes = self.soup.find_all('div', {'class': 'markdown'})
        return [''.join(code.findAll(text=True)) for code in codes]

    def language_names(self):
        languages = self.soup.find_all('h6')
        return [language.text.rstrip(':') for language in languages]

    def language_ids(self):
        languages = self.soup.find_all('code')
        return [language['data-language'] for language in languages]

    def times(self):
        times = self.soup.find_all('time')
        return [time['datetime'] for time in times]

    def difficulty(self):
        difficulty = self.soup.find('div', {'class': 'item-title'}).find('span').text
        return difficulty.replace(' ', '-').lower()

    def name(self):
        name = self.soup.find('div', {'class': 'item-title'}).find('a').text
        return name

    def kata_id(self):
        href = self.soup.find('div', {'class': 'item-title'}).find('a')['href']
        return href.split('/')[-1]


class KataParser:
    def __init__(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        self.elems = soup.find_all('div', {'class': 'list-item solutions'})

    def parse_katas(self):
        return [Kata(elem) for elem in self.elems]
