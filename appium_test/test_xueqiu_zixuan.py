# coding=utf-8

from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import pytest
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from hamcrest import *
from selenium.webdriver.support.wait import WebDriverWait

'''
使参数化时，每次执行不重新启动app
'''

class TestXueQiu:
    def setup_class(self):
        caps = {}
        caps["platformName"] = "android"
        caps["deviceName"] = "androdtest"
        caps["appPackage"] = "com.xueqiu.android"
        caps["appActivity"] = ".view.WelcomeActivityAlias"
        caps["autoGrantPermissions"]=True
        caps["automationName"]="Uiautomator2"

        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
        self.driver.implicitly_wait(20)
        #self.driver.tap()
        #self.driver.keyevent()
        #这个是主页面的元素，作用是等待元素出现在进行下一步的操作，类似显示等待
        self.driver.find_element(By.ID,"topic_author")
        self.driver.find_element(By.XPATH, "//*[ @ text = '自选']").click()

    @pytest.fixture()
    def add_fixture(self):
        yield
        # 点击取消按钮，回到初始状态
        self.driver.find_element(By.ID, "action_close").click()

    @pytest.mark.skip()
    @pytest.mark.parametrize("keyword,stock_type",[
        ('alibaba','BABA'),
        ('xiaomi', '01810'),
    ])
    def test_search_add(self,keyword,stock_type):
        #点击搜索
        self.driver.find_element(By.ID, "action_search").click()
        #输入搜索值
        self.driver.find_element(By.ID, "search_input_text").send_keys(keyword)
        #选择第一个搜索的结果进行点击
        self.driver.find_element(By.ID, "name").click()
        #add_status=self.driver.find_element(By.XPATH,"//*[contain(@id,'stockCode')] and @text='"+stock_type+"'/../../..//*[contain(@text,'加自选')]")
        self.driver.implicitly_wait(20)
        self.driver.find_element(By.XPATH,"//*[contains(@resource-id,'stockCode') and @text='"+stock_type+"']/../../..//*[contains(@text,'加自选')]").click()

        followed_btn=self.driver.find_element(By.XPATH,"//*[contains(@resource-id,'stockCode') and @text='"+stock_type+"']/../../..//*[contains(@text,'已添加')]")

        assert followed_btn.text=='已添加'
        self.driver.implicitly_wait(20)

    def test_cancel(self):
        self.driver.implicitly_wait(20)
        stockName = self.driver.find_element(By.ID, "portfolio_stockName")
        TouchAction(self.driver).long_press(el=stockName, duration=3000).release().perform()
        self.driver.implicitly_wait(20)
        self.driver.find_element(By.XPATH,"//*[@text='删除']").click()
        self.is_toast_exist("已从自选删除")==True


    def setup(self):
        pass

    def teardown(self):
        pass

    def teardown_class(self):
        sleep(10)
        self.driver.quit()

    #判断是否存在toast提示，message输入需要判断的提示信息，找到就返回true
    def is_toast_exist(self, message):
        try:
            element = WebDriverWait(self.driver, 10, 0.01).until(
                EC.presence_of_all_elements_located((By.XPATH, '//*[@text=\'{}\']'.format(message))))
            for i in element:
                print
                i.text
            return True
        except Exception as e:
            return False


