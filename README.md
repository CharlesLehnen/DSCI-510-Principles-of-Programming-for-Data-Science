# Building the Foundation of a Largescale Classification Dataset for African Megafauna from YouTube Livestreams Using Computer Vision

For my doctoral research, I am investigating the evolutionary and ecology relationship betweenGiant Galapagos tortoises (*Chelonoidis niger sspp.*) and Galapagos land iguanas (*Conolophus spp.*). As an aspect of this work, I will be stationing trail cameras on Santa Fe Island to observe and compare feeding habitats. In order to analyze this data, I will separate video footage into images, classify these images based on which species is present, and then analyze the behavior seen in each image. In order to develop this workflow, I wrote a program to capture images from a video at set intervals. Then, in order to analyze this data, I will separate video footage into images, classify these images based on which species is present, and then analyze the behavior seen in each image. To dramatically improve efficiency, a classification program will be very useful, so I developed the foundation of one.

There is not yet a publicly available labelling dataset for African megafauna in computer vision applications. YouTube Livestreams are a publicly available resource for viewing wildlife from around the world. I began the development of a classification dataset to train a model on African megafauna by completing the following:

1. Video download of YouTube livestreams of trail cameras in order to simulate my own trail camera footage
2. Image capture of these livestreams in real-time at set intervals for analysis
3. Object detection of the presence of animals in captured images
4. Cropping of images around individual animals
5. Manually classifying of individual animals by species as a proof of concept for developing a custom classifier
6. Preliminary analyses of the counts of individual animals at varying timepoints throughout the day



# Dependencies

This project was created and developed within a *minicoda* environment. All dependencies, including versions, that were used in the development of this project can be found in the `requirements.txt` file, which can be found in the root directory of the [project GitHub](https://github.com/CharlesLehnen/DSCI-510-Principles-of-Programming-for-Data-Science). The dependencies are listed here as well:

```
# This file may be used to create an environment using:
# $ conda create --name <env> --file <this file>
# platform: win-64
_r-mutex=1.0.1=anacondar_1
anyio=3.6.2=pyhd8ed1ab_0
aom=3.5.0=h63175ca_0
argon2-cffi=21.3.0=pyhd8ed1ab_0
argon2-cffi-bindings=21.2.0=py310h8d17308_3
asttokens=2.2.0=pyhd8ed1ab_0
asyncio=3.4.3=pypi_0
attrs=22.1.0=pyh71513ae_1
babel=2.11.0=pyhd8ed1ab_0
backcall=0.2.0=pyh9f0ad1d_0
backports=1.1=pyhd3eb1b0_0
backports.functools_lru_cache=1.6.4=pyhd8ed1ab_0
beautifulsoup4=4.11.1=pyha770c72_0
bleach=5.0.1=pyhd8ed1ab_0
brotlipy=0.7.0=py310h8d17308_1005
bzip2=1.0.8=h8ffe710_4
ca-certificates=2022.12.7=h5b45459_0
certifi=2022.12.7=pyhd8ed1ab_0
cffi=1.15.1=py310h628cb3f_2
charset-normalizer=2.1.1=pyhd8ed1ab_0
colorama=0.4.6=pyhd8ed1ab_0
contourpy=1.0.6=pypi_0
cryptography=38.0.4=py310h6e82f81_0
cycler=0.11.0=pypi_0
debugpy=1.6.4=py310h00ffb61_0
decorator=5.1.1=pyhd8ed1ab_0
defusedxml=0.7.1=pyhd8ed1ab_0
entrypoints=0.4=pyhd8ed1ab_0
executing=1.2.0=pyhd8ed1ab_0
expat=2.5.0=h1537add_0
ffmpeg=1.4=pypi_0
flit-core=3.8.0=pyhd8ed1ab_0
font-ttf-dejavu-sans-mono=2.37=hab24e00_0
font-ttf-inconsolata=3.000=h77eed37_0
font-ttf-source-code-pro=2.038=h77eed37_0
font-ttf-ubuntu=0.83=hab24e00_0
fontconfig=2.14.1=hbde0cde_0
fonts-conda-ecosystem=1=0
fonts-conda-forge=1=0
fonttools=4.38.0=pypi_0
freeglut=3.2.2=h0e60522_1
freetype=2.12.1=h546665d_1
ftfy=6.1.1=pypi_0
gettext=0.21.1=h5728263_0
glib=2.74.1=h12be248_1
glib-tools=2.74.1=h12be248_1
gst-plugins-base=1.21.2=h001b923_0
gstreamer=1.21.2=h6b5321d_0
icu=70.1=h0e60522_0
idna=3.4=pyhd8ed1ab_0
importlib-metadata=5.1.0=pyha770c72_0
importlib_resources=5.10.0=pyhd8ed1ab_0
intel-openmp=2022.2.1=h57928b3_19741
ipykernel=6.15.2=py310haa95532_0
ipython=8.6.0=py310haa95532_0
ipython_genutils=0.2.0=py_1
jasper=2.0.33=h77af90b_0
jedi=0.18.2=pyhd8ed1ab_0
jinja2=3.1.2=pyhd8ed1ab_1
joblib=1.2.0=pypi_0
jpeg=9e=h8ffe710_2
json5=0.9.6=pyhd3eb1b0_0
jsonschema=4.17.3=pyhd8ed1ab_0
jupyter-kite=2.0.2=pypi_0
jupyter_client=7.4.7=pyhd8ed1ab_0
jupyter_core=5.1.0=py310h5588dad_0
jupyter_server=1.23.3=pyhd8ed1ab_0
jupyterlab=3.5.0=pyhd8ed1ab_0
jupyterlab_pygments=0.2.2=pyhd8ed1ab_0
jupyterlab_server=2.16.3=pyhd8ed1ab_0
kiwisolver=1.4.4=pypi_0
krb5=1.19.3=hc8ab02b_0
lcms2=2.14=h90d422f_0
lerc=4.0.0=h63175ca_0
libblas=3.9.0=16_win64_mkl
libcblas=3.9.0=16_win64_mkl
libclang=15.0.6=default_h77d9078_0
libclang13=15.0.6=default_h77d9078_0
libdeflate=1.14=hcfcfb64_0
libffi=3.4.2=h8ffe710_5
libglib=2.74.1=he8f3873_1
libhwloc=2.8.0=h039e092_1
libiconv=1.17=h8ffe710_0
liblapack=3.9.0=16_win64_mkl
liblapacke=3.9.0=16_win64_mkl
libogg=1.3.5=h2bbff1b_1
libopencv=4.6.0=py310hb22e633_6
libpng=1.6.39=h19919ed_0
libprotobuf=3.21.11=h12be248_0
libsodium=1.0.18=h8d14728_1
libsqlite=3.40.0=hcfcfb64_0
libtiff=4.4.0=h8e97e67_4
libvorbis=1.3.7=h0e60522_0
libwebp-base=1.2.4=h8ffe710_0
libxcb=1.13=hcd874cb_1004
libxml2=2.10.3=hc3477c8_0
libzlib=1.2.13=hcfcfb64_4
m2w64-bwidget=1.9.10=2
m2w64-bzip2=1.0.6=6
m2w64-expat=2.1.1=2
m2w64-fftw=3.3.4=6
m2w64-flac=1.3.1=3
m2w64-gcc-libgfortran=5.3.0=6
m2w64-gcc-libs=5.3.0=7
m2w64-gcc-libs-core=5.3.0=7
m2w64-gettext=0.19.7=2
m2w64-gmp=6.1.0=2
m2w64-gsl=2.1=2
m2w64-libiconv=1.14=6
m2w64-libjpeg-turbo=1.4.2=3
m2w64-libogg=1.3.2=3
m2w64-libpng=1.6.21=2
m2w64-libsndfile=1.0.26=2
m2w64-libtiff=4.0.6=2
m2w64-libvorbis=1.3.5=2
m2w64-libwinpthread-git=5.0.0.4634.697f757=2
m2w64-libxml2=2.9.3=3
m2w64-mpfr=3.1.4=4
m2w64-pcre2=10.34=0
m2w64-speex=1.2rc2=3
m2w64-speexdsp=1.2rc3=3
m2w64-tcl=8.6.5=3
m2w64-tk=8.6.5=3
m2w64-tktable=2.10=5
m2w64-wineditline=2.101=5
m2w64-xz=5.2.2=2
m2w64-zlib=1.2.8=10
markupsafe=2.1.1=py310h8d17308_2
matplotlib=3.6.2=pypi_0
matplotlib-inline=0.1.6=pyhd8ed1ab_0
mistune=2.0.4=pyhd8ed1ab_0
mkl=2022.1.0=h6a75c08_874
msys2-conda-epoch=20160418=1
nb_conda=2.2.1=py310h5588dad_5
nb_conda_kernels=2.3.1=py310h5588dad_2
nbclassic=0.4.8=pyhd8ed1ab_0
nbclient=0.7.2=pyhd8ed1ab_0
nbconvert=7.2.5=pyhd8ed1ab_0
nbconvert-core=7.2.5=pyhd8ed1ab_0
nbconvert-pandoc=7.2.5=pyhd8ed1ab_0
nbformat=5.7.0=pyhd8ed1ab_0
nest-asyncio=1.5.6=pyhd8ed1ab_0
nodejs=0.1.1=pypi_0
notebook=6.5.2=pyha770c72_1
notebook-shim=0.2.2=pyhd8ed1ab_0
npm=0.1.1=pypi_0
numpy=1.23.5=py310h4a8f9c9_0
opencv=4.6.0=py310h5588dad_6
openh264=2.3.1=h63175ca_1
openjpeg=2.5.0=hc9384bd_1
openssl=3.0.7=hcfcfb64_1
optional-django=0.1.0=pypi_0
packaging=21.3=pyhd8ed1ab_0
pandas=1.5.2=pypi_0
pandoc=2.19.2=h57928b3_1
pandocfilters=1.5.0=pyhd8ed1ab_0
parso=0.8.3=pyhd8ed1ab_0
patsy=0.5.3=pypi_0
pcre2=10.40=h17e33f8_0
pickleshare=0.7.5=py_1003
pillow=9.3.0=pypi_0
pip=22.3.1=pyhd8ed1ab_0
pkgutil-resolve-name=1.3.10=pyhd8ed1ab_0
platformdirs=2.5.2=pyhd8ed1ab_1
plotly=5.11.0=pypi_0
plotly-express=0.4.1=pypi_0
prometheus_client=0.15.0=pyhd8ed1ab_0
prompt-toolkit=3.0.33=pyha770c72_0
psutil=5.9.4=py310h8d17308_0
pthread-stubs=0.4=hcd874cb_1001
pthreads-win32=2.9.1=hfa6e2cd_3
pure_eval=0.2.2=pyhd8ed1ab_0
py-opencv=4.6.0=py310hbbfc1a7_6
pycparser=2.21=pyhd8ed1ab_0
pygments=2.13.0=pyhd8ed1ab_0
pyopenssl=22.1.0=pyhd8ed1ab_0
pyparsing=3.0.9=pyhd8ed1ab_0
pyperclip=1.8.2=pypi_0
pyrsistent=0.19.2=py310h8d17308_0
pyshow=0.0.1=pypi_0
pysocks=1.7.1=py310h5588dad_5
python=3.10.8=h4de0772_0_cpython
python-dateutil=2.8.2=pyhd8ed1ab_0
python-fastjsonschema=2.16.2=pyhd8ed1ab_0
python_abi=3.10=3_cp310
pytube=12.1.0=pypi_0
pytz=2022.6=pyhd8ed1ab_0
pywin32=305=py310h2bbff1b_0
pywinpty=2.0.9=py310h00ffb61_0
pyzmq=24.0.1=py310hcd737a0_1
qt-main=5.15.6=hb9439ea_3
r-base=4.1.3=hdca333a_3
r-mass=7.3_58.1=r41h6d2157b_1
r-signal=0.7_7=r41he816bda_2
requests=2.28.1=pyhd8ed1ab_1
scikit-learn=1.2.0=pypi_0
scipy=1.9.3=pypi_0
seaborn=0.12.1=pypi_0
send2trash=1.8.0=pyhd8ed1ab_0
setuptools=65.5.1=pyhd8ed1ab_0
six=1.16.0=pyh6c4a22f_0
sklearn=0.0.post1=pypi_0
sniffio=1.3.0=pyhd8ed1ab_0
soupsieve=2.3.2.post1=pyhd8ed1ab_0
speechrecognition=3.9.0=pypi_0
stack_data=0.6.2=pyhd8ed1ab_0
statsmodels=0.13.5=pypi_0
svt-av1=1.3.0=h63175ca_0
tbb=2021.7.0=h91493d7_1
tenacity=8.1.0=pypi_0
terminado=0.15.0=py310h5588dad_0
threadpoolctl=3.1.0=pypi_0
tinycss2=1.2.1=pyhd8ed1ab_0
tk=8.6.12=h8ffe710_0
tomli=2.0.1=pyhd8ed1ab_0
torch=1.13.0=pypi_0
torchvision=0.14.0=pypi_0
tornado=6.2=py310h8d17308_1
traitlets=5.6.0=pyhd8ed1ab_0
typing_extensions=4.4.0=pyha770c72_0
tzdata=2022g=h191b570_0
ucrt=10.0.22621.0=h57928b3_0
urllib3=1.26.13=pyhd8ed1ab_0
vc=14.3=h3d8a991_9
vs2015_runtime=14.32.31332=h1d6e394_9
wcwidth=0.2.5=pyh9f0ad1d_2
webencodings=0.5.1=py_1
websocket-client=1.4.2=pyhd8ed1ab_0
wget=3.2=pypi_0
wheel=0.38.4=pyhd8ed1ab_0
win_inet_pton=1.1.0=py310h5588dad_5
winpty=0.4.3=4
x264=1!164.3095=h8ffe710_2
x265=3.5=h2d74725_3
xeus-python=0.15.0=pypi_0
xeus-python-shell=0.5.0=pypi_0
xorg-libxau=1.0.9=hcd874cb_0
xorg-libxdmcp=1.1.3=hcd874cb_0
xz=5.2.8=h8cc25b3_0
youtube-dl=2021.12.17=pypi_0
youtube-stream=0.0.14=pypi_0
zeromq=4.3.4=h0e60522_1
zipp=3.11.0=pyhd8ed1ab_0
zstd=1.5.2=h7755175_4
```

# Running the project

1) Install dependencies:

```
pip install -r requirements.txt
```


2) After installation of dependencies, you will call the files `download_videos.py` and `capture_images.py` by calling the single file:

```
python code/main.py
```

3) You will need to enter `Ctrl C` on your keyboard to terminate `youtube-dl`. This library evades all other methods to terminate unless the video has ended, which is not the case with 24/7 live cameras, so manual termination is required. Results can be viewed in the `code\data\videos` and `code\data\images` folders. 

4) If you are satisfied with the images, you can begin the classification process. First the program will prompt you to ask if you would like to generate full images that include bounding boxes around invidual animals. If you select `y`, you can view the results is the `code\data\images\bounded` directory. These images are useful for deciding if model parameters should be changed. Then, the program will ask if you would like to begin manual classification of images. If you select `y`, results of images features only invidual animals from a given images can be found in the folder `code\data\images\cropped`. This proess is begun by calling:

```
python code/image_classification.py
```

5) Once completed, you can run the preliminary analysis code. For purposes of visualization, it is recommended that the analysis be conducted in the Jupyter Notebook version of the analyses files which can be found at `code\analyze_data.ipynb`. 


# Methodology

## Imagery capture

I studied parallel processing in order to develop a program that could capture multiple videos and gather images from them in real-time using a `multiprocessing` workflow. Using `youtube-dl`, videos are captured for up to 6 hours at a time without timing out. Note that the `youtube-dl` program **must** be terminated manually with `Ctrl + C`. This program must be run overnight because of the difference in African timezones compared to the United States. I originally wanted this code to begin and stop each night automatically, but it does not seem like that is possible with the way that `youtube-dl` operates.

The streams [Namibia: Live stream in the Namib Desert](https://www.youtube.com/watch?v=ydYDqZQpim8) and [Africam Nkorho Bush Lodge powered by EXPLORE.org](https://www.youtube.com/watch?v=gUZjDCZEMDA) were used, although the code is designed so that many more urls could be passed in and be processed in parallel. A third live stream, [Tembe Elephant Park, South Africa](https://www.youtube.com/watch?v=UeB6UcZpUz) was originally use, but this link is no longer active. In order to not lose resolution with image capture, videos are high quality `.mp4` files by preserving highest quality of sources (1080p).

I utlized what I had learned about parrallel processing to capture images from the YouTube livestreams in real time. In order to have diversity in the images captured, I set my parameters to capture images every 10 minutes. Images were collected as `.jpg` files, stored in the `./code/data/images` folder of my directory. The program checks which files are in the folder before beginning so that it does not overwrite existing files so that it can be run on sequential nights without supervision. A selection of some images are included for your review.

Applying the concepts learned in class, both the `download_videos.py` and `capture_images.py` scripts can be run independently from one another using the `if __name__ == "__main__":` class definition. However, I designed these scripts intentionally to run simultaneously so that realtime analysis could be conducted. The parallel processing of these scripts is deployed by running the `get_data.py` script which calls in the functions defined in the `download_videos.py` and `capture_images.py` scripts.

I had collected over 12 hours of video, running this program overnight because of timezone differences, and hundreds of associated images before I shifted my methodologies to include taking timepoints at the moment of image capture in order to conduct further analyses with this information. Since that time, I have collected an additional 12 hours of video and 265 associated images. This resulted in 18,200 cropped images of individual animals that could theoretically be used for classification. 

## Image classification

Using the `torchvision` *FasterRCNN_ResNet50_FPN_V2* model that was presented in class, labelled bounding boxes were applied to the captured images. There is not a classifier built for African wildlife, so the COCO classification library was used to label animals more generally. In line with the concept of functional programming, primary functionality is stored in the `classify_and_crop` function so that it could be used elsewhere. For the same reason, the functions `separate_into_sets`, which divides filepaths randomly into training, validation, and test sets, as well as the bounding box drawing function `bounding_boxes` are now separated out into their own functions. When this program is called, the user is prompted whether they want to run the program or not before beginning, because the program may overwrite existing files.

Following object oriented programming principles, the `Dataset` class of the `Pytorch` was extended to make the `AnimalDataset` class which stores classified labels in a specific format that will be easily readable by a classifier like *Faster RCNN* to generate a customized model to species of interest. I had hoped to generate a large enough dataset to run a preliminary test of customizing the classifier with my data. However, I found that I needed far more than I could produce in this time period.

# Visualization

Beyond the visualizations of bounding boxes and cropped images from the classification workflow, the following analyses were also conducted. As you run the code, you will not have access to the same images because of the upload limits. However, examples of my output can be found in the `results` directory.

In general, I had hoped to have more continous datasets for these analyses. However, I was able to truncate the dataset through `pandas` filtering in order to analyze a biologically interesting time period of mid-day to dusk.

## Timeseries

A line plot for each site was plotted over time, This timeseries analysis showed a similar trend in activity between the two sites. Activity, as inferred by number of individuals, decreases from 1:30pm to 5:00pm across sites.   
## PCA

An interative 3D PCA can give further insight into the activity patterns of animals at the studied sites. Viewed from above, it is visible that ther is likely a difference in how animals respond to the change of hour on a given day. This initial observation could inspire a study into why these difference exist.

As an advanced visualization, by creating an interactive 3D plot, the complexity of the ecosystem can be better understood, as seen in the interplay between three variables. The reason this plot is so powerful is that because the plot is interactive, complex multi-dimensional relationshps can be more easily explored.

## Linear regression

In order to quantify the correlation between the count of animals and the time of day, a simple correlation analysis was conducted. The similar slopes in the trends between sites are inline with the trend in the time series. However, the trendlines are offset, which is in agreement with the above view of the PCA plot. Altogether, there is a similar response of animals to the changing times of the day across these two sites, however these responses are not identical even though these sites are geographically similar with overlapping species and common climatic conditions. It would be interesting to study why these similarities/differences may be occuring.

These initial analyses encourage further inquiry, but because of the short sampling period of two days, statstical significance cannot be derived from any of the exploratory analyses detailed here.

# Future Work

The analyses detalied about could provide information that would inform biologist seeking to collect appropriate field data, conservations on the need to adjust monitoring counts depending on the time of day, and even tour operators seeking to maximize the exposure of clients to wildlife. With more time, a classification dataset could be generated. I would then use the training and validation sets can be used to make a customized classifier. The accuracy of this classifier would be tested on the test set. This dataset would then be used to create a custom classifier built on the *FasterRCNN_ResNet50_FPN_V2* model. A well trained classifier requires the manual classification of 10,000+ images. This large quantity of images can be difficult to obtain, especially of subjects at different angles, moving differently, in different lighting, etc. By screencapturing from livestreams, thousands of a large variety of images can be produced. Because I designed this program using parallel processing techniques, multiple YouTube livestreams can be captured all while being manually classified nearly simultaneously by running the `get_data.py` and `image_classification` programs at the same time. Manual classification could potentially even constitute an undergraduate research project. Through USC's undergraduate research program, a small group of students could aid in this research by manually classifying wildlife and, in doing so, learn about principles of animal behavior, ecology, machine learning, and programming.

After species are identififed and quantified in each image, more complex ecological analyses could be conducted. The alpha and beta diversity of species between sites could be compared and the trends observed could be correlated with other factors to explore ecological questions.

Beyond my interest in this project as an important tool for my own doctoral research, this individual project could be furthter developed upon to become a useful tool. It could be run for many days during different seasons to analyze changing distributions of animals. Because it is conducted in realtime, could be used to inform conservation efforts or even aid in the response to poaching. This tool would be particularly for behavioral ecologists who could use a program like this to analyze behavior at set timepoints, a common methodology called "point sampling," instead of having to do so in the field.

It could feasibly be further developed to properly train a classifier of African wildlife following some further development and by running for long periods of time for multiple YouTube streams. 

Additionally, I will also use this model in my own dissertation work to classify images of tortoises, iguanas, and no animals in order to make the analysis of camera trap data much more efficient.
