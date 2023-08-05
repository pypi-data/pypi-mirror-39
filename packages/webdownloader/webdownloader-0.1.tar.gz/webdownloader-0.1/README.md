# Instalatiom
```sh
pip install pywebextract
```
# Downloader
### Basic functional
```python
from webdownloader import Downloader
downloader = Downloader()
page_content = downloader.get_page('https://www.google.com/')
len(page_content)
# or you can return full response
response = downloader.get_page('https://www.google.com/', full_response=True)
response.status_code
# by default it will create 3 attempts to open connection if there is a problem with a server, but you can use custom amount
response = downloader.post_page('https://www.some-not-reliable-site.com/', specific_attempts_count=5)
```
### Proxies usage
```python
from webdownloader import Downloader
downloader = Downloader(proxy_string_list=['104.144.176.:3128', '102.152.145.103:3128', '157.152.145.103:3128'], change_proxies_manually=True)
# from one random proxy (if one of proxies is not working it will take another one)
page_content = downloader.get_page('https://www.google.com/')
# from the same proxy
page_content = downloader.get_page('https://www.google.com/')
# from random proxy
downloader.change_proxies()
page_content = downloader.get_page('https://www.google.com/')
````
### Cookies and headers
```python
from webdownloader import Downloader
downloader = Downloader()
# cookies as a dict
page_content = downloader.get_page('https://www.google.com/', cookies={'TOKEN': '1234567890'})
# cookies as a string (from browser)
page_content = downloader.get_page('https://www.google.com/', cookies_text='CONSENT=YES+UK.en+; SID=somesid')
# by default there is a user agent in headers but you can change all headers
page_content = downloader.get_page('https://www.google.com/', headers={'User-Agent': 'Mozilla/5.0'})
# get session sookies
session_cookies_dict = downloader.get_session_cookies()
# save cookies to file
downloader.save_cookies_to_file(session_cookies_dict, name='mycookies')
# load cookies from file
cookies_dict = downloader.get_cookies_from_file(name='mycookies')
````
# License
MIT
