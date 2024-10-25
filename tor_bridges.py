import re
from datetime import datetime
from utils import index_to_splunk, retry

URL = 'https://check.torproject.org/torbulkexitlist'
    
def extract_ip_addresses(text):
    ''' Extracts IP addresses from a given text string. '''
    ip_pattern = r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
    matches = re.findall(ip_pattern, text)
    return matches

def run_tor_bridges():
    session = retry()
    response = session.get(URL,timeout=30, verify=False)
    ip_list = extract_ip_addresses(response.text)

    for ip in ip_list:
        data = {
            'misp_value': ip,
            'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'misp_event_info': 'TOR Exit Nodes',
            'url': URL
        }
        index_to_splunk(data, 'TOR_BRIDGES')
      
