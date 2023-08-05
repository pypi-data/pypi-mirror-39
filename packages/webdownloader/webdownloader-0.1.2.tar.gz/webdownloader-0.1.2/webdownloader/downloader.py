import validators
import logging
import random
import requests
import requests.utils
import json


class Downloader:
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'
    attempts = 3
    default_timeout = 45
    http_requests = None
    proxies = {}
    use_proxy = False
    change_proxies_manually = False
    use_session = False
    proxy_string_list = []
    failed_proxy_string_list = []

    def __init__(self, use_session=True, proxy_string_list=[], change_proxies_manually=False):
        """
        Initiation of the class
            :param self: 
            :param use_session=True: Are we going to keep session between requests?
            :param proxy_string_list=[]: Proxies list. (For example: '104.144.176.107:3128', '104.227.106.190:3128', by default proxies will change after each request)
            :param change_proxies_manually=False: Are we going to change proxies only manually?
        """
        self.use_session = use_session
        if proxy_string_list:
            self.change_proxies_manually = change_proxies_manually
            if change_proxies_manually:
                self.use_session = True
            else:
                self.use_session = False
            self.use_proxy = True
            self.attempts += 3
            self.proxy_string_list = proxy_string_list
        self.load_requests()

    def create_request(self, type, url, cookies={}, data={}, cookies_text='', headers={}, timeout=None, full_response=False, render_page=False, specific_attempts_count=None):
        """
        Create request
            :param self: 
            :param type: Type of the request (post/get)
            :param url: Url
            :param cookies={}: Cookies
            :param data={}: Payload data
            :param cookies_text='': Cookies in text mode. (It overwrites other cookies!)
            :param headers={}: Headers of the request. (It overwrites cookies and user agent!)
            :param timeout=None: Timeout for the request. (If None it will use default_timeout)
            :param full_response=False: Do we need to return full response or only text?
            :param render_page=False: Do we need to render page?
            :param specific_attempts_count=None: Set some int value to use custom attempts count
        """
        if not validators.url(url):
            logging.error('Url: {url} is not valid. Cannot create {type} request'.format(url=url, type=type))
            if full_response == False:
                return ''
            return None
        if headers == {}:
            headers = {'User-Agent': self.user_agent}
            if cookies_text != '':
                headers['Cookie'] = cookies_text
        if not specific_attempts_count:
            attempts = self.attempts
        else:
            attempts = specific_attempts_count
        if not timeout:
            timeout = self.default_timeout
        while attempts > 0:
            if self.use_proxy:
                if self.change_proxies_manually:
                    if self.proxies == {}:
                        self.proxies = self.get_random_proxies()
                else:
                    self.proxies = self.get_random_proxies()
                if attempts == 1:
                    self.proxies = {}
                    logging.warning('Cannot create {type} request to {url} with proxies. Will create request without it'.format(type=type, url=url))
            try:
                if type == 'post':
                    r = self.http_requests.post(url, cookies=cookies, data=data, headers=headers, proxies=self.proxies, timeout=timeout)
                else:
                    r = self.http_requests.get(url, cookies=cookies, params=data, headers=headers, proxies=self.proxies, timeout=timeout)
                if full_response:
                    return r
                else:
                    if render_page:
                        return self.render_html_page(r.text)
                    return r.text
            except:
                if self.use_proxy:
                    if self.change_proxies_manually is False:
                        self.mark_proxies_as_failed()
                attempts = attempts - 1
        logging.error('Cannot create {type} request to {url}'.format(type=type, url=url))
        if full_response == False:
            return ''

    def get_page(self, url, cookies={}, data={}, cookies_text='', headers={}, timeout=None, full_response=False, render_page=False, specific_attempts_count=None):
        """
        Create get request
            :param self: 
            :param url: Url
            :param cookies={}: Cookies
            :param data={}: Payload data
            :param cookies_text='': Cookies in text mode. (It overwrites other cookies!)
            :param headers={}: Headers of the request. (It overwrites cookies and user agent!)
            :param timeout=None: Timeout for the request. (If None it will use default_timeout)
            :param full_response=False: Do we need to return full response?
            :param render_page=False: Do we need to render page?
            :param specific_attempts_count=None: Set some int value to use custom attempts count
        """
        return self.create_request('get', url, cookies, data, cookies_text, headers, timeout, full_response, render_page, specific_attempts_count)

    def post_page(self, url, cookies={}, data={}, cookies_text='', headers={}, timeout=None, full_response=False, specific_attempts_count=None):
        """
        Create post request
            :param self: 
            :param url: Url
            :param cookies={}: Cookies
            :param data={}: Payload data
            :param cookies_text='': Cookies in text mode. (It overwrites other cookies!)
            :param headers={}: Headers of the request. (It overwrites cookies and user agent!)
            :param timeout=None: Timeout for the request. (If None it will use default_timeout)
            :param full_response=False: Do we need to return full response?
            :param specific_attempts_count=None: Set some int value to use custom attempts count
        """
        return self.create_request('post', url, cookies, data, cookies_text, headers, timeout, full_response, False, specific_attempts_count)

    # Others
    def load_requests(self):
        """
        Initiate http_requests
            :param self: 
        """
        if self.use_session:
            self.http_requests = requests.Session()
        else:
            self.http_requests = requests

    def reload_requests(self):
        """
        Reload http_requests
            :param self: 
        """
        self.load_requests()

    def render_html_page(self, page_content):
        """
        Render html page
            :param self: 
            :param page_content: Content of the page to render
        """
        try:
            from requests_html import HTML
            html = HTML(html=page_content)
            html.render(reload=False)
            return html.text
        except:
            logging.error('Cannot render the page', exc_info=True)
            return page_content

    # Proxies Logic
    def change_proxies(self, proxy_string=None):
        """
        Change proxies manually
            :param self: 
            :param proxies=None: Set new proxies
        """
        self.reload_requests()
        if not proxy_string:
            self.proxies = self.get_random_proxies()
        else:
            self.proxies = self.get_proxies_from_string(proxy_string)

    def get_proxies_from_string(self, proxy_string):
        """
        Convert string to proxies
            :param self: 
            :param proxy_string: 
        """
        return {'http': 'http://{0}'.format(proxy_string), 'https': 'https://{0}'.format(proxy_string)}

    def get_random_proxies(self):
        """
        Get random proxies from list
            :param self: 
        """
        if self.proxy_string_list:
            try:
                proxy_string = random.choice(self.proxy_string_list)
                return self.get_proxies_from_string(proxy_string)
            except:
                logging.warning('Cannot get random proxies. Using without proxies.', exc_info=True)
                return {}
        logging.warning('No proxies left. Failed proxies count: {}. Using without proxies.'.format(self.failed_proxy_string_list))
        return {}

    def mark_proxies_as_failed(self):
        """
        Mark current proxies as failed
            :param self: 
        """ 
        if self.proxies != {}:
            proxy_string = self.proxies['http'].split('http://')[-1]
            if self.proxy_string_list and proxy_string in self.proxy_string_list:
                self.failed_proxy_string_list.append(proxy_string)
                self.proxy_string_list.remove(proxy_string)
            else:
                logging.warning('No proxies left. Failed proxies count: {}'.format(self.failed_proxy_string_list))
        else:
            logging.warning('No proxies in use')

    # CookiesLogic
    def save_cookies_to_file(self, cookies={}, name='cookies', current_cookies=False):
        """
        Save cookies dict to the file
            :param self: 
            :param cookies={}: Dict of cookies (or use current_cookies)
            :param name='cookies': File name to save
            :param current_cookies=False: Save cookies from currents session?
        """
        try:
            if current_cookies:
                cookies = self.get_session_cookies()
            cookies = json.dumps(cookies)
            with open('{}.cookies'.format(name), 'w') as the_file:
                the_file.write(cookies)
        except:
            logging.error('Cannot save cookies to file', exc_info=True)

    def get_session_cookies(self):
        """
        Get cookies from the current session
            :param self: 
        """
        try:
            return requests.utils.dict_from_cookiejar(self.http_requests.cookies)
        except:
            logging.warning('Cannot get cookies')
            return {}

    def set_session_cookies(self, cookies):
        """
        Set cookies from the current session
            :param self: 
        """
        if isinstance(cookies, str):
            cookies = self.get_dict_cookies_from_text(cookies)
        if self.use_session:
            try:
                for key in cookies.keys():
                    self.http_requests.cookies.set(key, cookies[key])
            except:
                logging.warning('Cannot set cookies')
        else:
            logging.error('Session mode is not activated')

    def get_cookies_from_file(self, name='cookies'):
        """
        Return cookies dict from the file
            :param self: 
            :param name='cookies': File name to load
        """
        try:
            with open('{}.cookies'.format(name)) as the_file:
                cookies_text = the_file.read()
            try:
                cookies = json.loads(cookies_text)
            except:
                cookies = self.get_dict_cookies_from_text(cookies_text)
            return cookies
        except:
            logging.error('Cannot get cookies from file', exc_info=True)
            return {}

    def get_dict_cookies_from_text(self, cookies_text):
        """
        Returnt dict from cookies raw text
            :param self: 
            :param cookies_text: Raw cookies text, example: CONSENT=YES+UK.en+; SID=wgdombwvMd;
        """
        try:
            from http import cookies
            cookie = cookies.SimpleCookie()
            cookie.load(cookies_text)
            cookies = {}
            for key, morsel in cookie.items():
                cookies[key] = morsel.value
        except:
            logging.error('Cannot get cookies from raw text', exc_info=True)
            cookies = {}
        return cookies
    
    def __del__(self):
        """
        Close all connections
            :param self: 
        """
        if self.http_requests is not None:
            try:
                self.http_requests.close()
            except:
                try:
                    self.http_requests.session().close()
                except:
                    pass
