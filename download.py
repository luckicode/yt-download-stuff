from pytube import YouTube, Playlist
from pydub import AudioSegment
import os
from sys import argv
from urllib.parse import urlparse, parse_qs

# Function to download a video and convert it to MP3
def download_and_convert_to_mp3(video, download_path):
    # Get the audio stream of the video
    audio_stream = video.streams.filter(only_audio=True).first()
    # Download the audio stream to the specified download path
    audio_file_path = audio_stream.download(output_path=download_path)
    
    # Generate the MP3 file path by removing the extension from the downloaded file
    mp3_file_path = os.path.splitext(audio_file_path)[0] + '.mp3'
    # Load the audio file using pydub
    audio = AudioSegment.from_file(audio_file_path)
    # Export the audio file as MP3 format
    audio.export(mp3_file_path, format='mp3')
    
    # Remove the downloaded audio file
    os.remove(audio_file_path)
    print(f'Download and conversion to MP3 completed: {video.title}')

# Function to download a video in MP4 format
def download_as_mp4(video, download_path):
    # Get the highest resolution video stream
    video_stream = video.streams.get_highest_resolution()
    # Download the video stream to the specified download path
    video_stream.download(output_path=download_path)
    print(f'Downloading... {video.title}')

# Function to check if a URL is a playlist
def is_playlist(url):
    query = parse_qs(urlparse(url).query)
    return 'list' in query

# Getting the video or playlist link and format from the command line arguments
link = argv[1]
download_format = argv[2].lower()  # 'mp3' or 'mp4'

download_path = r"D:\Isaac\yt downloads"
download_path = download_path.strip()  # Remove any trailing spaces

# Create the download directory if it doesn't exist
if not os.path.exists(download_path):
    os.makedirs(download_path)

# Check if the provided URL is a playlist
if is_playlist(link):
    # Initialize a Playlist object with the playlist URL
    playlist = Playlist(link)
    print(f'Downloading playlist: {playlist.title} as {download_format.upper()}')
    
    # Iterate through each video in the playlist
    for video in playlist.videos:
        print(f"\nTitle: {video.title}")
        print(f"Number of views: {video.views}")
        print(f"Length of video: {video.length} seconds\n")
        
        # Download and convert the video to MP3 if the format is 'mp3'
        if download_format == 'mp3':
            download_and_convert_to_mp3(video, download_path)
        # Download the video in MP4 format if the format is 'mp4'
        elif download_format == 'mp4':
            download_as_mp4(video, download_path)
        else:
            print("Invalid format. Please choose 'mp3' or 'mp4'.")
    
    # Print a message indicating that the playlist has been downloaded
    print("Playlist downloaded!")
else:
    # If the URL is not a playlist, download the single video
    yt = YouTube(link)
    print(f'Downloading video: {yt.title} as {download_format.upper()}')

    print(f"\nTitle: {yt.title}")
    print(f"Number of views: {yt.views}")
    print(f"Length of video: {yt.length} seconds\n")

    # Download and convert the video to MP3 if the format is 'mp3'
    if download_format == 'mp3':
        download_and_convert_to_mp3(yt, download_path)
    # Download the video in MP4 format if the format is 'mp4'
    elif download_format == 'mp4':
        download_as_mp4(yt, download_path)
    else:
        print("Invalid format. Please choose 'mp3' or 'mp4'.")

    # Print a message indicating that the download and conversion process is completed
    print(f'Download and conversion to {download_format.upper()} completed.')