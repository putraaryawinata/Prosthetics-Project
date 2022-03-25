import cv2
import time
#Import the module
import posebody as pb

cap = cv2.VideoCapture(0)
pTime = 0
detector = pb.Pose_detector()

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('test#3.mp4', fourcc, 20.0, (640,  480))
val_angle = []
while True:
    success, img = cap.read()
    img = detector.detect_pose(img, draw=False)
    lmList = detector.position(img, draw=False)
    if len(lmList) == 0:
        continue
    #print(lmList)
    #Detect the landmark of the arm
    #if len(lmList) !=0:
        #print(lmList[14])
        #cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (255, 0, 0), cv2.FILLED)
    
    # left arm detection
    #point_1, point_2, point_3 = 16, 14, 12
    # left leg detection
    point_1, point_2, point_3 = 28, 26, 24

    angle = detector.angle(img, point_1, point_2, point_3, draw=True)
    #angle = 360 - angle
    val_angle.append(angle)
    print("{}: {}".format(len(val_angle), angle))
    #Detect the landmark of the leg
    #if len(lmList) !=0:
    #    print(lmList[14])
    #    cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    #cv2.putText(img, "fps: " + str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                #(255, 0, 0), 3)
    cv2.putText(img, "angle: " + str(int(angle)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
    
    #img = cv2.flip(img, 0)
    # write the flipped frame
    out.write(img)

    cv2.imshow("Image", img)
    cv2.waitKey(1)

out.release()