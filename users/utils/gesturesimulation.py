# LAG
# NO. OF VEHICLES IN SIGNAL CLASS
# stops not used
# DISTRIBUTION
# BUS TOUCHING ON TURNS
# Distribution using python class

# *** IMAGE XY COOD IS TOP LEFT
import random
import math
import time
import threading
import pygame
import sys
import os
import cv2
import mediapipe as mp
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Default values of signal times
defaultRed = 150
defaultYellow = 5
defaultGreen = 20
defaultMinimum = 10
defaultMaximum = 60

signals = []
noOfSignals = 4
simTime = 300       # change this to change time of simulation
timeElapsed = 0

currentGreen = -1   # Start with no green signal
currentYellow = 0   # Indicates whether yellow signal is on or off 
signalControlMode = False  # Whether gesture control is active
controlledSignal = 0  # Which signal is currently being controlled

# Average times for vehicles to pass the intersection
carTime = 2
bikeTime = 1
rickshawTime = 2.25 
busTime = 2.5
truckTime = 2.5

# Count of cars at a traffic signal
noOfCars = 0
noOfBikes = 0
noOfBuses =0
noOfTrucks = 0
noOfRickshaws = 0
noOfLanes = 2

speeds = {'car':2.25, 'bus':1.8, 'truck':1.8, 'rickshaw':2, 'bike':2.5}  # average speeds of vehicles

# Coordinates of start
x = {'right':[0,0,0], 'down':[755,727,697], 'left':[1400,1400,1400], 'up':[602,627,657]}    
y = {'right':[348,370,398], 'down':[0,0,0], 'left':[498,466,436], 'up':[800,800,800]}

vehicles = {'right': {0:[], 1:[], 2:[], 'crossed':0}, 'down': {0:[], 1:[], 2:[], 'crossed':0}, 'left': {0:[], 1:[], 2:[], 'crossed':0}, 'up': {0:[], 1:[], 2:[], 'crossed':0}}
vehicleTypes = {0:'car', 1:'bus', 2:'truck', 3:'rickshaw', 4:'bike'}
directionNumbers = {0:'right', 1:'down', 2:'left', 3:'up'}

# Coordinates of signal image, timer, and vehicle count
signalCoods = [(530,230),(810,230),(810,570),(530,570)]
signalTimerCoods = [(530,210),(810,210),(810,550),(530,550)]
vehicleCountCoods = [(480,210),(880,210),(880,550),(480,550)]
vehicleCountTexts = ["0", "0", "0", "0"]

# Coordinates of stop lines
stopLines = {'right': 590, 'down': 330, 'left': 800, 'up': 535}
defaultStop = {'right': 580, 'down': 320, 'left': 810, 'up': 545}
stops = {'right': [580,580,580], 'down': [320,320,320], 'left': [810,810,810], 'up': [545,545,545]}

mid = {'right': {'x':705, 'y':445}, 'down': {'x':695, 'y':450}, 'left': {'x':695, 'y':425}, 'up': {'x':695, 'y':400}}
rotationAngle = 3

# Gap between vehicles
gap = 15    # stopping gap
gap2 = 15   # moving gap

pygame.init()
simulation = pygame.sprite.Group()

class TrafficSignal:
    def __init__(self, red, yellow, green, minimum, maximum):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.minimum = minimum
        self.maximum = maximum
        self.signalText = "STOP"
        self.totalGreenTime = 0
        self.greenTimer = 0
        
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicleClass, direction_number, direction, will_turn):
        pygame.sprite.Sprite.__init__(self)
        self.lane = lane
        self.vehicleClass = vehicleClass
        self.speed = speeds[vehicleClass]
        self.direction_number = direction_number
        self.direction = direction
        self.x = x[direction][lane]
        self.y = y[direction][lane]
        self.crossed = 0
        self.willTurn = will_turn
        self.turned = 0
        self.rotateAngle = 0
        vehicles[direction][lane].append(self)
        self.index = len(vehicles[direction][lane]) - 1
        # path = "images/" + direction + "/" + vehicleClass + ".png"
        path = os.path.join(BASE_DIR, 'images', direction, f'{vehicleClass}.png')

        self.originalImage = pygame.image.load(path)
        self.currentImage = pygame.image.load(path)

    
        if(direction=='right'):
            if(len(vehicles[direction][lane])>1 and vehicles[direction][lane][self.index-1].crossed==0):    # if more than 1 vehicle in the lane of vehicle before it has crossed stop line
                self.stop = vehicles[direction][lane][self.index-1].stop - vehicles[direction][lane][self.index-1].currentImage.get_rect().width - gap         # setting stop coordinate as: stop coordinate of next vehicle - width of next vehicle - gap
            else:
                self.stop = defaultStop[direction]
            # Set new starting and stopping coordinate
            temp = self.currentImage.get_rect().width + gap    
            x[direction][lane] -= temp
            stops[direction][lane] -= temp
        elif(direction=='left'):
            if(len(vehicles[direction][lane])>1 and vehicles[direction][lane][self.index-1].crossed==0):
                self.stop = vehicles[direction][lane][self.index-1].stop + vehicles[direction][lane][self.index-1].currentImage.get_rect().width + gap
            else:
                self.stop = defaultStop[direction]
            temp = self.currentImage.get_rect().width + gap
            x[direction][lane] += temp
            stops[direction][lane] += temp
        elif(direction=='down'):
            if(len(vehicles[direction][lane])>1 and vehicles[direction][lane][self.index-1].crossed==0):
                self.stop = vehicles[direction][lane][self.index-1].stop - vehicles[direction][lane][self.index-1].currentImage.get_rect().height - gap
            else:
                self.stop = defaultStop[direction]
            temp = self.currentImage.get_rect().height + gap
            y[direction][lane] -= temp
            stops[direction][lane] -= temp
        elif(direction=='up'):
            if(len(vehicles[direction][lane])>1 and vehicles[direction][lane][self.index-1].crossed==0):
                self.stop = vehicles[direction][lane][self.index-1].stop + vehicles[direction][lane][self.index-1].currentImage.get_rect().height + gap
            else:
                self.stop = defaultStop[direction]
            temp = self.currentImage.get_rect().height + gap
            y[direction][lane] += temp
            stops[direction][lane] += temp
        simulation.add(self)

    def render(self, screen):
        screen.blit(self.currentImage, (self.x, self.y))

    def move(self):
        if(self.direction=='right'):
            if(self.crossed==0 and self.x+self.currentImage.get_rect().width>stopLines[self.direction]):   # if the image has crossed stop line now
                self.crossed = 1
                vehicles[self.direction]['crossed'] += 1
            if(self.willTurn==1):
                if(self.crossed==0 or self.x+self.currentImage.get_rect().width<mid[self.direction]['x']):
                    if((self.x+self.currentImage.get_rect().width<=self.stop or (currentGreen==0 and currentYellow==0) or self.crossed==1) and (self.index==0 or self.x+self.currentImage.get_rect().width<(vehicles[self.direction][self.lane][self.index-1].x - gap2) or vehicles[self.direction][self.lane][self.index-1].turned==1)):                
                        self.x += self.speed
                else:   
                    if(self.turned==0):
                        self.rotateAngle += rotationAngle
                        self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
                        self.x += 2
                        self.y += 1.8
                        if(self.rotateAngle==90):
                            self.turned = 1
                    else:
                        if(self.index==0 or self.y+self.currentImage.get_rect().height<(vehicles[self.direction][self.lane][self.index-1].y - gap2) or self.x+self.currentImage.get_rect().width<(vehicles[self.direction][self.lane][self.index-1].x - gap2)):
                            self.y += self.speed
            else: 
                if((self.x+self.currentImage.get_rect().width<=self.stop or self.crossed == 1 or (currentGreen==0 and currentYellow==0)) and (self.index==0 or self.x+self.currentImage.get_rect().width<(vehicles[self.direction][self.lane][self.index-1].x - gap2) or (vehicles[self.direction][self.lane][self.index-1].turned==1))):                
                    self.x += self.speed  # move the vehicle

        elif(self.direction=='down'):
            if(self.crossed==0 and self.y+self.currentImage.get_rect().height>stopLines[self.direction]):
                self.crossed = 1
                vehicles[self.direction]['crossed'] += 1
            if(self.willTurn==1):
                if(self.crossed==0 or self.y+self.currentImage.get_rect().height<mid[self.direction]['y']):
                    if((self.y+self.currentImage.get_rect().height<=self.stop or (currentGreen==1 and currentYellow==0) or self.crossed==1) and (self.index==0 or self.y+self.currentImage.get_rect().height<(vehicles[self.direction][self.lane][self.index-1].y - gap2) or vehicles[self.direction][self.lane][self.index-1].turned==1)):                
                        self.y += self.speed
                else:   
                    if(self.turned==0):
                        self.rotateAngle += rotationAngle
                        self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
                        self.x -= 2.5
                        self.y += 2
                        if(self.rotateAngle==90):
                            self.turned = 1
                    else:
                        if(self.index==0 or self.x>(vehicles[self.direction][self.lane][self.index-1].x + vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().width + gap2) or self.y<(vehicles[self.direction][self.lane][self.index-1].y - gap2)):
                            self.x -= self.speed
            else: 
                if((self.y+self.currentImage.get_rect().height<=self.stop or self.crossed == 1 or (currentGreen==1 and currentYellow==0)) and (self.index==0 or self.y+self.currentImage.get_rect().height<(vehicles[self.direction][self.lane][self.index-1].y - gap2) or (vehicles[self.direction][self.lane][self.index-1].turned==1))):                
                    self.y += self.speed
            
        elif(self.direction=='left'):
            if(self.crossed==0 and self.x<stopLines[self.direction]):
                self.crossed = 1
                vehicles[self.direction]['crossed'] += 1
            if(self.willTurn==1):
                if(self.crossed==0 or self.x>mid[self.direction]['x']):
                    if((self.x>=self.stop or (currentGreen==2 and currentYellow==0) or self.crossed==1) and (self.index==0 or self.x>(vehicles[self.direction][self.lane][self.index-1].x + vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().width + gap2) or vehicles[self.direction][self.lane][self.index-1].turned==1)):                
                        self.x -= self.speed
                else: 
                    if(self.turned==0):
                        self.rotateAngle += rotationAngle
                        self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
                        self.x -= 1.8
                        self.y -= 2.5
                        if(self.rotateAngle==90):
                            self.turned = 1
                    else:
                        if(self.index==0 or self.y>(vehicles[self.direction][self.lane][self.index-1].y + vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().height +  gap2) or self.x>(vehicles[self.direction][self.lane][self.index-1].x + gap2)):
                            self.y -= self.speed
            else: 
                if((self.x>=self.stop or self.crossed == 1 or (currentGreen==2 and currentYellow==0)) and (self.index==0 or self.x>(vehicles[self.direction][self.lane][self.index-1].x + vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().width + gap2) or (vehicles[self.direction][self.lane][self.index-1].turned==1))):                
                    self.x -= self.speed  # move the vehicle    
        elif(self.direction=='up'):
            if(self.crossed==0 and self.y<stopLines[self.direction]):
                self.crossed = 1
                vehicles[self.direction]['crossed'] += 1
            if(self.willTurn==1):
                if(self.crossed==0 or self.y>mid[self.direction]['y']):
                    if((self.y>=self.stop or (currentGreen==3 and currentYellow==0) or self.crossed == 1) and (self.index==0 or self.y>(vehicles[self.direction][self.lane][self.index-1].y + vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().height +  gap2) or vehicles[self.direction][self.lane][self.index-1].turned==1)):
                        self.y -= self.speed
                else:   
                    if(self.turned==0):
                        self.rotateAngle += rotationAngle
                        self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
                        self.x += 1
                        self.y -= 1
                        if(self.rotateAngle==90):
                            self.turned = 1
                    else:
                        if(self.index==0 or self.x<(vehicles[self.direction][self.lane][self.index-1].x - vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().width - gap2) or self.y>(vehicles[self.direction][self.lane][self.index-1].y + gap2)):
                            self.x += self.speed
            else: 
                if((self.y>=self.stop or self.crossed == 1 or (currentGreen==3 and currentYellow==0)) and (self.index==0 or self.y>(vehicles[self.direction][self.lane][self.index-1].y + vehicles[self.direction][self.lane][self.index-1].currentImage.get_rect().height + gap2) or (vehicles[self.direction][self.lane][self.index-1].turned==1))):                
                    self.y -= self.speed

# Initialization of signals with all red
def initialize():
    # Set all signals to red with no timers
    for i in range(noOfSignals):
        ts = TrafficSignal(0, 0, 0, 0, 0)
        signals.append(ts)

# Generating vehicles in the simulation
def generateVehicles():
    while(True):
        vehicle_type = random.randint(0,4)
        if(vehicle_type==4):
            lane_number = 0
        else:
            lane_number = random.randint(0,1) + 1
        will_turn = 0
        if(lane_number==2):
            temp = random.randint(0,4)
            if(temp<=2):
                will_turn = 1
            elif(temp>2):
                will_turn = 0
        temp = random.randint(0,999)
        direction_number = 0
        a = [400,800,900,1000]
        if(temp<a[0]):
            direction_number = 0
        elif(temp<a[1]):
            direction_number = 1
        elif(temp<a[2]):
            direction_number = 2
        elif(temp<a[3]):
            direction_number = 3
        Vehicle(lane_number, vehicleTypes[vehicle_type], direction_number, directionNumbers[direction_number], will_turn)
        time.sleep(0.75)

def simulationTime():
    global timeElapsed, simTime
    while(True):
        timeElapsed += 1
        time.sleep(1)
        if(timeElapsed==simTime):
            totalVehicles = 0
            print('Lane-wise Vehicle Counts')
            for i in range(noOfSignals):
                print('Lane',i+1,':',vehicles[directionNumbers[i]]['crossed'])
                totalVehicles += vehicles[directionNumbers[i]]['crossed']
            print('Total vehicles passed: ',totalVehicles)
            print('Total time passed: ',timeElapsed)
            print('No. of vehicles passed per unit time: ',(float(totalVehicles)/float(timeElapsed)))
            os._exit(1)

# Hand gesture detection functions
def get_finger_state(hand_landmarks, finger_tip, finger_dip, finger_pip, finger_mcp, wrist):
    """Check if a finger is extended"""
    tip = hand_landmarks.landmark[finger_tip]
    dip = hand_landmarks.landmark[finger_dip]
    pip = hand_landmarks.landmark[finger_pip]
    mcp = hand_landmarks.landmark[finger_mcp]
    wrist_point = hand_landmarks.landmark[wrist]
    
    # Check if finger is extended (tip is higher than dip for vertical gestures)
    return tip.y < dip.y and tip.y < pip.y and tip.y < mcp.y

def detect_gesture(hand_landmarks):
    """Detect hand gestures based on finger positions"""
    # Check each finger
    thumb_extended = get_finger_state(hand_landmarks, 4, 3, 2, 1, 0)
    index_extended = get_finger_state(hand_landmarks, 8, 7, 6, 5, 0)
    middle_extended = get_finger_state(hand_landmarks, 12, 11, 10, 9, 0)
    ring_extended = get_finger_state(hand_landmarks, 16, 15, 14, 13, 0)
    pinky_extended = get_finger_state(hand_landmarks, 20, 19, 18, 17, 0)
    
    # Count extended fingers
    extended_fingers = [index_extended, middle_extended, ring_extended, pinky_extended]
    count = sum(extended_fingers)
    
    # Gesture 1: Open hand (all fingers extended) - Activate control mode
    if all(extended_fingers) and thumb_extended:
        return "ACTIVATE_CONTROL"
    
    # Gesture 2: Closed fist (no fingers extended) - Deactivate control mode
    elif not any(extended_fingers) and not thumb_extended:
        return "DEACTIVATE_CONTROL"
    
    # Gesture 3: Pointing (only index finger extended) - Select signal
    elif index_extended and not middle_extended and not ring_extended and not pinky_extended:
        return "SELECT_SIGNAL"
    
    # Gesture 4: Victory/Two fingers (index and middle extended) - Turn green
    elif index_extended and middle_extended and not ring_extended and not pinky_extended:
        return "TURN_GREEN"
    
    # Gesture 5: Three fingers (index, middle, ring extended) - Turn yellow
    elif index_extended and middle_extended and ring_extended and not pinky_extended:
        return "TURN_YELLOW"
    
    # Gesture 6: Four fingers (all except pinky) - Turn red
    elif index_extended and middle_extended and ring_extended and pinky_extended:
        return "TURN_RED"
    
    return "NO_GESTURE"

def process_gestures():
    """Process hand gestures from webcam"""
    global currentGreen, currentYellow, signalControlMode, controlledSignal
    
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            continue
            
        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process frame with MediaPipe Hands
        results = hands.process(rgb_frame)
        
        gesture_detected = "NO_GESTURE"
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw hand landmarks
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                
                # Detect gesture
                gesture_detected = detect_gesture(hand_landmarks)
                
                # Display gesture text
                cv2.putText(frame, f"Gesture: {gesture_detected}", (10, 30), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Process gestures
        if gesture_detected == "ACTIVATE_CONTROL":
            signalControlMode = True
            controlledSignal = 0  # Start with first signal
            print("Gesture Control Activated - Controlling Signal", controlledSignal + 1)
            
        elif gesture_detected == "DEACTIVATE_CONTROL":
            signalControlMode = False
            currentGreen = -1
            currentYellow = 0
            print("Gesture Control Deactivated - All signals RED")
            
        elif gesture_detected == "SELECT_SIGNAL" and signalControlMode:
            controlledSignal = (controlledSignal + 1) % noOfSignals
            print(f"Now Controlling Signal {controlledSignal + 1}")
            time.sleep(1)  # Prevent rapid switching
            
        elif gesture_detected == "TURN_GREEN" and signalControlMode:
            if currentGreen != controlledSignal:
                currentGreen = controlledSignal
                currentYellow = 0
                signals[controlledSignal].greenTimer = 20  # Set green time
                print(f"Signal {controlledSignal + 1} turned GREEN")
            
        elif gesture_detected == "TURN_YELLOW" and signalControlMode:
            if currentGreen == controlledSignal:
                currentYellow = 1
                signals[controlledSignal].greenTimer = 5  # Set yellow time
                print(f"Signal {controlledSignal + 1} turned YELLOW")
            
        elif gesture_detected == "TURN_RED" and signalControlMode:
            if currentGreen == controlledSignal:
                currentGreen = -1
                currentYellow = 0
                print(f"Signal {controlledSignal + 1} turned RED")
        
        # Display control status
        status_text = f"Control: {'ON' if signalControlMode else 'OFF'}"
        if signalControlMode:
            status_text += f" | Signal: {controlledSignal + 1}"
        cv2.putText(frame, status_text, (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        cv2.imshow('Hand Gesture Control', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

def update_signal_timers():
    """Update signal timers for automatic transition"""
    global currentGreen, currentYellow
    
    if currentGreen >= 0 and signalControlMode:
        if currentYellow == 0:  # Green signal
            signals[currentGreen].greenTimer -= 1
            if signals[currentGreen].greenTimer <= 0:
                currentYellow = 1
                signals[currentGreen].greenTimer = 5  # Yellow time
        else:  # Yellow signal
            signals[currentGreen].greenTimer -= 1
            if signals[currentGreen].greenTimer <= 0:
                currentGreen = -1
                currentYellow = 0

class Main:
    thread4 = threading.Thread(name="simulationTime",target=simulationTime, args=()) 
    thread4.daemon = True
    thread4.start()

    thread2 = threading.Thread(name="initialization",target=initialize, args=())    # initialization
    thread2.daemon = True
    thread2.start()

    # Start gesture processing thread
    gesture_thread = threading.Thread(name="gestureProcessing", target=process_gestures, args=())
    gesture_thread.daemon = True
    gesture_thread.start()

    # Colours 
    black = (0, 0, 0)
    white = (255, 255, 255)
    green = (0, 255, 0)
    yellow = (255, 255, 0)
    red = (255, 0, 0)

    # Screensize 
    screenWidth = 1400
    screenHeight = 800
    screenSize = (screenWidth, screenHeight)

    # Setting background image i.e. image of intersection
    # background = pygame.image.load('images/mod_int.png')
    background = pygame.image.load(os.path.join(BASE_DIR, 'images', 'mod_int.png'))


    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("TRAFFIC SIMULATION WITH GESTURE CONTROL")

    # Loading signal images and font
    # redSignal = pygame.image.load('images/signals/red.png')
    # yellowSignal = pygame.image.load('images/signals/yellow.png')
    # greenSignal = pygame.image.load('images/signals/green.png')
    redSignal = pygame.image.load(os.path.join(BASE_DIR, 'images', 'signals', 'red.png'))
    yellowSignal = pygame.image.load(os.path.join(BASE_DIR, 'images', 'signals', 'yellow.png'))
    greenSignal = pygame.image.load(os.path.join(BASE_DIR, 'images', 'signals', 'green.png'))

    font = pygame.font.Font(None, 30)
    large_font = pygame.font.Font(None, 40)

    thread3 = threading.Thread(name="generateVehicles",target=generateVehicles, args=())    # Generating vehicles
    thread3.daemon = True
    thread3.start()

    last_timer_update = time.time()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                cv2.destroyAllWindows()
                sys.exit()

        # Update signal timers every second
        current_time = time.time()
        if current_time - last_timer_update >= 1:
            update_signal_timers()
            last_timer_update = current_time

        screen.blit(background,(0,0))   # display background in simulation
        
        # Display signals based on current state
        for i in range(0, noOfSignals):
            if i == currentGreen:
                if currentYellow == 1:
                    signals[i].signalText = str(signals[i].greenTimer)
                    screen.blit(yellowSignal, signalCoods[i])
                else:
                    signals[i].signalText = str(signals[i].greenTimer)
                    screen.blit(greenSignal, signalCoods[i])
            else:
                signals[i].signalText = "STOP"
                screen.blit(redSignal, signalCoods[i])
        
        signalTexts = ["","","",""]

        # Display signal text and vehicle count
        for i in range(0, noOfSignals):  
            signalTexts[i] = font.render(str(signals[i].signalText), True, white, black)
            screen.blit(signalTexts[i], signalTimerCoods[i]) 
            displayText = vehicles[directionNumbers[i]]['crossed']
            vehicleCountTexts[i] = font.render(str(displayText), True, black, white)
            screen.blit(vehicleCountTexts[i], vehicleCountCoods[i])

        # Display control information
        control_text = "Gesture Control: " + ("ACTIVE" if signalControlMode else "INACTIVE")
        control_surface = font.render(control_text, True, green if signalControlMode else red, white)
        screen.blit(control_surface, (50, 50))
        
        if signalControlMode:
            signal_text = f"Controlling Signal: {controlledSignal + 1}"
            signal_surface = font.render(signal_text, True, yellow, black)
            screen.blit(signal_surface, (50, 80))
            
            instruction_text = "Gestures: Open Hand=Activate, Fist=Deactivate, Point=Switch Signal"
            instruction_surface = font.render(instruction_text, True, black, white)
            screen.blit(instruction_surface, (50, 110))
            
            instruction_text2 = "2 Fingers=Green, 3 Fingers=Yellow, 4 Fingers=Red"
            instruction_surface2 = font.render(instruction_text2, True, black, white)
            screen.blit(instruction_surface2, (50, 140))

        timeElapsedText = font.render(("Time Elapsed: "+str(timeElapsed)), True, black, white)
        screen.blit(timeElapsedText, (1100, 50))

        # Display the vehicles
        for vehicle in simulation:  
            screen.blit(vehicle.currentImage, [vehicle.x, vehicle.y])
            vehicle.move()
            
        pygame.display.update()

if __name__ == "__main__":
    Main()