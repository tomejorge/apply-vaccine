import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException


class BaseActions:
    driver = None
    base_timeout = 10

    def visit(self, url):
        """ visit the specified url """
        self.driver.get(url)

    def get_url_path(self, url_path, timeout=base_timeout):
        """ wait for specific path in url """
        return WebDriverWait(self.driver, timeout=timeout) \
            .until(EC.url_contains(url_path))

    def find_element(self, locator):
        return self.wait_for_element_visible(locator)
        

    def find_all_elements(self, locator):
        """ give a locator that returns a list of all elements matching it """
        by = locator[0]
        value = locator[1]
        return self.driver.find_elements(by, value)
    
    def find_by_index(self, locator, index, timeout=base_timeout):
        """ find the given locator, specify a timeout if necessary """
        for i in range(0, 20):
            try:
                if timeout == 0:
                    return self.find_all_elements(locator)[index]
                else:
                    return WebDriverWait(self.driver, timeout=timeout) \
                        .until(EC.presence_of_element_located(locator),
                            message=f"could not find the presence of element with locator: {locator}")
            except StaleElementReferenceException:
                    pass


    def find(self, locator, timeout=base_timeout):
        """ find the given locator, specify a timeout if necessary """
        if timeout == 0:
            return self.find_element(locator)
        else:
            return WebDriverWait(self.driver, timeout=timeout) \
                .until(EC.presence_of_element_located(locator),
                       message=f"could not find the presence of element with locator: {locator}")

    def click(self, locator, timeout=base_timeout):
        """ click on the given locator, specify a timeout if necessary """
        self.find(locator, timeout=timeout).click()

    def switch_to_iframe(self, locator, timeout=base_timeout):
        """ switch to a new frame in order to be able to interact with the elements in it """
        frame = self.find(locator, timeout=timeout)
        self.driver.switch_to.frame(frame)

    def type(self, text, locator, timeout=base_timeout):
        """ type the text into the given locator, clearing the field first, specify a timeout if necessary """
        field = self.find(locator, timeout=timeout)
        field.clear()
        field.send_keys(text)

    def type_no_clear(self, text, locator, timeout=base_timeout):
        """ type the text into the given locator, without clearing the field first, specify a timeout if necessary """
        field = self.find(locator, timeout=timeout)
        # commented out below clear as it was interfering with the typing in the domain field in home_page
        # field.clear()
        field.send_keys(text)

    def type_with_delay(self, text, locator, timeout=base_timeout):
        """ type the text in the given locator, one character at a time, specify a timeout if necessary """
        element = self.find(locator, timeout=timeout)
        for key in text:
            element.send_keys(key)
            time.sleep(0.05)

    def type_clear_using_backspace(self, text, locator, timeout=base_timeout):
        """  type the text in the given locator, clear the field using backspace, specify a timeout if necessary - should
        only be used in case the normal type() function doesn't work"""
        field = self.find(locator, timeout=timeout)
        x = 100
        while x > 0:
            field.send_keys(Keys.BACK_SPACE)
            x = x - 1
        field.send_keys(text)

    def select_from_dropdown(self, specifier, locator, value, timeout=base_timeout):
        """ select from a dropdown, based on value, visible_text or index, specify a timeout if necessary """
        if specifier == "value":
            element = self.find(locator, timeout=timeout)
            Select(element).select_by_value(value)
        elif specifier == "visible_text":
            element = self.find(locator, timeout=timeout)
            Select(element).select_by_visible_text(value)
        else:  # by index
            element = self.find(locator, timeout=timeout)
            Select(element).select_by_index(value)

    def is_displayed(self, locator, timeout=base_timeout):
        """ check if the given locator is displayed on the screen """
        try:
            return self.find(locator, timeout).is_displayed()
        except:
            return False

    def is_selected(self, locator, timeout=base_timeout):
        """ check if a given element is in selected state """
        try:
            return self.find(locator, timeout).is_selected()
        except:
            return False

    # array related functions
    # NOTE: should only be used by the find_in_array function, which includes a timetout
    def find_element_in_array(self, locator, index):
        by = locator[0]
        value = locator[1]
        list = self.driver.find_all_elements(by, value)
        return list[index]

    # find the element at the given index in the array (locator), specify a timeout if necessary
    def find_in_array(self, locator, index, timeout=base_timeout):
        if timeout == 0:
            return self.find_element_in_array(locator, index)
        else:
            return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located(locator))

    # click on the element at the given index in the array (locator), specify a timeout if necessary
    def click_in_array(self, locator, index):
        self.find_in_array(locator, index).click()

    def find_stale_element(self, locator):
        """ this method tries to find an element and if we get a StaleElementReferenceException.
            we retry the ammount of times specified for the parameter attemps
            StaleElementReferenceException - means that the element is old because there was a page reload
            or a section reload through ajax
            - the values bellow should work for most cases """
        element = None
        for i in range(0, 20):
            try:
                element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located(locator))
            except StaleElementReferenceException as e:
                print(e)
                pass
        return element

    def find_stale_2(self, locator):
        """ find an element in a stale state """
        element = None
        attempt = 0
        while True and attempt <= 20:
            try:
                element = self.find(locator, 30)
            except StaleElementReferenceException:
                print("Timeout, retrying...")
                attempt += 1
                continue
            else:
                break
        return element

    def switch_to_alert(self):
        element = None
        attempt = 0
        while True and attempt <= 20:
            try:
                wait = WebDriverWait(self.driver, 5)
                wait.until(EC.alert_is_present())
                element = self.driver.switch_to.alert
            except TimeoutException:
                attempt += 1
                continue
        return element
