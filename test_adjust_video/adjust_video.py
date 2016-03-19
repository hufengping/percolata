import sys
import time
import numpy as np
import cv2
DARK_THRESHOLD = 60
BRIGHT_THRESHOLD = 170

def process_video(video_file):
    cap = cv2.VideoCapture(video_file)
    video_width = cap.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)
    video_height = cap.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)
    count = 0
    scale_sum = 0
    scale_avg = -1
    while True:
        ret, frame = cap.read()
        if ret == True:
            tmp_frame = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
            if count < 75:
                count += 1
                scale_sum += np.sum(tmp_frame) / (video_height*video_width)
            else:
                if scale_avg == -1:
                    scale_avg = scale_sum/75
                if scale_avg < DARK_THRESHOLD:
                    # The algorithm normalizes the brightness and increases the contrast of the image.
                    res_append = cv2.equalizeHist(tmp_frame)
                elif scale_avg > BRIGHT_THRESHOLD:
                    tmp_frame = np.uint8( tmp_frame * 0.8 )
                    clahe = cv2.createCLAHE(clipLimit=4.0)
                    # Equalizes the histogram of a grayscale image using Contrast Limited Adaptive Histogram Equalization. Simple illumination correction
                    res_append = clahe.apply(tmp_frame)
                else:
                    res_append = tmp_frame
                res = np.hstack((tmp_frame,res_append)) #stacking images side-by-side
                cv2.imshow('res.png',res)
                k = cv2.waitKey(10) & 0xff
                if k == 27: #press esc to quit
                    break
        else:
            break
    cap.release()
    cv2.destroyAllWindows()
    time.sleep(5)

# usage python adjust_video.py video_path
if __name__=='__main__':
    process_video(sys.argv[1])