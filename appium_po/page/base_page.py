from selenium.webdriver.remote.webdriver import WebDriver


class BasePage:
    # 当driver在各类的传递过程中，已经不能识别出driver的类型，需要使用driver:WebDriver类型推导
    def __init__(self,driver:WebDriver):
        self.driver=driver

    def find(self):
        #todo：处理弹框 异常处理 动态福鼎的元素处理
        pass
