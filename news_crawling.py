import requests
import pandas as pd
import re
from bs4 import BeautifulSoup

def clean_html(x):
  x = re.sub("\&\w*\;","",x)
  x = re.sub("<.*?>","",x)
  return x

def return_news_dataframe(news_query):
    client_id = #id
    client_secret = #key
    search_word = news_query 
    encode_type = 'json' 
    max_display = 10 
    sort = 'sim' 
    start = 1 

    url = f"https://openapi.naver.com/v1/search/news.{encode_type}?query={search_word}&display={str(int(max_display))}&start={str(int(start))}&sort={sort}"


    headers = {'X-Naver-Client-Id' : client_id,
            'X-Naver-Client-Secret':client_secret
            }

  
    r = requests.get(url, headers=headers)

    print(r)
    df = pd.DataFrame(r.json()['items'])
    df['title'] = df['title'].apply(lambda x: clean_html(x))
    df['description'] = df['description'].apply(lambda x: clean_html(x))
    return df

def get_naver_news(url):
    headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36" }

    res = requests.get(url, headers = headers)
    print(res)
    if res.status_code == 200:
        if 'news.naver.com' not in res.url:
            raise Exception('{}은 요청할 수 없는 url입니다'.format(res.url))
        
        soup = BeautifulSoup(res.text)
        title = soup.select_one("h3#articleTitle").text.strip()
        input_date = soup.select_one('span.t11').text.strip()
        article = soup.select_one('div#articleBodyContents').text.strip()
        article = article.replace('// flash 오류를 우회하기 위한 함수 추가 \nfunction _flash_removeCallback() {}', '')
        return title, input_date, article
    else:
        raise Exception("요청 실패 : {}".format(res.status_code))

def main():
    news_df = return_news_dataframe("코로나")
    urls = news_df['link']

    result = []
    error_cnt = 0
    for url in urls:
        print(url)
        try:
            info = get_naver_news(url)
            print(info)
            result.append(info)
        except:
            error_cnt += 1

    print('error_cnt : {}'.format(error_cnt))
    df = pd.DataFrame(result, columns = ['기사제목', '입력일', '기사내용'])
    df.to_csv('new_articles.csv', index = False, encoding = 'utf-8')
    print('종료')

if __name__ == "__main__":
    main()