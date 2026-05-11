import cv2
import pandas as pd
from ultralytics import YOLO
import matplotlib.pyplot as plt
import random

model = YOLO("yolov8n.pt")

cap = cv2.VideoCapture(0)

male = 0
female = 0
children = 0

brands = {
    "Nike": 0,
    "Puma": 0,
    "Adidas": 0
}

while True:

    ret, frame = cap.read()

    results = model(frame)

    for r in results:

        boxes = r.boxes

        for box in boxes:

            cls = int(box.cls[0])

            if cls == 0:

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                cv2.rectangle(frame,
                              (x1,y1),
                              (x2,y2),
                              (0,255,0),
                              2)

                h = y2 - y1

                if h > 300:
                    male += 1
                elif h > 200:
                    female += 1
                else:
                    children += 1

                brand = random.choice([
                    "Nike",
                    "Puma",
                    "Adidas"
                ])

                brands[brand] += 1

                cv2.putText(frame,
                            brand,
                            (x1,y1-10),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7,
                            (255,0,0),
                            2)

    cv2.imshow("Mall Analytics", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

data = {
    "Male":[male],
    "Female":[female],
    "Children":[children]
}

df = pd.DataFrame(data)

df.to_csv("data.csv", index=False)

plt.figure(figsize=(6,6))

plt.pie(brands.values(),
        labels=brands.keys(),
        autopct='%1.1f%%')

plt.title("Brand Interest Analysis")

plt.savefig("static/chart.png")
