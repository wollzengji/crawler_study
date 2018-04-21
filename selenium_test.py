from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

#使用本地chromedriver服务
browser = webdriver.Chrome(executable_path="D:\\selenium_server\\chromedriver")

#使用远程selenium-server服务
# browser = webdriver.Remote(
#    command_executor='http://127.0.0.1:4444/wd/hub',
#    desired_capabilities=DesiredCapabilities.CHROME)



try:
    browser.get('https://www.baidu.com')
    input = browser.find_element_by_id('kw')
    input.send_keys('Python')
    input.send_keys(Keys.ENTER)
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
    print(browser.current_url)
    print(browser.get_cookies())
    print(browser.page_source)
finally:
    browser.close()



# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
#
# driver = webdriver.Chrome(executable_path="D:\\selenium_server\\chromedriver")
# driver.get("http://www.python.org")
# assert "Python" in driver.title
# elem = driver.find_element_by_name("q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()