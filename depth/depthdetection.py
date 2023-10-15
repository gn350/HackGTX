import cv2
import numpy as np
import json

import sys
sys.path.append('../')

from modelviewscripts import test

detection = []

def depthdetection():
    print("Opening video")

    # Define bounds of color range to detect in HSV
    # Near object
    lower_hue_near = -10
    upper_hue_near = 9
    lower_saturation_near = 150
    upper_saturation_near = 255

    # Close object
    lower_hue_close = -10
    upper_hue_close = 4
    lower_saturation_close = 150
    upper_saturation_close = 255

    cap = cv2.VideoCapture('depthlab_videos/pole_and_stuff.mp4')    
    count = 0
    numFramesNear = 0
    numFramesClose = 0
    objectDetected = False
    closeObjectDetected = False
    scale = 2

    # live video footage
    cap_live = cv2.VideoCapture('C:/Users/gn747/Downloads/ccb_hallways.mp4')
    count_live = 0;

    # Parse video frames
    while cap.isOpened():
        ret, frame = cap.read()

        ret_live, frame_live = cap_live.read()

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
        # Define range of color in HSV
        lower_color_near = np.array([lower_hue_near, lower_saturation_near])
        upper_color_near = np.array([upper_hue_near, upper_saturation_near])

        # Threshold the HSV image to get only desired colors
        mask = cv2.inRange(hsv_frame[:,:,0:2], lower_color_near, upper_color_near)
        result = cv2.bitwise_and(frame, frame, mask=mask)
        display_result = cv2.resize(result, (display_width, display_height))

        # Find the average coordinates of masked area
        coordinates = np.column_stack(np.where(mask > 0))
        if ((len(coordinates) > 0)):
            average_coordinates = np.mean(coordinates, axis=0)
            # print("Average Coordinates: ", average_coordinates)
        else:
            average_coordinates = None

        text = ""

        # Decide which portion of the canvas masked area if object is detected
        if (objectDetected and int(average_coordinates[1]) < left_section and not(closeObjectDetected)):
            print("left near")
            text = "Left, Near"
            detection = [1, 0, 0]
            item = test.imageDetect(cap_live, int(average_coordinates[1]), int(average_coordinates[0]))
            with open("depth/data.json", "w") as json_file:
                data = {"detection": [1, 0, 0], "object": item}
                json.dump(data, json_file)
        elif (objectDetected and int(average_coordinates[1]) < center and not(closeObjectDetected)):
            print("center near")
            text = "Center, Near"
            detection = [0, 1, 0]
            witem = test.imageDetect(cap_live, int(average_coordinates[1]), int(average_coordinates[0]))
            with open("depth/data.json", "w") as json_file:
                data = {"detection": [0, 1, 0], "object": item}
                json.dump(data, json_file)
        elif (objectDetected and not(closeObjectDetected)):
            print("right near")
            text = "Right, Near"
            detection = [0, 0, 1] 
            item = test.imageDetect(cap_live, int(average_coordinates[1]), int(average_coordinates[0]))
            with open("depth/data.json", "w") as json_file:
                data = {"detection": [0, 0, 1], "object": item}
                json.dump(data, json_file)

        if (numFramesNear == 25):
            objectDetected = True
            print("Near object detected")


        # Close objects --------------------------------------------------
        # Define range of color in HSV
        lower_color_close = np.array([lower_hue_close, lower_saturation_close])
        upper_color_close = np.array([upper_hue_close, upper_saturation_close])

        # Threshold the HSV image to get only desired colors -- only for display purposes
        mask2 = cv2.inRange(hsv_frame[:,:,0:2], lower_color_close, upper_color_close)
        result2 = cv2.bitwise_and(frame, frame, mask=mask)
        display_result2 = cv2.resize(result, (display_width, display_height))


        # Decide which portion of the canvas masked area if object is detected
        if (objectDetected and int(average_coordinates[1]) < left_section):
            print("left close")
            text = "Left, Close"
            detection = [2, 0, 0]
            item = test.imageDetect(cap_live, int(average_coordinates[1]), int(average_coordinates[0]))
            with open("depth/data.json", "w") as json_file:
                data = {"detection": [2, 0, 0], "object": item}
                json.dump(data, json_file)
        elif (objectDetected and int(average_coordinates[1]) < center):
            print("center close")
            text = "Center, Close"
            detection = [0, 2, 0]
            item = test.imageDetect(cap_live, int(average_coordinates[1]), int(average_coordinates[0]))
            with open("depth/data.json", "w") as json_file:
                data = {"detection": [0, 2, 0], "object": item}
                json.dump(data, json_file)
        elif (objectDetected):
            print("right close")
            text = "Right, Close"
            detection = [0, 0, 2]
            item = test.imageDetect(cap_live, int(average_coordinates[1]), int(average_coordinates[0]))
            with open("depth/data.json", "w") as json_file:
                data = {"detection": [0, 0, 2], "object": item}
                json.dump(data, json_file)

        if (numFramesClose == 15):
            closeObjectDetected = True
            print("Close object detected")

        # Shows resulting masked video
        if np.any(result):
            if (len(coordinates) > (0.05*display_width*display_height)):
                numFramesClose += 1
                # display_result = cv2.circle(display_result, (int(average_coordinates[1]/scale), int(average_coordinates[0]/scale)), 5, (255, 0, 0), -1)
            # cv2.imshow("Close Object", display_result)
        
        # Shows resulting masked video
        if np.any(result):
            if (len(coordinates) > (0.05*display_width*display_height)):
                numFramesNear += 1
                display_result = cv2.circle(display_result, (int(average_coordinates[1]/scale), int(average_coordinates[0]/scale)), 5, (255, 0, 0), -1)
                display_result = cv2.putText(display_result, text, (int(average_coordinates[1]/scale) - 70, int(average_coordinates[0]/scale) + 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1)
            cv2.imshow("Near object", display_result)

        cv2.imshow('window-name', display_frame)
        count += 1
        count_live += 1
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
        
        # with open("depth/data.json", "w") as json_file:
        #         data = {"detection": [0, 0, 0]}
        #         json.dump(data, json_file)

    cap.release()
    cap_live.release()
    cv2.destroyAllWindows()  # destroy all opened windows

    print("Video finished")


depthdetection()