# Simple optical flow algorithm
#
#
# OpenCV version: 2.4.8
#
#
# Contact:
# Min-Hung (Steve) Chen at <cmhungsteve@gatech.edu>
# Chih-Yao Ma at <cyma@gatech.edu>
#
# Last update: 05/16/2016

import numpy as np
import cv2

# read the video file
cap = cv2.VideoCapture('youtubeHorseRide.mp4')

# information of the video
# property identifier:
# 1: ?; 2: s/frame; 3: width; 4: height; 6: ?; 7: ?
Fr = int(round(1 / cap.get(2)))
fps = int(cap.get(cv2.CAP_PROP_FPS))
Wd = int(cap.get(3))
Ht = int(cap.get(4))

# initialize the display window
cv2.namedWindow('flow map')
cv2.namedWindow('Previous, current frames')
# read the first frame
ret, prvs = cap.read()
prvs = cv2.cvtColor(prvs, cv2.COLOR_BGR2GRAY)  # convert to gray scale

# save in HSV (because of the optical flow algorithm we used)
hsv = np.zeros((Ht, Wd, 3)).astype('B')
hsv[..., 1] = 255

indFrame = 1
step = 3
# Define the codec and create VideoWriter object
# fourcc = cv2.cv.CV_FOURCC('X','V','I','D')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('opencvFlow_out.avi', fourcc, fps / step, (Wd, Ht))

while(cap.isOpened):

    # Capture frame-by-frame
    ret, next = cap.read()

    if (indFrame % step) == 0:

        if ret is True:

            # Get frame sizes
            height, width = prvs.shape

            next = cv2.cvtColor(next, cv2.COLOR_BGR2GRAY)

            # normalize across two frames
            # prvs = prvs.astype(float)
            # next = next.astype(float)

            # minVal_R = min(prvs[..., 0].min(), next[..., 0].min())
            # maxVal_R = max(prvs[..., 0].max(), next[..., 0].max())
            # minVal_G = min(prvs[..., 1].min(), next[..., 1].min())
            # maxVal_G = max(prvs[..., 1].max(), next[..., 1].max())
            # minVal_B = min(prvs[..., 2].min(), next[..., 2].min())
            # maxVal_B = max(prvs[..., 2].max(), next[..., 2].max())

            # prvs[..., 0] = (prvs[..., 0] - minVal_R) / (maxVal_R - minVal_R) * 255
            # prvs[..., 1] = (prvs[..., 1] - minVal_G) / (maxVal_G - minVal_G) * 255
            # prvs[..., 2] = (prvs[..., 2] - minVal_B) / (maxVal_B - minVal_B) * 255
            # next[..., 0] = (next[..., 0] - minVal_R) / (maxVal_R - minVal_R) * 255
            # next[..., 1] = (next[..., 1] - minVal_G) / (maxVal_G - minVal_G) * 255
            # next[..., 2] = (next[..., 2] - minVal_B) / (maxVal_B - minVal_B) * 255

            # convert to uint8
            # prvs = prvs.astype('B')
            # next = next.astype('B')

            imgDisplay = np.hstack((prvs, next))
            # cv2.imshow('Frame 1', prvs)
            # cv2.imshow('Frame 2', next)

            # compute the optical flow from two adjacent frames

            flow = cv2.calcOpticalFlowFarneback(
                prvs, next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            # show in RGB for visualization
            mag, ang = cv2.cartToPolar(flow[..., 0], flow[..., 1])
            hsv[..., 0] = ang * 180 / np.pi / 2
            hsv[..., 2] = cv2.normalize(mag, None, 0, 255, cv2.NORM_MINMAX)
            frameProc = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

            # cv2.imwrite('flow.png', frameProc)
            # write the processed frame
            out.write(frameProc)

            # Display the resulting frame
            imgDisplay = cv2.resize(imgDisplay, (0, 0), fx=0.5, fy=0.5)
            frameProc = cv2.resize(frameProc, (0, 0), fx=0.5, fy=0.5)
            cv2.imshow('Previous, current frames', imgDisplay)
            cv2.imshow('flow map', frameProc)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            prvs = next

        else:
            break

    indFrame = indFrame + 1

# When everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()
