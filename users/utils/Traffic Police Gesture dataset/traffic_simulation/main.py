import pygame
import sys
import cv2
from traffic_simulation import TrafficSimulation
from yolo_gesture_controller import YOLOGestureController, SimpleYOLOGestureController

def main():
    print("=" * 60)
    print("Traffic Simulation with YOLO Hand Gesture Control")
    print("=" * 60)
    
    # Initialize gesture controller
    try:
        gesture_controller = YOLOGestureController()
        
        # Start camera
        if gesture_controller.model is None:
            print("Using simulated gesture controller (no model found)")
            gesture_controller = SimpleYOLOGestureController()
            gesture_callback = gesture_controller.get_gesture_from_camera
        else:
            if not gesture_controller.start_camera():
                print("Camera not available. Using simulated gesture controller.")
                gesture_controller = SimpleYOLOGestureController()
                gesture_callback = gesture_controller.get_gesture_from_camera
            else:
                print("YOLO gesture controller initialized successfully!")
                gesture_callback = gesture_controller.get_gesture_from_camera
                
    except Exception as e:
        print(f"Error initializing YOLO controller: {e}")
        print("Falling back to simulated gesture controller...")
        gesture_controller = SimpleYOLOGestureController()
        gesture_callback = gesture_controller.get_gesture_from_camera
    
    # Initialize traffic simulation
    simulation = TrafficSimulation()
    
    def combined_gesture_callback():
        """Combine gesture detection with manual keyboard overrides"""
        # Get gesture from camera
        gesture_signal = gesture_callback()
        
        if gesture_signal == "QUIT":
            return "QUIT"
        
        # Check for manual keyboard overrides
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            gesture_controller.set_signal('RED') if hasattr(gesture_controller, 'set_signal') else None
            return 'RED'
        elif keys[pygame.K_g]:
            gesture_controller.set_signal('GREEN') if hasattr(gesture_controller, 'set_signal') else None
            return 'GREEN'
        elif keys[pygame.K_y]:
            gesture_controller.set_signal('YELLOW') if hasattr(gesture_controller, 'set_signal') else None
            return 'YELLOW'
        elif keys[pygame.K_l]:
            gesture_controller.set_signal('LEFT_GREEN') if hasattr(gesture_controller, 'set_signal') else None
            return 'LEFT_GREEN'
        elif keys[pygame.K_t]:
            gesture_controller.set_signal('RIGHT_GREEN') if hasattr(gesture_controller, 'set_signal') else None
            return 'RIGHT_GREEN'
        
        return gesture_signal
    
    try:
        print("\n🎮 CONTROLS:")
        print("🖐️  Show hand gestures to camera for automatic control")
        print("R - Force RED signal")
        print("G - Force GREEN signal") 
        print("Y - Force YELLOW signal")
        print("L - Force LEFT turn signal")
        print("T - Force RIGHT turn signal")
        print("SPACE - Cycle signals (simulated mode)")
        print("ESC - Exit simulation")
        print("Q - Quit camera window")
        print("\n🚦 GESTURE MAPPING:")
        print("✋ Stop signal -> RED")
        print("👆 Move straight -> GREEN") 
        print("👈 Left gestures -> LEFT_GREEN")
        print("👉 Right gestures -> RIGHT_GREEN")
        print("🔄 Left/Right over -> YELLOW")
        print("\nStarting simulation...")
        
        # Run simulation
        simulation.run(combined_gesture_callback)
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down...")
    except Exception as e:
        print(f"❌ Error during simulation: {e}")
        import traceback
        traceback.print_exc()
    finally:
        gesture_controller.release_camera()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    main()