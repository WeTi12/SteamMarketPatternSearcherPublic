from bs4 import BeautifulSoup
import requests
import json


def get_items_info(url):
    print("----- Getting inspect links for: " + url[47:] + " -----")

    # use response to get html content with script tags
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    script_tags = soup.find_all("script")

    # find the last tag (contains item info)
    last_tag = script_tags[-1]
    text = last_tag.text

    # find item info and parse it
    start_index = text.find("var g_rgAssets = ") + len("var g_rgAssets = ")
    end_index = text.find("var g_rgCurrency") - 4
    json_string = text[start_index:end_index]
    data = json.loads(json_string)

    # Extracting information for each item
    items = []
    for appid, appid_data in data.items():
        for contextid, contextid_data in appid_data.items():
            for item_id, item_info in contextid_data.items():
                # Extract the link from actions, if it exists
                link = item_info.get("actions", [{}])[0].get("link", "No link available")
                items.append({
                    "id": item_id,
                    "name": item_info["name"],
                    "link": link
                })

    # create real inspect links and get listing ids
    inspect_links = []
    listing_ids = []
    item_names = []
    for item in items:
        real_link = item["link"].replace("%assetid%", item["id"])
        inspect_links.append(real_link)
        listing_ids.append(real_link[66:real_link.find("A")])
        item_names.append(item["name"])
        print(real_link)

    # find the price of the item

    print("----- Getting prices for those inspect links -----")
    span_tags = soup.find_all("span", class_="market_listing_price_with_fee")
    prices = []
    for span in span_tags:
        prices.append(span.text.strip())
        print(span.text.strip())


    item_all = {
        "name": item_names,
        "inspect_links": inspect_links,
        "listing_ids": listing_ids,
        "prices": prices
    }

    return item_all

