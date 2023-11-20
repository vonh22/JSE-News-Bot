import requests
from bs4 import BeautifulSoup as bs
import gspread

gc = gspread.service_account(filename='')

sheet = gc.open('NewsProject')
worksheet = sheet.worksheet('JSENews')


def get_articles():
    r = requests.get("https://www.jamstockex.com/news/")
    soup = bs(r.content, "html.parser")
    articles = soup.find_all("article")

    url_list = []
    for article in articles:
        a_tag = article.find('a', href=True)
        title, URL = a_tag.text, a_tag['href']

        url_list.append(URL)

    return url_list


def get_jse_news_articles():
    url_list = worksheet.col_values(1)
    last_row_index = len(url_list) + 1
    current_urls = get_articles()
    new_urls = []
    updates = []
    for url in current_urls:
        if url not in url_list:
            cell_address_url = f'A{last_row_index}'
            updates.append({'range': cell_address_url, 'values': [[url]]})
            new_urls.append(url)
            last_row_index += 1

    if new_urls:
        worksheet.batch_update(updates)

    return new_urls


def find_old_articles(oldlist, newlist):
    url_indexes = []
    length_of_list = len(oldlist)
    for i in range(1, length_of_list):
        if oldlist[i] not in newlist:
            url_indexes.append(i+1)
    return url_indexes


def maintenance():
    url_list = worksheet.col_values(1)
    new_urls = get_articles()
    indexes = find_old_articles(url_list, new_urls)
    indexes.sort(reverse=True)
    for index in indexes:
        worksheet.delete_row(index)


