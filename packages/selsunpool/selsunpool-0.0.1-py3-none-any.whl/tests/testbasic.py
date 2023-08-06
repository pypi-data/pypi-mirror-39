import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException

from .context import (
    SeleniumPoolExecutor,
    SeleniumPoolException,
    selenium_job,
    WebDriver)


TEST_URLS = [
    'https://google.com',
    'https://microsoft.com',
    'https://github.com',
    'https://gitlab.com',
    'https://bitbucket.com',
]


@pytest.fixture(scope='module')
def workers():
    workers = [webdriver.Chrome(), webdriver.Chrome()]
    yield workers
    for d in workers:
        try:
            d.close()
        except Exception:
            pass


@selenium_job('driver')
def get_url(url, driver):
    driver.get(url)


@selenium_job('driver')
def xsearch(search_term, driver: WebDriver):
    try:
        driver.get('https://www.yahoo.com/')
        driver.implicitly_wait(10)
        elem = driver.find_element_by_name('p')
        elem.send_keys(search_term)
        elem.send_keys(Keys.ENTER)
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.title_contains(search_term))
        return driver.title
    except:
        return None


def xsearch_driver_param(search_term, __driver: WebDriver):
    try:
        driver = __driver
        driver.get('https://www.yahoo.com/')
        driver.implicitly_wait(10)
        elem = driver.find_element_by_name('p')
        elem.send_keys(search_term)
        elem.send_keys(Keys.ENTER)
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.title_contains(search_term))
        return driver.title
    except Exception:
        return None


def test_valid_job_func_with_wrapper(workers):
    try:
        @selenium_job('driver')
        def valid(driver):
            return None

        with SeleniumPoolExecutor(workers) as pool:
            pool.submit(valid)
            list(pool.job_results)
    except SeleniumPoolException:
        assert False


def test_missing_param_passed_by_executor():
    with pytest.raises(SeleniumPoolException):
        @selenium_job('xxx')
        def x(xxx=None):
            pass

        x()


def test_invalid_job_func(workers):
    def invalid(x):
        return x

    with pytest.raises(SeleniumPoolException):
        with SeleniumPoolExecutor(workers) as pool:
            pool.submit(invalid, None)


def test_driver_not_found_exception():
    with pytest.raises(SeleniumPoolException):
        _ = SeleniumPoolExecutor(wrap_drivers=[None, None])


def test_attribute_exception():
    with pytest.raises(ValueError):
        _ = SeleniumPoolExecutor(num_workers=0)


def test_drivers_returned_to_crib(workers):
    @selenium_job('driver')
    def get(url, driver):
        driver.get(url)

    with SeleniumPoolExecutor(workers) as executor:
        executor.map(get, TEST_URLS)
        list(executor.job_results)
        assert len(executor.drivers) == len(workers)


@selenium_job(webdriver_param_name='driver')
def job(url, driver):
    driver.get(url)
    return driver.title


def test_wrapper_id():
    assert hasattr(job, 'is_selenium_job')
    # print(dir(job))
    # print(job.__dict__)


def test_wrapper(workers):
    with SeleniumPoolExecutor(wrap_drivers=workers) as e:
        e.submit(job, 'https://google.com')
        results = list(e.job_results)
        assert 'Google' in results


def test_shutdown_without_drivers():
    pool = SeleniumPoolExecutor()
    try:
        pool.shutdown(wait=False)
    except TypeError:
        assert False


def test_shutdown_with_drivers(workers):
    pool = SeleniumPoolExecutor(workers, close_on_exit=True)
    try:
        pool.shutdown()
    except WebDriverException:
        assert False

# def test_abandon_generator():
#     with SeleniumPoolExecutor(num_workers=2) as pool:
#         pool.map(get_url, TEST_URLS)
#         next(pool.job_results)


if __name__ == '__main__':
    pass
