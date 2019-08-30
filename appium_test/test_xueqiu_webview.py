from time import sleep
import pytest
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
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
        #caps["chromedriverExecutableDir"]="/user/.../chromedriver/2.20/"
        caps["chromedriverUseSystemExecutable"]=True  #默认是true，绕过自己配置的webdriver路径，使用系统下载的路径,此选项未生效
        caps["chromedriverExecutable"]="/user/.../chromedriver/2.20/chromedriver"

        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
        self.driver.implicitly_wait(20)
        #self.driver.tap()
        #self.driver.keyevent()
        #这个是主页面的元素，作用是等待元素出现在进行下一步的操作，类似显示等待
        self.driver.find_element(By.ID,"topic_author")



    @pytest.mark.skip()
    @pytest.mark.parametrize("search,expected",[("alibaba","阿里巴巴"),("xiaomi","小米集团-W"),("google","谷歌A")])
    def test_search(self,search,expected):
        self.driver.find_element(By.ID,"tv_search").click()
        self.driver.find_element(By.ID,"search_input_text").send_keys(search)
        self.driver.find_element(By.ID,"name").click()
        searchText=self.driver.find_element(By.ID,"stockName").text
        assert searchText==expected

    @pytest.mark.skip()
    @pytest.mark.parametrize("keyword,stock_type,expect_price",[
        ('alibaba','BABA',100),
        ('xiaomi', 'ximi', 8),
    ])
    def test_search_price(self,keyword,stock_type,expect_price):
        self.driver.find_element(By.ID, "tv_search").click()
        self.driver.find_element(By.ID, "search_input_text").send_keys(keyword)
        self.driver.find_element(By.ID, "name").click()
        price=float(self.driver.find_element(By.XPATH,"//*[contain(@id,'stockCode')] and @text='"+stock_type+"'/../../..//*[contain(@id,'current_price')]"))
        print(price)
        assert price>100
        assert_that(price,close_to(expect_price,expect_price*0.1))

    #测试webview
    def test_webview(self):
        for i in range(20):
            print(self.driver.contexts)
        self.driver.find_element(MobileBy.XPATH,"//*[@text='开户']").click()
        #self.driver.find_element(MobileBy.XPATH, "//*[@text='基金']").click()

        sleep(10)
        print("--------")


        #进入web页面，此时会有加载过程，打印出上下文
        for i in range(20):
            print(self.driver.contexts)

        WebDriverWait(self.driver,10,1).until(lambda x:"WEBVIEW_com.xueqiu.android" in self.driver.contexts)
        print("====切换前===")
        #返回带有webview组件树，此时可以使用原生定位去定位webview内的元素
        print(self.driver.page_source)
        self.driver.switch_to.context("WEBVIEW_com.xueqiu.android")
        print("-----切换后-----")
        #返回html，可使用selenium的方式定位
        print(self.driver.page_source)





    def setup(self):
        pass

    def teardown(self):
        #点击取消按钮，回到初始状态
        #self.driver.find_element(By.ID,"action_close")
        pass

    def teardown_class(self):
        sleep(10)
        self.driver.quit()