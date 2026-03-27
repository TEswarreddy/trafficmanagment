import cv2
import numpy as np
from ultralytics import YOLO
import pygame
import os
import time

class YOLOGestureController:
    def __init__(self, model_path=None):
        self.model = None
        self.cap = None
        self.confidence_threshold = 0.3  # Lower threshold
        self.last_detection_time = 0
        self.current_signal = "GREEN"
        self.signal_timeout = 2.0  # Keep signal for 2 seconds after last detection
        
        # Gesture to traffic signal mapping
        self.gesture_mapping = {
            'stop_signal': 'RED',
            'move_straight': 'GREEN',
            'left': 'LEFT_GREEN',
            'right': 'RIGHT_GREEN',
            'left_turn': 'LEFT_GREEN',
            'right_turn': 'RIGHT_GREEN',
            'lane_left': 'LEFT_GREEN',
            'lane_right': 'RIGHT_GREEN',
            'left_over': 'YELLOW',
            'right_over': 'YELLOW'
        }
        
        # Try to find the trained model automatically
        if model_path is None:
            model_path = self.find_trained_model()
        
        self.load_model(model_path)
    
    def find_trained_model(self):
        """Automatically find the trained model"""
        possible_paths = [
            'traffic_gesture_model/yolov8_traffic_gesture2/weights/best.pt',
            'traffic_gesture_model/yolov8_traffic_gesture/weights/best.pt',
            'best_traffic_gesture.pt'
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                print(f"Found model at: {path}")
                return path
        
        print("No trained model found. Using simulated controller.")
        return None
    
    def load_model(self, model_path):
        """Load the trained YOLO model"""
        try:
            if model_path and os.path.exists(model_path):
                self.model = YOLO(model_path)
                print("✅ YOLO gesture model loaded successfully!")
                print(f"📊 Model classes: {self.model.names}")
                print(f"🎯 Confidence threshold: {self.confidence_threshold}")
            else:
                print("❌ No model file found. Using simulated gestures.")
                self.model = None
        except Exception as e:
            print(f"❌ Error loading YOLO model: {e}")
            print("🔄 Using simulated gesture controller...")
            self.model = None
    
    def start_camera(self, camera_id=0):
        """Start camera capture"""
        self.cap = cv2.VideoCapture(camera_id)
        if not self.cap.isOpened():
            print("❌ Error: Could not open camera")
            # Try different camera indices
            for i in range(1, 3):
                self.cap = cv2.VideoCapture(i)
                if self.cap.isOpened():
                    print(f"✅ Camera found at index {i}")
                    break
            
            if not self.cap.isOpened():
                return False
        
        # Set camera properties
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        return True
    
    def preprocess_frame(self, frame):
        """Preprocess frame for better detection"""
        # Flip frame for mirror effect
        frame = cv2.flip(frame, 1)
        
        # Enhance contrast
        frame = cv2.convertScaleAbs(frame, alpha=1.2, beta=10)
        
        return frame
    
    def detect_gestures(self, frame):
        """Detect gestures in frame using YOLO"""
        if self.model is None:
            return [], frame
        
        try:
            # Run YOLO inference with lower confidence threshold
            results = self.model(frame, verbose=False, conf=self.confidence_threshold)
            
            detections = []
            annotated_frame = results[0].plot()  # Get annotated frame
            
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
            
            return detections, annotated_frame
            
        except Exception as e:
            print(f"❌ Detection error: {e}")
            return [], frame
    
    def get_gesture_signal(self, detections):
        """Convert detected gestures to traffic signals"""
        if not detections:
            # If no recent detections, return to default after timeout
            if time.time() - self.last_detection_time > self.signal_timeout:
                return "GREEN"
            else:
                return self.current_signal
        
        # Get the detection with highest confidence
        best_detection = max(detections, key=lambda x: x['confidence'])
        gesture_name = best_detection['class_name']
        
        signal = self.gesture_mapping.get(gesture_name, "UNKNOWN")
        
        if signal != "UNKNOWN":
            self.current_signal = signal
            self.last_detection_time = time.time()
            print(f"🎯 Detected: {gesture_name} -> {signal} (confidence: {best_detection['confidence']:.2f})")
        
        return signal
    
    def get_gesture_from_camera(self):
        """Get gesture signal from camera feed"""
        if self.cap is None:
            if not self.start_camera():
                return "GREEN"  # Default signal
        
        ret, frame = self.cap.read()
        if not ret:
            return "GREEN"
        
        # Preprocess frame
        frame = self.preprocess_frame(frame)
        
        # Detect gestures
        detections, annotated_frame = self.detect_gestures(frame)
        
        # Get traffic signal from gesture
        gesture_signal = self.get_gesture_signal(detections)
        
        # Display information on frame
        cv2.putText(annotated_frame, f"Signal: {gesture_signal}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        if detections:
            best_detection = max(detections, key=lambda x: x['confidence'])
            cv2.putText(annotated_frame, 
                       f"Gesture: {best_detection['class_name']} ({best_detection['confidence']:.2f})", 
                       (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            # Draw hand ROI guidance
            h, w = frame.shape[:2]
            roi_size = 300
            x1 = max(0, (w - roi_size) // 2)
            y1 = max(0, (h - roi_size) // 2)
            cv2.rectangle(annotated_frame, (x1, y1), (x1 + roi_size, y1 + roi_size), (0, 255, 0), 2)
        else:
            cv2.putText(annotated_frame, "No gesture detected - Show hand in green box", (10, 70),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            # Draw hand ROI guidance
            h, w = frame.shape[:2]
            roi_size = 300
            x1 = max(0, (w - roi_size) // 2)
            y1 = max(0, (h - roi_size) // 2)
            cv2.rectangle(annotated_frame, (x1, y1), (x1 + roi_size, y1 + roi_size), (0, 0, 255), 2)
        
        cv2.putText(annotated_frame, "Press 'Q' to quit camera", (10, 110),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        
        # Show frame
        cv2.imshow('YOLO Hand Gesture Recognition', annotated_frame)
        
        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return "QUIT"
        
        return gesture_signal
    
    def set_confidence_threshold(self, threshold):
        """Set confidence threshold for detection"""
        self.confidence_threshold = max(0.1, min(0.9, threshold))
        print(f"Confidence threshold set to: {self.confidence_threshold}")
    
    def release_camera(self):
        """Release camera resources"""
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()

# Simulated controller for testing without camera
class SimpleYOLOGestureController:
    def __init__(self):
        self.current_signal = "GREEN"
        self.gesture_sequence = ["GREEN", "RED", "YELLOW", "LEFT_GREEN", "RIGHT_GREEN"]
        self.current_index = 0
        self.last_change_time = time.time()
        self.change_interval = 3.0  # Change every 3 seconds
    
    def get_gesture_from_camera(self):
        """Simulate gesture detection for testing"""
        # Auto-cycle through signals for demo
        current_time = time.time()
        if current_time - self.last_change_time > self.change_interval:
            self.current_index = (self.current_index + 1) % len(self.gesture_sequence)
            self.current_signal = self.gesture_sequence[self.current_index]
            self.last_change_time = current_time
            print(f"🔄 Auto-changing signal to: {self.current_signal}")
        
        # Manual override with spacebar
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.current_index = (self.current_index + 1) % len(self.gesture_sequence)
            self.current_signal = self.gesture_sequence[self.current_index]
            print(f"🎮 Manual signal change: {self.current_signal}")
            # Small delay to prevent rapid toggling
            pygame.time.delay(500)
        
        return self.current_signal
    
    def set_signal(self, signal):
        """Manually set signal for testing"""
        self.current_signal = signal
    
    def release_camera(self):
        """Dummy method for compatibility"""
        pass