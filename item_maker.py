import sys
import json

data = ""
with open("item.txt") as f:
    data = f.read()
     
if len(data) <= 2:
    x = {
        "name": "",
        "link": "",
        "patterns": []
    }
    x["name"] = sys.argv[1]
    x["link"] = sys.argv[2]

    for i in range(3, len(sys.argv)):
        x["patterns"].append(sys.argv[i])
    f = open("item.txt", "w")
    f.write(json.dumps(x))
    f.close()
else:
    x = json.loads(data)
    if type(x) == dict:
        if (x["link"] == sys.argv[2]):
            if(sys.argv[3] in x["patterns"]):
                exit(0)
            x["patterns"].append(sys.argv[3])
            f = open("item.txt", "w")
            f.write(json.dumps(x))
            f.close()
            exit(0)
        y = []
        y.append(x)
        x = {
            "name": "",
            "link": "",
            "patterns": []
        }
        x["name"] = sys.argv[1]
        x["link"] = sys.argv[2]

        for i in range(3, len(sys.argv)):
            x["patterns"].append(sys.argv[i])
        y.append(x)
        f = open("item.txt", "w")
        f.write(json.dumps(y))
        f.close()
    else:
        for i in x:
            if (i["link"] == sys.argv[2]):
                for j in range(3, len(sys.argv)):
                    if sys.argv[j] in i["patterns"]:
                        break
                    i["patterns"].append(sys.argv[j])
                f = open("item.txt", "w")
                f.write(json.dumps(x))
                f.close()
                exit(0)
        x2 = {
            "name": "",
            "link": "",
            "patterns": []
        }
        x2["name"] = sys.argv[1]
        x2["link"] = sys.argv[2]

        for i in range(3, len(sys.argv)):
            x2["patterns"].append(sys.argv[i])
        x.append(x2)
        f = open("item.txt", "w")
        f.write(json.dumps(x))
        f.close()
    
