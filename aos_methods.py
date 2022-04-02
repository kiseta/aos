import os
import sys
import datetime
from time import sleep
from selenium import webdriver
import aos_locators as locators
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("window-size=1400,1500")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

# s = Service(executable_path='chromedriver.exe')
# driver = webdriver.Chrome(service=s)


def setup():
    print('\n-------------------------~*~*~*~*------------------------')
    print(f'{locators.app} test started at: {datetime.datetime.now()}')
    print(f'Launch {locators.app}\n')
    driver.set_page_load_timeout(20)
    os.mkdir(locators.res_dir_name)
    driver.maximize_window()  # open web browser and maximize the window
    driver.implicitly_wait(10)  # wait for the browser response in general
    driver.get(locators.base_url)  # navigate to app website

    # check the correct URL and the correct title
    if driver.current_url == locators.base_url and driver.title == locators.home_page_title:
        print(f'Yoohoo! {locators.app} is launched! URL: {driver.current_url}')
        print(f'Page Title: ', {driver.title})
    else:
        print(driver.current_url)
        print(f'We are not on {locators.app} Home Page. Check your code')
        teardown()


def teardown():  # function to end the session
    if driver is not None:
        print('\n-------------------------~*~*~*~*------------------------')
        print(f'Test Completed at: {datetime.datetime.now()}')
        sleep(2)
        driver.close()
        driver.quit()


def log_in():
    print(f'\n------------------------~* LOGIN  *~------------------------')
    if driver.current_url == locators.base_url:
        sleep(2)
        driver.find_element(By.ID, 'menuUserLink').click()
        driver.implicitly_wait(30)
        assert driver.find_element(By.LINK_TEXT, 'CREATE NEW ACCOUNT').is_displayed()
        if driver.find_element(By.LINK_TEXT, 'CREATE NEW ACCOUNT').is_displayed():
            print(f'Login form is displayed - continue to Login')
            driver.find_element(By.NAME, 'username').send_keys(locators.user_name)
            sleep(1)
            driver.find_element(By.NAME, 'password').send_keys(locators.password)
            sleep(1)
            driver.find_element(By.ID, 'sign_in_btnundefined').click()
            sleep(1)
        else:
            print(f'Login Form is not displayed')


def validate_user_login():
    print(f'\n----------------~* VALIDATE USER LOGIN  *~----- ------------')
    check_user_name = driver.find_element(By.ID, 'menuUserLink').text
    print(f'{check_user_name} user name is displayed')
    if locators.user_name in check_user_name:
        print(f'Expected user: {locators.user_name} login Successful!')
        sleep(1)
    else:
        print(f'Expected Username: "{locators.user_name}" is not displayed!')
    ssh('validate_user_login')

def log_out():
    print(f'\n------------------------~* LOGOUT  *~------------------------')
    sleep(2)
    driver.find_element(By.ID, 'menuUserLink').click()
    sleep(1)
    driver.find_element(By.XPATH, '//a/div/label[contains(.,"Sign out")]').click()
    sleep(1)
    if driver.current_url == locators.base_url:
        print(f'Logout Successful! at {datetime.datetime.now()}')
    driver.refresh()
    sleep(3)
    # breakpoint()


def create_new_user():
    print(f'\n-----------------~* CREATE NEW USER *~--------------------')
    if driver.current_url == locators.base_url:
        driver.find_element(By.ID, 'menuUserLink').click()
        sleep(2)
        assert driver.find_element(By.LINK_TEXT, 'CREATE NEW ACCOUNT').is_displayed()
        print(f'Login form is displayed - continue to Create New Account')
        sleep(2)
        driver.find_element(By.LINK_TEXT, 'CREATE NEW ACCOUNT').click()
        sleep(2)
        if driver.current_url == locators.new_account_url:
            assert driver.find_element(By.XPATH, '//h3[contains(.,"CREATE ACCOUNT")]').is_displayed()
            sleep(1)
            print(f'CREATE ACCOUNT Page is displayed\n')
            # populate edit form fields
            for i in range(len(locators.list_name)):
                name, val = locators.list_name[i], locators.list_val[i]
                driver.find_element(By.NAME, name).send_keys(val)
                sleep(1)
            driver.find_element(By.XPATH, f'//option[contains(@label, "{locators.country}")]').click()
            sleep(1)
            driver.find_element(By.NAME, 'i_agree').click()
            sleep(1)
            ssh('create_new_user_form_populated')
            driver.find_element(By.ID, 'register_btnundefined').click()
            sleep(1)
            if driver.find_element(By.LINK_TEXT, locators.user_name).is_displayed():
                print(f'New User {locators.user_name}/{locators.user_email} registration successful!'
                      f'\nUserName: {locators.user_name} is displayed')
                logger('created')
                sleep(1)
            else:
                print(f'New User was not created. Try again.')


def delete_account():
    print(f'\n-----------------~* DELETE NEW USER *~---------------------')
    assert driver.find_element(By.LINK_TEXT, locators.user_name).is_displayed()
    sleep(1)
    driver.find_element(By.LINK_TEXT, locators.user_name).click()
    sleep(0.5)
    driver.find_element(By.XPATH, '//a/div/label[contains(.,"My account")]').click()
    sleep(0.5)
    if driver.find_element(By.XPATH, f'//label[contains(.,"{locators.full_name}")]').is_displayed():
        print(f'Account details page for user: \'{locators.full_name}\' is displayed')
        sleep(2)
        driver.execute_script("window.scrollTo(1000,1000 )")
        sleep(2)
        driver.find_element(By.CLASS_NAME, 'deleteBtnText').click()
        sleep(5)
        delete_popup = driver.find_element(By.CLASS_NAME, 'deleteAccountPopupContent').is_displayed()
        print(f'Delete popup is displayed: {delete_popup}')
        if delete_popup:
            # driver.find_element(By.XPATH, "//div[contains(text(), 'yes')]").click()
            driver.find_element(By.CLASS_NAME, 'deletePopupBtn').click()
            driver.implicitly_wait(3)
            assert driver.find_element(By.XPATH, "//*[contains(., 'deleted successfully')]").is_displayed()
            conf_screen = driver.find_element(By.XPATH, "//*[contains(., 'deleted successfully')]").is_displayed()
            print(f'Delete Confirmation screen is displayed: {conf_screen}')
            conf = driver.find_element(By.XPATH, "//p[contains(., 'deleted successfully')]").get_attribute('innerHTML')
            print(f'Confirmation message is displayed: {conf}')
            sleep(2)
            print(f'User {locators.full_name}/{locators.user_email} is deleted!')
            logger('deleted')
            sleep(2)
        else:
            print(f'Delete Popup is not displayed')
            driver.find_element(By.CLASS_NAME, 'deleteBtnText').click()
            sleep(30)


def validate_user_deleted():
    print(f'\n------------~* CONFIRM USER DOES NOT EXIST  *~-------------')
    sleep(2)
    error_label = driver.find_element(By.XPATH, '//label[contains(.,"Incorrect user name or password.")]').text
    if driver.find_element(By.XPATH, '//label[contains(.,"Incorrect user name or password.")]').is_displayed():
        print(f'Username/Password {locators.user_name}/{locators.password} is not found. Error: {error_label}')
        sleep(1)
        # close login popup
        ssh('validate_user_deleted')
        driver.find_element(By.XPATH, '//div[contains(@class,"closeBtn loginPopUpCloseBtn")]').click()
    else:
        print(error_label)
    sleep(2)


def checkout_shopping_cart():
    sleep(2)
    print(f'\n------------------------~* ADD ITEM TO CART  *~---------------------')
    driver.get(f'{locators.base_url}product/{locators.product_id}')
    locators.product_name = driver.find_element(By.CLASS_NAME, 'select').text
    print(f'Random product selected: {locators.product_name}, Product ID: {locators.product_id}')
    ssh('add_item_to_cart')
    driver.find_element(By.XPATH, '//button[text()="ADD TO CART"]').click()
    sleep(2)
    # navigate to cart
    print(f'\n------------------------~* SHOPPING CART  *~------------------------')
    driver.find_element(By.ID, 'shoppingCartLink').click()
    sleep(2)
    assert driver.find_element(By.XPATH, f'//H3[contains(.,"SHOPPING CART")]').is_displayed()
    print(f'SHOPPING CART page is displayed')
    assert driver.find_element(By.XPATH, f'//td/label[contains(.,"{locators.product_name}")]').is_displayed()
    print(f'Product: "{locators.product_name}" is in the cart')
    sleep(2)
    driver.find_element(By.ID, 'checkOutButton').click()

    # ----------------- check if login form is displayed
    if driver.current_url == 'https://advantageonlineshopping.com/#/login':
        print(f'\n------------------------~* CHECKOUT LOGIN  *~------------------------')
        print(f'Login page is displayed - Loging to checkout shopping cart')
        driver.find_element(By.NAME, 'usernameInOrderPayment').send_keys(locators.user_name)
        sleep(1)
        driver.find_element(By.NAME, 'passwordInOrderPayment').send_keys(locators.password)
        sleep(1)
        driver.find_element(By.ID, 'login_btnundefined').click()
        sleep(1)
    # -----------------------------------------------------

    sleep(2)
    print(f'\n------------------------~* CHECKOUT CART  *~------------------------')
    assert driver.find_element(By.XPATH, f'//H3[contains(.,"ORDER PAYMENT")]').is_displayed()
    assert driver.find_element(By.XPATH, f'//label[@class[contains(.,"selected")] and(text()="1. SHIPPING DETAILS ")]').is_displayed()
    print(f'ORDER PAYMENT > 1. SHIPPING DETAILS page is displayed')
    assert driver.find_element(By.XPATH, f'//label[contains(.,"{locators.full_name}")]').is_displayed()
    print(f'Customer Name: "{locators.full_name}" is displayed\n')
    sleep(2)
    driver.find_element(By.ID, 'next_btn').click()
    sleep(2)
    assert driver.find_element(By.XPATH, f'//label[@class[contains(.,"selected")] and(text()="2. PAYMENT METHOD")]').is_displayed()
    print(f'ORDER PAYMENT > 2. PAYMENT METHOD page is displayed')

    rndpay = 1  # random.randint(1, 2)

    if rndpay == 1:
        print(f'\n-------------------~* SAFEPAY PAYMENT  *~-------------------')
        # safe pay details
        driver.find_element(By.NAME, 'safepay').click()
        sleep(1)
        driver.find_element(By.NAME, 'safepay_username').send_keys('spusername')
        sleep(1)
        driver.find_element(By.NAME, 'safepay_password').send_keys('Pass1')
        sleep(1)
        # uncheck save checkbox if checked
        save_safepay = driver.find_element(By.NAME, 'save_safepay').is_selected()
        print(f'Safepay save checkbox selected: {save_safepay}')
        if save_safepay:
            driver.find_element(By.NAME, 'save_safepay').click()
            save_safepay = driver.find_element(By.NAME, 'save_safepay').is_selected()
            print(f'Safepay save checkbox selected: {save_safepay}')
            ssh('payment_completed')
        driver.find_element(By.ID, 'pay_now_btn_SAFEPAY').click()
        # ------------------------- END SAFEPAY PAY ---------------------------------------

    if rndpay == 2:
        print(f'\n-------------------~* MASTER CREDIT PAYMENT  *~-------------------')
        driver.find_element(By.NAME, 'masterCredit').click()
        sleep(1)
        driver.find_element(By.ID, 'creditCard').send_keys(locators.credit_card_num)
        sleep(0.5)
        driver.find_element(By.NAME, 'cvv_number').send_keys(locators.security_code)
        sleep(0.5)
        driver.find_element(By.NAME, 'cardholder_name').send_keys(locators.full_name)
        sleep(0.5)
        save_master_credit = driver.find_element(By.NAME, 'save_master_credit').is_selected()
        # uncheck save checkbox if checked
        print(f'MasterCredit save checkbox selected: {save_master_credit}')
        if save_master_credit:
            driver.find_element(By.NAME, 'save_master_credit').click()
            save_master_credit = driver.find_element(By.NAME, 'save_master_credit').is_selected()
            print(f'MasterCredit save checkbox selected: {save_master_credit}')

        driver.find_element(By.ID, 'pay_now_btn_ManualPayment').click()
        # ------------------------- END MASTER CREDIT ---------------------------------------

    sleep(2)
    print(f'\n------------------------~* ORDER CONFIRMATION  *~------------------------')
    thank_you_msg = 'Thank you for buying with Advantage'
    assert driver.find_element(By.XPATH, f'//span[contains(.,"{thank_you_msg}")]').is_displayed()
    print(f'"{thank_you_msg}" confirmation message is displayed')
    locators.order_number = driver.find_element(By.ID, 'orderNumberLabel').text
    locators.tracking_number = driver.find_element(By.ID, 'trackingNumberLabel').text
    print(f'Order Number: {locators.order_number}')
    print(f'Tracking Number: {locators.tracking_number}')
    ssh('new_order_confirmation')


def validate_order():
    print(f'\n------------------------~* VALIDATE ORDER PAGE *~------------------------')
    driver.find_element(By.ID, 'menuUserLink').click()
    sleep(1)
    driver.find_element(By.XPATH, '//a/div/label[contains(.,"My orders")]').click()
    sleep(1)
    assert driver.find_element(By.XPATH, f'//H3[contains(.,"MY ORDERS")]').is_displayed()
    print('MY ORDERS page is displayed')
    assert driver.find_element(By.XPATH, f'//td/label[contains(.,"{locators.order_number}")]').is_displayed()
    print(f'Order number: {locators.order_number} is displayed')
    pname = driver.find_element(By.XPATH, '//tr[2]/td[4]/span').text
    assert pname.upper() in locators.product_name
    print(f'Product name: {pname} is displayed')
    ssh('validate_order_page')
    print(f'\n------------------------~* DELETE ORDER *~------------------------')
    driver.find_element(By.XPATH, f"//*[contains(.,'{locators.order_number}')]/../td/span/a[text()='REMOVE']").click()
    sleep(1)
    driver.find_element(By.ID, 'confBtn_1').click()
    sleep(1)
    assert driver.find_element(By.XPATH, '//label[contains(.,"No orders")]')
    ssh('delete_order')
    print(f'Order {locators.order_number} is deleted')
    sleep(1)


def logger(action):
    # create variable to store the file content
    old_instance = sys.stdout
    log_file = open('aos.log', 'a')  # open log file and append a record
    sys.stdout = log_file
    print(f'{locators.user_email}\t'
          f'{locators.user_name}\t'
          f'{locators.password}\t'
          f'{datetime.datetime.now()}\t'
          f'{action}')
    sys.stdout = old_instance
    log_file.close()


def ssh(filename):
    driver.save_screenshot(locators.res_dir_name + '/' + filename + '.png')
    print(f'Screenshot {filename} is saved to {locators.res_dir_name}')


# setup()
# create_new_user()
# log_out()
# log_in()
# validate_user_login()
# checkout_shopping_cart()
# validate_order()
# delete_account()
# log_in()
# validate_user_deleted()
# teardown()
