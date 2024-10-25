import requests
import warnings
import json
from selenium import webdriver
from urllib3 import disable_warnings, exceptions
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter
from webdriver_manager.chrome import ChromeDriverManager 
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from msedge.selenium_tools import Edge, EdgeOptions

warnings.filterwarnings("ignore", category=DeprecationWarning)
disable_warnings(exceptions.InsecureRequestWarning)

HOST = 'sample'
SPLUNK_TOKEN = ''
SPLUNK_URL = ''

def get_browser(option='firefox'):
    ''' Function to set and return the desired browser '''
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
    
def index_to_splunk(data, source):
    ''' Indexes data to splunk '''
    session = retry()
    event = {"source": source, "host": HOST, "event": data}
    headers = {"Authorization": "Splunk " + SPLUNK_TOKEN}
    try:
        response = session.post(url=SPLUNK_URL, headers=headers, data=json.dumps(event), verify=False)
        status_code = response.status_code
        if status_code == 200:
            return True
        else:
            print(f"Failed to send data to Splunk. Status code: {status_code}")
            return False
    except TypeError:
        print("Invalid data format for Splunk indexing.")
        return False
    except exceptions.ConnectionError as conn_err:
        print(f"Connection error: {conn_err}")
        return False

def retry():
    ''' Creates a requests session with automatic retry functionality. '''
    retry_strategy = Retry(total=5, status_forcelist=[400, 404], allowed_methods=['GET', 'POST'], backoff_factor=1)
    adapter = HTTPAdapter(max_retries=retry_strategy)
    http = requests.Session()
    http.mount('http://', adapter)
    http.mount('https://', adapter)
    return http

def create_misp_event():
    # TODO
    pass
