# Steam Market Pattern Searcher

## About
The Steam Market Pattern Searcher is a Python script designed to search for specified patterns of CS2 items on the Steam Market. This tool aims to help users find items with specific patterns more efficiently.

## Installation

### Clone the Repository

First, clone the repository to your local machine using Git. If you don't have Git installed, you can download it from [git-scm.com](https://git-scm.com/).

```bash
git clone https://github.com/PSob888/SteamMarketPatternSearcher.git
cd SteamMarketPatternSearcher
```

### Install Python and Selenium
This script requires Python and Selenium. If you don't have Python installed, download it from python.org and follow the installation instructions for your operating system.

After installing Python, you can install all required dependencies by running this command:

```bash
pip install -r requirements.txt
```

Selenium requires a driver to interface with the chosen browser. Make sure you have the appropriate WebDriver for your browser installed (this project uses FireFox). For more information on Selenium drivers, visit the Selenium documentation.

## Usage
To use the script, navigate to the project directory and run item_maker.py with the required arguments: <item_name>, <steam_store_link>, and one or more <pattern_id> arguments.

Example:

```bash
python item_maker.py "AK-47 | Redline (Field-Tested)" "https://steamcommunity.com/market/listings/730/AK-47%20|%20Redline%20(Field-Tested)" 101 102 103
```
### Arguments
- **item_name:** The name of the CS:GO item you're searching for.
- **steam_store_link:** The full URL to the item's page on the Steam Market.
- **pattern_id:** One or more pattern IDs you want to search for. You can specify multiple pattern IDs by separating them with spaces.

## details.txt File
The **details.txt** file contains sensitive information and should be formatted as follows:
1. **First Line:** Your email
2. **Second Line:** password for your email
3. **Third Line:** The email address you want to send notifications to.

**Important:** Ensure that **details.txt** is stored securely and is not accessible to unauthorized users, as it contains sensitive information.

## loop.py
**loop.py** is the main loop of the script, use it to run the script after you made the **item.txt** and **details.txt** files
To use the script, navigate to the project directory and run program.py with the required arguments: <minutes>

```bash
python loop.py 5
```
### Arguments
- **minutes:** amount of minutes between each loop cycle.

## Additional information

Useful links for starting the script on AWS EC2  instance with ubuntu

https://askubuntu.com/questions/870530/how-to-install-geckodriver-in-ubuntu

https://stackoverflow.com/questions/72374955/failed-to-read-marionette-port-when-running-selenium-geckodriver-firefox-a

It is also usefull to install GNU Screen, in order to run the script in the background while not being connected to AWS instance
```bash
sudo apt install screen
```
https://linuxize.com/post/how-to-use-linux-screen/

## Disclaimer
This tool is intended for personal use and educational purposes only. Respect Steam's terms of service when using this script. The developers of this script are not responsible for any potential consequences of using this tool.
