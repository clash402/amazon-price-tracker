from bs4 import BeautifulSoup
from decouple import config
import requests as req
import smtplib
import lxml


# PROPERTIES
URL_AMAZON = "https://www.amazon.com/Instant-Pot-Duo-Evo-Plus/dp/B07W55DDFB/ref=sr_1_1?qid=1597662463"
HEADERS = {
    "Accept-Language": "en-us",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) "
                  "Version/14.0 Safari/605.1.15"
}

MY_EMAIL = config("MY_EMAIL")
MY_EMAIL_PASSWORD = config("MY_EMAIL_PASSWORD")
RECEIVING_EMAIL = config("RECEIVING_EMAIL")
SMTP = config("SMTP")

PORT = 587

res = req.get(URL_AMAZON, headers=HEADERS)
res.raise_for_status()

soup = BeautifulSoup(res.content, "lxml")
product_title = soup.find(id="productTitle").get_text().strip()
product_price = float(soup.find(id="priceblock_ourprice").get_text().split("$")[1])

buy_price = 100


# MAIN
if product_price < buy_price:
    msg_subject = "Price Drop!"
    msg_body = f"{product_title}\n${product_price}\n{URL_AMAZON}"
    msg = f"Subject:{msg_subject}\n\n{msg_body}"

    print(msg)

    # with smtplib.SMTP(SMTP, port=PORT) as connection:
    #     connection.starttls()
    #     connection.login(user=MY_EMAIL, password=MY_EMAIL_PASSWORD)
    #     connection.sendmail(
    #         from_addr=MY_EMAIL,
    #         to_addrs=RECEIVING_EMAIL,
    #         msg=msg
    #     )
