import time
import requests
from parsel import Selector
from database import create


BASE_URL = "https://sample-university-site.herokuapp.com"


def is_valid_page(url):
    try:
        r = requests.get(url, timeout=3)
        time.sleep(1)
        if r.text == "Invalid page.":
            return False
        else:
            return True
    except requests.ReadTimeout:
        print("Alguma coisa deu errado no acesso a url")


def fetch(url):
    try:
        response = requests.get(url, timeout=3)
        time.sleep(1)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except requests.ReadTimeout:
        print("Alguma coisa deu errado no acesso a url")


def scrape_details(html_content, url):
    selector = Selector(text=html_content)
    cpf = url[-14:]
    name = selector.css("body > div:nth-child(2)::text").get()
    score = selector.css("body > div:nth-child(3)::text").get()
    return {
        "cpf": cpf,
        "name": name,
        "score": score,
    }


def get_candidate_url(link):
    url = BASE_URL + link
    return url


def scrape_url_approvals(html_content):
    selector = Selector(text=html_content)
    if selector:
        link_list = selector.css(
            "body > li > a::attr(href)"
            ).getall()
        url_list = [
            get_candidate_url(link) for link in link_list
        ]
        return url_list
    else:
        return []


def scrape_next_page_url(html_content):
    selector = Selector(text=html_content)
    link = selector.css("body > div > a::attr(href)").get()
    if link:
        return BASE_URL + link
    else:
        return None


def get_data(amount):
    url = BASE_URL
    url_approvals_list = []
    while len(url_approvals_list) < amount:
        html_content = fetch(url)
        url_approvals = scrape_url_approvals(html_content)
        url_approvals_list.extend(url_approvals)
        url = scrape_next_page_url(html_content)

    url_approvals_list = url_approvals_list[0:amount]
    data = [
        scrape_details(fetch(url), url) for url in url_approvals_list
    ]
    create(data)
    return "Dados foram salvos no MongoDB"


def get_all_data():
    url = BASE_URL
    url_approvals_list = []
    status = True
    while status:
        html_content = fetch(url)
        url_approvals = scrape_url_approvals(html_content)
        url_approvals_list.extend(url_approvals)
        url = scrape_next_page_url(html_content)
        status = is_valid_page(url)
    data = [
        scrape_details(fetch(url), url) for url in url_approvals_list
    ]
    create(data)
    return "Dados foram salvos no MongoDB"
