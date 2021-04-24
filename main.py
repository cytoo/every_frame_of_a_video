import config
import cv2
import os
import time

from telegram.ext import Updater

VID_FRAMES = 0
VID_NAME = ""


def prog_bar(current, total):
    progress = int(current * 100 / total)
    print(f"Frame extraction: {progress}% {current}/{total}")


def extract_frames(vid_path: str):
    global VID_FRAMES, VID_NAME
    video_name = vid_path.split(".")[0]
    if not os.path.exists("extracted"):
        os.makedirs("extracted")
    frame_count = 1
    capture = cv2.VideoCapture(vid_path)
    total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    VID_FRAMES = total_frames
    VID_NAME = video_name
    while frame_count < total_frames:
        ret, frame = capture.read()
        file_frame_name = f"extracted/{video_name}_{frame_count}.jpg"
        cv2.imwrite(file_frame_name, frame)
        prog_bar(frame_count, VID_FRAMES)
        frame_count += 1
    capture.release()
    print(f"{video_name} extraced.")


def send_frames(client):
    bot = client.bot
    for i in range(1, VID_FRAMES):
        fname = f"extracted/{VID_NAME}_{i}.jpg"
        bot.send_photo(
            config.channel,
            photo=open(fname, "rb"),
            caption=f"frame {i} out of {VID_FRAMES}"
        )
        print(f"sent frame number {i}")
        time.sleep(60)

    bot.send_message(config.channel, "that's all fuckers")


if __name__ == "__main__":
    extract_frames(config.vid)
    send_frames(Updater(token=config.token, use_context=True))