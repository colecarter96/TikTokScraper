import glob
import subprocess
from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
import ffmpeg

def resize_and_pad_video(input_file, output_file):
    # Define the ffmpeg command
    command = [
        'ffmpeg',
        '-i', input_file,
        '-vf', 'scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:-1:-1:color=black',
        output_file
    ]
    
    try:
        # Run the command
        subprocess.run(command, check=True)
        print(f"Successfully processed {input_file} and saved as {output_file}.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")



def compileClips(videoFolder, outputVidName):
    video_files_path = videoFolder

    video_file_list = glob.glob(f"{video_files_path}/*.mp4")

    loaded_video_list = []

    for video in video_file_list:
        print(f"Adding video file:{video}")
        loaded_video_list.append(VideoFileClip(video))

    final_clip = concatenate_videoclips(loaded_video_list)

    merged_video_name = 'temp'

    # reshape_video(final_clip, merged_video_name, 1920, 1080)

    final_clip.write_videofile(f"{merged_video_name}.mp4")
    
    



def combine_videos(directory, output_file_temp, final_output_file):
    # Get a list of all video files in the directory
    video_files = [f for f in os.listdir(directory) if f.endswith(('.mp4', '.mkv', '.avi'))]  # Adjust file extensions as needed
    
    
    if not video_files:
        print("No video files found in the specified directory.")
        return
    
    # Create a temporary file list for ffmpeg
    file_list_path = os.path.join(directory, 'file_list.txt')
    
    print(file_list_path)
    with open(file_list_path, 'w') as f:
        for video_file in video_files:
            

            f.write(f"file '{video_file}'\n")

    


    # Run the ffmpeg command to combine videos
    command = ['ffmpeg', '-f', 'concat', '-safe', '0', '-i', file_list_path, '-c', 'copy', output_file_temp]
    
    
    try:
        subprocess.run(command, check=True)
        print(f"Successfully combined videos into {output_file_temp}.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred: {e}")
    finally:
        # Clean up the temporary file list
        os.remove(file_list_path)
    
    resize_and_pad_video(output_file_temp, final_output_file)
# Example usage

