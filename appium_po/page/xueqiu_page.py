#codong=utf-8

#雪球首页
from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from appium_po.page.profile_page import ProfilePage
from appium_po.page.search_page import SearchPage


class XueqiuPage:
    def __init__(self):
        caps = {}
        caps["platformName"] = "android"
        caps["deviceName"] = "androdtest"
        caps["appPackage"] = "com.xueqiu.android"
        caps["appActivity"] = ".view.WelcomeActivityAlias"
        caps["autoGrantPermissions"] = True
        caps["automationName"] = "Uiautomator2"


        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
        #隐式等待
        self.driver.implicitly_wait(15)
        #显示等待，判断升级的弹框是否出现
        WebDriverWait(self.driver,20).until(expected_conditions.visibility_of_all_elements_located((By.ID,"image_cancel")))
        print(self.driver.page_source)
        self.driver.find_element(By.ID,"image_cancel").click()
        # self.driver.tap()
        # self.driver.keyevent()
        # 这个是主页面的元素，作用是等待元素出现在进行下一步的操作，类似显示等待
        self.driver.find_element(By.ID, "topic_author")
        self.driver.find_element(By.XPATH, "//*[ @ text = '自选']").click()



    #使用公共方法代表这个页面提供的功能

    #进入搜索页
    def goto_search(self):
        # 点击搜索
        self.driver.find_element(By.ID, "action_search").click()
        return SearchPage(self.driver)

    #进入个人页
    def goto_profile(self):
        return ProfilePage()

    #推荐页面，没有进入新的页面，返回自身,并进行断言
    def get_default(self):
        return True