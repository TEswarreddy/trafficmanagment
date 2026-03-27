import os
import shutil
from ultralytics import YOLO

def fix_model_issues():
    """Fix common model detection issues"""
    
    print("🔧 Fixing model detection issues...")
    
    # Check if model exists
    model_path = 'traffic_gesture_model/yolov8_traffic_gesture2/weights/best.pt'
    
    if not os.path.exists(model_path):
        print("❌ Model file not found!")
        return False
    
    # Test model loading
    try:
        model = YOLO(model_path)
        print("✅ Model loaded successfully")
        print(f"📊 Model classes: {model.names}")
        
        # Test with a simple inference
        import numpy as np
        test_image = np.random.randint(0, 255, (640, 480, 3), dtype=np.uint8)
        results = model(test_image, verbose=False, conf=0.3)
        print("✅ Model inference test passed")
        
        return True
        
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return False

def create_backup_model():
    """Create a backup of the working model"""
    source = 'traffic_gesture_model/yolov8_traffic_gesture2/weights/best.pt'
    backup = 'backup_best_model.pt'
    
    if os.path.exists(source):
        shutil.copy2(source, backup)
        print(f"✅ Backup created: {backup}")
        return True
    return False

if __name__ == "__main__":
    print("🛠️  Running model diagnostics...")
    
    if fix_model_issues():
        print("🎉 Model issues fixed!")
        create_backup_model()
    else:
        print("❌ Could not fix model issues")
        print("\n💡 TROUBLESHOOTING TIPS:")
        print("1. Make sure your hand is clearly visible in the camera")
        print("2. Try different lighting conditions")
        print("3. Ensure your hand is within the green ROI box")
        print("4. Try holding gestures for 2-3 seconds")
        print("5. Check if camera is working with other applications")