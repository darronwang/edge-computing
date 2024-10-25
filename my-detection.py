import jetson.inference
import jetson.utils
import cv2
import time
import os

print('check')
image_path = "/home/nvidia/jetson-inference/data/images/cat_1.jpg"
if not os.path.isfile(image_path):
    print("Error: Image file does not exist.")
    exit()

net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.5)
camera = jetson.utils.videoSource(image_path)
display = jetson.utils.videoOutput("display://0")

print('start')
img = camera.Capture()
if img is None:
    print("Failed to capture image")
    exit()

detections = net.Detect(img)


img_cv = jetson.utils.cudaToNumpy(img)

for detection in detections:
    class_id = detection.ClassID
    confidence = detection.Confidence
    left = int(detection.Left)
    top = int(detection.Top)
    right = int(detection.Right)
    bottom = int(detection.Bottom)
    label = net.GetClassDesc(class_id)


    cv2.rectangle(img_cv, (left, top), (right, bottom), (0, 255, 0), 2)
    cv2.putText(img_cv, "{} {:.2f}".format(label, confidence), (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


    print("Detected {:s}".format(label))
    print("Confidence: {:.2f}%".format(confidence * 100))
    print("Bounding Box: (x1={:d}, y1={:d}, x2={:d}, y2={:d})".format(left, top, right, bottom))

display.Render(img)

display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))


time.sleep(5)


display.SetStatus("")
display.Close()
camera.Close()


save_path = "/home/nvidia/detected_image.jpg"
cv2.imwrite(save_path, img_cv)
print("Detected image saved to {}".format(save_path))