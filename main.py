import cv2
import re
import os
import sys
from instalooter.looters import PostLooter

destination = os.path.dirname(os.path.realpath(__file__)) + '/downloads/'

# TEXT SETTINGS
# font
font = cv2.FONT_HERSHEY_SIMPLEX

# fontScale
fontScale = 0.75

# White color in BGR
color = (255, 255, 255)

# Line thickness of 2 px
thickness = 1


def get_id_from_url(url):
    """Get the link ID from an instagram url"""
    regex = re.compile('https://www.instagram.com/p/(.*)/(?:.*)', re.I)
    return re.findall(regex, url)[0]


def download_instagram_vid(post_id):
    """Attempt to download the video"""
    try:
        looter = PostLooter(post_id)
    except ValueError:
        print("Couldn't get video from the link. The user's profile may be private.")
        sys.exit(1)
    info = looter.get_post_info(post_id)
    video = info['id']
    username = info['owner']['username']
    return video, username, looter.download_videos(destination)


def generate_source_vid(video, username):
    """Add username to bottom left of video"""
    cap = cv2.VideoCapture(destination + video + ".mp4")
    fps = cap.get(cv2.CAP_PROP_FPS)
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    x, y = size
    pos = (0, y - 10)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(destination + username + '_source.mp4', fourcc, fps, size)
    while cap.isOpened():
        ret, frame = cap.read()
        image = cv2.putText(frame, username + '/instagram', pos, font, fontScale, color, thickness, cv2.LINE_AA)
        if ret:
            # write the frame
            out.write(image)
        else:
            break
    out.release()
    cap.release()
    os.remove(destination + video + ".mp4")
    print('Done! File is located at ' + destination + username + '_source.mp4');


if __name__ == "__main__":
    link = input("Please enter a link from instagram: ")
    link_id = get_id_from_url(link)
    vid, user, dl_worked = download_instagram_vid(link_id)
    if dl_worked:
        generate_source_vid(vid, user)
