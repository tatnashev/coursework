from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, JavascriptException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from TextClass import Text
import datetime as dt
import time


def get_data(data, date):
    option = Options()

    option.add_argument("--disable-infobars")
    option.add_argument("start-maximized")
    option.add_argument("--disable-extensions")

    # Pass the argument 1 to allow and 2 to block
    option.add_experimental_option("prefs", {
        "profile.default_content_setting_values.notifications": 1
    })

    PATH = 'C:\Program Files (x86)\chromedriver.exe'
    driver = webdriver.Chrome(options=option, executable_path=PATH)

    url = 'https://project1917.ru/posts/' + date.strftime("%d.%m.%y")

    driver.get(url)

    separator = None

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(13)

        try:
            separator = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "header-separator"))
            )
            break
        except TimeoutException:
            pass

    texts = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "lenta__post"))
    )

    for text in texts:
        driver.execute_script("arguments[0].scrollIntoView();", text)
        if text.location['x'] > separator.location['x'] and text.location['y'] > separator.location['y']:
            break

        author = ''
        try:
            author = text.find_element_by_class_name('footnote-popup--hero.post-author__link').text
        except NoSuchElementException:
            pass

        try:
            author = text.find_element_by_class_name('post-author__link').text
        except NoSuchElementException:
            continue

        message = text.find_element_by_class_name('lenta-post__text')

        try:
            read_more = message.find_element_by_class_name('lenta-post__more')
            driver.implicitly_wait(10)
            if read_more.get_attribute('href'):
                continue

            get_more_text = ActionChains(driver)
            get_more_text.move_to_element(read_more)
            get_more_text.pause(5)
            get_more_text.click()
            get_more_text.perform()
            driver.implicitly_wait(3)
        except (NoSuchElementException, TimeoutException):
            pass
        except JavascriptException:
            print(message.text, '\n')

        message = message.text
        message = message.replace('\xad', '')
        message = message.replace('\n', '')
        if len(message):
            data[author].append(Text(date, message))

    time.sleep(15)
    driver.quit()