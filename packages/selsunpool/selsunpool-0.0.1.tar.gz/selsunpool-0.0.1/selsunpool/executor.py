import functools
import inspect
import logging
import typing
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed


from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver

from . import config


class SeleniumPoolException(Exception):
    pass


def selenium_job(webdriver_param_name: str):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapped(*args, **kwargs):
            passed_name = config.WEBDRIVER_VARNAME
            if passed_name not in kwargs:
                raise SeleniumPoolException(
                    "webdriver object not found in kwargs")
            if passed_name != webdriver_param_name:
                kwargs[webdriver_param_name] = kwargs.pop('__driver')
            return fn(*args, **kwargs)
        wrapped.is_selenium_job = True
        return wrapped
    return decorator


class SeleniumPoolExecutor:
    def __init__(self,
                 wrap_drivers: typing.Iterable[WebDriver]=None,
                 num_workers: int=2,
                 close_on_exit: bool=False,
                 webdriver_cls: WebDriver=None,
                 ):
        """

        :param num_workers:
        :param webdriver_cls:
        :param wrap_drivers:
        """
        self.num_workers = num_workers
        if self.num_workers < 1:
            raise ValueError('Wrong count for num_workers')
        self.webdriver_cls = webdriver_cls
        if wrap_drivers is not None:
            for driver in wrap_drivers:
                if not isinstance(driver, WebDriver):
                    raise SeleniumPoolException(
                        'Must pass an active selenium webdriver instance')
            self.drivers = set(wrap_drivers)
        else:
            self.drivers = None
        self._futures = set()
        self._jobs = []
        self._executor = ThreadPoolExecutor(max_workers=num_workers * 2)
        self.close_on_exit = close_on_exit

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()
        return False

    def _init_pool(self):
        if self.drivers is not None:
            return True
        if self.webdriver_cls is None:
            self.webdriver_cls = config.DEFAULT_WEBDRIVER
        self.drivers = {self.webdriver_cls()
                        for _ in range(self.num_workers)}
        return len(self.drivers) > 0

    def submit(self, fn, *args, **kwargs):
        if not hasattr(fn, 'is_selenium_job'):
            params = inspect.signature(fn).parameters
            if config.WEBDRIVER_VARNAME not in params:
                raise SeleniumPoolException(
                    'Driver Not Found in submit')
        self._jobs.append((fn, args, kwargs))

    def map(self, fn, *iterables):
        for args in zip(*iterables):
            self.submit(fn, *args)

    def shutdown(self, wait=True):
        thread_pool_down = self._executor.shutdown(wait)
        for future in as_completed(self._futures):
            self.drivers.add(future.driver)
        if self.close_on_exit and self.drivers is not None:
            for driver in self.drivers:
                try:
                    driver.close()
                except WebDriverException as exc:
                    logging.warning(exc)
        return thread_pool_down

    @property
    def job_results(self):
        if not self._init_pool():
            raise SeleniumPoolException(
                'Could not initialize the webdriver pool')
        for job in self._jobs:
            # unpack job
            fn, args, kwargs = job
            # get the first available driver
            if len(self.drivers) > 0:
                driver = self.drivers.pop()
            else:
                future = next(as_completed(self._futures))
                # return driver to free-driver pool
                self.drivers.add(future.driver)
                yield future.result()
                # abandon future object
                self._futures.remove(future)
                # pop off a driver from the pool
                driver = self.drivers.pop()
            # submit function to the executor and pass driver as kwarg to job fn
            kwargs[config.WEBDRIVER_VARNAME] = driver
            future = self._executor.submit(fn, *args, **kwargs)
            # attach driver to the future object for recall
            future.driver = driver
            # add future to set
            self._futures.add(future)
        # all jobs submitted. Collect remaining futures results
        for future in as_completed(self._futures):
            self.drivers.add(future.driver)
            yield future.result()
        self._futures.clear()
        self._jobs.clear()
