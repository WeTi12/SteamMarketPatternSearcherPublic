import sys
import time
from app_main import scraping_script

loop_minutes = 1
pattern_method = "old"

for arg in sys.argv[1:]:
    if arg.isdigit():
        loop_minutes = int(arg)
    elif arg in ["old", "new"]:
        pattern_method = arg

print(f"Looping every {loop_minutes} minutes with pattern method: {pattern_method}")

i = 1
while True:
    print("\nLoop: " + str(i))
    finished = scraping_script(pattern_method)
    if finished == True:
        print("Script finished, waiting for " + str(loop_minutes) + " minutes")
    else:
        print("Error running script, waiting for " + str(loop_minutes) + " minutes")
    i += 1
    time.sleep(loop_minutes * 60)
