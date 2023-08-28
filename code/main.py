import time
import multiprocessing
import download_video
import capture_images
from functools import partial

# Extract functions from imported modules
download_video_function = download_video.download_video
capture_images_function = capture_images.capture_images

if __name__ == "__main__":
    # Prompt user for URLs or use default
    default_urls = ["https://www.youtube.com/watch?v=ydYDqZQpim8"]
    urls_input = input("Enter the URLs (comma-separated) or press Enter to use default: ").strip()
    urls = urls_input.split(",") if urls_input else default_urls

    # Prompt user for duration or run indefinitely
    run_for_time = input("Do you want to run the script for a certain amount of time? (yes/no): ").lower()
    duration = 0
    if run_for_time == "yes":
        duration = int(input("Enter the duration in seconds: "))

    # Prompt user for video download choice
    download_video_choice = input("Do you want to download the video? (yes/no): ").lower()

    # Prompt user for screenshot choice and interval
    capture_images_choice = input("Do you want to take screenshots? (yes/no): ").lower()
    capture_interval = 180
    if capture_images_choice == "yes":
        capture_interval = int(input("Enter the screenshot interval in seconds (default is 180): "))

    # Prompt user for running classification script
    run_classification = input("Do you want to run the image_classification.py script simultaneously? (yes/no): ").lower()

    processes = []

    with multiprocessing.Pool() as pool:
        if download_video_choice == "yes":
            processes.extend([pool.apply_async(download_video_function, (url,)) for url in urls])

        if capture_images_choice == "yes":
            capture_images_with_interval = partial(capture_images_function, capture_interval=capture_interval)
            processes.extend([pool.apply_async(capture_images_with_interval, (url,)) for url in urls])

        if run_classification == "yes":
            # Assuming you have a function called classify_images in image_classification.py
            from image_classification import classify_images
            processes.append(pool.apply_async(classify_images))

        # If the user specified a duration, sleep for that duration and then terminate the processes
        if run_for_time == "yes":
            time.sleep(duration)
            for process in processes:
                process.terminate()

        # Retrieve final results
        results = [task.get() for task in processes]
