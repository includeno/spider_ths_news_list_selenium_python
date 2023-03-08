from selenium import webdriver
from selenium.webdriver.common.by import By
import re
from bs4 import BeautifulSoup
import pandas as pd
import time

def get_driver_options():
    import platform

    if platform.system() == 'Windows':
        print('当前系统为 Windows')
        # 设置浏览器选项
        options = webdriver.FirefoxOptions()
        #options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        #options.add_argument('--headless')
        options.add_argument('--disable-extensions')
        #options.add_argument('--disable-gpu')
        return options
    elif platform.system() == 'Linux':
        print('当前系统为 Linux')
        # 设置浏览器选项
        options = webdriver.FirefoxOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--headless')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        return options
    elif platform.system() == 'Darwin':
        print('当前系统为 macOS')
        # 设置浏览器选项
        options = webdriver.FirefoxOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        #options.add_argument('--headless')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        return options
    else:
        print('无法确定当前系统类型')
        return None
    
    
def get_table(count=None):
    csv_file="links.csv"
    start_urls=[
        'https://stock.10jqka.com.cn/usstock/mgyw_list/',
        'https://stock.10jqka.com.cn/usstock/mggsxw_list/',
        'https://stock.10jqka.com.cn/usstock/gjgs_list/',
        'https://stock.10jqka.com.cn/usstock/zggxw_list/',
        'https://stock.10jqka.com.cn/usstock/mgcbsj_list/',
        'https://stock.10jqka.com.cn/usstock/mgscfx_list/',
        'https://stock.10jqka.com.cn/usstock/mgxg_list/',
    ]
    if(count!=None):
        start_urls=start_urls[:count]
    script='window.scrollTo(0, document.body.scrollHeight);'

    result_list=[]
    page_count=0
    
    for start_url in start_urls:
        url=start_url
        driver = webdriver.Firefox(options=get_driver_options())
        if(driver==None):
            print("driver does not exist",flush=True)
            raise Exception("system driver error")
        time.sleep(10)
        result=[]
        while(url!=None):
            # 设置最大等待时间为10秒
            driver.implicitly_wait(10)
            driver.set_page_load_timeout(15)
            html = ""
            try:
                time.sleep(3)
                driver.get(url)
                html = driver.page_source
            except Exception as e:
                print("driver error",e,flush=True)
                html = driver.page_source
            print("========"*15)
            print("url:",url)
            print("page_count:",page_count)
            print("html:",len(html),flush=True)
            # 获取页面源代码
            soup = BeautifulSoup(html, 'html.parser')

            news_list = soup.select_one('div[class="list-con"]')
            try:
                for li in news_list.find_all(name='li'):
                    title=li.select_one('span[class="arc-title"]').select_one('a').text.strip()
                    time_str=li.select_one('span[class="arc-title"]').select_one('span').text.strip()
                    news_url=li.select_one('span[class="arc-title"]').select_one('a').get('href').strip()
                    des=li.select_one('span[class="arc-title"]').select_one('a').text.strip()

                    temp={'link':news_url,'title':title,'time':time_str,'des':des}
                    print("line:",str(temp))
                    result.append(temp)
            except:
                print("news_list error",news_list,flush=True)
                time.sleep(3)
                continue
            result_list=result_list+result
            page_count=page_count+1
            
            try:
                next_page_url = soup.select_one('a[class="next"]').get('href').strip()
                url=next_page_url
            except:
                url=None
                print("next_page_url error",flush=True)
                break
        print("result:",(result),flush=True)
        df = pd.DataFrame(result, columns=['link','title','time','des'])
        try:
            csv_df=pd.read_csv(csv_file,index=False)
            csv_df.merge(df)
            csv_df.drop_duplicates(subset=['link'],keep='last',inplace=True)
            csv_df.to_csv(csv_file)
            print("csv 合并成功",flush=True)
        except:
            df.to_csv(csv_file,index=False)
            print("csv 新建成功",flush=True)
    
    driver.quit()
    return csv_file,result_list

#get_table(1)