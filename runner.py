import multiprocessing
import os
import subprocess
import time
import schedule

# List of JSON files to process
json_files = ['CCTV.json', 'PLA.json', 'ChinaNews.json', 'GlobalTimes.json', 'QQ.json', 'SCMP.json', 'Sina.json', 'Sohu.json', 'Tibet.json', 'CNR.json','JS7.json','Huanqiu.json', '163.json']

# Function to run new_scraper.py with a JSON file as input
def run_scraper(json_file):
    command = ['python', 'new_scraper.py', json_file]
    subprocess.run(command)

def run_daily():
    # Create a pool of worker processes
    pool = multiprocessing.Pool()

    # Map the run_scraper function to each JSON file in parallel
    pool.map(run_scraper, json_files)

    # Close the pool and wait for all processes to finish
    pool.close()
    pool.join()

    print("All scrapers have finished.")

# Schedule the script to run daily at a specific time (e.g., 1:00 AM)
schedule.every().day.at("10:55").do(run_daily)

while True:
    schedule.run_pending()
    
    # Check if it's 1:00 AM and scrapers haven't finished
    current_time = time.strftime("%H:%M")
    if current_time == "10:55":
        print("Scrapers haven't finished by 11:00 AM. Waiting for 2 hours...")
        time.sleep(2 * 60 * 60)  # Wait for 2 hours (in seconds) = 2 * 60 * 60 seconds = 7200 seconds
        # After 2 hours, the script will continue to the next scheduling iteration (3:00 AM).
