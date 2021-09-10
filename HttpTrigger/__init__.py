import logging

import azure.functions as func
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def main(req: func.HttpRequest, msg: func.Out[func.QueueMessage]) -> str:
    logging.info('Python HTTP trigger function processed a request.')

    options = Options()
    options.headless = True

    driver = webdriver.Firefox(options=options)
    driver.get("https://tnhlab.org/vaccination")
    title = driver.title
    logging.info(f"Page Title: {title}")

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        msg.set(name)
        return func.HttpResponse(f"Hello, {name}. You just visited {title}")
    else:
        return func.HttpResponse(
             f"You just visited {title}",
             status_code=200
        )
