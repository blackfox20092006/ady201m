import threading
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from queue import Queue
import os

NUM_THREADS = 4
LINKS_PER_HASHTAG = 100
HASHTAG_FILE = 'ythashtags.dat'

hashtag_queue = Queue()
result_links = []
lock = threading.Lock()

def scrape_videos_worker():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--log-level=3')
    driver = webdriver.Chrome(options=options)

    while not hashtag_queue.empty():
        try:
            hashtag = hashtag_queue.get()
            print(f"[Thread {threading.get_ident()}] Starting to process hashtag: {hashtag}")
            
            url = f"https://www.youtube.com/hashtag/{hashtag}"
            driver.get(url)
            time.sleep(3) 

            found_links_this_hashtag = set()
            scrolls_with_no_new_links = 0

            while len(found_links_this_hashtag) < LINKS_PER_HASHTAG:
                html_source = driver.page_source
                found = re.findall(r'/watch\?v=[\w-]{11}', html_source)
                
                links_before_add = len(found_links_this_hashtag)
                for link in found:
                    found_links_this_hashtag.add(link)
                
                links_after_add = len(found_links_this_hashtag)

                print(f"[Thread {threading.get_ident()}] Found {len(found_links_this_hashtag)}/{LINKS_PER_HASHTAG} links for hashtag '{hashtag}'")

                if links_after_add == links_before_add:
                    scrolls_with_no_new_links += 1
                else:
                    scrolls_with_no_new_links = 0
                
                if scrolls_with_no_new_links >= 5:
                    print(f"[Thread {threading.get_ident()}] No new videos loaded for hashtag '{hashtag}'. Stopping.")
                    break
                    
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
                time.sleep(2)

            with lock:
                result_links.extend(list(found_links_this_hashtag))

            print(f"[Thread {threading.get_ident()}] Finished hashtag: {hashtag}")
            hashtag_queue.task_done()

        except Exception as e:
            print(f"[Thread {threading.get_ident()}] Encountered an error: {e}")
            hashtag_queue.task_done()
            continue
            
    driver.quit()

if __name__ == "__main__":
    if not os.path.exists(HASHTAG_FILE):
        print(f"Error: File '{HASHTAG_FILE}' not found. Please create this file.")
    else:
        with open(HASHTAG_FILE, 'r', encoding='utf-8') as f:
            for line in f:
                hashtag = line.strip()
                if hashtag:
                    hashtag_queue.put(hashtag)
        
        print(f"Read {hashtag_queue.qsize()} hashtags from the file.")

        threads = []
        print(f"Starting execution with {NUM_THREADS} threads...")
        for _ in range(NUM_THREADS):
            thread = threading.Thread(target=scrape_videos_worker)
            thread.daemon = True
            thread.start()
            threads.append(thread)
        
        hashtag_queue.join()
        print("All hashtags have been processed.")

        final_links = {f"https://youtube.com{link}" for link in result_links}
        
        print("\n--- COLLECTED VIDEO LIST ---")
        if final_links:
            for link in sorted(list(final_links)):
                print(link)
            print(f"\nFound a total of {len(final_links)} unique videos.")
        else:
            print("No videos were found.")