import requests
import re
import sys

URL = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"

def get_prices_re(url):

    print(f"\nscrape1：使用RE擷取Books to Scrape旅遊類書籍價格")
    try:
        #發送GET請求並取得HTML原始碼
        print(f"正在請求: {url}")
        response = requests.get(url, timeout=10)
        
        #檢查HTTP狀態碼，如果不是2xx則拋出異常
        response.raise_for_status()
        html_content = response.text

        #解決價格印出亂碼問題
        response.encoding = 'utf-8'
    
        price_pattern = re.compile(r'£\d+\.\d{2}')
        
        #使用re.findall()找出所有符合價格格式的字串
        all_prices = price_pattern.findall(html_content)
        
        print(f"成功找到 {len(all_prices)} 個價格。")
        print("\n[價格列表]")
        print(all_prices)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP錯誤發生:{e}")
        print(f"狀態碼:{response.status_code if 'response' in locals() else '未知'}")
    except requests.exceptions.ConnectionError:
        print("連線錯誤：請檢查網路連線或目標網站是否可用。")
    except requests.exceptions.Timeout:
        print("請求超時：目標網站回應時間過長。")
    except requests.exceptions.RequestException as e:
        print(f"在發送請求或處理回應時發生未知錯誤: {e}")
    except Exception as e:
        print(f"發生一般性錯誤: {e}")

if __name__ == "__main__":
    get_prices_re(URL)