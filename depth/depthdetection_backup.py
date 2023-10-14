import cv2
import numpy as np

print("Opening video")

# Define bounds of color range to detect in HSV
# Darker - RGB (169, 50, 24) --> HSV (11, 86, 66)
# Lighter - RGB (198, 80, 38) --> HSV (16, 81, 78)
lower_hue = -10
upper_hue = 8
lower_saturation = 150
upper_saturation = 255

cap = cv2.VideoCapture('videos/trashCenter.mp4')
count = 0
numFrames = 0

# Parse video frames
while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Change the dimensions of the displayed video
    height, width, layers = frame.shape
    display_height = int(height / 2)
    display_width = int(width / 2)
    display_frame = cv2.resize(frame, (display_width, display_height))

    # Convert BGR to HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define range of color in HSV
    lower_color = np.array([lower_hue, lower_saturation])
    upper_color = np.array([upper_hue, upper_saturation])

    # Threshold the HSV image to get only desired colors
    mask = cv2.inRange(hsv_frame[:,:,0:2], lower_color, upper_color)
    result = cv2.bitwise_and(frame, frame, mask=mask)
    display_result = cv2.resize(result, (display_width, display_height))

    # Find the average coordinates of object
    coordinates = np.column_stack(np.where(mask > 0))
    if (len(coordinates) > 0 and numFrames > 50):
        average_coordinates = np.mean(coordinates, axis=0)
        print("Average Coordinates: ", average_coordinates)
    else:
        average_coordinates = None

    # Shows resulting masked video
    if np.any(result):
        # print("Frame contains the specified color range.")
        cv2.imshow("Filtered Frame", display_result)
        numFrames += 1
    
    if (numFrames == 25):
        print("Close object detected")

    cv2.imshow('window-name', display_frame)
    # cv2.imwrite("frame%d.jpg" % count, display_frame)  # Fixed typo here
    count += 1
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()  # destroy all opened windows

print("Video finished")

