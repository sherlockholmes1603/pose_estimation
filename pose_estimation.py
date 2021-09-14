import numpy as np
import cv2
import mediapipe as mp
import math

mpdraw = mp.solutions.drawing_utils
mppose = mp.solutions.pose
pose = mppose.Pose()

cap = cv2.VideoCapture('1.mp4')
see = 0
push_ups = 0

while cap.isOpened():
    success, img = cap.read()
    # img = cv2.resize(img, (600, 600))
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    h, w, c = img.shape
    lmlist = []
    if results.pose_landmarks:
        # mpdraw.draw_landmarks(img, results.pose_landmarks, mppose.POSE_CONNECTIONS)
        for id, lm in enumerate(results.pose_landmarks.landmark):
            cx, cy = int(lm.x * w), int(lm.y * h)
            # print(cx, cy)
            lmlist.append([id, cx, cy])
            # cv2.circle(img, (cx, cy), 5, [255, 0, 0])
        # print(lmlist)
        x1, y1 = lmlist[11][1:]
        cv2.circle(img, (x1, y1), 10, [255, 0, 0], cv2.FILLED)
        x2, y2 = lmlist[13][1:]
        cv2.circle(img, (x2, y2), 10, [255, 0, 0], cv2.FILLED)
        x3, y3 = lmlist[15][1:]
        cv2.circle(img, (x3, y3), 10, [255, 0, 0], cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), [255, 255, 255], 3)
        cv2.line(img, (x3, y3), (x2, y2), [255, 255, 255], 3)
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) - math.atan2(y1 - y2, x1 - x2))
        if angle<0:
            angle += 360
        angle = 360 - angle
        cv2.putText(img, str(int(angle)), (x2 + 20, y2 + 20), cv2.FONT_HERSHEY_COMPLEX, 2, [0, 0, 255], 2)
        if see == 0:
            if angle<90:
                see = 1
        if see == 1:
            if angle>150:
                push_ups += 1
                see = 0
        text = "No. of push ups = " + str(push_ups)
        cv2.putText(img, text, (100 , 40), cv2.FONT_HERSHEY_COMPLEX, 2, [255, 255, 255], 2)
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)

cap.release()
cv2.destroyAllWindows()


