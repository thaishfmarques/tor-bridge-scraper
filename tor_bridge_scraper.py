import time
import re
import sys
import warnings
import json
import requests
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager 
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from msedge.selenium_tools import Edge, EdgeOptions
from urllib3 import exceptions, disable_warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
disable_warnings(exceptions.InsecureRequestWarning)

URLS = ['https://t.me/s/tor_bridges','https://t.me/s/mosty_tor2']
SPLUNK_TOKEN = ''
SPLUNK_URL = ''
HOST = ''
SOURCE = 'tor_crawler'

log = Logger().getLogger("TOR BRIDGE CRAWLER")

def get_browser(option='edge'):
    ''' Função para configurar e retornar o navegador desejado '''
    if option == 'chrome':
        chrome_options = webdriver.ChromeOptions()
        caps = webdriver.DesiredCapabilities.CHROME.copy()
        caps['detach'] = True
        chrome_options.add_argument('--incognito')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        return webdriver.Chrome(ChromeDriverManager().install(), desired_capabilities=caps)
    
    elif option == 'edge':
        edge_options = EdgeOptions()
        edge_options.use_chromium = True
        edge_options.add_experimental_option('excludeSwitches', ['disable-popup-blocking', 'enable-logging'])
        edge_options.add_argument('--inPrivate')
        return Edge(EdgeChromiumDriverManager().install(), options=edge_options)
    
    elif option == 'firefox':
        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument('-incognito')
        return webdriver.Firefox(executable_path=GeckoDriverManager().install())

def fetch_messages(driver, url):
    ''' Função para navegar para a URL e extrair mensagens '''
    driver.get(url)
    body = driver.find_element_by_tag_name('body')
    
    # Descer até o final da página para carregar todas as mensagens
    for _ in range(3):
        body.send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(3)
    
    time.sleep(2)
    return driver.find_elements_by_class_name('tgme_widget_message_text')

def extract_ip_ports(messages):
    ''' Função para extrair IPs e portas das mensagens '''
    all_matches = []
    for message in messages:
        matches = re.findall(r".*\s([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:\d+).*", message.text)
        all_matches.extend(matches)
    return sorted(set(all_matches))

def filter_ip_ports(ip_ports):
    ''' Função para filtrar IPs e portas desejadas '''
    filtered = []
    for ip_port in ip_ports:
        match = re.search(r":(\d+)$", ip_port)
        if match and match.group(1) in {'443', '80'}:
            filtered.append(ip_port)
    return filtered

def index_to_splunk(data):  
    ''' Envia resultados para o splunk '''
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    try:
        event = {"source": 'TorBridgesCrawler', "host": HOST, "event": data}
        headers = {"Authorization": "Splunk " + SPLUNK_TOKEN}
        res = session.post(url=SPLUNK_URL, headers=headers, data=json.dumps(event), verify=False)
        status = res.status_code
        if status == 200:
            pass
        else:
            log.error('Event not indexed. status_code: %s', status)
    except TypeError:
        log.error('Event not indexed.\nMotive: Token not found. SPLUNK_TOKEN: %s', SPLUNK_TOKEN)
        return False
    except exceptions.ConnectionError as conn_err:
        log.error('Connection Refused\nMotive: %s', conn_err)
        print(f'\nConnection Refused\nMotive: {conn_err}')
        return False

def main():
    driver = get_browser()
    try:
        for url in URLS: 
            messages = fetch_messages(driver, url)
            all_matches = extract_ip_ports(messages)

            results = []
            for match in all_matches:
                result = {
                    'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'misp_value': match.split(':')[0],
                    'port': match.split(':')[1],
                    'misp_event_info': 'TOR Exit Nodes',
                    'url': url # Adicionando a URL de origem
                }
                results.append(result)
            for result in results:
                print(result)
                index_to_splunk(result)
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
