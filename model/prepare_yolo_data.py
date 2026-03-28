import os
import shutil
import random
from PIL import Image

class YOLODataPreparer:
    def __init__(self, dataset_path, output_path):
        self.dataset_path = dataset_path
        self.output_path = output_path
        
        # Map the actual directory names to our class names
        self.directory_mapping = {
            'stop signal': 'stop_signal',
            'move straight': 'move_straight', 
            'left': 'left',
            'right': 'right',
            'left turn 1': 'left_turn',  # Note the actual folder name
            'left turn': 'left_turn',    # Test folder name
            'right turn': 'right_turn',
            'lane left': 'lane_left',
            'lane right': 'lane_right',
            'left over': 'left_over',
            'right over': 'right_over'
        }
        
        self.gesture_classes = list(set(self.directory_mapping.values()))
        
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
    
    def create_directory_structure(self):
        """Create YOLO dataset directory structure"""
        dirs = [
            'images/train',
            'images/val',
            'labels/train', 
            'labels/val'
        ]
        
        for dir_path in dirs:
            full_path = os.path.join(self.output_path, dir_path)
            os.makedirs(full_path, exist_ok=True)
            print(f"Created directory: {full_path}")
    
    def scan_dataset_structure(self):
        """Scan and print the actual dataset structure"""
        print("Scanning dataset structure...")
        
        if not os.path.exists(self.dataset_path):
            print(f"Dataset path does not exist: {self.dataset_path}")
            return False
            
        items = os.listdir(self.dataset_path)
        print(f"Items in dataset path: {items}")
        
        for item in items:
            item_path = os.path.join(self.dataset_path, item)
            if os.path.isdir(item_path):
                image_count = len([f for f in os.listdir(item_path) 
                                 if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
                print(f"Directory: {item} - {image_count} images")
        
        return True
    
    def convert_dataset_to_yolo(self, train_split=0.8):
        """Convert the traffic gesture dataset to YOLO format"""
        print("Converting dataset to YOLO format...")
        
        all_images = []
        image_class_map = {}
        
        # First, let's find all valid directories
        valid_dirs = []
        for actual_dir, mapped_class in self.directory_mapping.items():
            dir_path = os.path.join(self.dataset_path, actual_dir)
            if os.path.exists(dir_path):
                valid_dirs.append((actual_dir, mapped_class, dir_path))
                print(f"Found directory: {actual_dir} -> {mapped_class}")
            else:
                print(f"Directory not found: {actual_dir}")
        
        if not valid_dirs:
            print("No valid directories found!")
            return [], []
        
        # Process each directory
        for actual_dir, mapped_class, dir_path in valid_dirs:
            print(f"Processing {actual_dir} as {mapped_class}...")
            
            image_files = [f for f in os.listdir(dir_path) 
                          if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            
            for img_file in image_files:
                img_path = os.path.join(dir_path, img_file)
                
                # Create YOLO format annotation
                success = self.create_yolo_annotation(img_path, mapped_class)
                if success:
                    all_images.append(img_path)
                    image_class_map[img_path] = mapped_class
        
        print(f"Successfully processed {len(all_images)} images")
        
        # Split into train and validation sets
        random.shuffle(all_images)
        split_idx = int(len(all_images) * train_split)
        train_images = all_images[:split_idx]
        val_images = all_images[split_idx:]
        
        print(f"Train images: {len(train_images)}, Val images: {len(val_images)}")
        
        # Move images to appropriate directories
        self.organize_images(train_images, val_images, image_class_map)
        
        return train_images, val_images
    
    def create_yolo_annotation(self, img_path, class_name):
        """Create YOLO format annotation file"""
        try:
            # Get image dimensions
            with Image.open(img_path) as img:
                width, height = img.size
            
            # Create bounding box (assuming the hand covers most of the image)
            # In production, you'd want proper bounding box annotations
            x_center = 0.5
            y_center = 0.5
            bbox_width = 0.8  # Hand covers 80% of image width
            bbox_height = 0.8 # Hand covers 80% of image height
            
            # Get class index
            class_idx = self.gesture_classes.index(class_name)
            
            # Create annotation content
            annotation_content = f"{class_idx} {x_center} {y_center} {bbox_width} {bbox_height}"
            
            # Write annotation file
            base_name = os.path.splitext(os.path.basename(img_path))[0]
            annotation_path = os.path.join(
                self.output_path, 'labels', 'train', base_name + '.txt'
            )
            
            with open(annotation_path, 'w') as f:
                f.write(annotation_content)
            
            return True
            
        except Exception as e:
            print(f"Error processing {img_path}: {e}")
            return False
    
    def organize_images(self, train_images, val_images, image_class_map):
        """Organize images into train and val directories"""
        print("Organizing images into train/val directories...")
        
        # Copy training images
        for img_path in train_images:
            try:
                dest_path = os.path.join(self.output_path, 'images', 'train', os.path.basename(img_path))
                shutil.copy2(img_path, dest_path)
            except Exception as e:
                print(f"Error copying training image {img_path}: {e}")
        
        # Copy validation images and create their annotations
        for img_path in val_images:
            try:
                # Copy image
                dest_path = os.path.join(self.output_path, 'images', 'val', os.path.basename(img_path))
                shutil.copy2(img_path, dest_path)
                
                # Create validation annotation
                class_name = image_class_map[img_path]
                with Image.open(img_path) as img:
                    width, height = img.size
                
                class_idx = self.gesture_classes.index(class_name)
                annotation_content = f"{class_idx} 0.5 0.5 0.8 0.8"
                
                base_name = os.path.splitext(os.path.basename(img_path))[0]
                annotation_path = os.path.join(
                    self.output_path, 'labels', 'val', base_name + '.txt'
                )
                
                with open(annotation_path, 'w') as f:
                    f.write(annotation_content)
                    
            except Exception as e:
                print(f"Error processing validation image {img_path}: {e}")
    
    def create_data_yaml(self):
        """Create data.yaml file for YOLO training"""
        data = {
            'path': os.path.abspath(self.output_path),
            'train': 'images/train',
            'val': 'images/val',
            'nc': len(self.gesture_classes),
            'names': self.gesture_classes
        }
        
        yaml_content = f"""# Traffic Gesture Dataset
path: {data['path']}
train: {data['train']}
val: {data['val']}
nc: {data['nc']}

names:
"""
        for idx, name in enumerate(data['names']):
            yaml_content += f"  {idx}: {name}\n"
        
        yaml_path = os.path.join(self.output_path, 'data.yaml')
        with open(yaml_path, 'w') as f:
            f.write(yaml_content)
        
        print(f"Created data.yaml file at: {yaml_path}")
        print(f"Dataset contains {data['nc']} classes: {data['names']}")

def main():
    # Update these paths according to your actual dataset location
    # Based on your directory structure, try these paths:
    possible_paths = [
        "Traffic police gesture/Train",
        "Traffic Police Gesture dataset/Train", 
        "Train",
        "../Train",
        "../../Train"
    ]
    
    dataset_path = None
    for path in possible_paths:
        if os.path.exists(path):
            dataset_path = path
            break
    
    if dataset_path is None:
        print("Could not find dataset directory. Please update the path manually.")
        print("Current working directory:", os.getcwd())
        print("Available directories:")
        for item in os.listdir('.'):
            print(f"  {item}")
        return
    
    output_path = "datasets/traffic_gestures"
    
    print(f"Using dataset path: {dataset_path}")
    print(f"Output path: {output_path}")
    
    preparer = YOLODataPreparer(dataset_path, output_path)
    
    # First, scan the dataset structure
    if not preparer.scan_dataset_structure():
        return
    
    # Create directory structure
    preparer.create_directory_structure()
    
    # Convert dataset
    train_imgs, val_imgs = preparer.convert_dataset_to_yolo()
    
    if not train_imgs:
        print("No images were processed. Please check the dataset path.")
        return
    
    # Create data.yaml
    preparer.create_data_yaml()
    
    print("YOLO dataset preparation completed!")
    print(f"Total images processed: {len(train_imgs) + len(val_imgs)}")
    print(f"Training images: {len(train_imgs)}")
    print(f"Validation images: {len(val_imgs)}")

if __name__ == "__main__":
    main()