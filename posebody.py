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
        self.mpHands = mp.solutions.hands
        self.pose = self.mpPose.Pose()
        self.hand = self.mpHands.Hands()
        self.mp_drawing_styles = mp.solutions.drawing_styles
        

    #Detecting the pose and the hand
    ##THE HAND
    def detect_hands(self, img, draw=True):
        imgRGB_hands = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hand.process(imgRGB_hands)
        if results.multi_hand_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img, results.multi_hand_landmarks,
                                           self.mpHands.HAND_CONNECTIONS,
                                           #self.mp_drawing_styles.get_default_hand_landmarks_style(),
                                           #self.mp_drawing_styles.get_default_hand_connections_style()
                                           )
        return img
    #Determine the position of the detected hand
    def draw_finger_angles(self, img, joint_list):
        imgRGB_hands = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hand.process(imgRGB_hands)
        # Loop through hands
        if results.multi_hand_landmarks:
            for hand in results.multi_hand_landmarks:
                #Loop through joint sets 
                for joint in joint_list:
                    a = np.array([hand.landmark[joint[0]].x, hand.landmark[joint[0]].y]) # First coord
                    b = np.array([hand.landmark[joint[1]].x, hand.landmark[joint[1]].y]) # Second coord
                    c = np.array([hand.landmark[joint[2]].x, hand.landmark[joint[2]].y]) # Third coord
                    
                    radians = np.arctan2(c[1] - b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
                    angle = np.abs(radians*180.0/np.pi)
                    
                    if angle > 180.0:
                        angle = 360-angle
                        
                    cv2.putText(img, str(round(angle, 2)), tuple(np.multiply(b, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        return img


    ##THE POSE
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

        #Adjustment of the prototype
        angle = 180 - angle

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
