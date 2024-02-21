import json
from message_sender import message_sender
from item_info_getter import get_item_info
from pattern_getter import get_pattern_info

#load item data from file
print("scraping script started")
data = ""
with open("item.txt") as f:
    data = f.read()

data = json.loads(data)

if type(data) == dict:
    data = [data]

for item in data:
    #getting inspect links and prices
    baseurl = item["link"]
    item_info = None
    patterns = None
    item_info = get_item_info(baseurl)
    patterns = get_pattern_info(item_info)

    for i in range(0, len(item_info["inspect_links"])):
        if patterns[i] in item["patterns"]:
            #load email data from file
            print("Pattern found, sending message")
            message_sender(item, patterns[i], prices[i], listing_ids[i], inspect_links[i])
            print(patterns[i], prices[i], listing_ids[i], item["link"], inspect_links[i])
            #remove item or patternfrom list and file if found
            if len(item["patterns"]) > 1:
                item["patterns"].remove(patterns[i])
                f = open("item.txt", "w")
                f.write(json.dumps(data))
                f.close()
            else:
                data.remove(item)
                f = open("item.txt", "w")
                f.write(json.dumps(data))
                f.close()
            print("Item removed")

print("----- Scraping script finished -----")
            
