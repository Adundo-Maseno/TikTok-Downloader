from flask import Flask, render_template, request, redirect
from flask.config import T
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import requests
import datetime
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from urllib.parse import urljoin
import urllib.error

app = Flask(__name__)

# Path to GeckoDriver
GECKODRIVER_PATH = 'D:\\tiktok\\drv'
DOWNLOADS_DIR = 'downloads'

# Get video URLs
video_urls ,video_tags = [],[]

@app.route('/')
def index():
    video_data = zip(range(1, len(video_urls) + 1),video_urls, video_tags)
      # Log the data
    for id,url, tag in video_data:
        if video_data:
            print(f"{id} - Video URL: {url}, Tag: {tag}")
        else:
            print('Video data is still empty')
    return render_template('index.html',video_data = video_data)

@app.route('/download', methods=['POST'])
def download_videos():
    search_term = request.form['search_term']
    num_videos = int(request.form['num_videos'])

    # Clear video URLs and tags lists
    video_urls.clear()
    video_tags.clear()

    print(f"You want to download {num_videos} trending on topic {search_term}")
    if not video_urls and not video_tags:
        try:
            # Create downloads directory if it doesn't exist
            os.makedirs(DOWNLOADS_DIR, exist_ok=True)

            # Initialize Firefox WebDriver
            options = webdriver.FirefoxOptions()
            driver  = webdriver.Firefox()
        
            base_url = 'https://www.tiktok.com/'
            relative_url ='/en'
            abstiktok_url =urljoin(base_url,relative_url)

            
            driver.get(abstiktok_url)
            time.sleep(10)  # Wait for page to load
            
            # Continue as guest
            guest_button = driver.find_element(By.XPATH, '//*[@id="loginContainer"]/div/div/div[3]/div/div[2]/div/div/div')
            guest_button.click()
            time.sleep(2)
            
            # Perform search
            search_box = driver.find_element(By.XPATH, '//*[@id="app-header"]/div/div[2]/div/form/input')
            search_box.send_keys(search_term)
            search_box.submit()
            time.sleep(2)  # Wait for search results
            
        
            while len(video_urls) < num_videos and len(video_tags) < num_videos:
                video_elements = driver.find_elements(By.CSS_SELECTOR, '.css-1as5cen-DivWrapper a')
                tag_elements = driver.find_elements(By.CSS_SELECTOR,'.css-1as5cen-DivWrapper picture img')
                for video_element,tag_element in zip(video_elements,tag_elements):
                    video_url = video_element.get_attribute('href')
                    video_tag = tag_element.get_attribute('alt')
                    if video_url.startswith('https://www.tiktok.com/@'):
                        video_urls.append(video_url)
                        video_tags.append(video_tag)
                        print(f"Url: {video_url}_Tag: {video_tag}")
                
                #print number of videos found
                print(f"{len(video_urls)} URLs found and {len(video_tags)} tags found though you wanted {num_videos}")

                if len(video_urls) >= num_videos and len(video_tags)>= num_videos:
                    break 
                # Scroll down to load more videos
                driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                time.sleep(2)  # Wait for more videos to load


                # Download video and tags
            for i, (video_url,video_tag) in enumerate(zip(video_urls,video_tags), start=1):
                download_video(video_url,i,search_term,driver)
                video_details(video_tag,i,search_term,video_url)

            driver.quit()
        except Exception as e:
            print(f"Error occurred: {e}")
            # Handle the error as needed, such as logging it
            # Reset the video URLs and tags lists
            video_urls.clear()
            video_tags.clear()
            driver.quit()
    else:
        print(f"{len(video_urls)} {len(video_tags)}")
        video_urls.clear()
        video_tags.clear()
        driver.quit()
    
    return redirect('/')


def download_video(url,id,search_term,driver):
    try:
        cookies = {
            '_ga': 'GA1.1.255336023.1711557752',
            '__gads': 'ID=525fab2189bd3113:T=1711557753:RT=1711558298:S=ALNI_MZ9F9XsVhSkzSKWeWV7Q6KkXRVGwQ',
            '__gpi': 'UID=00000d84ddc649fc:T=1711557753:RT=1711558298:S=ALNI_MZSe-0KKU69Kv6adCvygmQuI7miZg',
            '__eoi': 'ID=e645cd084ddd5fcc:T=1711557753:RT=1711558298:S=AA-AfjY3CfIGOnCRSvPnzW7Jbfkp',
            '_ga_ZSF3D6YSLC': 'GS1.1.1711557751.1.1.1711558325.0.0.0',
            }

        headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'cookie': '_ga=GA1.1.255336023.1711557752; __gads=ID=525fab2189bd3113:T=1711557753:RT=1711558298:S=ALNI_MZ9F9XsVhSkzSKWeWV7Q6KkXRVGwQ; __gpi=UID=00000d84ddc649fc:T=1711557753:RT=1711558298:S=ALNI_MZSe-0KKU69Kv6adCvygmQuI7miZg; __eoi=ID=e645cd084ddd5fcc:T=1711557753:RT=1711558298:S=AA-AfjY3CfIGOnCRSvPnzW7Jbfkp; _ga_ZSF3D6YSLC=GS1.1.1711557751.1.1.1711558325.0.0.0',
            'dnt': '1',
            'hx-current-url': 'https://ssstik.io/en',
            'hx-request': 'true',
            'hx-target': 'target',
            'hx-trigger': '_gcaptcha_pt',
            'origin': 'https://ssstik.io',
            'referer': 'https://ssstik.io/en',
            'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        }

        params = {
        'url': 'dl',
        }

        data = {
            'id': url,
            'locale': 'en',
            'tt': 'NmdHS1A3',
        }

        response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
        downloadSoup =BeautifulSoup(response.text,"html.parser")
        downloadLink = downloadSoup.a['href']
        time.sleep(30)

        mp4File = urlopen(downloadLink)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        with open(f"downloads/{search_term}_{id}_{timestamp}.mp4","wb") as output:
            while True:
                data=mp4File.read(4096)
                if data:
                    output.write(data)
                else:
                    break
    except urllib.error.URLError as e:
        print(f"URLError: {e}")
        # Handle the error as needed, such as retrying the download or logging the error
        driver.quit()
        return redirect('/')  # Redirect to the homepage

# Function to log video tags to a text file with timestamp
def video_details(video_tag, id, search_term,video_url):
    # Sanitize the video tag to remove any invalid characters
    sanitized_video_tag = re.sub(r'[<>:"/\\|?*]', '', video_tag)
    
    # Create the filename with sanitized video tag
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"downloads/{search_term}_{id}_{current_time}.txt"
    
    # Write the video details to the file
    with open(filename, "w", encoding="utf-8") as file:
        file.write("Video Details\n")
        file.write("-" * 50 + "\n")
        # Write content
        file.write(f"Video ID: {id}\n")
        file.write(f"Search Term: {search_term}\n")
        file.write(f"Video URL: {video_url}\n")
        file.write(f"Video Tag: {sanitized_video_tag}\n")
    time.sleep(5)

if __name__ == '__main__':
    app.run(debug=True)
