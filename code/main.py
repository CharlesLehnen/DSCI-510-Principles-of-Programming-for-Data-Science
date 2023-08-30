import time
import multiprocessing
import download_video
import capture_images
from functools import partial

# Extract functions from imported modules
download_video_function = download_video.download_video
capture_images_function = capture_images.capture_images

def process_url(url):
    # Download the video for the given URL
    download_video_function(url)
    # Capture images from the downloaded video
    capture_images_function(url)

if __name__ == "__main__":
    # Prompt the user for URLs or use default values
    user_urls = input("Enter the YouTube video URLs separated by commas or press Enter to use default: ").strip()
    if user_urls:
        urls = [url.strip() for url in user_urls.split(",")]
    else:
        # Default URLs
        urls = ["https://www.youtube.com/watch?v=ydYDqZQpim8"]

    # Prompt the user for capture_interval or use default value
    try:
        capture_interval = int(input(f"Enter the capture interval in seconds or press Enter to use default ({300} seconds): ").strip())
    except ValueError:
        capture_interval = 300

    with multiprocessing.Pool() as pool:
        # use partial() so I can feed in keyword args
        capture_images_with_interval = partial(capture_images_function, capture_interval = capture_interval)

        # This was the real trick to get all functions for all urls to run in parallel!
        download_results = [pool.apply_async(download_video_function, (url,)) for url in urls]
        capture_results = [pool.apply_async(capture_images_with_interval, (url,)) for url in urls]

        # Retrieve final results
        download_results = [result.get() for result in download_results]
        capture_results = [result.get() for result in capture_results]