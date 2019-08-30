from time import sleep
import pytest
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By


class TestXueQiu:
    def setup(self):
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

    @pytest.mark.skip()
    def test_click_tap(self):
        self.driver.tap()

    @pytest.mark.skip()
    def test_sendkey_keyevent(self):
        self.driver.keyevent()

    @pytest.mark.skip()
    def test_get_attribute(self):
        self.driver.find_element(By.ID,"").get_attribute("")

    @pytest.mark.skip()
    def test_source(self):
        self.driver.page_source


    #进入首页后，向上滑动5次
    def test_swipe(self):
        for i in range(5):
            self.driver.swipe(200,1500,200,700)


    def test_swipe_precent(self):
        size=self.driver.get_window_size()
        print(size)
        x=size['width']
        y=size['height']

        self.driver.swipe(x*0.8,y*0.8,x*0.2,y*0.2,1000)
        self.driver.find_element_by_accessibility_id("Views").click()

    def test_uiautomator(self):
        self.driver.find_element_by_android_uiautomator('new UiScrollable('
                                                        'new UiSelector().scrollable(true)'
                                                        '.instance(0)).scrollIntoView(new UiSelector()'
                                                        '.text("WebView").instance(0));').click()

        element = self.driver.find_element(':uiautomator', 'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().text("WebView").instance(0));')

    def test_longPress(self):
        #长按，可传入元素，或坐标定位，及超时时间el=None, x=None, y=None, duration=1000
        TouchAction(self.driver).long_press()

    @pytest.mark.skip()
    def test_wrong_phone(self):
        self.driver.find_element(By.ID, "user_profile_icon").click()
        self.driver.find_element(By.ID,"iv_login_phone").click()
        self.driver.find_element(By.ID,"tv_login_with_account").click()
        self.driver.find_element(By.XPATH,'//android.widget.EditText[@text="请输入手机号或邮箱"]').send_keys("13717768110")
        self.driver.find_element(By.XPATH,'//android.widget.EditText[@text="请输入登录密码"]').send_keys("111111")
        self.driver.find_element(By.ID,"button_next").click()
        wrongText=self.driver.find_element(By.ID,"md_content").get_attribute("text")
        #print(wrongText)
        assert wrongText=="手机号码填写错误"

    @pytest.mark.skip()
    def test_wrong_password(self):
        self.driver.find_element(By.ID, "user_profile_icon").click()
        self.driver.find_element(By.ID, "iv_login_phone").click()
        self.driver.find_element(By.ID, "tv_login_with_account").click()
        self.driver.find_element(By.XPATH, '//android.widget.EditText[@text="请输入手机号或邮箱"]').send_keys("13717777777")
        self.driver.find_element(By.XPATH, '//android.widget.EditText[@text="请输入登录密码"]').send_keys("111111")
        self.driver.find_element(By.ID, "button_next").click()
        wrongText = self.driver.find_element(By.ID, "md_content").get_attribute("text")
        # print(wrongText)
        assert wrongText == "用户名或密码错误"

    @pytest.mark.skip()
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
    def test_search_price(self,keyword):
        self.driver.find_element(By.ID, "tv_search").click()
        self.driver.find_element(By.ID, "search_input_text").send_keys(keyword)
        self.driver.find_element(By.ID, "name").click()
        price=self.driver.find_element(By.XPATH,"//*[contain(@id,'stockCode')] and @text='BABA'/../../..//*[contain(@id,'current_price')]")
        print(price)
        assert price>100

    def teardown(self):
        sleep(10)
        self.driver.quit()


    def test_log(self):
        print(self.driver.log_types)
        #返回logcat（android的），bugreport，server（appium的）
        print(self.driver.get_log("logcat"))