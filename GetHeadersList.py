import html

import requests
from bs4 import BeautifulSoup



def get_headers():
    url = "https://en.cppreference.com/w/c/header.html"
    # 发起请求并获取页面内容
    response = requests.get(url)
    response.raise_for_status()  # 确保请求成功
    soup = BeautifulSoup(response.text, "html.parser")

    # 查找tr标签，并且class为t-dsc
    tr_tags = soup.find_all("tr", class_="t-dsc")

    header_names = []
    for tr in tr_tags:
        first_td = tr.find("td")
        if not first_td:
            continue
        member_div = first_td.find("div", class_="t-dsc-member-div")
        if not member_div:
            continue

        # 定位第一个子div
        header_div = member_div.find("div")
        if not header_div:
            continue

        header_span = header_div.find("span", class_="t-lines")
        if header_span:
            inner_span = header_span.find("span")
            if inner_span:
                header_text = html.unescape(inner_span.get_text())
                clean_header = header_text.strip().strip("<>").strip()
                header_names.append(clean_header)

    print(header_names)
    return header_names
