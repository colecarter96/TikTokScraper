from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os
import urllib

# Takes the download link with the correct params for ssstik.io on my mac to download the video

def writeVideo(download_link, file_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'Accept': 'application/octet-stream',
        'Referer': 'https://ssstik.io/'  # Same referer as seen in the request
    }

    session = requests.Session()

    try:
        response = session.get(download_link, headers=headers, stream=True)
        response.raise_for_status()  # Raise an error for bad responses

        # Allow application/octet-stream as a valid content type
        content_type = response.headers.get('Content-Type')
        if 'video' not in content_type and content_type != 'application/octet-stream':
            print(f"Error: The URL does not point to a valid video file. Content-Type: {content_type}")
            return

        # Download in chunks
        with open(file_path, 'wb') as out_file:
            for chunk in response.iter_content(chunk_size=8192):
                out_file.write(chunk)

        print(f"Downloaded file: {file_path}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")


# Takes link and gets the request from ssstik.io

def downloadVideo(link, id, outputFolder):
    
    print(f"Downloading video id {id} from : {link}")

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'hx-current-url': 'https://ssstik.io/en-1',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'priority': 'u=1, i',
        'referer': 'https://ssstik.io/en-1',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'en',
        'tt': 'enZLWjFn',
    }

    response = requests.post('https://ssstik.io/abc', params=params, headers=headers, data=data)
    downloadSoup = BeautifulSoup(response.text, "html.parser")
    downloadLink = downloadSoup.a["href"]
    print(downloadLink)
    
    file_path = os.path.join(outputFolder, f"{id}.mp4")

   
    writeVideo(downloadLink, file_path)


# Opens chrome with selenium
# you have to log in with your TikTok acct in 20s (I used QR Code)
# Allow for page to scroll
# Captures video links and then sends them to be downloaded and written

def runDownload(link, hrefDivTitle, outputFolder, numVideos, numSkip):
    print("STEP 1: Open Chrome browser")
    options = Options()
    options.add_argument("start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    driver = webdriver.Chrome(options=options)
    # Change the tiktok link
    driver.get(link)



    # IF YOU GET A TIKTOK CAPTCHA, CHANGE THE TIMEOUT HERE
    # to 60 seconds, just enough time for you to complete the captcha yourself.
    time.sleep(20)


    scroll_pause_time = 1
    screen_height = driver.execute_script("return window.screen.height;")
    i = 1

    print("STEP 2: Scrolling page")
    while True:
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        i += 1
        time.sleep(scroll_pause_time)
        scroll_height = driver.execute_script("return document.body.scrollHeight;")  
        if (screen_height) * i > scroll_height:
            break 



    soup = BeautifulSoup(driver.page_source, "html.parser")
    videos = soup.find_all("div", {"class": hrefDivTitle})

    vidIndex = {}

    for video in videos:
        
        if video.find("div", {"class": "css-1df8vyd-DivPhotoIconContainer e19c29qe25"}):
            vidIndex[video] = 1
        else:
            vidIndex[video] = 0


    print(len(vidIndex))
    # print(next(iter(vidIndex.items())))

    for index, video in enumerate(vidIndex):
        if index < numSkip:
            continue

        print("_________")
        print(vidIndex[video])
        print(video.a["href"])

        if vidIndex[video] == 1:
            # downloadSlideShow(video.a["href"], index)
            print("Video skipped, id: " + str(index))
        else:
            link = video.a["href"]
            print(link)
            downloadVideo(link, index, outputFolder)
            time.sleep(10)
        
        print(video.a['href'])
        if index >= numVideos + numSkip:
            break

    driver.quit()