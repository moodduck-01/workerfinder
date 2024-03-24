import requests, os, re
from time import sleep
from bs4 import BeautifulSoup

url = "https://zelenka.guru/"
bot_token = "7084551552:AAEiCt34ot6PcUAO62fCqISeCX8dI0vElEI"
chat_id = "-1002076612134"

def sendToTelegram(message):
    url = f"https://api.telegram.org/bot7084551552:AAEiCt34ot6PcUAO62fCqISeCX8dI0vElEI/sendMessage"
    params = {"chat_id": "-1002076612134", "text": message}
    requests.post(url, params=params)

def getPostsLinks(content: str) -> list:
    try:
        postsLinks = []
        soup = BeautifulSoup(content, 'lxml')
        posts = soup.find_all('div', class_='discussionListItem')
        if posts:
            for post in posts:
                post_link = post.find('a', class_='listBlock').get('href')
                postsLinks.append(url + post_link)
            return postsLinks
        else:
            print('Тем нет')
    except: pass

def getPostsInfo(content: str):
    postName = ""
    postText = ""
    author = ""
    authorTG = ""
    prefixes = ""
    soup = BeautifulSoup(content, 'lxml')

    title_bar = soup.find('div', class_='titleBar')
    if title_bar:
        post_name_element = title_bar.find('h1')
        if post_name_element:
            postName = post_name_element.text.strip()
        else:
            postName = "Название поста не найдено"
    else:
        postName = "Название поста не найдено"

    try: 
        prefix_elements = title_bar.find_all('span', class_='prefix')
        prefixes = [prefix.text.strip() for prefix in prefix_elements]
    except:
        prefixes = ""

    user_text = soup.find('div', class_='userText')
    if user_text:
        author_element = user_text.find('span', class_='style2')
        if author_element:
            author = author_element.text.strip()
        else:
            author = "Автор не найден"
    else:
        author = "Автор не найден"

    message_text = soup.find('blockquote', class_='messageText')
    if message_text:
        postText = message_text.text.strip()
    else:
        postText = "Текст сообщения не найден"

    telegram_link = soup.find('a', class_="button")
    if telegram_link:
        tg = telegram_link['href']
        if "t.me" in tg:
            authorTG = tg
        else:
            authorTG = "Ссылка на Telegram не найдена"
    else:
        authorTG = "Ссылка на Telegram не найдена"
    return postName, postText, author, authorTG, prefixes

def workerParser():
    try:
        headers = {
            'authority': 'zelenka.guru',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7',
            'cache-control': 'max-age=0',
            'cookie': '_ga=GA1.1.577208103.1695888902; G_ENABLED_IDPS=google; _ym_uid=1697462160500270260; _ym_d=1697462160; xf_user=6695939%2C2b17a6cb8a010f5a9b304409670c561fd8bf5bda; xf_logged_in=1; zelenka.guru_xf_tc_lmad=%5B%22707bc75d150c0ab4753d9e2f21634f93%22%5D; dfuid=763fda819e5c1f3b8de63a753e3cf66c; xf_session=ce8350d9d09e43d1f27f92db88560c42; _ga_J7RS527GFK=GS1.1.1711181317.42.1.1711181343.0.0.0',
            'sec-ch-ua': '"Not A(Brand";v="99", "Opera GX";v="107", "Chromium";v="121"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0',
        }
        
        r = requests.get(f'https://zelenka.guru/forums/832/', headers=headers)
        if r.status_code == 200:
            postsLinks = getPostsLinks(r.text)
            if postsLinks:
                for link in postsLinks:
                    r = requests.get(link, headers=headers)
                    if r.status_code == 200:
                        postName, postText, author, authorTG, prefixes = getPostsInfo(r.text)
                        message = f"📍 Название темы: {postName.strip()} ({', '.join(prefixes) or 'Без префиксов'})\n👶 Автор: {author.strip()}\n\n{postText.strip()}\n\n{'🟢 TG: https:' + authorTG.strip() if 't.me' in authorTG else '🔴 TG: Ссылка на Telegram не найдена' }"
                        sendToTelegram(message)
                    sleep(1)

        for i in range(2, 10 + 1):
            r = requests.get(f'https://zelenka.guru/forums/832/page-{i}', headers=headers)
            if r.status_code == 200:
                postsLinks = getPostsLinks(r.text)
                if postsLinks:
                    for link in postsLinks:
                        r = requests.get(link, headers=headers)
                        if r.status_code == 200:
                            postName, postText, author, authorTG, prefixes = getPostsInfo(r.text)
                            message = f"📍 Название темы: {postName.strip()} ({', '.join(prefixes) or 'Без префиксов'})\n👶 Автор: {author.strip()}\n\n{postText.strip()}\n\n{'🟢 TG: https:' + authorTG.strip() if 't.me' in authorTG else '🔴 TG: Ссылка на Telegram не найдена' }"
                            sendToTelegram(message)
                        sleep(1)
    except Exception as e:
        print(e)

def main():
    workerParser()

if __name__ == "__main__":
    main()