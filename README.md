# Building the Foundation of a Largescale Classification Dataset for African Megafauna from YouTube Livestreams Using Computer Vision

There was not yet a publicly available labelling dataset for African megafauna in computer vision applications. YouTube Livestreams are a publicly available resource for viewing wildlife from around the world. I began the development of a classification dataset to train a model on African megafauna by completing the following:

1. Video download of YouTube livestreams of trail cameras in order to simulate my own trail camera footage
2. Image capture of these livestreams in real-time at set intervals for analysis
3. Object detection of the presence of animals in captured images
4. Cropping of images around individual animals
5. Manually classifying of individual animals by species as a proof of concept for developing a custom classifier

# Dependencies

This project was created and developed within a *minicoda* environment. All dependencies, including versions, that were used in the development of this project can be found in the `requirements.txt` and `environment.yml` files, which can be found in the root directory of the [project GitHub](https://github.com/CharlesLehnen/DSCI-510-Principles-of-Programming-for-Data-Science).

# Running the project

1) Install dependencies:

```
pip install -r requirements.txt --upgrade
```

Or can create an environment with the appropriate dependencies, which is the method I reccomend

```
conda env create -f environment.yml
```

2) After installation of dependencies, you will call the file `download_videos.py` which will prompt you to input urls you wish to download from.

3) You will need to enter `Ctrl C` on your keyboard to terminate `yt-dlp`. This library evades all other methods to terminate unless the video has ended, which is not the case with 24/7 live cameras, so manual termination is required. Results can be viewed in the `code\data\videos` folder.

4) Call `capture_images.py` to generate screenshots from the video. This will prompt you to input the urls you used which will be used in naming image files. It will also prompt you for the capture interval for how often you want screenshots to be taken. The results can be found in the `code\data\images` folder. 

4) If you are satisfied with the images, you can begin the classification process. First the program will prompt you to ask if you would like to generate full images that include bounding boxes around invidual animals. If you select `y`, you can view the results is the `code\data\images\bounded` directory. These images are useful for deciding if model parameters should be changed. Then, the program will ask if you would like to begin manual classification of images. If you select `y`, results of images features only invidual animals from a given images can be found in the folder `code\data\images\cropped`. This proess is begun by calling the `image_classification.py` script.


# Methodology

## Imagery capture

I studied parallel processing in order to develop a program that could capture multiple videos and gather images from them in real-time using a `multiprocessing` workflow. Using `youtube-dl`, videos were captured for up to 6 hours at a time without timing out. Note that the `youtube-dl` program **must** be terminated manually with `Ctrl + C`. This program must be run overnight because of the difference in African timezones compared to the United States. I originally wanted this code to begin and stop each night automatically, but it does not seem like that is possible with the way that `youtube-dl` operates.

Since that time, the code has been modified to use `yt-dlp` instead. The keyboard interrupt issue persists. However, now parallel processing is not possible as video files are protected as they are being created so cannot be screenshot in real-time. Because of this, I removed the `main.py` script and recommend not running the video download and screenshotting scripts simultaneously any longer.

The streams [Namibia: Live stream in the Namib Desert](https://www.youtube.com/watch?v=ydYDqZQpim8) and [Africam Nkorho Bush Lodge powered by EXPLORE.org](https://www.youtube.com/watch?v=gUZjDCZEMDA) were originally used, although the code is designed so that many more urls could be passed in and be processed in parallel. A third live stream, [Tembe Elephant Park, South Africa](https://www.youtube.com/watch?v=UeB6UcZpUz) was originally used as well, but this link is no longer active. In order to not lose resolution with image capture, videos are high quality `.mp4` files by preserving highest quality of sources (1080p).

## Image classification

Using the `torchvision` *FasterRCNN_ResNet50_FPN_V2* model that was presented in class, labelled bounding boxes were applied to the captured images. There is not a classifier built for African wildlife, so the COCO classification library was used to label animals more generally. In line with the concept of functional programming, primary functionality is stored in the `classify_and_crop` function so that it could be used elsewhere. For the same reason, the functions `separate_into_sets`, which divides filepaths randomly into training, validation, and test sets, as well as the bounding box drawing function `bounding_boxes` are now separated out into their own functions. When this program is called, the user is prompted whether they want to run the program or not before beginning, because the program may overwrite existing files.

Following object oriented programming principles, the `Dataset` class of the `Pytorch` was extended to make the `AnimalDataset` class which stores classified labels in a specific format that will be easily readable by a classifier like *Faster RCNN* to generate a customized model to species of interest. I had hoped to generate a large enough dataset to run a preliminary test of customizing the classifier with my data. However, I found that I needed far more than I could produce in this time period.

# Future Work

The analyses detalied about could provide information that would inform biologist seeking to collect appropriate field data, conservations on the need to adjust monitoring counts depending on the time of day, and even tour operators seeking to maximize the exposure of clients to wildlife. With more time, a classification dataset could be generated. I would then use the training and validation sets can be used to make a customized classifier. The accuracy of this classifier would be tested on the test set. This dataset would then be used to create a custom classifier built on the *FasterRCNN_ResNet50_FPN_V2* model. A well trained classifier requires the manual classification of 10,000+ images. This large quantity of images can be difficult to obtain, especially of subjects at different angles, moving differently, in different lighting, etc. By screencapturing from livestreams, thousands of a large variety of images can be produced. Because I designed this program initialy using parallel processing techniques, multiple YouTube livestreams can be captured all while being manually classified nearly simultaneously by running the `get_data.py` and `image_classification` programs at the same time. Manual classification could potentially even constitute an undergraduate research project. This is no longer the case in the current version, however multiple urls can still be downloaded and then screenshotted simultaneously. A small group of students could aid in this research by manually classifying wildlife and, in doing so, learn about principles of animal behavior, ecology, machine learning, and programming.

After species are identififed and quantified in each image, more complex ecological analyses could be conducted. The alpha and beta diversity of species between sites could be compared and the trends observed could be correlated with other factors to explore ecological questions.

Beyond my interest in this project as an important tool for my own doctoral research, this individual project could be furthter developed upon to become a useful tool. It could be run for many days during different seasons to analyze changing distributions of animals. Because it is conducted in realtime, could be used to inform conservation efforts or even aid in the response to poaching. This tool would be particularly for behavioral ecologists who could use a program like this to analyze behavior at set timepoints, a common methodology called "point sampling," instead of having to do so in the field.

It could feasibly be further developed to properly train a classifier of African wildlife following some further development and by running for long periods of time for multiple YouTube streams. 

Additionally, I will also use this model in my own dissertation work to classify images of tortoises, iguanas, and no animals in order to make the analysis of camera trap data much more efficient.