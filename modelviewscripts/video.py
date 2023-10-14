import cv2 as cv 
from ultralytics import YOLO

videoPath = "/home/rajoayalew/Clones/model/ccb_hallways.mp4"
modelPath = "/home/rajoayalew/Clones/model/runs/detect/train2/weights/last.pt"

cv.startWindowThread()
capture = cv.VideoCapture(videoPath)

model = YOLO(modelPath)
threshold = 0.5

success, frame = capture.read()

while success:

    results = model(frame)

    for result in results:

        for box in result.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = box

            if score > threshold:
                cv.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
                cv.putText(frame, result.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                                cv.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv.LINE_AA)

    frame = cv.resize(frame, (500, 750))
    cv.imshow("Image", frame)

    success, frame = capture.read()

    # Wait for 1 millisecond for a key event or the window to be closed
    key = cv.waitKey(1) & 0xFF

    # Check if the 'ESC' key or the close button is pressed
    if key == 27 or cv.getWindowProperty("Image", cv.WND_PROP_VISIBLE) < 1:
        break

cv.destroyAllWindows()
