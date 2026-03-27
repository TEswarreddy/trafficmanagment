from ultralytics import YOLO
import os
import shutil

def check_dataset():
    """Check if dataset is properly prepared"""
    dataset_path = "datasets/traffic_gestures"
    
    if not os.path.exists(dataset_path):
        print(f"Dataset path {dataset_path} does not exist!")
        return False
    
    # Check required files
    required_dirs = [
        'images/train',
        'images/val', 
        'labels/train',
        'labels/val'
    ]
    
    for dir_path in required_dirs:
        full_path = os.path.join(dataset_path, dir_path)
        if not os.path.exists(full_path):
            print(f"Missing directory: {full_path}")
            return False
    
    # Check if there are images
    train_images = [f for f in os.listdir(os.path.join(dataset_path, 'images/train')) 
                   if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    val_images = [f for f in os.listdir(os.path.join(dataset_path, 'images/val')) 
                 if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    print(f"Training images: {len(train_images)}")
    print(f"Validation images: {len(val_images)}")
    
    if len(train_images) == 0:
        print("No training images found!")
        return False
        
    if len(val_images) == 0:
        print("Warning: No validation images found!")
        # Create a minimal validation set from training if needed
        if len(train_images) > 10:
            print("Creating validation set from training images...")
            val_dir = os.path.join(dataset_path, 'images/val')
            for img_file in train_images[:5]:  # Move 5 images to validation
                src = os.path.join(dataset_path, 'images/train', img_file)
                dst = os.path.join(val_dir, img_file)
                shutil.copy2(src, dst)
                
                # Also copy corresponding label
                label_name = os.path.splitext(img_file)[0] + '.txt'
                src_label = os.path.join(dataset_path, 'labels/train', label_name)
                dst_label = os.path.join(dataset_path, 'labels/val', label_name)
                if os.path.exists(src_label):
                    shutil.copy2(src_label, dst_label)
    
    return True

def train_yolo_model():
    """Train YOLOv8 model on traffic gesture dataset"""
    
    print("Checking dataset...")
    if not check_dataset():
        print("Dataset preparation failed. Please run prepare_yolo_data.py first.")
        return
    
    # Load YOLOv8 model
    print("Loading YOLOv8 model...")
    model = YOLO('yolov8n.pt')  # Using nano version for faster training
    
    # Train the model with adjusted parameters
    print("Starting training...")
    
    try:
        results = model.train(
            data='datasets/traffic_gestures/data.yaml',
            epochs=50,  # Reduced for testing
            imgsz=320,  # Smaller for faster training
            batch=8,    # Smaller batch for CPU
            patience=10,
            save=True,
            device='cpu',  # Use 'cuda' if you have GPU
            project='traffic_gesture_model',
            name='yolov8_traffic_gesture',
            optimizer='Adam',
            lr0=0.001,
            augment=True,
            degrees=10,
            translate=0.1,
            scale=0.5,
            fliplr=0.5,
            mosaic=1.0,
            mixup=0.0,
            verbose=True
        )
        
        print("Training completed!")
        
        # Validate the model
        print("Validating model...")
        metrics = model.val()
        print(f"mAP50: {metrics.box.map50:.4f}")
        print(f"mAP50-95: {metrics.box.map:.4f}")
        
        # Save the best model
        best_model_path = 'best_traffic_gesture.pt'
        model.export(format='pt')  # Save as PyTorch model
        print(f"Best model saved as: {best_model_path}")
        
        return model
        
    except Exception as e:
        print(f"Training error: {e}")
        print("Trying with simpler configuration...")
        
        # Fallback training with minimal parameters
        results = model.train(
            data='datasets/traffic_gestures/data.yaml',
            epochs=30,
            imgsz=320,
            batch=4,
            device='cpu',
            project='traffic_gesture_model',
            name='simple_train'
        )
        
        return model

if __name__ == "__main__":
    train_yolo_model()