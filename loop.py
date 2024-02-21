import sys
import time
from app_main import scraping_script

loop_minutes = 1
if len(sys.argv) > 1:
    loop_minutes = int(sys.argv[1])
print(f"Looping every {loop_minutes} minutes")

i = 1
while True:
    print("\nLoop: " + str(i))
    finished = scraping_script()
    if finished == True:
        print("Script finished, waiting for " + str(loop_minutes) + " minutes")
    else:
        print("Error running script, waiting for " + str(loop_minutes) + " minutes")
    i += 1
    time.sleep(loop_minutes * 60)
