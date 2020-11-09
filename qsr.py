import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

PATH = "path/to/your/chromedriver"
driver = webdriver.Chrome(executable_path=PATH)


def test_results(results):
    "needs driver.find_element_by_id('result-stats')"
    # if a huge number then keep going
    txt = results.text.split()

    ind = txt.index('results') - 1

    if txt[ind].count(',') > 1:
        return True
    else:
        return False

def click_last_page(driver):
    span = driver.find_element_by_id('xjs')
    #     table = span.find_elements_by_css_selector("*")[1]

    ind = []
    for child in span.find_elements_by_css_selector("*"):
        if child.tag_name == 'tbody':
            nav = child.find_elements_by_css_selector("*")[0]

            for sc in nav.find_elements_by_css_selector("*"):
                e = sc, sc.tag_name, sc.text
                ind.append(e)

    last_page = [(el, tag, text) for (el, tag, text) in ind if len(text) != 0 and text != 'Next'][-1][0]
    last_page.click()


def get_QSR(query, path=PATH):
    """
    :param query: (str) query to search for
    :param path: (str) path to chromedriver
    :return: (int) qsr - number of quoted search results - can be thought of as competition metric
    """
    start = time.time()
    driver = webdriver.Chrome(executable_path=PATH)
    split_query = query.split()

    if len(split_query) > 5:
        return "Use a shorter query"
    elif len(split_query) == 5:

        w1, w2, w3, w4, w5 = split_query[0], split_query[1], split_query[2], split_query[3], split_query[4]
        url = f"https://www.google.com/search?q={w1}+{w2}+{w3}+{w4}+{w5}&num=100"
    elif len(split_query) == 4:

        w1, w2, w3, w4 = split_query[0], split_query[1], split_query[2], split_query[3]
        url = f"https://www.google.com/search?q={w1}+{w2}+{w3}+{w4}&num=100"
    elif len(split_query) == 3:

        w1, w2, w3 = split_query[0], split_query[1], split_query[2]
        url = f"https://www.google.com/search?q={w1}+{w2}+{w3}&num=100"
    elif len(split_query) == 2:
        w1, w2 = split_query[0], split_query[1]
        url = f"https://www.google.com/search?q={w1}+{w2}&num=100"
    else:
        w1 = split_query[0]
        url = f"https://www.google.com/search?q={w1}&num=100"

    driver.get(url)

    # check to see if we need to scroll
    try:
        test = driver.find_element_by_id('result-stats')
        click_to_last = test_results(results=test)
    except:
        click_to_last = True

    if not click_to_last:
        qsr_ind = test.text.split().index('results') - 1
        qsr = test.text.split()[qsr_ind]
        driver.close()

        return int(qsr.replace(',', ''))

    else:
        pass

    span = driver.find_element_by_id('xjs')

    ind = []
    for child in span.find_elements_by_css_selector("*"):
        if child.tag_name == 'tbody':
            nav = child.find_elements_by_css_selector("*")[0]

            for sc in nav.find_elements_by_css_selector("*"):
                e = sc, sc.tag_name, sc.text
                ind.append(e)

    last_page = [(el, tag, text) for (el, tag, text) in ind if len(text) != 0 and text != 'Next'][-1][0]
    last_page.click()

    try:
        res = driver.find_element_by_id('result-stats').text
    except Exception as e:
        # click previous
        span = driver.find_element_by_id('xjs')
        ind = []
        for child in span.find_elements_by_css_selector("*"):
            if child.tag_name == 'tbody':
                nav = child.find_elements_by_css_selector("*")[0]

                for sc in nav.find_elements_by_css_selector("*"):
                    e = sc, sc.tag_name, sc.text
                    ind.append(e)

        prev_page = [(el, tag, text) for (el, tag, text) in ind if len(text) != 0 and text != 'Next'][0][0]
        prev_page.click()

        res = driver.find_element_by_id('result-stats').text

    driver.quit()

    qsr_ind = res.split().index('results') - 1
    qsr = res.split()[qsr_ind]

    end = time.time()
    print("Scrape took " + str(round(end - start, 4)) + " seconds")
    return int(qsr.replace(',', ''))
