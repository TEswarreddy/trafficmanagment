from ultralytics import YOLO
import os

def train_quick():
    """Quick training with minimal epochs for testing"""
    # Create a simple dataset structure first
    # You need to run prepare_yolo_data.py first
    
    model = YOLO('yolov8n.pt')
    
    results = model.train(
        data='datasets/traffic_gestures/data.yaml',
        epochs=50,
        imgsz=416,
        batch=8,
        device='cpu',
        project='quick_traffic_gesture',
        name='quick_train',
        patience=5,
        save=True
    )
    
    print("Quick training completed!")

if __name__ == "__main__":
    train_quick()