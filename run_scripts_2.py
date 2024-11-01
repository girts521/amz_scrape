import concurrent.futures
import subprocess
import os

# List of scripts to run
scripts = [
    'nike.py',
    'adidas.py',
    'nivea.py',
    'loreal.py'
    ]

# Function to run a script
def run_script(script):
    try:
        print(f"Starting {script}")
        result = subprocess.run(['python3', script], check=True, capture_output=True, text=True)
        print(f"Finished {script}: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script}: {e.stderr}")
    except Exception as e:
        print(f"Unexpected error running {script}: {e}")

# Function to run the update script
def run_update_script():
    try:
        print("Starting update_db.py")
        result = subprocess.run(['python3', 'update_db.py'], check=True, capture_output=True, text=True)
        print(f"Finished update_db.py: {result.stdout}")
    except subprocess.CalledProcessError as e:
        print(f"Error running update_db.py: {e.stderr}")
    except Exception as e:
        print(f"Unexpected error running update_db.py: {e}")

# Main function to manage concurrent execution
def main():
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        futures = {executor.submit(run_script, script): script for script in scripts}
        for future in concurrent.futures.as_completed(futures):
            script = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"{script} generated an exception: {e}")

    # Run the update script after all others are done
    # run_update_script()

if __name__ == '__main__':
    main()
