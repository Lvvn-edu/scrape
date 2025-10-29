import requests
from bs4 import BeautifulSoup
import json
import re
import sys

URL = "http://books.toscrape.com/catalogue/category/books/travel_2/index.html"

def get_book_bs4(url):
    print(f"\nscrape2：使用BS4擷取Books to Scrape旅遊類書籍詳細資訊")
    books_data = []

    try:
        #發送GET請求
        print(f"正在請求: {url}")
        response = requests.get(url, timeout=10)
        response.raise_for_status() #檢查HTTP狀態碼
        #解決價格印出亂碼問題
        response.encoding = 'utf-8'
        
        #建立Soup物件
        soup = BeautifulSoup(response.text, 'lxml')
        
        #定位頁面上所有書籍的容器
        all_books = soup.find_all('article', class_='product_pod')
        
        if not all_books:
            print("警告：未找到書籍容器")
            return
        for book in all_books:
            # 擷取書名(Title)
            title_tag = book.select_one('h3 > a')
            title = title_tag.get('title', 'N/A') if title_tag else 'N/A'
            
            # 擷取價格
            price_tag = book.select_one('p.price_color')
            price = price_tag.text.strip() if price_tag else 'N/A'
            
            # 擷取評分
            rating_tag = book.select_one('p[class*="star-rating"]')
            rating = 'N/A'
            if rating_tag:
                class_list = rating_tag.get('class', [])
                if len(class_list) >= 2:
                    rating = class_list[1] 

            #整理成字典
            book_info = {
                'title': title,
                'price': price,
                'rating': rating
            }
            books_data.append(book_info)

        print(f"成功擷取 {len(books_data)} 本書籍的詳細資訊。")
        print("\n[JSON 輸出]")
        json_output = json.dumps(books_data, ensure_ascii=False, indent=4)
        print(json_output)

    except requests.exceptions.HTTPError as e:
        print(f"HTTP錯誤發生:{e}")
        print(f"狀態碼: {response.status_code if 'response' in locals() else '未知'}")
    except requests.exceptions.ConnectionError:
        print("連線錯誤：請檢查網路連線或目標網站是否可用。")
    except requests.exceptions.Timeout:
        print("請求超時：目標網站回應時間過長。")
    except requests.exceptions.RequestException as e:
        print(f"在發送請求或處理回應時發生未知錯誤: {e}")
    except Exception as e:
        print(f"發生一般性錯誤: {e}")

if __name__ == "__main__":

    get_book_bs4(URL)
