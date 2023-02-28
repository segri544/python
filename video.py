import cv2
import os

# Open the video file
video_file = "vid.mp4"
cap = cv2.VideoCapture(video_file)

# Set the time interval for capturing images (in seconds)
interval = 10

# Create the folder to save the images
folder_name = "images"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# Initialize variables
frame_count = 0
img_count=1
time_elapsed = 0

# Define the region of interest (ROI)
x = 0  # x coordinate of the top-left corner of the ROI
y = 350  # y coordinate of the top-left corner of the ROI       # bu değere matlab dan ulas
# width = 1280  # width of the ROI
# height = 720  # height of the ROI



# Loop through the video frames
while cap.isOpened():
    # Read the next frame
    ret, frame = cap.read()

    # Check if the frame was successfully read
    if not ret:
        break
    height, width, channels = frame.shape
    # Get the frame rate of the video
    fps = cap.get(cv2.CAP_PROP_FPS)
    # Calculate the time elapsed
    time_elapsed = frame_count / fps
    # Check if it is time to capture a sample image
    if time_elapsed >= interval:

        # Save the sample image
        image_file = os.path.join(folder_name, f"sample_image_{img_count}.jpg")
        # Crop the image
        frame = frame[y:y+height, x:x+width]

        cv2.imwrite(image_file, frame)
        print(f"Sample image saved: {img_count}")
        # Reset the time elapsed
        time_elapsed = 0
        img_count+=1
        frame_count=0

    # Increase the frame count
    frame_count += 1

# Release the video capture object
cap.release()