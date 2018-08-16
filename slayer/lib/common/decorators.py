import logging
import time
import math


def dec_log_execution_time(method):
    def timed_function(*args, **kw):
        line_length = 42
        # logging.debug("{0} start".format(method.__name__).center(line_length, '-'))
        start_time = time.time()
        result = method(*args, **kw)
        end_time = time.time()
        logging.debug(
            ('{0} Total time: %2.2f sec'.format(method.__name__) % (end_time - start_time)).center(line_length, '-'))
        return result

    return timed_function

def retry_until_not_none(retries=3, delay=1):
    """Retries a function or method until it returns different than None

    delay sets the initial delay in seconds, and backoff sets the factor by which
    the delay should lengthen after each failure. backoff must be greater or equal ot 1.
    tries must be at least 0, and delay
    greater than 0."""

    retries = math.floor(retries)
    if retries < 0:
        raise ValueError("tries must be 0 or greater")
    if delay <= 0:
        raise ValueError("delay must be greater than 0")

    def deco_retry(f):
        def f_retry(*args, **kwargs):
            mtries, mdelay = retries, delay  # make mutable
            retry_value = None
            while mtries > 0:
                try:
                    retry_value = f(*args, **kwargs)  # Do an attempt
                    if retry_value is not None:
                        return retry_value
                    else:
                        # TODO: Change exception
                        raise Exception("Couldn't get the element")
                except:
                    mtries -= 1  # consume an attempt
                    if mtries > 0:
                        logging.debug("Retrying...")
                    time.sleep(mdelay)  # wait...
            return retry_value  # Ran out of tries
        return f_retry  # true decorator -> decorated function
    return deco_retry  # @retry(arg[, ...]) -> true decorator



def dec_retry_bool_function(retries, wait=3, backoff=2):
    """Retries a function or method until it returns True.

    @wait sets the initial delay in seconds, and @backoff sets the factor by which
    the delay should lengthen after each failure. @backoff must be greater than 1,
    @retries must be at least 0, and delay greater than 0."""
    # TODO: Improve to use condition instead of a bool value (True)
    if backoff <= 1:
        raise ValueError("backoff must be greater than 1")

    tries = math.floor(retries)
    if tries < 0:
        raise ValueError("tries must be 0 or greater")
    if wait <= 0:
        raise ValueError("delay must be greater than 0")

    def deco_retry(f):
        def function_retry(*args, **kwargs):
            mtries, mdelay = tries, wait  # mutable values

            function_value = f(*args, **kwargs)
            while mtries > 0:
                if function_value is True:  # Done on success
                    return True
                logging.debug("Retrying...")
                mtries -= 1
                time.sleep(mdelay)
                mdelay *= backoff
                function_value = f(*args, **kwargs)  # Try again
            return False  # Ran out of tries
        return function_retry  # true decorator -> decorated function
    return deco_retry  # @retry(arg[, ...]) -> true decorator


# TODO: change behavior so it takes screenshots before/after function ends
# TODO: Use context in order to access the webdriver and step name
def take_screenshot(method):
    def web_function(*args, **kw):
        result = method(*args, **kw)
        # self.driver.get_screenshot_as_file(os.path.join(os.getcwd(),
        # "screenshots", screenshot_name))
        return result

    return web_function
