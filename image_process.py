#text to speech conversion module import(google's API)
from gtts import gTTS
import cv2
import os
from PIL import Image
from moviepy.editor import AudioFileClip, VideoFileClip

#1 speech creation section
#opening file as read mode
with open("inputFile.txt","r") as file:  
    targetedText = file.read()#reading the text from the file,targetedText will store a string of whole text
#find the word after "keyword:"
keywordIndex = targetedText.find("keyword:")
if keywordIndex !=-1:
    keywordValue = targetedText[(keywordIndex+(len("keyword:"))):].split()[0]
    targetedText = targetedText[(keywordIndex+(len("keyword:"))+len(keywordValue)):].strip()#strip remove leading and trailing whitespace
else:
    print("keyword is not in first place")

print(keywordValue)
print(targetedText)
#language of speech
targetLang = 'en'

#making the text in speech using gTTS
speech = gTTS(text=targetedText, lang=targetLang, slow=False)

#2 image resizing portion
#saving the speech as audio file
speech.save("myTextToAudio.mp3")

#Image folder path reading
folderPath = "H:\code_studio_task\images"

#all image list by entering the folder
imgNameList = os.listdir(folderPath)

#resizing the all images and save them to their original file
for file in imgNameList:
    filePath = os.path.join(folderPath,file)
    with Image.open(filePath) as img:
        resizedImg = img.resize((200,200))
        resizedImg.save(filePath)
       
#3 video creation section start
fps = 0.5
videoName = 'imageToVideo.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#initialize video writer
video = cv2.VideoWriter(videoName,fourcc,fps,(200,200))

#add targeted images to the video
for image in imgNameList:
    decision = image.find(keywordValue)
    if decision !=-1:
        imagePath = os.path.join(folderPath,image)
        imgFrame = cv2.imread(imagePath)
        video.write(imgFrame)

#release video write and all gui
video.release()
cv2.destroyAllWindows()

#4 merge the audio and video using moviepy
#load the audiofile
audioMp3 = AudioFileClip("H:\code_studio_task\myTextToAudio.mp3")
print(f"previous audio duration {audioMp3.duration}")
#load the videofile
videoMp4 = VideoFileClip(videoName)
print(f"video duration {videoMp4.duration}")

#trimming the audio duration because audio is longer than video
audioMp3 = audioMp3.subclip(0, videoMp4.duration)  # Trim audio to match the video's duration
print(f"present audio duration {audioMp3.duration}")

# Set the audio to the video
video_with_audio = videoMp4.set_audio(audioMp3)

# Save the final video
video_with_audio.write_videofile("final_video.mp4", codec="libx264", audio_codec="aac")