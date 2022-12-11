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
    
    # Record start time
    start = time.time()

    # Start video capture
    with multiprocessing.Pool() as pool:
        pool.map(download_video_function, urls)

    # Start parallel image capture
    with multiprocessing.Pool() as pool:
        pool.map(partial(capture_images_function, capture_interval = capture_interval), urls)

    # Record end time
    end = time.time()

    # Calculate elapsed time
    elapsed_time = end - start
    
    print(f'Video was downloaded and captured for {elapsed_time}')