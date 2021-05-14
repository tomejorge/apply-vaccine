from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from base.base_actions import BaseActions
import pytest
import time


@pytest.mark.usefixtures("browser")
class TestApply(BaseActions):

    url = "https://www.regionh.dk/presse-og-nyt/pressemeddelelser-og-nyheder/Sider/Vaccination-mod-COVID-19.aspx"

    accept_cookies_button = (By.CSS_SELECTOR, "button[aria-label='Accepter']")
    survey_link = (By.CSS_SELECTOR, "a[href*='https://www.survey-xact.dk/']")
    next_button = (By.CSS_SELECTOR, "input[class='next-button']")
    name_input = (By.CSS_SELECTOR, "input[name='t50100775']")
    age_input = (By.CSS_SELECTOR, "input[name='n35965768']")
    address_input = (By.CSS_SELECTOR, "input[name='t50088645']")
    post_number_input = (By.CSS_SELECTOR, "input[name='t50088674']")
    phone_number_input = (By.CSS_SELECTOR, "input[name='n50088775']")
    closer_center_select = (By.CSS_SELECTOR, "input[id='ch_50088941-106780586']")
    

    def click_next(self):
        return self.click(self.next_button)

    @pytest.mark.parametrize("name, age, phone_number", 
    [('Tomé Jorge', '38', '91862225'),
     ('Svenia Nowak', '31', '50341365')], ids=['tome', 'svenia'])
    def test_auto_apply_vaccine(self, name, age, phone_number):
        action = ActionChains(self.driver)
        self.visit(self.url)
        self.click(self.accept_cookies_button)
        self.click(self.survey_link)
        self.click_next()
        names = self.find_by_index(self.name_input, 0)
        action.send_keys_to_element(names, name).perform()
        self.click_next()
        action = ActionChains(self.driver)
        ages = self.find_by_index(self.age_input, 0)
        action.send_keys_to_element(ages, age).perform()
        self.click_next()
        action = ActionChains(self.driver)
        address = self.find_by_index(self.address_input, 0)
        action.send_keys_to_element(address, "Floras Allé, 22, 1TV").perform()
        self.click_next()
        action = ActionChains(self.driver)
        post_number = self.find_by_index(self.post_number_input, 0)
        action.send_keys_to_element(post_number, "2720").perform()
        self.click_next()
        action = ActionChains(self.driver)
        phone = self.find_by_index(self.phone_number_input, 0)
        action.send_keys_to_element(phone, phone_number).perform()
        self.click_next()
        action = ActionChains(self.driver)
        closer_center = self.find(self.closer_center_select)
        action.move_to_element(closer_center).click(closer_center).perform()
        self.click_next()
        self.click_next()
        self.click_next()

        

        
