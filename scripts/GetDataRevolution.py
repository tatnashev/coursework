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


# Site design differs on 6-8 November 1917
def get_data_revolution(data):
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

    url = 'https://project1917.ru/posts/06.11.17'

    driver.get(url)

    # Loading page
    driver.implicitly_wait(10)

    reverse = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, 'read-reverse'))
    )

    click_reverse = ActionChains(driver)
    click_reverse.move_to_element(reverse)
    click_reverse.pause(3)
    click_reverse.click()
    click_reverse.perform()

    # Loading reversed page
    driver.implicitly_wait(5)

    last_block = None

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(10)

        try:
            last_block = WebDriverWait(driver, 7).until(
                EC.presence_of_element_located((By.ID, 'oct-post-31417'))
            )
            break
        except TimeoutException:
            pass

    texts = WebDriverWait(driver, 40).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "post.post_0.ng-scope"))
    )

    for text in texts:
        if text.location['x'] >= last_block.location['x'] and text.location['y'] >= last_block.location['y']:
            break

        driver.execute_script("arguments[0].scrollIntoView();", text)

        day = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'timeline__date-day'))
        )
        date = dt.date(day=int(day.text), month=11, year=1917)

        author = ''
        try:
            author = text.find_element_by_class_name('post-author__name').text
            driver.implicitly_wait(10)
        except NoSuchElementException:
            continue

        message = text.find_element_by_class_name('post__text')
        message = message.text
        message = message.replace('\xad', '')
        message = message.replace('\n', '')
        if len(message):
            data[author].append(Text(date, message))

    time.sleep(15)
    driver.quit()