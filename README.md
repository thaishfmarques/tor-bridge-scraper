# tor-bridge-scraper
## Description

Python script that uses Selenium to automate navigation to a Telegram open group page and extract messages containing IPs and ports without having to use the API. The script filters the results to keep only the IPs using ports 443 or 80 and stores the results in a dictionary with the current date and IP. 

The need of scrolling up the page only exists because I wanted a portion of IPS from the last 30 days or so. So is the filter for ports 80 and 443.

## Prerequisites

- Python 3.9+
- `pip3` (gerenciador de pacotes do Python)
- Legacy selenium==3.141.0 

## Installation

1. Clone the repository to your local machine:

    ```bash
    git clone <URL_DO_REPOSITORIO>
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
    python tor_bridge_scraper.py
    ```

2. The script will open a browser, navigate to the specified page, and extract the messages containing IPs and ports.

3. The filtered results (IP and port) will be displayed in the console, stored in a dictionary with the current date and IP.

## Browser Configuration

By default, the script is configured to use Firefox. To change the browser, edit the get_browser function and change the value of the option variable to one of the following values: 'chrome', 'edge', or 'firefox'. Or just 

## Estrutura do Código

- `get_browser(option='firefox')`: Configures and returns the desired browser.
- `fetch_messages(driver, url)`: Navigates to the URL and extracts the messages.
- `extract_ip_ports(messages)`: Extracts the IPs and ports from the messages.
- `filter_ip_ports(ip_ports)`: Filters the IPs and ports that end in 443 or 80.
- `main()`: Main function that orchestrates the calls to other functions and prints the final results.

## Sample Output

```json
[
    {
        "data": "2024-07-20 12:34:56",
        "ip": "192.168.0.1:443"
    },
    {
        "data": "2024-07-20 12:34:56",
        "ip": "10.0.0.1:80"
    }
]
```

## Notes

Ensure that the corresponding browser driver is installed and configured correctly. Use with caution in production environments.  
Depending on the content of the Telegram page, adjustments may be necessary to ensure all messages are loaded and processed correctly.

## License

This project is licensed under the MIT License. See the LICENSE file for more information.
