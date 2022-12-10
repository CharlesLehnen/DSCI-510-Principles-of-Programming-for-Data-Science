import os
import subprocess
import time
import signal
from urllib.parse import urlparse
import asyncio
import capture_images

# Register a signal handler that will be called when the user presses CTRL+C
signal.signal(signal.SIGINT, lambda signum, frame: youtube_dl_process.kill())

async def download_video(url, video_length=7):
    # Set up folder and file structure
    video_folder = os.path.join("data", "videos")
    if not os.path.exists(video_folder):
        os.mkdir(video_folder)
    parsed_url = urlparse(url)
    video_id = parsed_url.query.split("&")[0].split("=")[1]

    # Download video
    video_output = os.path.join(os.getcwd(), "data", "videos")
    command = [
        "youtube-dl",
        "--output", f"{video_output}/video_%(id)s.%(ext)s",
        "--no-part",
        url
    ]

    # Start the youtube_dl_process asynchronously
    # try:
    #     youtube_dl_process = await asyncio.create_subprocess_exec(*command)
    #     await asyncio.wait([youtube_dl_process], timeout=video_length)
    # except asyncio.TimeoutError:
    #     youtube_dl_process.kill()
    #     raise
    # finally:
    #     youtube_dl_process.kill()
    
    # try:
    #     youtube_dl_process = await asyncio.create_subprocess_exec(*command)
    #     await asyncio.wait_for(youtube_dl_process, timeout=video_length)
    #     if youtube_dl_process.returncode != 0:
    #         raise asyncio.TimeoutError
    # except asyncio.TimeoutError:
    #     youtube_dl_process.kill()
    #     raise
    # finally:
    #     youtube_dl_process.kill()
    
    # Start the youtube_dl_process asynchronously
    youtube_dl_process = await asyncio.create_subprocess_exec(*command)

    # Wait for the youtube_dl_process to finish or timeout, whichever happens first
    # try:
    #     youtube_dl_process = asyncio.create_task(asyncio.create_subprocess_exec(*command))
    #     await asyncio.wait_for(youtube_dl_process, timeout=video_length)
    # except asyncio.TimeoutError:
    #     youtube_dl_process.kill()
    #     raise
    # finally:
    #     youtube_dl_process.kill()
        
    # THIS one works but have to hold donw ctrl c    
    try:
        youtube_dl_process = await asyncio.create_subprocess_exec(*command)
        await asyncio.wait_for(youtube_dl_process.wait(), timeout=video_length)
    except asyncio.TimeoutError:
        youtube_dl_process.kill()
        raise
    finally:
        youtube_dl_process.kill()


    # try:
    #     await asyncio.wait_for(youtube_dl_process, timeout=video_length)
    # except asyncio.TimeoutError:
    #     youtube_dl_process.kill()
    #     raise
        

    # Check the return code of the youtube_dl_process
    if youtube_dl_process.returncode != 0:
        youtube_dl_process.kill()
        raise

    # Capture images from the video
    await capture_images.capture_images(video_id)

if __name__ == "__main__":
    # Set the URL of the YouTube live video and run
    url = "https://www.youtube.com/watch?v=ydYDqZQpim8"
    asyncio.run(download_video(url))
