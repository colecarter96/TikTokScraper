from scrapeVideos import runDownload
from compileVideo1 import combine_videos
from uploadYoutube import get_authenticated_service, upload_video
import os
import glob
import cv2



if __name__ == "__main__":

    # Define link to videos, hrefDivTitle, where the href tag to the link of the video is and other variables

    link = f"https://www.tiktok.com/search?lang=en&q=dying%20laughing%20&t=1729902807995"
    hrefDivTitle = "css-13fa1gi-DivWrapper e1cg0wnj1"
    outputFolder = "videos"
    numVideos = 5
    numSkip = 0

    outputTemp = "temp4.mp4"
    outputTitle = "TIKTOK_COMPILATION_4.mp4"

    # Download the videos using ssstik.io

    print("Downloading Videos! :)")
    runDownload(link, hrefDivTitle, outputFolder, numVideos, numSkip)

    
    # Compile and resize the videos using ffmpeg

    print("Forming Video! :)")
    combine_videos(outputFolder, outputTemp, outputTitle)
    

    
    
    # Connect to youtube using your account

    print("Connecting to Youtube API")
    # Authenticate and build the YouTube API service
    youtube = get_authenticated_service()
    
   
    # Specify the video details

    video_file = outputTitle  # Path to the video file
    title = "TIK TOK COMPILATION 4"  # Title of the video
    description = """#tiktok #funny #omghilarious
               #tiktok #funny #omghilarious #hilarious #hilariousmoments #dog #dogfail #kidfail #fail #failarmy

                    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠋⣉⣉⣉⣉⣉⣉⠙⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                    ⣿⣿⣿⣿⣿⡿⠟⢁⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⡈⠻⢿⣿⣿⣿⣿⣿
                    ⣿⣿⣿⡿⠋⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠙⢿⣿⣿⣿
                    ⣿⣿⡟⢀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⢻⣿⣿
                    ⣿⡟⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⢻⣿
                    ⣿⢀⣿⣿⣿⠟⠁⣠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠈⠻⣿⣿⣿⡀⣿
                    ⡇⢸⣿⣿⠋⣠⡾⠿⠛⠛⠛⠿⣿⣿⣿⣿⣿⣿⠿⠛⠛⠛⠻⢷⣄⠙⣿⣿⡇⢸
                    ⡇⢸⣿⣿⣾⣿⢀⣠⣤⣤⣤⣤⣀⣿⣿⣿⣿⣀⣤⣤⣤⣤⣄⡀⣿⣷⣾⣿⡇⢸
                    ⡇⠸⠟⣫⣥⣶⣧⠹⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠏⣼⣶⣬⣍⠻⠇⢸
                    ⡧⣰⣿⣿⣿⣿⣿⢰⣦⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣤⣴⡆⣿⣿⣿⣿⣿⣆⢼
                    ⡇⣿⣿⣿⣿⣿⡟⠈⠙⠛⠻⠿⠿⠿⠿⠿⠿⠿⠿⠟⠛⠋⠁⢻⣿⣿⣿⣿⣿⢸
                    ⣿⣌⡻⠿⠿⢋⣴⣦⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⡀⢀⣴⣦⡙⠿⠿⢟⣡⣾
                    ⣿⣿⣿⣷⣄⠙⢿⣿⣿⣶⣤⣀⡀⡀⡀⡀⡀⡀⣀⣤⣶⣿⣿⡿⠋⣠⣾⣿⣿⣿
                    ⣿⣿⣿⣿⣿⣷⣦⣉⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⣉⣴⣾⣿⣿⣿⣿⣿
                    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⣌⣉⣉⣉⣉⣉⣉⣡⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿"""
    tags = ["tiktok", "compilation", "funny", "fails", "dog", "cat", "omghilarious", "hilarious"]  # Tags for the video
    category_id = "24"  # 'Entertainmen'
    privacy_status = "public"  # Options: "public", "private", "unlisted"
    


    
        
    # Upload the video
    
    print("Uploading Video! :)")
    upload_video(youtube, video_file, title, description, tags, category_id, privacy_status)


    if os.path.exists(outputTemp):
        os.remove(outputTemp)
    else:
        print("The file does not exist, (temp)")
    
    if os.path.exists(outputTitle):
        os.remove(outputTitle)
    else:
        print("The file does not exist, (Compilation)")




    