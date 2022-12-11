import time
import multiprocessing
import download_video
import capture_images
from functools import partial

# Extract functions from imported modules
download_video_function = download_video.download_video
capture_images_function = capture_images.capture_images

if __name__ == "__main__":
    # Select capture interval for capturing images
    capture_interval = 120

    # Set the URLs of the YouTube live videos and run
    urls = ["https://www.youtube.com/watch?v=ydYDqZQpim8", "https://www.youtube.com/watch?v=gUZjDCZEMDA"]
        # Original link I wanted does not work right now: "https://www.youtube.com/watch?v=UeB6UcZpUzk"

    with multiprocessing.Pool() as pool:
        # use partial() so I can feed in keyword args
        capture_images_with_interval = partial(capture_images_function, capture_interval = capture_interval)

        # This was the real trick to get all functions for all urls to run in parallel!
        download_results = [pool.apply_async(download_video_function, (url,)) for url in urls]
        capture_results = [pool.apply_async(capture_images_with_interval, (url,)) for url in urls]

        # Retrieve final results
        download_results = [result.get() for result in download_results]
        capture_results = [result.get() for result in capture_results]


