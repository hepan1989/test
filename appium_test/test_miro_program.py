from appium import webdriver
from selenium.webdriver.common.by import By


class TestMicroProgram:

    def setup(self):
        caps = {}
        caps["platformName"] = "android"
        caps["deviceName"] = "androdtest"
        caps["appPackage"] = "com.tencent.mm"
        caps["appActivity"] = ".ui.LauncherUI"
        caps["noReset"]=True
        #caps["autoGrantPermissions"] = True
        # caps["chromedriverExecutableDir"]="/user/.../chromedriver/2.20/"
        #caps["chromedriverUseSystemExecutable"] = True  # 默认是true，绕过自己配置的webdriver路径，使用系统下载的路径,此选项未生效
        #caps["chromedriverExecutable"] = "/user/.../chromedriver/2.20/chromedriver"

        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
        self.driver.implicitly_wait(20)

    def test_xueqiu(self):
        self.driver.find_element(By.XPATH,"//*[@text='文件传输助手']").click()
        self.driver.find_element(By.XPATH, "//*[@text='雪球股票']").click()
        print(self.driver.page_source)
        self.driver.find_element(By.XPATH, "//android.widget.Image[@index='0']").click()
        self.driver.find_element(By.XPATH, "//android.widget.EditText[@text='请输入股票名称/代码']").send_keys("alibaba")
        self.driver.find_element(By.XPATH, "//android.view.View[ @ text = '阿里巴巴']").click()