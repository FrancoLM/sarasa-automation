import logging
import time


def log_exec_time(method):
    def timed_function(*args, **kw):
        line_length = 42
        logging.info("{0} start".format(method.__name__).center(line_length, '-'))
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()
        logging.info(('{0} Total time: %2.2f sec'.format(method.__name__) % (te-ts)).center(line_length, '-'))
        logging.info('%s' % ('-' * line_length))
        return result
    return timed_function


# TODO: change behavior so it takes screenshots before/after function ends
# TODO: Use context in order to access the webdriver and step name
def take_screenshot(method):
    def web_function(*args, **kw):
        result = method(*args, **kw)
        # self.driver.get_screenshot_as_file(os.path.join(os.getcwd(), "screenshots", screenshot_name))
        return result
    return web_function
