from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
import selenium

from bs4 import BeautifulSoup
import pdb
import pickle
import time
import os.path


# global
WEMAKEPRICE_1212 = 'https://front.wemakeprice.com/special/5000214'
SUCCESS_FILE = "success.txt"
use_user_data = True
driver = None

def init_chrome_driver():
    print("Chrome Driver 초기화..")
    global driver
    if use_user_data:
        chrome_options = ChromeOptions()
        chrome_options.add_argument("user-data-dir=selenium")
        driver = webdriver.Chrome('D:\chromedriver', chrome_options=chrome_options)
    else:
        driver = webdriver.Chrome('D:\chromedriver')
    driver.implicitly_wait(3)

def login_check():
    print("Login 확인..")
    driver.get("https://front.wemakeprice.com/mypage/verify")
    time.sleep(0.5)
    driver.get("https://front.wemakeprice.com/mypage/verify")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    if need_login():
        login()
    pdb.set_trace()

def open_product_order_page(test=False):
    print("제품 페이지로 이동..")
    if test:
        driver.get("https://front.wemakeprice.com/product/132254617")
        return

    # jump to product order page (example)
    while True:
        if not os.path.exists(SUCCESS_FILE):
            print("Waiting...")
            time.sleep(0.2)
            continue

        with open(SUCCESS_FILE) as f:
            product_url = f.read().strip()
            driver.get(product_url)
            break


def set_option():
    print("제품 옵션 설정..")
    # 구매하기 버튼 클릭
    try:
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        product_select = soup.select("#_itemSelbox")
        option_select = soup.select("#_optionSelbox")

        if bool(product_select):
            # 옵션이 있으면, 품절이 아닌 첫번째 옵션을 그냥 선택하여 진행
            # open option menu
            driver.find_element_by_css_selector("#_itemSelbox > a").send_keys(Keys.ENTER)
            time.sleep(0.5)

            # soldout 이 아닌 첫번째 옵션을 선택
            driver.find_element_by_css_selector("#_itemSelbox .item_option a:not(.soldout)").send_keys(Keys.ENTER)
            time.sleep(0.5)

            # check if open option list box or not
            option_select = soup.select("#_optionSelbox")

            if bool(option_select):
                driver.find_element_by_css_selector("#_optionSelbox .ui_option_list a:not(.soldout)").send_keys(Keys.ENTER)
                time.sleep(0.5)

        elif bool(option_select):
            # 옵션이 있으면, 품절이 아닌 첫번째 옵션을 그냥 선택하여 진행
            # open option menu
            driver.find_element_by_css_selector("#_optionSelbox > a").send_keys(Keys.ENTER)
            time.sleep(0.5)

            # soldout 이 아닌 첫번째 옵션을 선택
            driver.find_element_by_css_selector("#_optionSelbox .ui_option_list a:not(.soldout)").send_keys(Keys.ENTER)
            time.sleep(0.5)

        # 구매하기 버튼 클릭
        req_order = driver.find_element_by_css_selector(".info_product.wrap_button > .button_box > .btn_sys.red_big_xb.buy")
        req_order.send_keys(Keys.ENTER)
        time.sleep(0.5)
    except NoSuchElementException as e:
        print(e)
        ret = input("[긴급] 구매하기 버튼을 직접 클릭한 후, Enter를 눌러주세요")
    pdb.set_trace()

def configure_my_payment():
    print("결제 옵션 설정..")
    # 간편결제 버튼이 보이는 곳까지 스크롤.. 이거 안하면, click 정상동작 안함
    driver.execute_script("window.scrollTo(0, 1000)")

    # 간편결제 클릭
    btn = driver.find_element_by_id("onSelectEasy")
    btn.click()
    time.sleep(0.5)

    # 페이코 선택 클릭
    pay_list = driver.find_element_by_css_selector("#easySelect > li:nth-child(3) > a")
    pay_list.click()
    time.sleep(0.5)

    # 구매 및 결제대행서비스 이용약관 등에 모두 동의합니다. -> Click
    agree_checkbox = driver.find_element_by_id("orderConditions")
    agree_checkbox.click()
    time.sleep(0.5)


def send_order():
    print("구매버튼 클릭..")
    # 구매버튼 클릭
    req_pay = driver.find_element_by_id("btnPaymentSubmit").click()
    req_pay.click()
    time.sleep(0.5)
    print("결제화면으로 전환")
    #pdb.set_trace()
    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[starts-with(@src, 'http://thunder/spidio.net/CF9F4DA6B7533431/devinfo/devdect')]")))
    #WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//iframe[starts-with()]")))

def payment_process():
    print("결제 프로세스 진행..")
    # driver.switch_to.frame(driver.find_element_by_css_selector("iframe"))
    # or
    # 결제 iframe 으로 전환
    #pdb.set_trace()
    driver.switch_to.frame(driver.find_element_by_css_selector("#pgframe"))
    # driver.find_element_by_css_selector("#NAX_BLOCK")

    # iframe 안으로 진입
    driver.switch_to.frame(driver.find_element_by_css_selector("#naxIfr"))

    # iframe 안으로 진입
    driver.switch_to.frame(driver.find_element_by_css_selector("#kcpPaycoIframe"))

    # confirm 버튼 클릭
    driver.find_element_by_css_selector(".confirmByPgCd").click()

    # 결제버튼 클릭
    driver.find_element_by_css_selector(".btn_pay").click()

def input_passwd():
    print("비밀번호 입력..")
    print("\n\n[!] 비밀번호는 직접 입력하세요... Program Exit")
    # 비밀번호 화면...등장
    # 비밀번호 입력 iframe 으로 전환
    # driver.switch_to.frame(driver.find_element_by_css_selector(".ly_payment.iframe iframe"))
    #
    # table = {
    #     0: "#A_35C",
    #     1: "#A_3F5",
    #     2: "#A_29C",
    #     3: '#A_267',
    #     4: "#A_128",
    #     5: "#A_4d7",
    #     6: "#A_879",
    #     7: "#A_D63",
    #     8: "#A_EC7",
    #     9: "#A_91E"
    # }
    # my_passwd = [1, 2, 1, 5, 7, 7]
    # my_passwd2 = list(map(lambda x: table[x], my_passwd))
    #
    # pdb.set_trace()
    # for num_id in my_passwd2:
    #     driver.find_element_by_css_selector(num_id).click()
    #     time.sleep(0.5)


def main():
    init_chrome_driver()
    login_check()
    # open_product_order_page(test=True)
    open_product_order_page()
    set_option()
    configure_my_payment()
    send_order()
    payment_process()
    input_passwd()


if __name__ == "__main__":
    main()