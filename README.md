# tor-bridge-scraper
## Description

This project collects Tor bridge information from Telegram groups and Tor exit node information from the Tor Project's bulk exit list. The collected data is then indexed to Splunk for analysis and monitoring.
The need of scrolling up the page only exists because I wanted a portion of IPS from the last 30 days or so. So is the filter for ports 80 and 443.

## Prerequisites

- Python 3.9+
- `pip3` (gerenciador de pacotes do Python)
- Legacy selenium==3.141.0
- requests
- urllib3
- webdriver_manager
- (Optional) appropriate browser drivers (Chrome, Firefox, Edge)

## Project Structure

```
tor_bridge_scraper/
├── utils.py           # Common functions (http session, IP extraction, Splunk indexing)
├── tor_bridges.py     # Script for fetching Tor exit nodes from the Tor Project
├── telegram_bridges.py  # Script for scraping Tor bridges from Telegram
└── main.py            # Entry point for running both scripts
```

## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone <repository_url>
    cd tor-bridge-scraper
    ```

2. Install the necessary dependencies:

    ```bash
    pip3 install -r requirements.txt
    ```

## Dependencies

The project uses the following Python libraries:

- `selenium`: For browser automation.
- `webdriver_manager`: To manage browser drivers.
- `datetime`

## Usage

1. Run the main script:

    ```bash
    python main.py
    ```
This will: 

2. Fetch Tor exit node information from the Tor Project's bulk exit lis
3. Scrape Tor bridge information from the specified Telegram groups.
4. Index the collected data to Splunk.


## Browser Configuration

By default, the script is configured to use Firefox. To change the browser, edit the get_browser function and change the value of the option variable to one of the following values: 'chrome', 'edge', or 'firefox'.

## Code Structure

### telegram_bridges.py

- `get_browser(option='firefox')`: Configures and returns the desired browser.
- `fetch_messages(driver, url)`: Navigates to the URL and extracts the messages.
- `extract_ip_ports(messages)`: Extracts the IPs and ports from the messages.
- `filter_ip_ports(ip_ports)`: Filters the IPs and ports that end in 443 or 80.
- `main()`: Main function that orchestrates the calls to other functions and prints the final results.

### tor_bridges.py

- `extract_ip_addresses(text)`: Extracts IP addresses from a given text string using regular expressions.
- `main()`: Main function that fetches the Tor bulk exit list, extracts IP addresses, and indexes them to Splunk.

### utils.py

- `retry()`: Creates a requests session with automatic retry functionality.
- `index_to_splunk(data, source)`: Indexes data to Splunk with specified source.
- `get_browser(option='firefox')`: Configures and returns a Selenium webdriver instance for the specified browser.

## Sample Output
### telegram_bridges.py
```json
[
    {
        "data": "2024-07-20 12:34:56",
        "misp_value": "192.168.0.1", 
        "port": "443",
        "misp_event_info": "TOR Exit Nodes",
        "url": "https://t.me/s/tor_bridges"
    },
    {
        "data": "2024-07-20 12:34:56",
        "misp_value": "10.0.0.1",
        "port": "80",
        "misp_event_info": "TOR Exit Nodes",
        "url": "https://t.me/s/tor_bridges" 
    }
]
```

### tor_bridges.py

```json
{
    "misp_value": "185.228.168.223",
    "data": "2024-07-20 13:00:00",
    "misp_event_info": "TOR Exit Nodes",
    "url": "https://check.torproject.org/torbulkexitlist"
}
```

## Notes

Ensure that the corresponding browser driver is installed and configured correctly. Use with caution in production environments.  
Depending on the content of the Telegram page, adjustments may be necessary to ensure all messages are loaded and processed correctly.

## License

This project is licensed under the MIT License. See the LICENSE file for more information.
