import subprocess
import sys
import time

def run_script(script_name):
    try:
        completed_process = subprocess.run(['python', script_name], check=True, text=True)
        print(f"Script {script_name} finished with return code {completed_process.returncode}")
        print(f"Output: {completed_process.stdout}")
        print(f"Error: {completed_process.stderr}", file=sys.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}", file=sys.stderr)

loop_minutes = 1
if len(sys.argv) > 1:
    loop_minutes = int(sys.argv[1])
print(f"Looping every {loop_minutes} minutes...")

i = 0;
while True:
    print("\nLoop: " + str(i))
    script_to_run = 'inspect_link_getter.py'
    run_script(script_to_run)
    i += 1
    print("Script finished, waiting for " + str(loop_minutes) + " minutes...")
    time.sleep(loop_minutes * 60)
