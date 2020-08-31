import requests
from bs4 import BeautifulSoup
import json

url="https://www.goodreads.com/"

response = requests.get("https://www.goodreads.com/author/list/4634532.Nguy_n_Nh_t_nh?page=" + str(1) + "&per_page=30")
soup = BeautifulSoup(response.content, "html.parser")
titles = soup.findAll('a', class_='bookTitle')
i = 1

list_book = []
while (titles != []):
    for link in titles:
        book = {}
        book["title"] = link.find('span').text
        print(book["title"])
        book["link"] = link.attrs["href"]
        book["id"] = book["link"].split("/")[-1].split("-")[0]

        response_book = requests.get(url + book["link"] + "?page=1")
        soup_book = BeautifulSoup(response_book.content, "html.parser")

        book["author"] = [author.text.strip() for author in soup_book.findAll('a', class_='authorName')]
        book["rate"] = soup_book.find('span', itemprop='ratingValue').text.strip()
        discription = soup_book.find('div', id='description')
        if (discription != None):
            book["description"] = discription.findAll('span')[-1].text.strip()
        else:
            book["description"] = ""

        ######### GET REVIEW #########

        review_blocks = soup_book.findAll('div', class_='friendReviews elementListBrown')

        list_review = []
        j = 1
        while (review_blocks != []):
            print(j)
            for review_block in review_blocks:
                review = {}
                author = review_block.find("a", class_="user")
                review["id"] = author.attrs['href'][11:].split('-')[0]
                review["name"] = author.attrs['name']
                rate = review_block.find("span", class_="staticStars notranslate")
                if (rate != None):
                    review["rate"] = len(rate.findAll("span", class_="staticStar p10"))
                else:
                    review["rate"] = None
                review["date"] = review_block.find("a", class_="reviewDate createdAt right").text.strip()
                review["content"] = review_block.find("div", class_="reviewText stacked").findAll("span")[
                    -1].text.strip()

                ######### GET LIST COMMENTS OF REVIEW #########

                link_cmt = review_block.find("div", class_="updateActionLinks").findAll("a")[-1].attrs["href"]
                response_cmt = requests.get(url + link_cmt)
                soup_cmt = BeautifulSoup(response_cmt.content, "html.parser")

                list_cmt = []
                cmts = soup_cmt.findAll('div', class_="comment u-anchorTarget")
                for cmt in cmts:
                    js_cmt = {}
                    author_cmt = cmt.find("span", class_="commentAuthor")
                    js_cmt["name"] = author_cmt.text.strip()
                    js_cmt["id"] = author_cmt.find('a').attrs["href"].split("/")[-1].split("-")[0]
                    js_cmt["date"] = cmt.find("div", class_="right").text.strip()
                    js_cmt["cmt"] = cmt.find("div", class_="mediumText reviewText").text.strip()
                    list_cmt.append(js_cmt)
                review["list_cmt"] = list_cmt
                list_review.append(review)

            j += 1
            response_book = requests.get(url + book["link"] + "?page=" + str(j))
            soup_book = BeautifulSoup(response_book.content, "html.parser")
            review_blocks = soup_book.findAll('div', class_='friendReviews elementListBrown')
        book["review"] = list_review

        list_book.append(book)
    i += 1
    response = requests.get(
        "https://www.goodreads.com/author/list/4634532.Nguy_n_Nh_t_nh?page=" + str(i) + "&per_page=30")
    soup = BeautifulSoup(response.content, "html.parser")
    titles = soup.findAll('a', class_='bookTitle')

with open('data.json', 'w', encoding='utf8') as json_file:
    json.dump(list_book, json_file, ensure_ascii=False)