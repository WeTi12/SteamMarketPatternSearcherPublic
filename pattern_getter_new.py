import requests

baseurl = "https://api.csfloat.com/?url=" 

def get_pattern_info_new(items):
    print("----- Scraping patterns -----")

    patterns = []
    pattern = -1

    for link in items["inspect_links"]:
        a_index = link.find("A")
        print("Getting pattern of item: " + items["name"][0] + ", " + link[66:a_index+1])

        response = requests.get(baseurl + link)

        if response.status_code == 200:
            data = response.json()
            pattern = data['iteminfo']['paintindex']
        else:
            print(f"Error: {response.status_code}")
            pattern = ''

        if pattern == -1:
            print("Couldn't scrape item pattern, FloatDB error/slow internet issue")
        else:
            print(pattern)
        
        patterns.append(pattern)
        pattern = -1

    return patterns
