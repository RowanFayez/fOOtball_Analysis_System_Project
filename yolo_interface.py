from ultralytics import YOLO
import torch


model = YOLO("weights/best.pt")


result = model.predict(
    'input_videos/08fd33_4.mp4',
    save=True,
    project="output",   
    name="results"      
)

print(result[0])
for box in result[0].boxes:
    print(box)
