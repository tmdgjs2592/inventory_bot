import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from selenium import webdriver
import time
import random
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By



class WelcomeScreen(QDialog):
    def __init__(self):
        self.widget_count = 0
        super(WelcomeScreen, self).__init__()
        loadUi("ui/InventoryGUI.ui", self)
        self.websites.clicked.connect(self.gotowebsite)

    def gotowebsite(self):
        website = WebsiteScreen()
        if self.widget_count < 1:
            widget.addWidget(website)
            self.widget_count += 1
        widget.setCurrentIndex(widget.currentIndex() +1)
        

class WebsiteScreen(QDialog):
    def __init__(self):
        self.count = 1
        self.back = self.count -1
        super(WebsiteScreen, self).__init__()
        loadUi("ui/Websites.ui", self)
        self.amazon1.clicked.connect(self.gotoAmazon)
        self.amazon1.clicked.connect(Amazon().show)
        self.target.clicked.connect(self.gotoTarget)
        self.back_btn.clicked.connect(self.go_back)

    
    def gotoAmazon(self):
        amazon = Amazon()
        widget.addWidget(amazon)
        widget.setCurrentIndex(widget.currentIndex() + self.count)
        self.count +=1
        

    def gotoTarget(self):
        target = Target()
        widget.addWidget(target)
        widget.setCurrentIndex(widget.currentIndex() + self.count)
        self.count += 1
        
        
    
    def go_back(self):
        loadUi("ui/InventoryGUI.ui", self)
        widget.setCurrentIndex(widget.currentIndex() - 1)


class Amazon(QDialog):
    def __init__(self):
        self.ps5_amazon = 0
        super(Amazon, self).__init__()
        loadUi("ui/Amazon.ui", self)
        self.back_btn.clicked.connect(self.go_back)
        self.submit.clicked.connect(self.amazon_login)

    def amazon_login(self):
        options = webdriver.ChromeOptions()
        # options.add_argument('--proxy-server=%s' % py)
        options.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'")
        options.headless=True
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)    
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")

        driver = webdriver.Chrome(executable_path=r"C:\Users\tmdgj\Downloads\chromedriver_win32\chromedriver.exe", options=options)

        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'})
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        amazon_user = self.amazon_email.text()
        amazon_pswd = self.amazon_password.text()
        URL = 'https://www.amazon.com/gp/css/order-history?ref_=nav_AccountFlyout_orders'
        try:
            driver.get(URL)
            for keys in amazon_user:
                driver.find_element_by_id("ap_email").send_keys(keys)
            driver.find_element_by_id("continue").click()
            time.sleep(1.0)
            if driver.find_elements_by_xpath("//h4[contains(text(), 'There was a problem')]"):
                raise ValueError
            time.sleep(1.0)
            driver.find_element_by_id("ap_password").send_keys(amazon_pswd)
            driver.find_element_by_id('signInSubmit').click()
            time.sleep(1.0)
            if driver.find_elements_by_xpath("//h4[contains(text(), 'There was a problem')]"):
                raise ValueError
            add_phone = driver.find_elements_by_xpath("//h1[contains(text(), 'Add mobile number')]")
            if len(add_phone)>0:
                driver.find_element_by_id("ap-account-fixup-phone-skip-link").click()
            
            # if driver.find_elements_by_xpath("//span[contains(text(), 'For your security, approve the notification sent to:')]"):
            #     pass
        except ValueError:
            self.error.setText("Incorrect Email or Password.")
        time.sleep(2.0)
        data = driver.find_elements_by_partial_link_text('PlayStation 5 Console')
        driver.find_element_by_link_text('2').click()
        time.sleep(1.0)
        data2 = driver.find_elements_by_partial_link_text('PlayStation 5 Console')
        total = len(data) + len(data2)
        self.ps5_amazon = total
        self.profit_ps5 = 200 * total

        self.amazon_table()

    def amazon_table(self):
        self.back_btn.clicked.connect(self.go_back2)
        super(Amazon, self).__init__()
        data=loadUi("ui/amazon_ps5.ui", self)
        widget.addWidget(data)
        widget.setCurrentIndex(widget.currentIndex() +1)
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 342)
        self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(str(self.ps5_amazon)))
        self.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(str(self.profit_ps5)))

    def go_back(self):
        loadUi("ui/Websites.ui",self)
        widget.setCurrentIndex(1)
    
    def go_back2(self):
        loadUi("ui/Websites.ui",self)
        widget.setCurrentIndex(1)


class Target(QDialog):
    def __init__(self):
        self.ps5_target = 0
        super(Target,self).__init__()
        loadUi("ui/Target.ui", self)
        self.back_btn.clicked.connect(self.go_back)
        self.submit.clicked.connect(self.target_login)

    def target_login(self):
        
        options = webdriver.ChromeOptions()
        # options.add_argument('--proxy-server=%s' % py)
        options.add_argument("user-agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'")
        options.headless=False
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)    
        options.add_argument("--disable-blink-features")
        options.add_argument("--disable-blink-features=AutomationControlled")

        driver = webdriver.Chrome(executable_path=r"C:\Users\tmdgj\Downloads\chromedriver_win32\chromedriver.exe", options=options)

        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'})
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        URL = 'https://www.target.com/account/orders?lnk=acct_nav_my_account'
        target_user = self.emailfield.text()
        target_password = self.password.text()
        try:
            driver.get(URL)
            time.sleep(1.0)
            for key in target_user:
                time.sleep(random.uniform(0.1, 0.2))
                driver.find_element_by_xpath("//input[@name='username']").send_keys(key)
            for key in target_password:
                password = driver.find_element_by_xpath("//input[@name='password']")
                password.send_keys(key)
                time.sleep(random.uniform(0.1 ,0.2))
            signin = driver.find_element_by_xpath("//button[@id = 'login']")
            signin.click()
            time.sleep(0.5)
            no_account = driver.find_elements_by_xpath("//div[contains(text(), 'That password is incorrect')]")
            no_account1 = driver.find_elements_by_xpath("//span[@id='username--ErrorMessage']")
            no_account2= driver.find_elements_by_xpath("//span[@id='password--ErrorMessage']")
            if len(no_account) > 0 or len(no_account1)>0 or len(no_account2)>0:
                raise ValueError
        except ValueError:
            self.error.setText("Incorrect Email or Password.")
        time.sleep(1.5)
        ps5_cancel = driver.find_elements_by_xpath("//p[contains(text(), 'Canceled')]" and "//img[@alt='PlayStation 5 Digital Edition Console']")
        ps5_img = driver.find_elements_by_xpath("//img[@alt='PlayStation 5 Digital Edition Console']")
        self.ps5 = len(ps5_img) - len(ps5_cancel)
        self.profit_target = self.ps5 * 250
        self.target_table()
        
    
    def target_table(self):
        self.back_btn.clicked.connect(self.go_back2)
        super(Target, self).__init__()
        data=loadUi("ui/target_table.ui", self)
        widget.addWidget(data)
        widget.setCurrentIndex(widget.currentIndex() +1)
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 342)
        self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem(str(self.ps5)))
        self.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(str(self.profit_target)))
        
    
    def go_back(self):
        loadUi("ui/Websites.ui", self)
        widget.setCurrentIndex(1)

    def go_back2(self):
        loadUi("ui/Websites.ui", self)
        widget.setCurrentIndex(1)
     


app = QApplication(sys.argv)
welcome=WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(800)
widget.setFixedWidth(1200)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")