#-*- coding=utf-8 -*-
import pdb
import os.path
import requests as req
from bs4 import BeautifulSoup as bs
import time
import multiprocessing
import sys


# global
WEMAKEPRICE_1212 = 'https://front.wemakeprice.com/special/5000214'
SUCCESS_FILE = "success.txt"

def is_my_product(product_desc):
    product_desc = product_desc.upper()
    if '뿌링클' in product_desc or \
        'BHC' in product_desc:
        return True
    return False

def open_my_product_link():
    res = req.get(WEMAKEPRICE_1212)
    if not res.ok:
        print("[Error] reason: %s" + res.reason.encode("utf-8"))
        return

    html = bs(res.text, 'html.parser')
    product = html.find_all('div', {'class': 'box_imagedeal type4'})[0]
    a_tags = product.find_all('a', recursive=False)
    for num, a_tag in enumerate(a_tags[:10], 1):
        if os.path.exists(SUCCESS_FILE):
            print("[Sub Process] Already Open MyProduct url(1). So, Exit subprocess")
            return

        product_link = a_tag.attrs['href']
        if not a_tag.attrs['href'].startswith("http"):
            product_link = "https:" + a_tag.attrs['href']

        product_desc = a_tag.find('p', {'class': 'text'}).text
        if is_my_product(product_desc):
            print("********* {no}: {link}, {desc}".format(no=str(num).zfill(2), link=product_link, desc=product_desc))
            if os.path.exists(SUCCESS_FILE):
                print("[Sub Process] Already Open MyProduct url(2). So, Exit subprocess")
                return
            with open(SUCCESS_FILE, "w") as f:
                print("---> Find it. URL: %s" % product_link)
                f.write(product_link)
                return
        else:
            print("{no}: {link}, {desc}".format(no=str(num).zfill(2), link=product_link, desc=product_desc))
    print("Not Found Your Product... Exit Subprocess")


def main():
    if os.path.exists(SUCCESS_FILE):
        os.remove(SUCCESS_FILE)

    # try to connecto product url. limited by 50
    for _ in range(50):
        if os.path.exists(SUCCESS_FILE):
            with open(SUCCESS_FILE) as f:
                product_link = f.read().strip()
                print("Open My Product URL: %s" % product_link)
            print("[Main Process] Open MyProduct success. program exit.")
            sys.exit(0)
        p = multiprocessing.Process(target=open_my_product_link)
        print("\n\n\n'Find MyProduct' Process Start !!!")
        p.start()
        time.sleep(0.5)

if __name__ == "__main__":
    main()