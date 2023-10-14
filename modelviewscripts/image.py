import cv2 as cv 
from ultralytics import YOLO

imagePath = "/home/rajoayalew/Clones/model/image4.jpeg"
modelPath = "/home/rajoayalew/Clones/model/runs/detect/train2/weights/last.pt"

model = YOLO(modelPath)
threshold = 0.5

frame = cv.imread(imagePath)
results = model(frame)
print (type(results))
print (len(results))

for result in results:

    for box in result.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = box

        if score > threshold:
            cv.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
            cv.putText(frame, result.names[int(class_id)].upper(), (int(x1), int(y1 - 10)),
                            cv.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv.LINE_AA)

frame = cv.resize(frame, (500, 750))
cv.imshow("Image", frame)

while True:
    # Wait for 1 millisecond for a key event or the window to be closed
    key = cv.waitKey(1) & 0xFF

    # Check if the 'ESC' key or the close button is pressed
    if key == 27 or cv.getWindowProperty("Image", cv.WND_PROP_VISIBLE) < 1:
        break

cv.destroyAllWindows()

"""
for result in result.boxes.data.tolist():
    x1, y1, x2, y2, score, classId = result

    if score > threshold:
        cv.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 4)
        cv.putText(frame, results.names[int(classId)].upper(), (int(x1), int(y1-10)),
                        cv.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv.LINE_AA)

    cv.imshow(frame)
"""