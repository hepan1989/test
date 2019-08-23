from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from appium_po.page.base_page import BasePage


class SearchPage(BasePage):


    def search(self,keyword):
        self.driver.find_element(By.ID, "search_input_text").send_keys(keyword)
        return self

    def select(self,index):
        # 选择第一个搜索的结果进行点击
        self.driver.find_elements(By.ID, "name")[index].click()

        return self

    def get_pric(self,stock_type):

        price = float(self.driver.find_element(By.XPATH,
                                               "//*[contains(@resource-id,'stockCode') and @text='" + stock_type + "']/../../..//*[contains(@resource-id,'current_price')]").text)
        return price

    def get_name(self):
        return self.driver.page_source
