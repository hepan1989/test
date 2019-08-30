from time import sleep
import pytest
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By
from hamcrest import *



'''
使参数化时，每次执行不重新启动app，使用fixture的方法
'''

class TestXueQiu:
    def setup_class(self):
        caps = {}
        caps["platformName"] = "android"
        caps["deviceName"] = "androdtest"
        caps["appPackage"] = "com.xueqiu.android"
        caps["appActivity"] = ".view.WelcomeActivityAlias"
        caps["autoGrantPermissions"]=True

        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
        self.driver.implicitly_wait(20)
        #self.driver.tap()
        #self.driver.keyevent()
        #这个是主页面的元素，作用是等待元素出现在进行下一步的操作，类似显示等待
        self.driver.find_element(By.ID,"topic_author")



    @pytest.fixture()
    def search_fixture(self):
        yield
        # 点击取消按钮，回到初始状态
        self.driver.find_element(By.ID, "action_close").click()

    @pytest.mark.parametrize("search,expected",[("alibaba","阿里巴巴"),("xiaomi","小米集团-W"),("google","谷歌A")])
    def test_search(self,search,expected):
        self.driver.find_element(By.ID,"tv_search").click()
        self.driver.find_element(By.ID,"search_input_text").send_keys(search)
        self.driver.find_element(By.ID,"name").click()
        searchText=self.driver.find_element(By.ID,"stockName").text
        assert searchText==expected

    @pytest.mark.parametrize("keyword,stock_type,expect_price",[
        ('alibaba','BABA',100),
        ('xiaomi', 'ximi', 8),
    ])
    #search_fixture加入fixture，完成此用例的自定义的teardown
    def test_search_price(self,search_fixture,keyword,stock_type,expect_price):
        self.driver.find_element(By.ID, "tv_search").click()
        self.driver.find_element(By.ID, "search_input_text").send_keys(keyword)
        self.driver.find_element(By.ID, "name").click()
        price=float(self.driver.find_element(By.XPATH,"//*[contain(@id,'stockCode')] and @text='"+stock_type+"'/../../..//*[contain(@id,'current_price')]"))
        print(price)
        assert price>100
        assert_that(price,close_to(expect_price,expect_price*0.1))


    def teardown_class(self):
        sleep(10)
        self.driver.quit()