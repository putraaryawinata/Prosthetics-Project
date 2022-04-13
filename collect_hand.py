import cv2
import time
#Import the module
import posebody as pb

previousTime = 0
detector = pb.Pose_detector()

## OPTION: USING video on file
cap = cv2.VideoCapture(0)

## OPTION: USING direct video Define the codec and create VideoWriter object
#cap = cv2.VideoCapture('filename')
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out_frame_size = (int(cap.get(3)), int(cap.get(4))) #size in (width, height)
out = cv2.VideoWriter('outhand.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, out_frame_size)

while cap.isOpened():
    success, img = cap.read()
        
    # BGR 2 RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)    
    # Flip on horizontal
    img = cv2.flip(img, 1)
        
    # Detections
    results = detector.hand.process(img)
    if type(results.multi_hand_landmarks) == type(None):
        print('tidak terdeteksi')
        continue
    
    # RGB 2 BGR
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    joint_list = [[7,6,5], [11,10,9], [15,14,13], [19,18,17]]
    # Rendering results
    if results.multi_hand_landmarks:
        for num, hand in enumerate(results.multi_hand_landmarks):
            detector.mpDraw.draw_landmarks(img, hand, detector.mpHands.HAND_CONNECTIONS, 
                                           detector.mpDraw.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                           detector.mpDraw.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                          )
                
        detector.draw_finger_angles(img, joint_list)
        
    cv2.imshow('Hand Tracking', img)

    out.write(img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

out.release()
cap.release()
cv2.destroyAllWindows()