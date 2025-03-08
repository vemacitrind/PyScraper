import yt_dlp
import sys
import os
import threading
import time
import instaloader

downloading = False
#color pattern--
red = '\u001B[31m'
green = '\u001B[32m'
yellow = '\u001B[33m'
blue = '\u001B[34m'
magenta = '\u001B[35m'
cyan = '\u001B[36m'
white = '\u001B[37m'

def show_loading():
    symbols = ['/', '-', '\\', '|']
    i = 0
    while downloading:
        sys.stdout.write(f"{yellow}\rDownloading... {symbols[i % len(symbols)]} ")
        sys.stdout.flush()
        time.sleep(0.2)
        i += 1
    sys.stdout.write("\r")

def download_video(url, quality="1080p", output_path="Downloads"):
    global downloading
    downloading = True

    loader_thread = threading.Thread(target=show_loading)
    loader_thread.start()

    try:
        quality_formats = {
            "360p": "bestvideo[height<=360]+bestaudio/best[height<=360]",
            "480p": "bestvideo[height<=480]+bestaudio/best[height<=480]",
            "720p": "bestvideo[height<=720]+bestaudio/best[height<=720]",
            "1080p": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        }
        format_selection = quality_formats.get(quality, quality_formats["1080p"])

        ydl_opts = {
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',  
            'format': format_selection, 
            'merge_output_format': 'mp4',  
            'noplaylist': True,  
            'quiet': True, 
            'no_warnings': True,  
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

    except Exception as e:
        print(red,"\n[✘] Error:", e,white,sep="")

    downloading = False
    loader_thread.join()
    print(green,"\r[✔] Download Complete! Saved in ", output_path,white,sep="")

def download_reel(link):
    """Downloads an Instagram reel from the given link."""
    global downloading
    downloading = True

    loader_thread = threading.Thread(target=show_loading)
    loader_thread.start()

    try:
        ig = instaloader.Instaloader(download_video_thumbnails=False,
                                     download_comments=False,
                                     save_metadata=False,
                                     post_metadata_txt_pattern="")

        short_code = link.split('/')[-2]
        post = instaloader.Post.from_shortcode(ig.context, short_code)
        
        ig.download_post(post, target="Downloads")

    except Exception as e:
        print(f"\r{red}[✘] Error: {e}{white}") 

    finally:
        downloading = False
        loader_thread.join()
        sys.stdout.write("\r" + " " * 50 + "\r") 
        print(f"{green}[✔] Downloaded Successfully{white}")

if __name__ == '__main__':
    ascii_art = f"""
    {blue}8888888b.           {magenta} .d8888b.                                                     
    {blue}888   Y88b          {magenta}d88P  Y88b                                                    
    {blue}888    888          {magenta}Y88b.                                                         
    {blue}888   d88P 888  888 {magenta} "Y888b.    .d8888b 888d888 8888b.  88888b.   .d88b.  888d888 
    {blue}8888888P"  888  888 {magenta}    "Y88b. d88P"    888P"      "88b 888 "88b d8P  Y8b 888P"   
    {blue}888        888  888 {magenta}      "888 888      888    .d888888 888  888 88888888 888     
    {blue}888        Y88b 888 {magenta}Y88b  d88P Y88b.    888    888  888 888 d88P Y8b.     888     
    {blue}888         "Y88888 {magenta} "Y8888P"   "Y8888P 888    "Y888888 88888P"   "Y8888  888     
    {blue}                888 {magenta}                                    888                       
    {blue}           Y8b d88P {magenta}                                    888                       
    {blue}            "Y88P"  {magenta}                                    888                       
        """
    print(ascii_art)
    print(cyan,'[1].Instragram Post/Reel',sep="")
    print(cyan,'[2].Youtube video',white,sep="")

    choice = input(f'{cyan}Enter choice : {yellow}')
    if choice == '1':
        post_url = input(f"{cyan}Enter post URL: {yellow}")
        download_reel(post_url)
    elif choice == '2':
        video_url = input(f"{cyan}Enter YouTube video URL: {yellow}")
        print("\nChoose Video Quality: 360p, 480p, 720p, 1080p (default: 1080p)")
        video_quality = input(f"{cyan}Enter quality:{yellow} ").strip().lower()
        download_video(video_url, quality=video_quality)
    else :
        print(red,'[x]Invalid Option!',white,sep="")