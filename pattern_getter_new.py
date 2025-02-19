import requests

baseurl = "https://api.csfloat.com/?url=" 

def get_pattern_info_new(items):
    print("----- Scraping patterns -----")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    patterns = []
    pattern = -1

    for link in items["inspect_links"]:
        a_index = link.find("A")
        print("Getting pattern of item: " + items["name"][0] + ", " + link[66:a_index+1])

        response = requests.get(baseurl + link, headers=headers)

        if response.status_code == 200:
            data = response.json()
            pattern = data['iteminfo']['paintindex']
        else:
            print(f"Error: {response.status_code}, {response.text}")
            pattern = ''

        if pattern == -1:
            print("Couldn't scrape item pattern, FloatDB error/slow internet issue")
        else:
            print(pattern)
        
        patterns.append(pattern)
        pattern = -1

    return patterns
