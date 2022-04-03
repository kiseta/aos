import random
from faker import Faker
from datetime import datetime
fake = Faker(locale=['en_CA', 'en_US'])


# ------------------ AOS WEB ELEMENTS ------------------------------
app = 'Advantage Online Shopping'
base_url = 'https://advantageonlineshopping.com/#/'
# base_url = 'http://localhost:8080/#/'
new_account_url = base_url + 'register'
new_account_page_title = 'CREATE NEW ACCOUNT'
home_page_title = '\xa0Advantage Shopping'

first_name = fake.first_name()
last_name = fake.last_name()
full_name = f'{first_name} {last_name}'
user_name = f'{first_name}{last_name}'.lower()[:10] + str(fake.pyint(11, 99))
password = 'Pass1'
user_email = f'{user_name}@{fake.free_email_domain()}'
phone = fake.bothify(text='1-(###)-###-####')
country = 'Canada'
city = fake.city()[:10]
address = fake.street_address()
province = fake.province_abbr()
postal_code = fake.postalcode()
product_name = ''
credit_card_num = fake.credit_card_number(card_type=None)
security_code = fake.pyint(1111, 9999)
order_number = ''
tracking_number = ''
product_id = random.choice([i for i in range(1, 35) if i != 13])
res_dir_name = datetime.now().strftime("res_%Y%m%d_%H%M%S")
n = 0
email_subject = f'{fake.catch_phrase()},{fake.catch_phrase()}'
hr = f'\n------------------------~*~--------------------------'

list_name = ['usernameRegisterPage', 'emailRegisterPage', 'passwordRegisterPage', 'confirm_passwordRegisterPage',
             'first_nameRegisterPage', 'last_nameRegisterPage', 'phone_numberRegisterPage',
             'cityRegisterPage', 'addressRegisterPage', 'state_/_province_/_regionRegisterPage',
             'postal_codeRegisterPage']

list_val = [user_name, user_email, password, password,
            first_name, last_name, phone,
            city, address, province, postal_code]

print(list_val)
print(credit_card_num, security_code)

# -------------------------------------------------
speaker_url = 'https://advantageonlineshopping.com/#/category/Speakers/4'
tablet_url = 'https://advantageonlineshopping.com/#/category/Tablets/3'
laptop_url = 'https://advantageonlineshopping.com/#/category/Laptops/1'
mice_url = 'https://advantageonlineshopping.com/#/category/Mice/5'
headphone_url = 'https://advantageonlineshopping.com/#/category/Headphones/2'
see_offer_url = 'https://advantageonlineshopping.com/#/product/3'
explore_now_url = 'https://advantageonlineshopping.com/#/category/Tablets/3'
item_1 = 'https://advantageonlineshopping.com/#/product/16'
item_2 = 'https://advantageonlineshopping.com/#/product/10'
item_3 = 'https://advantageonlineshopping.com/#/product/21'
chat_url = 'https://advantageonlineshopping.com/chat.html'
fb_link = 'https://www.facebook.com/MicroFocus/'
twitter_link = 'https://twitter.com/MicroFocus'
linkedin_link = 'https://www.linkedin.com/company/micro-focus '

list_title = ['SPEAKERS', 'TABLETS', 'LAPTOPS', 'MICE', 'HEADPHONES', 'SEE OFFER', 'POPULAR ITEM 1', ' POPULAR ITEM 2', ' POPULAR ITEM 3']
list_url = [speaker_url, tablet_url, laptop_url, mice_url, headphone_url, see_offer_url, item_1, item_2, item_3]
list_id = ['speakersTxt', 'tabletsTxt', 'laptopsTxt', 'miceTxt', 'headphonesTxt', 'see_offer_btn', 'details_16', 'details_10', 'details_21']
# -------------------------------------------------
