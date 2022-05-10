import cv2
import time
#Import the module
import posebody as pb
import csv

pTime = 0
detector = pb.Pose_detector()

## OPTION: USING video on file
cap = cv2.VideoCapture('video_angle10mei22#1(naikTangga).mp4')

## OPTION: USING direct video Define the codec and create VideoWriter object
#cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('test#4.mp4', fourcc, 20.0, (640,  480)) #please change the number to avoid overwriting
out_frame_size = (int(cap.get(3)), int(cap.get(4))) #size in (width, height)
out = cv2.VideoWriter('./video_output/video_angle10mei22#1(naikTangga).avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, out_frame_size)
val_angle = []
fps_arr = []

index = 0

header = ['fps', 'angle']
with open('data_angle10mei22#1(naikTangga).csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    # write the header
    writer.writerow(header)
    
while cap.isOpened():
    cTime = time.time()
    if cTime - pTime < 0.1:
        print("less: {}".format(cTime - pTime))
        continue
    fps = 1 / (cTime - pTime)
    pTime = cTime
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
    
    
    #point_1, point_2, point_3 = 16, 14, 12 # left arm detection
    point_1, point_2, point_3 = 28, 26, 24 # left leg detection
    #point_4, point_5, point_6 = 27, 25, 23 # right leg detection

    angle_leg_left = detector.angle(img, point_1, point_2, point_3, draw=True)
    #angle_leg_right = detector.angle(img, point_4, point_5, point_6, draw=True)

    #angle = 360 - angle
    val_angle.append(angle_leg_left)
    print("{}: {}".format(len(val_angle), angle_leg_left))
    #Detect the landmark of the leg
    #if len(lmList) !=0:
    #    print(lmList[14])
    #    cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)

    cv2.putText(img, "fps: " + str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)
    #cv2.putText(img, "angle: " + str(int(angle_leg_left)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                #(255, 0, 0), 3)
    
    #img = cv2.flip(img, 0)
    # write the flipped frame
    index += 1
    row = [int(fps), int(angle_leg_left)]
    with open('data_angle10mei22#1(naikTangga).csv', 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        # write each data
        if index%3 == 0:
            writer.writerow(row)

    out.write(img)

    cv2.imshow("Image", img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
            break

out.release()
cv2.destroyWindow("Image")