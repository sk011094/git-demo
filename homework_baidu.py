from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import time
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize the service object
service_obj = Service('./chromedriver')
driver = webdriver.Chrome(service=service_obj)

# 關鍵字列表
keywords = ['吉伊卡哇', '小八貓', '小泽亚李', 'hello kitty', '布丁狗', 'kuromi']

# 定義函數以獲取元素
def get_element(driver, xpath):
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))

# 定義搜索函數
def search_keyword(driver, keyword, retries=3):
    try:
        # 重新加載首頁
        url = "https://baike.baidu.com/"
        driver.get(url)

        # 等待搜索框可見並可操作
        search = get_element(driver, '//input[@class="searchInput"]')

        # 清空搜索框，輸入關鍵字
        search.clear()  
        search.send_keys(keyword)
        search.send_keys(Keys.ENTER)

        # 等待搜索結果頁面加載
        search_title = get_element(driver, "//div[@class='lemmaTitleBox_JGWzt']//h1").text
        search_result = get_element(driver, "//div[@class='lemmaSummary_mCyDI J-summary']").text
        search_result1 = get_element(driver, "//div[@class='J-lemma-content']").text

        # 輸出結果
        print(f"關鍵字: {keyword}")
        print("標題:\n", search_title, "\n")
        print("搜索結果:\n", search_result, "\n")
        print("搜索結果:\n", search_result1, "\n")
        print("---------------------------------------------")

    except (NoSuchElementException, TimeoutException):
        print(f'關鍵字 "{keyword}" 的搜索結果定位失敗')
        print('沒有搜索結果')
        print("---------------------------------------------")
        return

    except StaleElementReferenceException:
        if retries > 0:
            print(f"關鍵字 {keyword} 的元素已經過期，正在重試...（剩餘重試次數：{retries}）")
            time.sleep(3)  # 增加一個短暫的等待時間，讓頁面穩定
            search_keyword(driver, keyword, retries - 1)
        else:
            print(f"關鍵字 {keyword} 重試失敗，跳過該關鍵字。")
            print("---------------------------------------------")

# 依次搜索每個關鍵字
for keyword in keywords:
    search_keyword(driver, keyword, retries=10) 

# 關閉瀏覽器
driver.quit()
