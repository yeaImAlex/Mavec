import cv2
import numpy as np

def detect_red_gate(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 120, 70])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 120, 70])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = mask1 | mask2

    height, width, _ = frame.shape
    roi = mask[height // 3: height, width // 3: 2 * width // 3]

    contours, _ = cv2.findContours(roi, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        area = cv2.contourArea(contour)
        
        if area > 200:  

            epsilon = 0.05 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            if len(approx) >= 4: 
                x, y, w, h = cv2.boundingRect(contour)
                aspect_ratio = w / float(h)
                

                if aspect_ratio > 3:  
                    cv2.rectangle(frame, (x + width // 3, y + height // 3), 
                                  (x + width // 3 + w, y + height // 3 + h), (0, 255, 0), 2)
                    cv2.putText(frame, "Boom Gate Detected", (x + width // 3, y + height // 3 - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    cv2.imshow('mask', roi)
    return frame, len(contours) > 0 


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        processed_frame, red_detected = detect_red_gate(frame)


        cv2.imshow('Boom Gate Detection', processed_frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
