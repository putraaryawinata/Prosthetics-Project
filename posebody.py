import cv2
import mediapipe as mp
import time
import numpy as np
import math

class Pose_detector():

    #Initialize the class
    def __init__(self):
    #def __init__(self, mode=False, upBody=False, smooth=True,
                 #detectionCon=0.5, trackCon=0.5):

        self.mode = False
        self.upBody = False
        self.smooth = True
        self.detectionCon = 0.5
        self.trackCon = 0.5

        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose()

    #Detecting the pose
    def detect_pose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, self.results.pose_landmarks,
                                           self.mpPose.POSE_CONNECTIONS)
        return img

    #Determine the position of the detected pose
    def position(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList

    #Determine the length of a vector
    def length(vector):
        return (vector.T @ vector)**(0.5)

    #Determine the angle between two point of the pose
    def angle(self, img, point_1, point_2, point_3, draw=True):

        # Get the landmarks
        x1, y1 = self.lmList[point_1][1:]
        x2, y2 = self.lmList[point_2][1:]
        x3, y3 = self.lmList[point_3][1:]
        vector_a = np.array([x1 - x2, y1 - y2])
        vector_b = np.array([x3 - x2, y3 - y2])
        
        print(vector_a)
        # Calculate the Angle
        angle = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        #angle = np.dot(vector_a, vector_b) / (self.length(vector_a) * self.length(vector_b))

        if angle < 0:
            angle += 360
        if angle > 180:
            angle = 360 - angle

        # print(angle)

        # Draw
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(angle)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angle
