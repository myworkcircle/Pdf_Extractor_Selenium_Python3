import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options



class Pdf_Extractor:
    def __init__(self):
        """ Initialized Chromedriver"""
        download_dir = "/home/pallav/Documents/radicli/pdf_files/"
        profile = {
            "download.default_directory": download_dir, #Change default directory for downloads
            "download.prompt_for_download": False, #To auto download the file
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,
            "download.extensions_to_open": "applications/pdf",
            }
        Path_to_chromium = '/home/pallav/Downloads/chromedriver'
        chrome_option = Options()
        chrome_option.add_experimental_option("prefs", profile)
        self.driver = webdriver.Chrome(Path_to_chromium,chrome_options=chrome_option)

   
    def Link_1(self,url):
        self.driver.get(url)
        time.sleep(5)

        first_pdf_url = self.driver.find_element_by_xpath('/html/body/div[1]/section[4]/div/div[1]/div/div/a[2]')
        second_pdf_url = self.driver.find_element_by_xpath('/html/body/div[1]/section[4]/div/div[2]/div/div/a[2]')
        
        metadata = [{}]
        first_title = self.driver.find_element_by_xpath('/html/body/div[1]/section[4]/div/div[1]/div/div/h4').text
        second_title = self.driver.find_element_by_xpath('/html/body/div[1]/section[4]/div/div[2]/div/div/h4').text
        first_pdf = first_pdf_url.get_attribute('href')
        second_pdf = second_pdf_url.get_attribute('href')
        metadata.extend({'title':first_title,'title2':second_title})
        time.sleep(4)
        self.driver.get(first_pdf)
        time.sleep(5)
        self.driver.get(second_pdf)

    def Link_2(self,base_url):
        self.driver.get(base_url)
        time.sleep(5)

        links = self.driver.find_element_by_xpath('/html/body/div[1]/section[2]/div/div')
        url_element = []
        url_element = links.find_elements_by_css_selector('a')
        url_list = []

        for j in url_element:
            url_list.append(j.text)

        pdf_details = [{}]
        for i in url_list:
            try:
                run_test = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT,i)))
                run_test.click()
            except (StaleElementReferenceException, TimeoutException):
                pass
            time.sleep(4)
            
            """ Pdf Metadata Extraction"""
            title = self.driver.find_element_by_xpath('/html/body/div[1]/section[2]/div/div/table[1]/tbody/tr[4]/td[3]/h3/strong').text
            date = self.driver.find_element_by_xpath('/html/body/div[1]/section[2]/div/div/table[1]/tbody/tr[2]/td[3]/h2').text
            to = self.driver.find_element_by_xpath('/html/body/div[1]/section[2]/div/div/table[1]/tbody/tr[3]/td[3]/strong').text
            pdf_details.append({'title':title,'date':date,'to':to})
            """ Pdf Metadata Extraction Ends """


            pdf_location = self.driver.find_element_by_xpath('/html/body/div[1]/section[2]/div/div/table[1]/tbody/tr[1]/td[3]/strong/a')
            time.sleep(6)
            link_to_pdf = pdf_location.get_attribute('href')
            self.driver.get(link_to_pdf)
            time.sleep(6)
            self.driver.back()
            time.sleep(3)
    

    def Link_3(self,url):
        self.driver.get(url)
        time.sleep(5)

        links = self.driver.find_element_by_xpath('/html/body/div[1]/section[2]/div/div')
        url_element = []
        url_element = links.find_elements_by_css_selector('a')
        url_list = []

        pdf_details = []
        for j in url_element:
            url_list.append(j.get_attribute('href'))
            pdf_details.append(j.text)

        
        metadata = [{}]
        for i in range(0,len(url_list)-1):
            if(i!=1 and i!=2):
                self.driver.get(url_list[i])
                time.sleep(3)
        
        self.driver.get(url_list[len(url_list)-1])
        last_one = self.driver.find_element_by_xpath('/html/body/div[1]/section[2]/div/div/table/tbody/tr[1]/td[3]/strong/a')
        p_url = last_one.get_attribute('href')
        self.driver.get(p_url)


if __name__ == '__main__':

    bot = Pdf_Extractor()
    bot.Link_1('https://www.privacy.gov.ph/data-privacy-act-primer/')
    bot.Link_2('https://www.privacy.gov.ph/memorandum-circulars/')
    bot.Link_3('https://www.privacy.gov.ph/advisories/')




