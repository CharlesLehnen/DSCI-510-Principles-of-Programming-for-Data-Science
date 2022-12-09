import os
import time
import subprocess

# Set URL of YouTube live video
url = "https://www.youtube.com/watch?v=ydYDqZQpim8"
first, second = url.split('=')

# Use youtube-dl to extract the streaming URL of the video
url_output = subprocess.run(["youtube-dl", "-g", "-f", "worst", url], capture_output=True)

# Set the time interval (in seconds) for image extraction
interval = 100

# Set the name of the folder for images
folder_name = "images" + "_" + second

# Create new folder if does not exist
if not os.path.exists(folder_name):
    subprocess.run(["mkdir", folder_name])
    
while True:
    # Use subprocess.run to try to run the ffmpeg command in the CL
    # Chose 75kb because want the images a certain size for training/validating classifier
    subprocess.run(["ffmpeg", "-i", url_output.stdout.decode('utf-8'), "-vf", "scale=min(1280\,iw):min(960\,ih):force_original_aspect_ratio=decrease", "-fs", "75000", "-f", "image2", f"{folder_name}/img_%03d.jpeg"])
    
    # Sleep between extractions
    time.sleep(interval)



    
    
    
    
    #os.system('ffmpeg -i {url_output.stdout.decode('utf-8')} -vcodec copy {folder_name}/img_{timestamp}.jpeg'.format(folder_name=folder_name, timestamp=timestamp))
    

    
    #print(f"{url_output.stdout.decode('utf-8')}")
    
    #print('"{url_output.stdout.decode('utf-8')}"'.format(url_output=url_output))
    
    #print('"{folder_name}/img_{timestamp}.jpeg"'.format(folder_name=folder_name, timestamp=timestamp))
    
    
    
    
#this is just what I was using to troubleshoot in the CL
#ffmpeg -i "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1670598186/ei/yvmSY-XjDtaBsfIPq_-RiAI/ip/104.175.212.63/id/ydYDqZQpim8.37/itag/91/source/yt_live_broadcast/requiressl/yes/ratebypass/yes/live/1/sgoap/gir%3Dyes%3Bitag%3D139/sgovp/gir%3Dyes%3Bitag%3D160/hls_chunk_host/rr2---sn-a5mekn6z.googlevideo.com/playlist_duration/30/manifest_duration/30/vprv/1/playlist_type/DVR/initcwndbps/2380000/mh/XM/mm/44/mn/sn-a5mekn6z/ms/lva/mv/m/mvi/2/pl/18/dover/11/pacing/0/keepalive/yes/fexp/24001373,24007246/mt/1670576192/sparams/expire,ei,ip,id,itag,source,requiressl,ratebypass,live,sgoap,sgovp,playlist_duration,manifest_duration,vprv,playlist_type/sig/AOq0QJ8wRgIhANQUpHE4V_zhA_as4o5KguaZziQLhrkivnGYEqrjuNStAiEAmQZz2vxsw-Mf4yRZylO-xqFP6aFjtQyzQK_mwWJjyrQ%3D/lsparams/hls_chunk_host,initcwndbps,mh,mm,mn,ms,mv,mvi,pl/lsig/AG3C_xAwRAIgL-dohp-FTx7R9RauV4yV2j1RPaTKq3Q8H3JOkfIDJh4CIERa72KWWRd48CPtMIOK6aovSNJJqpTWijC6vCUI52xn/playlist/index.m3u8" -vcodec copy images_ydYDqZQpim8/img_20221209_010307_821231.jpeg
