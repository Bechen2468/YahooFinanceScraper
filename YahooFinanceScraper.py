import random
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from Runtime_Data import Runtime_Data
from Settings_Flags import *
from difflib import get_close_matches



class YFScraper:
    def __init__(self):
        self.runtime_Data = Runtime_Data()
        return
    
    def sleep(self, minSeconds, maxSeconds):
        sleep_time = random.uniform(minSeconds, maxSeconds)
        self.runtime_Data.sleep_duration += sleep_time
        time.sleep(sleep_time)
        return

    def get_browser(self) -> webdriver.Firefox:
        browser_options = webdriver.FirefoxOptions()
        # start browser
        browser = webdriver.Firefox(options= browser_options)
        browser.fullscreen_window = True
        return browser

    def wait_for_browser(self, browser) -> bool:
        ready = False
        while(not ready):
            self.sleep(0.5, 0.8)
            ready = browser.execute_script("return document.readyState === 'complete';")
        self.sleep(2, 4)
        return ready

    def scroll(self, browser):
        loaded = False
        while(True):
            loaded = browser.execute_script("return document.readyState === 'complete';")

            if loaded and browser.execute_script("return document.body.scrollHeight === window.pageYOffset;"):
                break

            if loaded:
                loaded = False
                browser.execute_script("window.scrollTo(document.body.scrollWidth, document.body.scrollHeight);")
            self.sleep(0.3, 1)
        return
    
    def button_click(self, browser, button_name) -> bool:
        try:
            rejectCookieButton = browser.find_elements(By.NAME, button_name)
            if(len(rejectCookieButton) == 1):
                rejectCookieButton[0].click()
                success = True
        except Exception as e:
            success = False
        return success

    def scrape(self, tickers, flags = 0):
        self.runtime_Data.start()
        data = []
        browser = self.get_browser()

        for ticker in tickers:
            #region setup
            url = 'https://finance.yahoo.com/quote/{ticker}/analysis'
            browser.get(url)
            self.wait_for_browser(browser)
            #endregion

            #region handle cookie popup
            if self.button_click(browser, 'reject'):
                self.sleep(2, 5)
            #endregion

            #region check if ticker was found
            if 'analysis' not in browser.current_url:
                continue
            #endregion

            data['earnings_est'] = []

            if flags & EARNINGS_EST:
                data['earnings_est'].append(self.scrape_earnings_est(browser, ticker))



        self.runtime_Data.end()
        return
    

    def scrape_earnings_est(browser, ticker):
        browser.scroll()
        
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        data = []
        table = None
        found = True
        
        #region grab table
        try:
            css_selector = "table:-soup-contains('Earnings Estimate')"
            table = soup.select_one(css_selector)
        except Exception as e:
            print(e)
            found = False
        #endregion

        if found:
            #region grab dates
            try:
                for descriptor in ['Current Qtr.', 'Current Year']:
                    css_selector = "span:-soup-contains('" + descriptor + "')"
                    date = table.select_one(css_selector).parent
                    date = date.find_all('span')[0]
                    
                    month = 'January'
                    year = 0
                    quarterly = True
                    month_map_eng = ['January','February','March','April','May','June','July','August','September','October','November','December']
                
                    temp = date.find_all('span')
                    if len(temp) >= 2:
                        month = get_close_matches(temp[1].text, month_map_eng, n= 1)[0]
                    else:
                        quarterly = False

                    year = date.find_all('span')[1 if quarterly else 0].next_sibling.strip()
                    year = ''.join(char for char in year if char.isdigit())
                    year = int(year)

                    date = datetime.strptime(f"{month} {year}", "%B %Y")
                    data2 = [ticker, date, quarterly]
                    data.append(data2)
                
            except Exception as e:
                print(str(e)) #temp
            
            #endregion

            #region grab all Data
            try:
                descriptors = ['No. of Analysts', 'Avg. Estimate', 'Low Estimate', 'High Estimate', 'Year Ago EPS']
                names = ['analystCount', 'estAvg', 'estLowest', 'estHigh', 'EpsPrevYear']
                datatypes = [int, float, float, float, float]

                for i in range(0, len(descriptors)):
                    descriptor = descriptors[i]
                    name = names[i]
                    datatype = datatypes[i]

                    css_selector = "span:-soup-contains('" + descriptor +"')"
                    row = table.select_one(css_selector).parent.parent
                    cells = row.find_all('td')

                    c = 0
                    for j in [1, 3]:
                        value = cells[j].text
                        if value != 'N/A':
                            value = value.strip()
                            value = ''.join(char for char in value if char.isdigit() or char == ',')
                            value = value.replace(',', '.')
                            value = int(value) if datatype == int else (float(value) if datatype == float else value)
                        else:
                            value = None
                        data[c].append(value)
                        c += 1

            except Exception as e:
                print(e)
                found = False
            #endregion

        return data