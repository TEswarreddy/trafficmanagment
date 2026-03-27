import cv2
import numpy as np
from ultralytics import YOLO
import time

class GestureDetectorDebug:
    def __init__(self, model_path):
        self.model = YOLO(model_path)
        self.cap = cv2.VideoCapture(0)
        self.confidence_threshold = 0.3  # Lower threshold for better detection
        
    def test_detection(self):
        print("Starting gesture detection debug...")
        print(f"Model classes: {self.model.names}")
        print(f"Confidence threshold: {self.confidence_threshold}")
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
                
            # Flip frame for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Create a copy for drawing
            debug_frame = frame.copy()
            
            # Run inference
            start_time = time.time()
            results = self.model(frame, verbose=False, conf=self.confidence_threshold)
            inference_time = time.time() - start_time
            
            detections = []
            
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        confidence = box.conf.item()
                        class_id = int(box.cls.item())
                        class_name = self.model.names[class_id]
                        bbox = box.xyxy[0].cpu().numpy()
                        
                        detections.append({
                            'class_name': class_name,
                            'confidence': confidence,
                            'bbox': bbox
                        })
            
            # Draw hand region of interest
            h, w = frame.shape[:2]
            roi_size = 300
            x1 = max(0, (w - roi_size) // 2)
            y1 = max(0, (h - roi_size) // 2)
            x2 = min(w, x1 + roi_size)
            y2 = min(h, y1 + roi_size)
            
            cv2.rectangle(debug_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(debug_frame, "Hand ROI", (x1, y1-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
            
            # Display detections
            if detections:
                for det in detections:
                    x1, y1, x2, y2 = det['bbox'].astype(int)
                    cv2.rectangle(debug_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    label = f"{det['class_name']} {det['confidence']:.2f}"
                    cv2.putText(debug_frame, label, (x1, y1-10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)
                
                best_det = max(detections, key=lambda x: x['confidence'])
                status = f"Detected: {best_det['class_name']} ({best_det['confidence']:.2f})"
                color = (0, 255, 0)
            else:
                status = "No gesture detected"
                color = (0, 0, 255)
            
            # Display information
            cv2.putText(debug_frame, status, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            cv2.putText(debug_frame, f"Inference: {inference_time*1000:.1f}ms", (10, 70), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.putText(debug_frame, "Press 'q' to quit, 'c' to change threshold", (10, h-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            cv2.imshow('Gesture Detection Debug', debug_frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('c'):
                # Change confidence threshold
                new_thresh = input(f"Enter new confidence threshold (current: {self.confidence_threshold}): ")
                try:
                    self.confidence_threshold = float(new_thresh)
                    print(f"Confidence threshold changed to: {self.confidence_threshold}")
                except:
                    print("Invalid threshold")
        
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Try different model paths
    model_paths = [
        'traffic_gesture_model/yolov8_traffic_gesture2/weights/best.pt',
        'traffic_gesture_model/yolov8_traffic_gesture/weights/best.pt',
        'best_traffic_gesture.pt'
    ]
    
    model_path = None
    for path in model_paths:
        try:
            detector = GestureDetectorDebug(path)
            print(f"Successfully loaded model: {path}")
            model_path = path
            break
        except:
            print(f"Failed to load model: {path}")
            continue
    
    if model_path:
        detector.test_detection()
    else:
        print("No valid model found!")