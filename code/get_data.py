import time
import multiprocessing
from functools import partial
import download_video
import capture_images

# Extract functions from imported modules
download_video_function = download_video.download_video
capture_images_function = capture_images.capture_images

if __name__ == "__main__":
    
    # Select capture interval for capturing images
    capture_interval = 120
    
    # Set the URLs of the YouTube live videos and run
    urls = ["https://www.youtube.com/watch?v=ydYDqZQpim8", "https://www.youtube.com/watch?v=gUZjDCZEMDA"]
    # Original link I wanted does not work right now: "https://www.youtube.com/watch?v=UeB6UcZpUzk"

    # Start video capture and image capture in parallel
    with multiprocessing.Pool() as pool:
        for url in urls:
            download_result = pool.apply_async(download_video_function, (url,))
            capture_result = pool.apply_async(partial(capture_images_function, capture_interval = capture_interval), (url,))
            
            # Wait for process to finish
            download_result.wait()
            capture_result.wait()
