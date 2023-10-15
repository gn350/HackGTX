
"""
# Import dependencies
import cv2
import torch
import matplotlib.pyplot as plt
import matplotlib as cm
import time
import numpy as np

midas = torch.hub.load('intel-isl/MiDaS', 'MiDaS_small')
midas.to('cuda')
midas.eval()
# Input transformation pipeline
transforms = torch.hub.load('intel-isl/MiDaS', 'transforms')
transform = transforms.small_transform

videoPath = "/home/rajoayalew/Clones/model/testsamples/ccb_hallways.mp4"

# Hook into OpenCV
cap = cv2.VideoCapture(videoPath)

while cap.isOpened():
    ret, frame = cap.read()

    # Transform input for midas
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    imgbatch = transform(img).to('cuda')

    # Make a prediction
    with torch.no_grad():
        prediction = midas(imgbatch)
        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size = img.shape[:2],
            mode='bicubic',
            align_corners=False
        ).squeeze()

        output = prediction.cpu().numpy()

    heatmap_img = (cm.viridis(output) * 255).astype(np.uint8)
    cv2.imshow("CV2Frame", heatmap_img)
    plt.imshow(output)
    cv2.imshow('CV2Frame', frame)
    plt.pause(0.00001)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()

plt.show()
"""

import cv2
import torch
import torchvision.transforms as transforms
from matplotlib import cm
import numpy as np

# Download the MiDaS
midas = torch.hub.load('intel-isl/MiDaS', 'MiDaS_small')
midas.to('cuda')  # Move the model to GPU
midas.eval()

# Input transformation pipeline
transforms = torch.hub.load('intel-isl/MiDaS', 'transforms')
transform = transforms.small_transform

videoPath = "/home/rajoayalew/Clones/model/testsamples/ccb_hallways.mp4"

# Hook into OpenCV
cap = cv2.VideoCapture(videoPath)

# Define the output video settings
output_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
output_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = 60
output_filename = 'output_video.mp4'
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # or use 'MJPG' for MJPEG codec

# Create VideoWriter object
video_writer = cv2.VideoWriter(output_filename, fourcc, fps, (output_width, output_height))

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        break

    # Transform input for MiDaS
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    imgbatch = transform(img).to('cuda')

    # Make a prediction
    with torch.no_grad():
        prediction = midas(imgbatch)
        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=img.shape[:2],
            mode='bicubic',
            align_corners=False
        ).squeeze()

        output = prediction.cpu().numpy()

    # Normalize the values to [0, 255] range
    normalized_output = (output - output.min()) / (output.max() - output.min()) * 255
    heatmap_img = normalized_output.astype(np.uint8)

    # Apply colormap
    heatmap_colored = cv2.applyColorMap(heatmap_img, cv2.COLORMAP_VIRIDIS)

    # Save the heatmap image as JPG (optional)
    cv2.imwrite('heatmap.jpg', heatmap_colored)

    # Write the frame to the output video
    video_writer.write(heatmap_colored)

    cv2.imshow('Heatmap', heatmap_colored)
    cv2.imshow('CV2Frame', frame)
    cv2.waitKey(1)  # Adjust the wait key delay as needed

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
video_writer.release()
cv2.destroyAllWindows()
