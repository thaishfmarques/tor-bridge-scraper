import time
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager 
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from msedge.selenium_tools import Edge, EdgeOptions

URL = 'https://t.me/s/tor_bridges'

def get_browser(option='firefox'):
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

def main():
    driver = get_browser()
    try:
        messages = fetch_messages(driver, URL)
        all_matches = extract_ip_ports(messages)
        filtered_matches = filter_ip_ports(all_matches)
        
        results = []
        for match in filtered_matches:
            result = {
                'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'ip': match
            }
            results.append(result)
        
        for result in results:
            print(result)
        
    finally:
        driver.quit()

if __name__ == '__main__':
    main()