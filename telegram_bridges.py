import time
import re
import logging 
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from utils import get_browser, index_to_splunk

URLS = ['https://t.me/s/tor_bridges']

log = logging.getLogger("TOR BRIDGE CRAWLER")

def fetch_messages(driver, url):
    ''' Function to navigate to URL and extract messages '''
    driver.get(url)
    body = driver.find_element_by_tag_name('body')
    
    for _ in range(3):
        body.send_keys(Keys.CONTROL + Keys.HOME)
        time.sleep(3)
    
    time.sleep(2)
    return driver.find_elements_by_class_name('tgme_widget_message_text')

def extract_ip_ports(messages):
    ''' Function to extract IPs and ports from messages '''
    all_matches = []
    for message in messages:
        matches = re.findall(r".*\s([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}:\d+).*", message.text)
        all_matches.extend(matches)
    return sorted(set(all_matches))

def filter_ip_ports(ip_ports):
    ''' Function to filter desired IPs and ports '''
    filtered = []
    for ip_port in ip_ports:
        match = re.search(r":(\d+)$", ip_port)
        if match and match.group(1) in {'443', '80'}:
            filtered.append(ip_port)
    return filtered

def run_telegram_bridges():
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
                    'url': url # Add origin URL
                }
                results.append(result)
            for result in results:
                print(result)
                index_to_splunk(result, 'TELEGRAM_BRIDGES')
    finally:
        driver.quit()
