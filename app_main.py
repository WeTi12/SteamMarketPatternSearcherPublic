import json
from message_sender import message_sender
from items_info_getter import get_items_info
from pattern_getter import get_pattern_info


def scraping_script():
    #load item data from file
    try:
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
            items_info = None
            patterns = None
            items_info = get_items_info(baseurl)
            patterns = get_pattern_info(items_info)

            for i in range(0, len(items_info["inspect_links"])):
                if patterns[i] in item["patterns"]:
                    print("Pattern found, sending message")
                    message_sender(item, patterns[i], items_info["prices"][i], items_info["listing_ids"][i], items_info["inspect_links"][i])
                    print(patterns[i], items_info["prices"][i], items_info["listing_ids"][i], items_info["name"][i], items_info["inspect_links"][i])
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
    except Exception as e:
        print(e)
        print("----- Error running scraping script -----")
        return False
    
    return True
            
