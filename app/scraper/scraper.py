from typing import List
from ..encryption import decrypt
from . import schemas
from selenium import webdriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time

def login(web, user: schemas.User):
    web.get('https://www.bolha.com/prijava/')
    time.sleep(0.25)

    cookies = web.find_element(
        'xpath', '//*[@id="didomi-notice-agree-button"]')
    cookies.click()

    user_name = web.find_element('xpath', '//*[@id="login_username"]')
    user_name.send_keys(user.user_name)

    bolha_password = decrypt(user.bolha_password)

    password = web.find_element('xpath', '//*[@id="login_password"]')
    password.send_keys(bolha_password)

    login = web.find_element('xpath', '//*[@id="login_login"]')
    login.click()

def add_ad(ad: schemas.Ad, user: schemas.User):
    web = webdriver.Chrome(ChromeDriverManager().install())
    login(web, user)

    web.get('https://www.bolha.com/objava-oglasa/')
    time.sleep(0.25)

    category = ad.category.split('.')
    row = web.find_elements(
        'xpath', '//*[@id="adCategorySelectorForm"]/div[3]/div[1]/ul/li')[int(category[0])-1]
    row.click()
    for c in category[1:]:
        row = row.find_elements('tag name', 'li')[int(c)-1]
        row.click()
    
    go = web.find_element(
        'xpath', '//*[@id="adCategorySelectorForm"]/div[3]/div[2]/div/div[1]/button')
    go.click()
    time.sleep(0.25)

    title = web.find_element('xpath', '//*[@id="ad-title"]')
    title.send_keys(ad.title)

    content = web.find_element('xpath', '//*[@id="ad-description"]')
    content.send_keys(ad.content)

    if ad.price == None:
        as_agreed = web.find_element(
            'xpath', '// *[ @ id = "ad-price-priceOnRequest"]')
        as_agreed.click()
    else:
        price = web.find_element('xpath', '//*[@id="ad-price-amount"]')
        price.send_keys(ad.price)

    post = web.find_element('xpath', '// *[ @ id = "ad-submitButton"]')
    post.click()

    web.get('https://www.bolha.com/moja-bolha/uporabnik/moji-oglasi/aktivni-oglasi')
    time.sleep(0.25)

    bolha_id = web.find_element(
        'class name', 'UserEntityInfoMetaList-item--adId')
    bolha_id = bolha_id.find_element('tag name', 'strong')
    return bolha_id.text
    
def remove(bolha_id: str, user: schemas.User):
    web = webdriver.Chrome(ChromeDriverManager().install())
    login(web, user)
    web.get('https://www.bolha.com/moja-bolha/uporabnik/moji-oglasi/aktivni-oglasi')

    select = web.find_element("id", f"ad_{bolha_id}")
    select.click()
    delete = web.find_element(
        "class name", "UserEntityListMassActions-item--delete")
    delete.click()
    time.sleep(.1)
    confirm = web.find_element(
        "class name", "ModalDialog-action--confirm")
    confirm.click()

def update(ad: schemas.UpdateAd, user: schemas.User):
    remove(ad.bolha_id, user)
    bolha_id = add_ad(ad, user)
    return bolha_id

def positions(ad_ids: List[str], user: schemas.User):
    web = webdriver.Chrome(ChromeDriverManager().install())
    login(web, user)
    web.get('https://www.bolha.com/moja-bolha/uporabnik/moji-oglasi/aktivni-oglasi')
    # wait for page to load
    time.sleep(.25)
    # getting to the element with information about my add position
    positions = []
    for ad_id in ad_ids:
        grandparent = web.find_element(
            'class name', 'UserEntityListItem--' + ad_id)
        parent = grandparent.find_elements(
            'class name', 'UserEntityOptions-textWrapper')[1]
        n = parent.find_elements('tag name', 'p')[1]
        numbers = n.find_element('tag name', 'strong')
        # converting first element of the string (position of the add) to integer
        number = int(float(numbers.text[0:2]))
        positions.append(number)
    return positions

def position(ad_id: str, user:schemas.User):
    web = webdriver.Chrome(ChromeDriverManager().install())
    login(web, user)
    web.get('https://www.bolha.com/moja-bolha/uporabnik/moji-oglasi/aktivni-oglasi')
    # wait for page to load
    time.sleep(.25)
    # getting to the element with information about my add position

    grandparent = web.find_element(
        'class name', 'UserEntityListItem--' + ad_id)
    parent = grandparent.find_elements(
        'class name', 'UserEntityOptions-textWrapper')[1]
    n = parent.find_elements('tag name', 'p')[1]
    numbers = n.find_element('tag name', 'strong')
    # converting first element of the string (position of the add) to integer
    position = int(float(numbers.text[0:2]))

    return position