import requests
import bs4
import fake_headers
import lxml
import json

LINK = r'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
result = []

def get_html(url):
    headers = fake_headers.Headers(headers=True, os='win', browser='chrome').generate()
    response = requests.get(url, headers=headers)
    return response.text



def parse_data(html):
    soup = bs4.BeautifulSoup(html, 'lxml')
    vacancies = soup.find_all('div', class_='serp-item')
    for vacancy in vacancies:
        title = vacancy.find('a').text
        try:
            salary = vacancy.find('span', class_='bloko-header-section-3').text
        except:
            salary = 'Зарплата не указана'
        link_to_vacancy = vacancy.find('a').get('href')

        company = vacancy.find('a', class_='bloko-link bloko-link_kind-tertiary').text

        city = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-address', 'class': 'bloko-text'}).text

        result.append({
            'title': title,
            'link_to_vacancy': link_to_vacancy,
            'salary': salary,
            'company': company,
            'city': city
            })
    return result

def main():
    with open('data.json', 'w', encoding='utf-8') as file:
        json.dump(parse_data(get_html(LINK)), file, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    main()
    print('Готово!\n')