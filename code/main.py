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

    with multiprocessing.Pool() as pool:
        # Process each URL in parallel
        pool.map(process_url, urls)
