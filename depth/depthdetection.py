import cv2
import numpy as np

print("Opening video")

# Define bounds of color range to detect in HSV
# Darker - RGB (169, 50, 24) --> HSV (11, 86, 66)
# Lighter - RGB (198, 80, 38) --> HSV (16, 81, 78)
# CLose object
lower_hue_close = -10
upper_hue_close = 8
lower_saturation_close = 150
upper_saturation_close = 255

# Near object
lower_hue_near = 18
upper_hue_near = 26
lower_saturation_near = 150
upper_saturation_near = 255

# Far object
lower_hue_far = 18
upper_hue_far = 26
lower_saturation_far = 150
upper_saturation_far = 255

cap = cv2.VideoCapture('videos/trashCenter.mp4')
count = 0
numFrames = 0
objectDetected = False
scale = 2

leftDetected = 0
cetnerDetected = 0
rightDetected = 0

# Parse video frames
while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Change the dimensions of the displayed video
    height, width, layers = frame.shape
    display_height = int(height / scale)
    display_width = int(width / scale)
    display_frame = cv2.resize(frame, (display_width, display_height))

    # Divide canvas into sections
    section_width = width // 3
    left_section = section_width
    center = 2*section_width
    right_section = width

    # Convert BGR to HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Near objects --------------------------------------------------


    # Close objects --------------------------------------------------
    # Define range of color in HSV
    lower_color = np.array([lower_hue_close, lower_saturation_close])
    upper_color = np.array([upper_hue_close, upper_saturation_close])

    # Threshold the HSV image to get only desired colors
    mask = cv2.inRange(hsv_frame[:,:,0:2], lower_color, upper_color)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    display_result = cv2.resize(result, (display_width, display_height))

    # Find the average coordinates of object
    coordinates = np.column_stack(np.where(mask > 0))
    if (len(coordinates) > 0 and objectDetected):
        average_coordinates = np.mean(coordinates, axis=0)
        # print("Average Coordinates: ", average_coordinates)
    else:
        average_coordinates = None

    # Decide which portion of the canvas object is in
    if (objectDetected and int(average_coordinates[1]) < left_section):
        print("left frame")
        leftDetected = 3
    elif (objectDetected and int(average_coordinates[1]) < center):
        print("center frame")
        cetnerDetected = 3
    elif (objectDetected):
        print("right frame")
        rightDetected = 3

    

    # Shows resulting masked video
    if np.any(result):
        if (objectDetected):
            # print("inside")
            display_result = cv2.circle(display_result, (int(average_coordinates[1]/scale), int(average_coordinates[0]/scale)), 5, (255, 0, 0), -1)
        cv2.imshow("Filtered Frame", display_result)
        numFrames += 1
    
    if (numFrames == 25):
        objectDetected = True
        print("Close object detected")

    cv2.imshow('window-name', display_frame)
    # cv2.imwrite("frame%d.jpg" % count, display_frame)  # Fixed typo here
    count += 1
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()  # destroy all opened windows

print("Video finished")

