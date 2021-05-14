import pytest
from selenium import webdriver
from pathlib import Path
from datetime import datetime

home = Path(__file__).resolve().parent
reports_folder = home.joinpath('reports')

time_now = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # define the location and file name for the plugin pytest-html to save the html report
    # reports folder has been defined at the beginning of the file
    config.option.htmlpath = reports_folder / "report.html"


@pytest.fixture(scope="function")
def browser(request):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--enable-automation')
    options.add_argument("--start-maximized")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument('--no-sandbox')
    options.add_argument('--ignore-certificate-errors')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)
    request.cls.driver = driver
    driver.maximize_window()

    yield webdriver
    driver.close()
    driver.quit()