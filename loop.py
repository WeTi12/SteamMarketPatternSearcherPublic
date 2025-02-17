import sys
import time
from app_main import scraping_script

loop_minutes = 1
pattern_method = "new"

if len(sys.argv) > 1:
    loop_minutes = int(sys.argv[1])
    if len(sys.argv) > 2:
        pattern_method = sys.argv[2]
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
