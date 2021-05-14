import pytest
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver



@pytest.fixture(scope="class")
def browser(request):
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options, executable_path=ChromeDriverManager().install())
    request.cls.driver = driver
    driver.maximize_window()

    yield webdriver
    # driver.close()
    # driver.quit()