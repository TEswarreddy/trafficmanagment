# # LAG
# # NO. OF VEHICLES IN SIGNAL CLASS
# # stops not used
# # DISTRIBUTION
# # BUS TOUCHING ON TURNS
# # Distribution using python class
# # *** IMAGE XY COOD IS TOP LEFT

# import random
# import math
# import time
# import threading
# import pygame
# import sys
# import os

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# # Default signal timings
# defaultRed = 120
# defaultYellow = 5
# defaultGreen = 25
# defaultMinimum = 12
# defaultMaximum = 55

# signals = []
# noOfSignals = 4
# simTime = 600                      # simulation duration in seconds
# timeElapsed = 0
# currentGreen = 0
# nextGreen = (currentGreen + 1) % noOfSignals
# currentYellow = 0

# # Emergency control
# emergencyActive = False
# emergencyDirection = None

# # Average time per vehicle type to cross (seconds)
# carTime     = 1.8
# bikeTime    = 1.0
# rickshawTime= 1.5
# busTime     = 3.2
# truckTime   = 3.5
# ambulanceTime = 1.2

# noOfLanes = 2
# detectionTime = 5

# speeds = {
#     'car':       2.4,
#     'bus':       1.9,
#     'truck':     1.8,
#     'rickshaw':  2.1,
#     'bike':      2.7,
#     'ambulance': 3.8
# }

# # Starting coordinates for each direction and lane
# x = {'right': [0, 0, 0],       'down': [755, 727, 697], 'left': [1400,1400,1400], 'up': [602,627,657]}
# y = {'right': [348,370,398],   'down': [0, 0, 0],       'left': [498,466,436],    'up': [800,800,800]}

# vehicles = {
#     'right': {0:[], 1:[], 2:[], 'crossed':0},
#     'down':  {0:[], 1:[], 2:[], 'crossed':0},
#     'left':  {0:[], 1:[], 2:[], 'crossed':0},
#     'up':    {0:[], 1:[], 2:[], 'crossed':0}
# }

# vehicleTypes = {
#     0:'car', 1:'bus', 2:'truck', 3:'rickshaw', 4:'bike', 5:'ambulance'
# }

# directionNumbers = {0:'right', 1:'down', 2:'left', 3:'up'}

# signalCoods       = [(530,230), (810,230), (810,570), (530,570)]
# signalTimerCoods  = [(530,210), (810,210), (810,550), (530,550)]
# vehicleCountCoods = [(480,210), (880,210), (880,550), (480,550)]

# stopLines   = {'right': 590, 'down': 330, 'left': 800, 'up': 535}
# defaultStop = {'right': 580, 'down': 320, 'left': 810, 'up': 545}
# stops = {
#     'right': [580,580,580],
#     'down':  [320,320,320],
#     'left':  [810,810,810],
#     'up':    [545,545,545]
# }

# mid = {
#     'right': {'x':705, 'y':445},
#     'down':  {'x':695, 'y':450},
#     'left':  {'x':695, 'y':425},
#     'up':    {'x':695, 'y':400}
# }

# rotationAngle = 3
# gap  = 30     # increased gap between stopped vehicles
# gap2 = 25     # increased moving gap

# pygame.init()
# simulation = pygame.sprite.Group()

# class TrafficSignal:
#     def __init__(self, red, yellow, green, minimum, maximum):
#         self.red = red
#         self.yellow = yellow
#         self.green = green
#         self.minimum = minimum
#         self.maximum = maximum
#         self.signalText = "30"
#         self.totalGreenTime = 0

# class Vehicle(pygame.sprite.Sprite):
#     def __init__(self, lane, vehicleClass, direction_number, direction, will_turn):
#         pygame.sprite.Sprite.__init__(self)
#         self.lane = lane
#         self.vehicleClass = vehicleClass
#         self.speed = speeds[vehicleClass]
#         self.direction_number = direction_number
#         self.direction = direction
#         self.x = x[direction][lane]
#         self.y = y[direction][lane]
#         self.crossed = 0
#         self.willTurn = will_turn
#         self.turned = 0
#         self.rotateAngle = 0

#         vehicles[direction][lane].append(self)
#         self.index = len(vehicles[direction][lane]) - 1

#         path = os.path.join(BASE_DIR, 'images', direction, f'{vehicleClass}.png')
#         self.originalImage = pygame.image.load(path)
#         self.currentImage = pygame.image.load(path)

#         # Set stop position dynamically
#         prev_vehicle = vehicles[direction][lane][self.index-1] if self.index > 0 else None
#         if prev_vehicle and prev_vehicle.crossed == 0:
#             if direction == 'right':
#                 self.stop = prev_vehicle.stop - prev_vehicle.currentImage.get_rect().width - gap
#             elif direction == 'left':
#                 self.stop = prev_vehicle.stop + prev_vehicle.currentImage.get_rect().width + gap
#             elif direction == 'down':
#                 self.stop = prev_vehicle.stop - prev_vehicle.currentImage.get_rect().height - gap
#             elif direction == 'up':
#                 self.stop = prev_vehicle.stop + prev_vehicle.currentImage.get_rect().height + gap
#         else:
#             self.stop = defaultStop[direction]

#         # Adjust start position
#         temp = self.currentImage.get_rect().width if direction in ['right', 'left'] else self.currentImage.get_rect().height
#         temp += gap
#         if direction == 'right':
#             x[direction][lane] -= temp
#             stops[direction][lane] -= temp
#         elif direction == 'left':
#             x[direction][lane] += temp
#             stops[direction][lane] += temp
#         elif direction == 'down':
#             y[direction][lane] -= temp
#             stops[direction][lane] -= temp
#         elif direction == 'up':
#             y[direction][lane] += temp
#             stops[direction][lane] += temp

#         simulation.add(self)

#     def move(self):
#         global emergencyActive, emergencyDirection

#         # Check for emergency trigger
#         if (self.vehicleClass == "ambulance" and self.crossed == 0 and self.direction_number != currentGreen and not emergencyActive):
#             print(f"!!! EMERGENCY DETECTED - Ambulance waiting at RED from {self.direction.upper()} !!!")
#             emergencyActive = True
#             emergencyDirection = self.direction_number

#         dir = self.direction
#         is_green = (currentGreen == self.direction_number and currentYellow == 0)

#         if dir == 'right':
#             vehicle_dim = self.currentImage.get_rect().width
#             mid_x = mid[dir]['x']
#             stop_line = stopLines[dir] + 20

#             if self.crossed == 0 and self.x + vehicle_dim > stop_line:
#                 self.crossed = 1
#                 vehicles[dir]['crossed'] += 1
#                 if self.vehicleClass == "ambulance":
#                     print(f"Ambulance from {dir} has crossed → check if more")

#             if self.willTurn:
#                 if self.crossed == 0 or self.x + vehicle_dim < mid_x:
#                     if (self.x + vehicle_dim <= self.stop or is_green or self.crossed == 1) and \
#                        (self.index == 0 or self.x + vehicle_dim < (vehicles[dir][self.lane][self.index-1].x - gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
#                         self.x += self.speed
#                 else:
#                     if self.turned == 0:
#                         self.rotateAngle += rotationAngle
#                         self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
#                         self.x += 2
#                         self.y += 1.8
#                         if self.rotateAngle == 90:
#                             self.turned = 1
#                     else:
#                         if self.index == 0 or self.y + self.currentImage.get_rect().height < (vehicles[dir][self.lane][self.index-1].y - gap2) or self.x + vehicle_dim < (vehicles[dir][self.lane][self.index-1].x - gap2):
#                             self.y += self.speed
#             else:
#                 if (self.x + vehicle_dim <= self.stop or self.crossed == 1 or is_green) and \
#                    (self.index == 0 or self.x + vehicle_dim < (vehicles[dir][self.lane][self.index-1].x - gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
#                     self.x += self.speed

#         elif dir == 'down':
#             vehicle_dim = self.currentImage.get_rect().height
#             mid_y = mid[dir]['y']
#             stop_line = stopLines[dir]

#             if self.crossed == 0 and self.y + vehicle_dim > stop_line:
#                 self.crossed = 1
#                 vehicles[dir]['crossed'] += 1
#                 if self.vehicleClass == "ambulance":
#                     print(f"Ambulance from {dir} has crossed → check if more")

#             if self.willTurn:
#                 if self.crossed == 0 or self.y + vehicle_dim < mid_y:
#                     if (self.y + vehicle_dim <= self.stop or is_green or self.crossed == 1) and \
#                        (self.index == 0 or self.y + vehicle_dim < (vehicles[dir][self.lane][self.index-1].y - gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
#                         self.y += self.speed
#                 else:
#                     if self.turned == 0:
#                         self.rotateAngle += rotationAngle
#                         self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
#                         self.x -= 2.5
#                         self.y += 2
#                         if self.rotateAngle == 90:
#                             self.turned = 1
#                     else:
#                         if self.index == 0 or self.x > (vehicles[dir][self.lane][self.index-1].x + vehicles[dir][self.lane][self.index-1].currentImage.get_rect().width + gap2) or self.y < (vehicles[dir][self.lane][self.index-1].y - gap2):
#                             self.x -= self.speed
#             else:
#                 if (self.y + vehicle_dim <= self.stop or self.crossed == 1 or is_green) and \
#                    (self.index == 0 or self.y + vehicle_dim < (vehicles[dir][self.lane][self.index-1].y - gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
#                     self.y += self.speed

#         elif dir == 'left':
#             vehicle_dim = self.currentImage.get_rect().width
#             mid_x = mid[dir]['x']
#             stop_line = stopLines[dir]

#             if self.crossed == 0 and self.x < stop_line:
#                 self.crossed = 1
#                 vehicles[dir]['crossed'] += 1
#                 if self.vehicleClass == "ambulance":
#                     print(f"Ambulance from {dir} has crossed → check if more")

#             if self.willTurn:
#                 if self.crossed == 0 or self.x > mid_x:
#                     if (self.x >= self.stop or is_green or self.crossed == 1) and \
#                        (self.index == 0 or self.x > (vehicles[dir][self.lane][self.index-1].x + vehicles[dir][self.lane][self.index-1].currentImage.get_rect().width + gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
#                         self.x -= self.speed
#                 else:
#                     if self.turned == 0:
#                         self.rotateAngle += rotationAngle
#                         self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
#                         self.x -= 1.8
#                         self.y -= 2.5
#                         if self.rotateAngle == 90:
#                             self.turned = 1
#                     else:
#                         if self.index == 0 or self.y > (vehicles[dir][self.lane][self.index-1].y + vehicles[dir][self.lane][self.index-1].currentImage.get_rect().height + gap2) or self.x > (vehicles[dir][self.lane][self.index-1].x + gap2):
#                             self.y -= self.speed
#             else:
#                 if (self.x >= self.stop or self.crossed == 1 or is_green) and \
#                    (self.index == 0 or self.x > (vehicles[dir][self.lane][self.index-1].x + vehicles[dir][self.lane][self.index-1].currentImage.get_rect().width + gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
#                     self.x -= self.speed

#         elif dir == 'up':
#             vehicle_dim = self.currentImage.get_rect().height
#             mid_y = mid[dir]['y']
#             stop_line = stopLines[dir]

#             if self.crossed == 0 and self.y < stop_line:
#                 self.crossed = 1
#                 vehicles[dir]['crossed'] += 1
#                 if self.vehicleClass == "ambulance":
#                     print(f"Ambulance from {dir} has crossed → check if more")

#             if self.willTurn:
#                 if self.crossed == 0 or self.y > mid_y:
#                     if (self.y >= self.stop or is_green or self.crossed == 1) and \
#                        (self.index == 0 or self.y > (vehicles[dir][self.lane][self.index-1].y + vehicles[dir][self.lane][self.index-1].currentImage.get_rect().height + gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
#                         self.y -= self.speed
#                 else:
#                     if self.turned == 0:
#                         self.rotateAngle += rotationAngle
#                         self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
#                         self.x += 1
#                         self.y -= 1
#                         if self.rotateAngle == 90:
#                             self.turned = 1
#                     else:
#                         if self.index == 0 or self.x < (vehicles[dir][self.lane][self.index-1].x - vehicles[dir][self.lane][self.index-1].currentImage.get_rect().width - gap2) or self.y > (vehicles[dir][self.lane][self.index-1].y + gap2):
#                             self.x += self.speed
#             else:
#                 if (self.y >= self.stop or self.crossed == 1 or is_green) and \
#                    (self.index == 0 or self.y > (vehicles[dir][self.lane][self.index-1].y + vehicles[dir][self.lane][self.index-1].currentImage.get_rect().height + gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
#                     self.y -= self.speed

# def count_waiting_ambulances(dir_num):
#     count = 0
#     direction = directionNumbers[dir_num]
#     for lane in range(3):
#         for v in vehicles[direction][lane]:
#             if v.crossed == 0 and v.vehicleClass == 'ambulance':
#                 count += 1
#     return count

# # Initialization
# def initialize():
#     ts1 = TrafficSignal(0, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
#     signals.append(ts1)
#     ts2 = TrafficSignal(ts1.red + ts1.yellow + ts1.green, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
#     signals.append(ts2)
#     ts3 = TrafficSignal(defaultRed, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
#     signals.append(ts3)
#     ts4 = TrafficSignal(defaultRed, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
#     signals.append(ts4)
#     print("→ Signals initialized")
#     repeat()

# # Adaptive timing calculation
# def setTime():
#     global emergencyActive
#     if emergencyActive:
#         print("  (Emergency active → skipping normal adaptive timing)")
#         return

#     print(f"→ Calculating green time for next direction: {directionNumbers[nextGreen]}")

#     noOfCars = noOfBikes = noOfBuses = noOfTrucks = noOfRickshaws = noOfAmbulances = 0

#     dir_name = directionNumbers[nextGreen]

#     for lane in range(3):
#         for v in vehicles[dir_name][lane]:
#             if v.crossed == 0:
#                 vc = v.vehicleClass
#                 if vc == 'car':
#                     noOfCars += 1
#                 elif vc == 'bus':
#                     noOfBuses += 1
#                 elif vc == 'truck':
#                     noOfTrucks += 1
#                 elif vc == 'rickshaw':
#                     noOfRickshaws += 1
#                 elif vc == 'bike':
#                     noOfBikes += 1
#                 elif vc == 'ambulance':
#                     noOfAmbulances += 1

#     total_time = (noOfCars * carTime + noOfRickshaws * rickshawTime + noOfBuses * busTime + noOfTrucks * truckTime + noOfBikes * bikeTime + noOfAmbulances * ambulanceTime)
#     greenTime = math.ceil(total_time / 3)  # Divide by number of lanes (3)
#     greenTime = max(defaultMinimum, min(defaultMaximum, greenTime))
#     signals[nextGreen].green = greenTime
#     print(f"  → Assigned green time = {greenTime} seconds  (vehicles: C:{noOfCars} Bk:{noOfBikes} Bs:{noOfBuses} T:{noOfTrucks} R:{noOfRickshaws} Amb:{noOfAmbulances})")

# def repeat():
#     global currentGreen, currentYellow, nextGreen, emergencyActive, emergencyDirection

#     while True:
#         if emergencyActive:
#             print("\n" + "="*60)
#             print("          EMERGENCY VEHICLE PRIORITY MODE ACTIVATED")
#             print("="*60)
#             print(f"Direction getting priority: {directionNumbers[emergencyDirection].upper()}")

#             previousGreen = currentGreen
#             currentGreen = emergencyDirection
#             currentYellow = 0
#             nextGreen = (currentGreen + 1) % noOfSignals

#             for i in range(noOfSignals):
#                 if i != currentGreen:
#                     signals[i].red = 300  # large value to prevent quick cycle
#                     signals[i].green = 0
#                     signals[i].yellow = 0

#             num_amb = count_waiting_ambulances(emergencyDirection)
#             initial_green = max(20, num_amb * 10)
#             signals[currentGreen].green = initial_green
#             signals[currentGreen].yellow = defaultYellow
#             print(f"→ Setting emergency green to {initial_green}s for {num_amb} ambulances")

#             while signals[currentGreen].green > 0 or count_waiting_ambulances(emergencyDirection) > 0:
#                 if signals[currentGreen].green <= 0 and count_waiting_ambulances(emergencyDirection) > 0:
#                     num_amb_remaining = count_waiting_ambulances(emergencyDirection)
#                     extension = max(10, num_amb_remaining * 10)
#                     signals[currentGreen].green += extension
#                     print(f"→ Extending emergency green by {extension}s for {num_amb_remaining} remaining ambulances")

#                 printStatus()
#                 updateValues()
#                 time.sleep(1)

#             currentYellow = 1
#             while signals[currentGreen].yellow > 0:
#                 printStatus()
#                 updateValues()
#                 time.sleep(1)

#             currentYellow = 0
#             print("\n→ Emergency cleared. Returning to normal adaptive control.")
#             emergencyActive = False

#             for i in range(noOfSignals):
#                 signals[i].green = defaultGreen
#                 signals[i].yellow = defaultYellow
#                 signals[i].red = defaultRed

#             currentGreen = previousGreen
#             nextGreen = (currentGreen + 1) % noOfSignals
#             continue

#         print(f"\n→ Green for {directionNumbers[currentGreen]}")
#         while signals[currentGreen].green > 0:
#             printStatus()
#             updateValues()

#             if signals[nextGreen].red == detectionTime:
#                 thread = threading.Thread(target=setTime)
#                 thread.daemon = True
#                 thread.start()

#             time.sleep(1)

#         currentYellow = 1
#         print(f"→ Yellow for {directionNumbers[currentGreen]}")
#         while signals[currentGreen].yellow > 0:
#             printStatus()
#             updateValues()
#             time.sleep(1)

#         currentYellow = 0

#         signals[currentGreen].green = defaultGreen
#         signals[currentGreen].yellow = defaultYellow

#         currentGreen = nextGreen
#         nextGreen = (currentGreen + 1) % noOfSignals

# # Print the signal timers on cmd
# def printStatus():
#     for i in range(0, noOfSignals):
#         if(i==currentGreen):
#             if(currentYellow==0):
#                 print(" GREEN TS",i+1,"-> r:",signals[i].red," y:",signals[i].yellow," g:",signals[i].green)
#             else:
#                 print("YELLOW TS",i+1,"-> r:",signals[i].red," y:",signals[i].yellow," g:",signals[i].green)
#         else:
#             print(" RED TS",i+1,"-> r:",signals[i].red," y:",signals[i].yellow," g:",signals[i].green)
#     print()

# # Update values of the signal timers after every second
# def updateValues():
#     for i in range(0, noOfSignals):
#         if(i==currentGreen):
#             if(currentYellow==0):
#                 if signals[i].green > 0:
#                     signals[i].green -=1
#                 signals[i].totalGreenTime +=1
#             else:
#                 if signals[i].yellow > 0:
#                     signals[i].yellow -=1
#         else:
#             if signals[i].red > 0:
#                 signals[i].red -=1

# def generateVehicles():
#     while(True):
#         rand = random.randint(0,99)
#         if rand < 2:
#             vehicle_type = 5 # ambulance
#         else:
#             vehicle_type = random.randint(0,4) # normal vehicles
#         if(vehicle_type==4):
#             lane_number = 0
#         else:
#             lane_number = random.randint(0,1) + 1
#         will_turn = 0
#         if(lane_number==2):
#             temp = random.randint(0,4)
#             if(temp<=2):
#                 will_turn = 1
#             elif(temp>2):
#                 will_turn = 0
#         direction_number = random.randint(0,3)
      
#         Vehicle(lane_number, vehicleTypes[vehicle_type], direction_number, directionNumbers[direction_number], will_turn)
#         time.sleep(2)

# def simulationTime():
#     global timeElapsed, simTime
#     while(True):
#         timeElapsed += 1
#         time.sleep(1)
#         if(timeElapsed==simTime):
#             totalVehicles = 0
#             print('Lane-wise Vehicle Counts')
#             for i in range(noOfSignals):
#                 print('Lane',i+1,':',vehicles[directionNumbers[i]]['crossed'])
#                 totalVehicles += vehicles[directionNumbers[i]]['crossed']
#             print('Total vehicles passed: ',totalVehicles)
#             print('Total time passed: ',timeElapsed)
#             print('No. of vehicles passed per unit time: ',(float(totalVehicles)/float(timeElapsed)))
#             os._exit(1)
   
# class Main:
#     thread4 = threading.Thread(name="simulationTime",target=simulationTime, args=())
#     thread4.daemon = True
#     thread4.start()
#     thread2 = threading.Thread(name="initialization",target=initialize, args=()) # initialization
#     thread2.daemon = True
#     thread2.start()
#     # Colours
#     black = (0, 0, 0)
#     white = (255, 255, 255)
#     # Screensize
#     screenWidth = 1400
#     screenHeight = 800
#     screenSize = (screenWidth, screenHeight)
#     # Setting background image i.e. image of intersection
#     background = pygame.image.load(os.path.join(BASE_DIR, 'images', 'mod_int.png'))
#     screen = pygame.display.set_mode(screenSize)
#     pygame.display.set_caption("SIMULATION")
#     # Loading signal images and font
#     redSignal = pygame.image.load(os.path.join(BASE_DIR, 'images', 'signals', 'red.png'))
#     yellowSignal = pygame.image.load(os.path.join(BASE_DIR, 'images', 'signals', 'yellow.png'))
#     greenSignal = pygame.image.load(os.path.join(BASE_DIR, 'images', 'signals', 'green.png'))
#     font = pygame.font.Font(None, 30)
#     thread3 = threading.Thread(name="generateVehicles",target=generateVehicles, args=()) # Generating vehicles
#     thread3.daemon = True
#     thread3.start()
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 sys.exit()
#         screen.blit(background,(0,0)) # display background in simulation
#         for i in range(0,noOfSignals): # display signal and set timer according to current status: green, yello, or red
#             if(i==currentGreen):
#                 if(currentYellow==1):
#                     if(signals[i].yellow==0):
#                         signals[i].signalText = "STOP"
#                     else:
#                         signals[i].signalText = signals[i].yellow
#                     screen.blit(yellowSignal, signalCoods[i])
#                 else:
#                     if(signals[i].green==0):
#                         signals[i].signalText = "SLOW"
#                     else:
#                         signals[i].signalText = signals[i].green
#                     screen.blit(greenSignal, signalCoods[i])
#             else:
#                 if(signals[i].red<=10):
#                     if(signals[i].red==0):
#                         signals[i].signalText = "GO"
#                     else:
#                         signals[i].signalText = signals[i].red
#                 else:
#                     signals[i].signalText = "---"
#                 screen.blit(redSignal, signalCoods[i])
#         signalTexts = ["","","",""]
#         # display signal timer and vehicle count
#         for i in range(0,noOfSignals):
#             signalTexts[i] = font.render(str(signals[i].signalText), True, white, black)
#             screen.blit(signalTexts[i],signalTimerCoods[i])
#             displayText = vehicles[directionNumbers[i]]['crossed']
#             vehicleCountTexts = font.render(str(displayText), True, black, white)
#             screen.blit(vehicleCountTexts,vehicleCountCoods[i])
#         timeElapsedText = font.render(("Time Elapsed: "+str(timeElapsed)), True, black, white)
#         screen.blit(timeElapsedText,(1100,50))
#         # 🚑 Draw Emergency Banner
#         if emergencyActive:
#             emergencyFont = pygame.font.Font(None, 60)
#             emergencyText = emergencyFont.render(
#                 "🚑 EMERGENCY VEHICLE - " + directionNumbers[emergencyDirection].upper(),
#                 True,
#                 (255, 0, 0),
#                 (255, 255, 255)
#                 )
#             text_rect = emergencyText.get_rect(center=(700, 40))
#             screen.blit(emergencyText, text_rect)
#         # display the vehicles
#         for vehicle in simulation:
#             screen.blit(vehicle.currentImage, [vehicle.x, vehicle.y])
#             vehicle.move()
#         to_remove = []
#         for vehicle in simulation:
#             if vehicle.direction == 'right' and vehicle.x > 1400 + 100:
#                 to_remove.append(vehicle)
#             elif vehicle.direction == 'down' and vehicle.y > 800 + 100:
#                 to_remove.append(vehicle)
#             elif vehicle.direction == 'left' and vehicle.x < -100:
#                 to_remove.append(vehicle)
#             elif vehicle.direction == 'up' and vehicle.y < -100:
#                 to_remove.append(vehicle)
#         for vehicle in to_remove:
#             simulation.remove(vehicle)
#             vehicles[vehicle.direction][vehicle.lane].remove(vehicle)
#         for dir_num in range(4):
#             direction = directionNumbers[dir_num]
#             for lane in range(3):
#                 for i in range(len(vehicles[direction][lane])):
#                     vehicles[direction][lane][i].index = i
#         pygame.display.update()

# Main()


# LAG
# NO. OF VEHICLES IN SIGNAL CLASS
# stops not used
# DISTRIBUTION
# BUS TOUCHING ON TURNS
# Distribution using python class
# *** IMAGE XY COOD IS TOP LEFT

# import random
# import math
# import time
# import threading
# import pygame
# import sys
# import os

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# # Default signal timings
# defaultRed = 120
# defaultYellow = 5
# defaultGreen = 25
# defaultMinimum = 12
# defaultMaximum = 55

# signals = []
# noOfSignals = 4
# simTime = 600                      # simulation duration in seconds
# timeElapsed = 0
# currentGreen = 0
# nextGreen = (currentGreen + 1) % noOfSignals
# currentYellow = 0

# # Emergency control
# emergencyActive = False
# emergencyDirection = None

# # Average time per vehicle type to cross (seconds)
# carTime     = 1.8
# bikeTime    = 1.0
# rickshawTime= 1.5
# busTime     = 3.2
# truckTime   = 3.5
# ambulanceTime = 1.2

# noOfLanes = 2
# detectionTime = 5

# speeds = {
#     'car':       2.4,
#     'bus':       1.9,
#     'truck':     1.8,
#     'rickshaw':  2.1,
#     'bike':      2.7,
#     'ambulance': 3.8
# }

# # Starting coordinates for each direction and lane
# x = {'right': [0, 0, 0],       'down': [755, 727, 697], 'left': [1400,1400,1400], 'up': [602,627,657]}
# y = {'right': [348,370,398],   'down': [0, 0, 0],       'left': [498,466,436],    'up': [800,800,800]}

# vehicles = {
#     'right': {0:[], 1:[], 2:[], 'crossed':0},
#     'down':  {0:[], 1:[], 2:[], 'crossed':0},
#     'left':  {0:[], 1:[], 2:[], 'crossed':0},
#     'up':    {0:[], 1:[], 2:[], 'crossed':0}
# }

# vehicleTypes = {
#     0:'car', 1:'bus', 2:'truck', 3:'rickshaw', 4:'bike', 5:'ambulance'
# }

# directionNumbers = {0:'right', 1:'down', 2:'left', 3:'up'}

# signalCoods       = [(530,230), (810,230), (810,570), (530,570)]
# signalTimerCoods  = [(530,210), (810,210), (810,550), (530,550)]
# vehicleCountCoods = [(480,210), (880,210), (880,550), (480,550)]
# waitingCountCoods = [(480,230), (880,230), (880,570), (480,570)]

# stopLines   = {'right': 590, 'down': 330, 'left': 800, 'up': 535}
# defaultStop = {'right': 580, 'down': 320, 'left': 810, 'up': 545}
# stops = {
#     'right': [580,580,580],
#     'down':  [320,320,320],
#     'left':  [810,810,810],
#     'up':    [545,545,545]
# }

# mid = {
#     'right': {'x':705, 'y':445},
#     'down':  {'x':695, 'y':450},
#     'left':  {'x':695, 'y':425},
#     'up':    {'x':695, 'y':400}
# }

# rotationAngle = 3
# gap  = 30     # increased gap between stopped vehicles
# gap2 = 25     # increased moving gap

# pygame.init()
# simulation = pygame.sprite.Group()

# class TrafficSignal:
#     def __init__(self, red, yellow, green, minimum, maximum):
#         self.red = red
#         self.yellow = yellow
#         self.green = green
#         self.minimum = minimum
#         self.maximum = maximum
#         self.signalText = "30"
#         self.totalGreenTime = 0

# class Vehicle(pygame.sprite.Sprite):
#     def __init__(self, lane, vehicleClass, direction_number, direction, will_turn):
#         pygame.sprite.Sprite.__init__(self)
#         self.lane = lane
#         self.vehicleClass = vehicleClass
#         self.speed = speeds[vehicleClass]
#         self.direction_number = direction_number
#         self.direction = direction
#         self.x = x[direction][lane]
#         self.y = y[direction][lane]
#         self.crossed = 0
#         self.willTurn = will_turn
#         self.turned = 0
#         self.rotateAngle = 0

#         vehicles[direction][lane].append(self)
#         self.index = len(vehicles[direction][lane]) - 1

#         path = os.path.join(BASE_DIR, 'images', direction, f'{vehicleClass}.png')
#         self.originalImage = pygame.image.load(path)
#         self.currentImage = pygame.image.load(path)

#         # Set stop position dynamically
#         prev_vehicle = vehicles[direction][lane][self.index-1] if self.index > 0 else None
#         if prev_vehicle and prev_vehicle.crossed == 0:
#             if direction == 'right':
#                 self.stop = prev_vehicle.stop - prev_vehicle.currentImage.get_rect().width - gap
#             elif direction == 'left':
#                 self.stop = prev_vehicle.stop + prev_vehicle.currentImage.get_rect().width + gap
#             elif direction == 'down':
#                 self.stop = prev_vehicle.stop - prev_vehicle.currentImage.get_rect().height - gap
#             elif direction == 'up':
#                 self.stop = prev_vehicle.stop + prev_vehicle.currentImage.get_rect().height + gap
#         else:
#             self.stop = defaultStop[direction]

#         # Adjust start position
#         temp = self.currentImage.get_rect().width if direction in ['right', 'left'] else self.currentImage.get_rect().height
#         temp += gap
#         if direction == 'right':
#             x[direction][lane] -= temp
#             stops[direction][lane] -= temp
#         elif direction == 'left':
#             x[direction][lane] += temp
#             stops[direction][lane] += temp
#         elif direction == 'down':
#             y[direction][lane] -= temp
#             stops[direction][lane] -= temp
#         elif direction == 'up':
#             y[direction][lane] += temp
#             stops[direction][lane] += temp

#         simulation.add(self)

#     def move(self):
#         global emergencyActive, emergencyDirection

#         # Check for emergency trigger
#         if (self.vehicleClass == "ambulance" and self.crossed == 0 and self.direction_number != currentGreen and not emergencyActive):
#             print(f"!!! EMERGENCY DETECTED - Ambulance waiting at RED from {self.direction.upper()} !!!")
#             emergencyActive = True
#             emergencyDirection = self.direction_number

#         dir = self.direction
#         is_green = (currentGreen == self.direction_number and currentYellow == 0)

#         if dir == 'right':
#             vehicle_dim = self.currentImage.get_rect().width
#             mid_x = mid[dir]['x']
#             stop_line = stopLines[dir] + 20

#             if self.crossed == 0 and self.x + vehicle_dim > stop_line:
#                 self.crossed = 1
#                 vehicles[dir]['crossed'] += 1
#                 if self.vehicleClass == "ambulance":
#                     print(f"Ambulance from {dir} has crossed → check if more")

#             if self.willTurn:
#                 if self.crossed == 0 or self.x + vehicle_dim < mid_x:
#                     if (self.x + vehicle_dim <= self.stop or is_green or self.crossed == 1) and \
#                        (self.index == 0 or self.x + vehicle_dim < (vehicles[dir][self.lane][self.index-1].x - gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
#                         self.x += self.speed
#                 else:
#                     if self.turned == 0:
#                         self.rotateAngle += rotationAngle
#                         self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
#                         self.x += 2
#                         self.y += 1.8
#                         if self.rotateAngle == 90:
#                             self.turned = 1
#                     else:
#                         if self.index == 0 or self.y + self.currentImage.get_rect().height < (vehicles[dir][self.lane][self.index-1].y - gap2) or self.x + vehicle_dim < (vehicles[dir][self.lane][self.index-1].x - gap2):
#                             self.y += self.speed
#             else:
#                 if (self.x + vehicle_dim <= self.stop or self.crossed == 1 or is_green) and \
#                    (self.index == 0 or self.x + vehicle_dim < (vehicles[dir][self.lane][self.index-1].x - gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
#                     self.x += self.speed

#         elif dir == 'down':
#             vehicle_dim = self.currentImage.get_rect().height
#             mid_y = mid[dir]['y']
#             stop_line = stopLines[dir]

#             if self.crossed == 0 and self.y + vehicle_dim > stop_line:
#                 self.crossed = 1
#                 vehicles[dir]['crossed'] += 1
#                 if self.vehicleClass == "ambulance":
#                     print(f"Ambulance from {dir} has crossed → check if more")

#             if self.willTurn:
#                 if self.crossed == 0 or self.y + vehicle_dim < mid_y:
#                     if (self.y + vehicle_dim <= self.stop or is_green or self.crossed == 1) and \
#                        (self.index == 0 or self.y + vehicle_dim < (vehicles[dir][self.lane][self.index-1].y - gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
#                         self.y += self.speed
#                 else:
#                     if self.turned == 0:
#                         self.rotateAngle += rotationAngle
#                         self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
#                         self.x -= 2.5
#                         self.y += 2
#                         if self.rotateAngle == 90:
#                             self.turned = 1
#                     else:
#                         if self.index == 0 or self.x > (vehicles[dir][self.lane][self.index-1].x + vehicles[dir][self.lane][self.index-1].currentImage.get_rect().width + gap2) or self.y < (vehicles[dir][self.lane][self.index-1].y - gap2):
#                             self.x -= self.speed
#             else:
#                 if (self.y + vehicle_dim <= self.stop or self.crossed == 1 or is_green) and \
#                    (self.index == 0 or self.y + vehicle_dim < (vehicles[dir][self.lane][self.index-1].y - gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
#                     self.y += self.speed

#         elif dir == 'left':
#             vehicle_dim = self.currentImage.get_rect().width
#             mid_x = mid[dir]['x']
#             stop_line = stopLines[dir]

#             if self.crossed == 0 and self.x < stop_line:
#                 self.crossed = 1
#                 vehicles[dir]['crossed'] += 1
#                 if self.vehicleClass == "ambulance":
#                     print(f"Ambulance from {dir} has crossed → check if more")

#             if self.willTurn:
#                 if self.crossed == 0 or self.x > mid_x:
#                     if (self.x >= self.stop or is_green or self.crossed == 1) and \
#                        (self.index == 0 or self.x > (vehicles[dir][self.lane][self.index-1].x + vehicles[dir][self.lane][self.index-1].currentImage.get_rect().width + gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
#                         self.x -= self.speed
#                 else:
#                     if self.turned == 0:
#                         self.rotateAngle += rotationAngle
#                         self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
#                         self.x -= 1.8
#                         self.y -= 2.5
#                         if self.rotateAngle == 90:
#                             self.turned = 1
#                     else:
#                         if self.index == 0 or self.y > (vehicles[dir][self.lane][self.index-1].y + vehicles[dir][self.lane][self.index-1].currentImage.get_rect().height + gap2) or self.x > (vehicles[dir][self.lane][self.index-1].x + gap2):
#                             self.y -= self.speed
#             else:
#                 if (self.x >= self.stop or self.crossed == 1 or is_green) and \
#                    (self.index == 0 or self.x > (vehicles[dir][self.lane][self.index-1].x + vehicles[dir][self.lane][self.index-1].currentImage.get_rect().width + gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
#                     self.x -= self.speed

#         elif dir == 'up':
#             vehicle_dim = self.currentImage.get_rect().height
#             mid_y = mid[dir]['y']
#             stop_line = stopLines[dir]

#             if self.crossed == 0 and self.y < stop_line:
#                 self.crossed = 1
#                 vehicles[dir]['crossed'] += 1
#                 if self.vehicleClass == "ambulance":
#                     print(f"Ambulance from {dir} has crossed → check if more")

#             if self.willTurn:
#                 if self.crossed == 0 or self.y > mid_y:
#                     if (self.y >= self.stop or is_green or self.crossed == 1) and \
#                        (self.index == 0 or self.y > (vehicles[dir][self.lane][self.index-1].y + vehicles[dir][self.lane][self.index-1].currentImage.get_rect().height + gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
#                         self.y -= self.speed
#                 else:
#                     if self.turned == 0:
#                         self.rotateAngle += rotationAngle
#                         self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
#                         self.x += 1
#                         self.y -= 1
#                         if self.rotateAngle == 90:
#                             self.turned = 1
#                     else:
#                         if self.index == 0 or self.x < (vehicles[dir][self.lane][self.index-1].x - vehicles[dir][self.lane][self.index-1].currentImage.get_rect().width - gap2) or self.y > (vehicles[dir][self.lane][self.index-1].y + gap2):
#                             self.x += self.speed
#             else:
#                 if (self.y >= self.stop or self.crossed == 1 or is_green) and \
#                    (self.index == 0 or self.y > (vehicles[dir][self.lane][self.index-1].y + vehicles[dir][self.lane][self.index-1].currentImage.get_rect().height + gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
#                     self.y -= self.speed

# def count_waiting_ambulances(dir_num):
#     count = 0
#     direction = directionNumbers[dir_num]
#     for lane in range(3):
#         for v in vehicles[direction][lane]:
#             if v.crossed == 0 and v.vehicleClass == 'ambulance':
#                 count += 1
#     return count

# def count_waiting_vehicles(dir_num):
#     count = 0
#     direction = directionNumbers[dir_num]
#     for lane in range(3):
#         for v in vehicles[direction][lane]:
#             if v.crossed == 0:
#                 count += 1
#     return count

# # Initialization
# def initialize():
#     minGreen = defaultGreen + defaultYellow
#     ts1 = TrafficSignal(defaultRed - minGreen * 0, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
#     signals.append(ts1)
#     ts2 = TrafficSignal(ts1.red + minGreen, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
#     signals.append(ts2)
#     ts3 = TrafficSignal(ts2.red + minGreen, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
#     signals.append(ts3)
#     ts4 = TrafficSignal(ts3.red + minGreen, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
#     signals.append(ts4)
#     print("→ Signals initialized")
#     repeat()

# # Adaptive timing calculation
# def setTime():
#     global emergencyActive
#     if emergencyActive:
#         print("  (Emergency active → skipping normal adaptive timing)")
#         return

#     print(f"→ Calculating green time for next direction: {directionNumbers[nextGreen]}")

#     noOfCars = noOfBikes = noOfBuses = noOfTrucks = noOfRickshaws = noOfAmbulances = 0

#     dir_name = directionNumbers[nextGreen]

#     for lane in range(3):
#         for v in vehicles[dir_name][lane]:
#             if v.crossed == 0:
#                 vc = v.vehicleClass
#                 if vc == 'car':
#                     noOfCars += 1
#                 elif vc == 'bus':
#                     noOfBuses += 1
#                 elif vc == 'truck':
#                     noOfTrucks += 1
#                 elif vc == 'rickshaw':
#                     noOfRickshaws += 1
#                 elif vc == 'bike':
#                     noOfBikes += 1
#                 elif vc == 'ambulance':
#                     noOfAmbulances += 1

#     total_time = (noOfCars * carTime + noOfRickshaws * rickshawTime + noOfBuses * busTime + noOfTrucks * truckTime + noOfBikes * bikeTime + noOfAmbulances * ambulanceTime)
#     greenTime = math.ceil(total_time / 3)  # Divide by number of lanes (3)
#     greenTime = max(defaultMinimum, min(defaultMaximum, greenTime))
#     signals[nextGreen].green = greenTime
#     print(f"  → Assigned green time = {greenTime} seconds  (vehicles: C:{noOfCars} Bk:{noOfBikes} Bs:{noOfBuses} T:{noOfTrucks} R:{noOfRickshaws} Amb:{noOfAmbulances})")

# def repeat():
#     global currentGreen, currentYellow, nextGreen, emergencyActive, emergencyDirection

#     while True:
#         # Check for pending emergencies in other directions even during normal operation
#         for i in range(noOfSignals):
#             if i != currentGreen and count_waiting_ambulances(i) > 0 and not emergencyActive:
#                 print(f"!!! EMERGENCY DETECTED in direction {directionNumbers[i].upper()} during normal operation !!!")
#                 emergencyActive = True
#                 emergencyDirection = i
#                 break

#         if emergencyActive:
#             print("\n" + "="*60)
#             print("          EMERGENCY VEHICLE PRIORITY MODE ACTIVATED")
#             print("="*60)
#             print(f"Direction getting priority: {directionNumbers[emergencyDirection].upper()}")

#             previousGreen = currentGreen
#             currentGreen = emergencyDirection
#             currentYellow = 0
#             nextGreen = (currentGreen + 1) % noOfSignals

#             for i in range(noOfSignals):
#                 if i != currentGreen:
#                     signals[i].red = 300  # large value to prevent quick cycle
#                     signals[i].green = 0
#                     signals[i].yellow = 0

#             num_amb = count_waiting_ambulances(emergencyDirection)
#             initial_green = max(20, num_amb * 10)
#             signals[currentGreen].green = initial_green
#             signals[currentGreen].yellow = defaultYellow
#             print(f"→ Setting emergency green to {initial_green}s for {num_amb} ambulances")

#             while signals[currentGreen].green > 0 or count_waiting_ambulances(emergencyDirection) > 0:
#                 if signals[currentGreen].green <= 0 and count_waiting_ambulances(emergencyDirection) > 0:
#                     num_amb_remaining = count_waiting_ambulances(emergencyDirection)
#                     extension = max(10, num_amb_remaining * 10)
#                     signals[currentGreen].green += extension
#                     print(f"→ Extending emergency green by {extension}s for {num_amb_remaining} remaining ambulances")

#                 printStatus()
#                 updateValues()
#                 time.sleep(1)

#             currentYellow = 1
#             while signals[currentGreen].yellow > 0:
#                 printStatus()
#                 updateValues()
#                 time.sleep(1)

#             currentYellow = 0
#             print("\n→ Emergency cleared. Returning to normal adaptive control.")
#             emergencyActive = False

#             for i in range(noOfSignals):
#                 signals[i].green = defaultGreen
#                 signals[i].yellow = defaultYellow
#                 signals[i].red = defaultRed

#             currentGreen = previousGreen
#             nextGreen = (currentGreen + 1) % noOfSignals
#             continue

#         print(f"\n→ Green for {directionNumbers[currentGreen]}")
#         while signals[currentGreen].green > 0:
#             printStatus()
#             updateValues()

#             if signals[nextGreen].red == detectionTime:
#                 thread = threading.Thread(target=setTime)
#                 thread.daemon = True
#                 thread.start()

#             time.sleep(1)

#         currentYellow = 1
#         print(f"→ Yellow for {directionNumbers[currentGreen]}")
#         while signals[currentGreen].yellow > 0:
#             printStatus()
#             updateValues()
#             time.sleep(1)

#         currentYellow = 0

#         signals[currentGreen].green = defaultGreen
#         signals[currentGreen].yellow = defaultYellow

#         currentGreen = nextGreen
#         nextGreen = (currentGreen + 1) % noOfSignals

# # Print the signal timers on cmd
# def printStatus():
#     for i in range(0, noOfSignals):
#         if(i==currentGreen):
#             if(currentYellow==0):
#                 print(" GREEN TS",i+1,"-> r:",signals[i].red," y:",signals[i].yellow," g:",signals[i].green)
#             else:
#                 print("YELLOW TS",i+1,"-> r:",signals[i].red," y:",signals[i].yellow," g:",signals[i].green)
#         else:
#             print(" RED TS",i+1,"-> r:",signals[i].red," y:",signals[i].yellow," g:",signals[i].green)
#     print()

# # Update values of the signal timers after every second
# def updateValues():
#     for i in range(0, noOfSignals):
#         if(i==currentGreen):
#             if(currentYellow==0):
#                 if signals[i].green > 0:
#                     signals[i].green -=1
#                 signals[i].totalGreenTime +=1
#             else:
#                 if signals[i].yellow > 0:
#                     signals[i].yellow -=1
#         else:
#             if signals[i].red > 0:
#                 signals[i].red -=1

# def generateVehicles():
#     while(True):
#         rand = random.randint(0,99)
#         if rand < 2:
#             vehicle_type = 5 # ambulance
#         else:
#             vehicle_type = random.randint(0,4) # normal vehicles
#         if(vehicle_type==4):
#             lane_number = 0
#         else:
#             lane_number = random.randint(0,1) + 1
#         will_turn = 0
#         if(lane_number==2):
#             temp = random.randint(0,4)
#             if(temp<=2):
#                 will_turn = 1
#             elif(temp>2):
#                 will_turn = 0
#         direction_number = random.randint(0,3)
      
#         Vehicle(lane_number, vehicleTypes[vehicle_type], direction_number, directionNumbers[direction_number], will_turn)
#         time.sleep(2)

# def simulationTime():
#     global timeElapsed, simTime
#     while(True):
#         timeElapsed += 1
#         time.sleep(1)
#         if(timeElapsed==simTime):
#             totalVehicles = 0
#             print('Lane-wise Vehicle Counts')
#             for i in range(noOfSignals):
#                 print('Lane',i+1,':',vehicles[directionNumbers[i]]['crossed'])
#                 totalVehicles += vehicles[directionNumbers[i]]['crossed']
#             print('Total vehicles passed: ',totalVehicles)
#             print('Total time passed: ',timeElapsed)
#             print('No. of vehicles passed per unit time: ',(float(totalVehicles)/float(timeElapsed)))
#             os._exit(1)
   
# class Main:
#     thread4 = threading.Thread(name="simulationTime",target=simulationTime, args=())
#     thread4.daemon = True
#     thread4.start()
#     thread2 = threading.Thread(name="initialization",target=initialize, args=()) # initialization
#     thread2.daemon = True
#     thread2.start()
#     # Colours
#     black = (0, 0, 0)
#     white = (255, 255, 255)
#     # Screensize
#     screenWidth = 1400
#     screenHeight = 800
#     screenSize = (screenWidth, screenHeight)
#     # Setting background image i.e. image of intersection
#     background = pygame.image.load(os.path.join(BASE_DIR, 'images', 'mod_int.png'))
#     screen = pygame.display.set_mode(screenSize)
#     pygame.display.set_caption("SIMULATION")
#     # Loading signal images and font
#     redSignal = pygame.image.load(os.path.join(BASE_DIR, 'images', 'signals', 'red.png'))
#     yellowSignal = pygame.image.load(os.path.join(BASE_DIR, 'images', 'signals', 'yellow.png'))
#     greenSignal = pygame.image.load(os.path.join(BASE_DIR, 'images', 'signals', 'green.png'))
#     font = pygame.font.Font(None, 30)
#     thread3 = threading.Thread(name="generateVehicles",target=generateVehicles, args=()) # Generating vehicles
#     thread3.daemon = True
#     thread3.start()
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 sys.exit()
#         screen.blit(background,(0,0)) # display background in simulation
#         for i in range(0,noOfSignals): # display signal and set timer according to current status: green, yello, or red
#             if(i==currentGreen):
#                 if(currentYellow==1):
#                     if(signals[i].yellow==0):
#                         signals[i].signalText = "STOP"
#                     else:
#                         signals[i].signalText = signals[i].yellow
#                     screen.blit(yellowSignal, signalCoods[i])
#                 else:
#                     if(signals[i].green==0):
#                         signals[i].signalText = "SLOW"
#                     else:
#                         signals[i].signalText = signals[i].green
#                     screen.blit(greenSignal, signalCoods[i])
#             else:
#                 if(signals[i].red<=10):
#                     if(signals[i].red==0):
#                         signals[i].signalText = "GO"
#                     else:
#                         signals[i].signalText = signals[i].red
#                 else:
#                     signals[i].signalText = "---"
#                 screen.blit(redSignal, signalCoods[i])
#         signalTexts = ["","","",""]
#         # display signal timer and vehicle count
#         for i in range(0,noOfSignals):
#             signalTexts[i] = font.render(str(signals[i].signalText), True, white, black)
#             screen.blit(signalTexts[i],signalTimerCoods[i])
#             displayText = vehicles[directionNumbers[i]]['crossed']
#             vehicleCountTexts = font.render("Crossed: "+str(displayText), True, black, white)
#             screen.blit(vehicleCountTexts,vehicleCountCoods[i])
#             waiting = count_waiting_vehicles(i)
#             waitingText = font.render("Waiting: "+str(waiting), True, black, white)
#             screen.blit(waitingText, waitingCountCoods[i])
#         timeElapsedText = font.render(("Time Elapsed: "+str(timeElapsed)), True, black, white)
#         screen.blit(timeElapsedText,(1100,50))
#         # Mode text
#         if not emergencyActive:
#             modeText = font.render("Mode: Normal Adaptive Control", True, black, white)
#             screen.blit(modeText, (1100, 80))
#         # 🚑 Draw Emergency Banner
#         if emergencyActive:
#             emergencyFont = pygame.font.Font(None, 60)
#             emergencyText = emergencyFont.render(
#                 "🚑 EMERGENCY VEHICLE - " + directionNumbers[emergencyDirection].upper(),
#                 True,
#                 (255, 0, 0),
#                 (255, 255, 255)
#                 )
#             text_rect = emergencyText.get_rect(center=(700, 40))
#             screen.blit(emergencyText, text_rect)
#             ambWaiting = count_waiting_ambulances(emergencyDirection)
#             ambText = font.render(f"Ambulances Waiting: {ambWaiting}", True, (255, 0, 0), white)
#             amb_rect = ambText.get_rect(center=(700, 100))
#             screen.blit(ambText, amb_rect)
#         # display the vehicles
#         for vehicle in simulation:
#             screen.blit(vehicle.currentImage, [vehicle.x, vehicle.y])
#             vehicle.move()
#         to_remove = []
#         for vehicle in simulation:
#             if vehicle.direction == 'right' and vehicle.x > 1400 + 100:
#                 to_remove.append(vehicle)
#             elif vehicle.direction == 'down' and vehicle.y > 800 + 100:
#                 to_remove.append(vehicle)
#             elif vehicle.direction == 'left' and vehicle.x < -100:
#                 to_remove.append(vehicle)
#             elif vehicle.direction == 'up' and vehicle.y < -100:
#                 to_remove.append(vehicle)
#         for vehicle in to_remove:
#             simulation.remove(vehicle)
#             vehicles[vehicle.direction][vehicle.lane].remove(vehicle)
#         for dir_num in range(4):
#             direction = directionNumbers[dir_num]
#             for lane in range(3):
#                 for i in range(len(vehicles[direction][lane])):
#                     vehicles[direction][lane][i].index = i
#         pygame.display.update()

# Main()

# LAG
# NO. OF VEHICLES IN SIGNAL CLASS
# stops not used
# DISTRIBUTION
# BUS TOUCHING ON TURNS
# Distribution using python class
# *** IMAGE XY COOD IS TOP LEFT





# ========================================================================================
# import random
# import math
# import time
# import threading
# import pygame
# import sys
# import os

# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# # Default signal timings
# defaultRed = 120
# defaultYellow = 5
# defaultGreen = 25
# defaultMinimum = 12
# defaultMaximum = 55

# signals = []
# noOfSignals = 4
# simTime = 600                      # simulation duration in seconds
# timeElapsed = 0
# currentGreen = 0
# nextGreen = (currentGreen + 1) % noOfSignals
# currentYellow = 0

# # Emergency control
# emergencyActive = False
# emergencyDirection = None

# # Average time per vehicle type to cross (seconds)
# carTime     = 1.8
# bikeTime    = 1.0
# rickshawTime= 1.5
# busTime     = 3.2
# truckTime   = 3.5
# ambulanceTime = 1.2

# noOfLanes = 2
# detectionTime = 5

# speeds = {
#     'car':       2.4,
#     'bus':       1.9,
#     'truck':     1.8,
#     'rickshaw':  2.1,
#     'bike':      2.7,
#     'ambulance': 3.8
# }

# # Starting coordinates for each direction and lane
# x = {'right': [0, 0, 0],       'down': [755, 727, 697], 'left': [1400,1400,1400], 'up': [602,627,657]}
# y = {'right': [348,370,398],   'down': [0, 0, 0],       'left': [498,466,436],    'up': [800,800,800]}

# vehicles = {
#     'right': {0:[], 1:[], 2:[], 'crossed':0},
#     'down':  {0:[], 1:[], 2:[], 'crossed':0},
#     'left':  {0:[], 1:[], 2:[], 'crossed':0},
#     'up':    {0:[], 1:[], 2:[], 'crossed':0}
# }

# vehicleTypes = {
#     0:'car', 1:'bus', 2:'truck', 3:'rickshaw', 4:'bike', 5:'ambulance'
# }

# directionNumbers = {0:'right', 1:'down', 2:'left', 3:'up'}

# signalCoods       = [(530,230), (810,230), (810,570), (530,570)]
# signalTimerCoods  = [(530,210), (810,210), (810,550), (530,550)]

# stopLines   = {'right': 590, 'down': 330, 'left': 800, 'up': 535}
# defaultStop = {'right': 580, 'down': 320, 'left': 810, 'up': 545}
# stops = {
#     'right': [580,580,580],
#     'down':  [320,320,320],
#     'left':  [810,810,810],
#     'up':    [545,545,545]
# }

# mid = {
#     'right': {'x':705, 'y':445},
#     'down':  {'x':695, 'y':450},
#     'left':  {'x':695, 'y':425},
#     'up':    {'x':695, 'y':400}
# }

# rotationAngle = 3
# gap  = 30     # increased gap between stopped vehicles
# gap2 = 25     # increased moving gap

# pygame.init()
# simulation = pygame.sprite.Group()

# class TrafficSignal:
#     def __init__(self, red, yellow, green, minimum, maximum):
#         self.red = red
#         self.yellow = yellow
#         self.green = green
#         self.minimum = minimum
#         self.maximum = maximum
#         self.signalText = "30"
#         self.totalGreenTime = 0

# class Vehicle(pygame.sprite.Sprite):
#     def __init__(self, lane, vehicleClass, direction_number, direction, will_turn):
#         pygame.sprite.Sprite.__init__(self)
#         self.lane = lane
#         self.vehicleClass = vehicleClass
#         self.speed = speeds[vehicleClass]
#         self.direction_number = direction_number
#         self.direction = direction
#         self.x = x[direction][lane]
#         self.y = y[direction][lane]
#         self.crossed = 0
#         self.willTurn = will_turn
#         self.turned = 0
#         self.rotateAngle = 0

#         vehicles[direction][lane].append(self)
#         self.index = len(vehicles[direction][lane]) - 1

#         path = os.path.join(BASE_DIR, 'images', direction, f'{vehicleClass}.png')
#         self.originalImage = pygame.image.load(path)
#         self.currentImage = pygame.image.load(path)

#         # Set stop position dynamically
#         prev_vehicle = vehicles[direction][lane][self.index-1] if self.index > 0 else None
#         if prev_vehicle and prev_vehicle.crossed == 0:
#             if direction == 'right':
#                 self.stop = prev_vehicle.stop - prev_vehicle.currentImage.get_rect().width - gap
#             elif direction == 'left':
#                 self.stop = prev_vehicle.stop + prev_vehicle.currentImage.get_rect().width + gap
#             elif direction == 'down':
#                 self.stop = prev_vehicle.stop - prev_vehicle.currentImage.get_rect().height - gap
#             elif direction == 'up':
#                 self.stop = prev_vehicle.stop + prev_vehicle.currentImage.get_rect().height + gap
#         else:
#             self.stop = defaultStop[direction]

#         # Adjust start position
#         temp = self.currentImage.get_rect().width if direction in ['right', 'left'] else self.currentImage.get_rect().height
#         temp += gap
#         if direction == 'right':
#             x[direction][lane] -= temp
#             stops[direction][lane] -= temp
#         elif direction == 'left':
#             x[direction][lane] += temp
#             stops[direction][lane] += temp
#         elif direction == 'down':
#             y[direction][lane] -= temp
#             stops[direction][lane] -= temp
#         elif direction == 'up':
#             y[direction][lane] += temp
#             stops[direction][lane] += temp

#         simulation.add(self)

#     def move(self):
#         global emergencyActive, emergencyDirection

#         # Check for emergency trigger
#         if (self.vehicleClass == "ambulance" and self.crossed == 0 and self.direction_number != currentGreen and not emergencyActive):
#             print(f"!!! EMERGENCY DETECTED - Ambulance waiting at RED from {self.direction.upper()} !!!")
#             emergencyActive = True
#             emergencyDirection = self.direction_number

#         dir = self.direction
#         is_green = (currentGreen == self.direction_number and currentYellow == 0)

#         if dir == 'right':
#             vehicle_dim = self.currentImage.get_rect().width
#             mid_x = mid[dir]['x']
#             stop_line = stopLines[dir] + 20

#             if self.crossed == 0 and self.x + vehicle_dim > stop_line:
#                 self.crossed = 1
#                 vehicles[dir]['crossed'] += 1
#                 if self.vehicleClass == "ambulance":
#                     print(f"Ambulance from {dir} has crossed → check if more")

#             if self.willTurn:
#                 if self.crossed == 0 or self.x + vehicle_dim < mid_x:
#                     if (self.x + vehicle_dim <= self.stop or is_green or self.crossed == 1) and \
#                        (self.index == 0 or self.x + vehicle_dim < (vehicles[dir][self.lane][self.index-1].x - gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
#                         self.x += self.speed
#                 else:
#                     if self.turned == 0:
#                         self.rotateAngle += rotationAngle
#                         self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
#                         self.x += 2
#                         self.y += 1.8
#                         if self.rotateAngle == 90:
#                             self.turned = 1
#                     else:
#                         if self.index == 0 or self.y + self.currentImage.get_rect().height < (vehicles[dir][self.lane][self.index-1].y - gap2) or self.x + vehicle_dim < (vehicles[dir][self.lane][self.index-1].x - gap2):
#                             self.y += self.speed
#             else:
#                 if (self.x + vehicle_dim <= self.stop or self.crossed == 1 or is_green) and \
#                    (self.index == 0 or self.x + vehicle_dim < (vehicles[dir][self.lane][self.index-1].x - gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
#                     self.x += self.speed

#         elif dir == 'down':
#             vehicle_dim = self.currentImage.get_rect().height
#             mid_y = mid[dir]['y']
#             stop_line = stopLines[dir]

#             if self.crossed == 0 and self.y + vehicle_dim > stop_line:
#                 self.crossed = 1
#                 vehicles[dir]['crossed'] += 1
#                 if self.vehicleClass == "ambulance":
#                     print(f"Ambulance from {dir} has crossed → check if more")

#             if self.willTurn:
#                 if self.crossed == 0 or self.y + vehicle_dim < mid_y:
#                     if (self.y + vehicle_dim <= self.stop or is_green or self.crossed == 1) and \
#                        (self.index == 0 or self.y + vehicle_dim < (vehicles[dir][self.lane][self.index-1].y - gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
#                         self.y += self.speed
#                 else:
#                     if self.turned == 0:
#                         self.rotateAngle += rotationAngle
#                         self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
#                         self.x -= 2.5
#                         self.y += 2
#                         if self.rotateAngle == 90:
#                             self.turned = 1
#                     else:
#                         if self.index == 0 or self.x > (vehicles[dir][self.lane][self.index-1].x + vehicles[dir][self.lane][self.index-1].currentImage.get_rect().width + gap2) or self.y < (vehicles[dir][self.lane][self.index-1].y - gap2):
#                             self.x -= self.speed
#             else:
#                 if (self.y + vehicle_dim <= self.stop or self.crossed == 1 or is_green) and \
#                    (self.index == 0 or self.y + vehicle_dim < (vehicles[dir][self.lane][self.index-1].y - gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
#                     self.y += self.speed

#         elif dir == 'left':
#             vehicle_dim = self.currentImage.get_rect().width
#             mid_x = mid[dir]['x']
#             stop_line = stopLines[dir]

#             if self.crossed == 0 and self.x < stop_line:
#                 self.crossed = 1
#                 vehicles[dir]['crossed'] += 1
#                 if self.vehicleClass == "ambulance":
#                     print(f"Ambulance from {dir} has crossed → check if more")

#             if self.willTurn:
#                 if self.crossed == 0 or self.x > mid_x:
#                     if (self.x >= self.stop or is_green or self.crossed == 1) and \
#                        (self.index == 0 or self.x > (vehicles[dir][self.lane][self.index-1].x + vehicles[dir][self.lane][self.index-1].currentImage.get_rect().width + gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
#                         self.x -= self.speed
#                 else:
#                     if self.turned == 0:
#                         self.rotateAngle += rotationAngle
#                         self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
#                         self.x -= 1.8
#                         self.y -= 2.5
#                         if self.rotateAngle == 90:
#                             self.turned = 1
#                     else:
#                         if self.index == 0 or self.y > (vehicles[dir][self.lane][self.index-1].y + vehicles[dir][self.lane][self.index-1].currentImage.get_rect().height + gap2) or self.x > (vehicles[dir][self.lane][self.index-1].x + gap2):
#                             self.y -= self.speed
#             else:
#                 if (self.x >= self.stop or self.crossed == 1 or is_green) and \
#                    (self.index == 0 or self.x > (vehicles[dir][self.lane][self.index-1].x + vehicles[dir][self.lane][self.index-1].currentImage.get_rect().width + gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
#                     self.x -= self.speed

#         elif dir == 'up':
#             vehicle_dim = self.currentImage.get_rect().height
#             mid_y = mid[dir]['y']
#             stop_line = stopLines[dir]

#             if self.crossed == 0 and self.y < stop_line:
#                 self.crossed = 1
#                 vehicles[dir]['crossed'] += 1
#                 if self.vehicleClass == "ambulance":
#                     print(f"Ambulance from {dir} has crossed → check if more")

#             if self.willTurn:
#                 if self.crossed == 0 or self.y > mid_y:
#                     if (self.y >= self.stop or is_green or self.crossed == 1) and \
#                        (self.index == 0 or self.y > (vehicles[dir][self.lane][self.index-1].y + vehicles[dir][self.lane][self.index-1].currentImage.get_rect().height + gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
#                         self.y -= self.speed
#                 else:
#                     if self.turned == 0:
#                         self.rotateAngle += rotationAngle
#                         self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
#                         self.x += 1
#                         self.y -= 1
#                         if self.rotateAngle == 90:
#                             self.turned = 1
#                     else:
#                         if self.index == 0 or self.x < (vehicles[dir][self.lane][self.index-1].x - vehicles[dir][self.lane][self.index-1].currentImage.get_rect().width - gap2) or self.y > (vehicles[dir][self.lane][self.index-1].y + gap2):
#                             self.x += self.speed
#             else:
#                 if (self.y >= self.stop or self.crossed == 1 or is_green) and \
#                    (self.index == 0 or self.y > (vehicles[dir][self.lane][self.index-1].y + vehicles[dir][self.lane][self.index-1].currentImage.get_rect().height + gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
#                     self.y -= self.speed

# def count_waiting_ambulances(dir_num):
#     count = 0
#     direction = directionNumbers[dir_num]
#     for lane in range(3):
#         for v in vehicles[direction][lane]:
#             if v.crossed == 0 and v.vehicleClass == 'ambulance':
#                 count += 1
#     return count

# def count_waiting_vehicles(dir_num):
#     count = 0
#     direction = directionNumbers[dir_num]
#     for lane in range(3):
#         for v in vehicles[direction][lane]:
#             if v.crossed == 0:
#                 count += 1
#     return count

# # Initialization
# def initialize():
#     minGreen = defaultGreen + defaultYellow
#     ts1 = TrafficSignal(defaultRed - minGreen * 0, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
#     signals.append(ts1)
#     ts2 = TrafficSignal(ts1.red + minGreen, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
#     signals.append(ts2)
#     ts3 = TrafficSignal(ts2.red + minGreen, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
#     signals.append(ts3)
#     ts4 = TrafficSignal(ts3.red + minGreen, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
#     signals.append(ts4)
#     print("→ Signals initialized")
#     repeat()

# # Adaptive timing calculation
# def setTime():
#     global emergencyActive
#     if emergencyActive:
#         print("  (Emergency active → skipping normal adaptive timing)")
#         return

#     print(f"→ Calculating green time for next direction: {directionNumbers[nextGreen]}")

#     noOfCars = noOfBikes = noOfBuses = noOfTrucks = noOfRickshaws = noOfAmbulances = 0

#     dir_name = directionNumbers[nextGreen]

#     for lane in range(3):
#         for v in vehicles[dir_name][lane]:
#             if v.crossed == 0:
#                 vc = v.vehicleClass
#                 if vc == 'car':
#                     noOfCars += 1
#                 elif vc == 'bus':
#                     noOfBuses += 1
#                 elif vc == 'truck':
#                     noOfTrucks += 1
#                 elif vc == 'rickshaw':
#                     noOfRickshaws += 1
#                 elif vc == 'bike':
#                     noOfBikes += 1
#                 elif vc == 'ambulance':
#                     noOfAmbulances += 1

#     total_time = (noOfCars * carTime + noOfRickshaws * rickshawTime + noOfBuses * busTime + noOfTrucks * truckTime + noOfBikes * bikeTime + noOfAmbulances * ambulanceTime)
#     greenTime = math.ceil(total_time / 3)  # Divide by number of lanes (3)
#     greenTime = max(defaultMinimum, min(defaultMaximum, greenTime))
#     signals[nextGreen].green = greenTime
#     print(f"  → Assigned green time = {greenTime} seconds  (vehicles: C:{noOfCars} Bk:{noOfBikes} Bs:{noOfBuses} T:{noOfTrucks} R:{noOfRickshaws} Amb:{noOfAmbulances})")

# def repeat():
#     global currentGreen, currentYellow, nextGreen, emergencyActive, emergencyDirection

#     while True:
#         # Check for pending emergencies in other directions even during normal operation
#         for i in range(noOfSignals):
#             if i != currentGreen and count_waiting_ambulances(i) > 0 and not emergencyActive:
#                 print(f"!!! EMERGENCY DETECTED in direction {directionNumbers[i].upper()} during normal operation !!!")
#                 emergencyActive = True
#                 emergencyDirection = i
#                 break

#         if emergencyActive:
#             print("\n" + "="*60)
#             print("          EMERGENCY VEHICLE PRIORITY MODE ACTIVATED")
#             print("="*60)
#             print(f"Direction getting priority: {directionNumbers[emergencyDirection].upper()}")

#             previousGreen = currentGreen
#             currentGreen = emergencyDirection
#             currentYellow = 0
#             nextGreen = (currentGreen + 1) % noOfSignals

#             for i in range(noOfSignals):
#                 if i != currentGreen:
#                     signals[i].red = 300  # large value to prevent quick cycle
#                     signals[i].green = 0
#                     signals[i].yellow = 0

#             num_amb = count_waiting_ambulances(emergencyDirection)
#             initial_green = max(20, num_amb * 10)
#             signals[currentGreen].green = initial_green
#             signals[currentGreen].yellow = defaultYellow
#             print(f"→ Setting emergency green to {initial_green}s for {num_amb} ambulances")

#             while signals[currentGreen].green > 0 or count_waiting_ambulances(emergencyDirection) > 0:
#                 if signals[currentGreen].green <= 0 and count_waiting_ambulances(emergencyDirection) > 0:
#                     num_amb_remaining = count_waiting_ambulances(emergencyDirection)
#                     extension = max(10, num_amb_remaining * 10)
#                     signals[currentGreen].green += extension
#                     print(f"→ Extending emergency green by {extension}s for {num_amb_remaining} remaining ambulances")

#                 printStatus()
#                 updateValues()
#                 time.sleep(1)

#             currentYellow = 1
#             while signals[currentGreen].yellow > 0:
#                 printStatus()
#                 updateValues()
#                 time.sleep(1)

#             currentYellow = 0
#             print("\n→ Emergency cleared. Returning to normal adaptive control.")
#             emergencyActive = False

#             for i in range(noOfSignals):
#                 signals[i].green = defaultGreen
#                 signals[i].yellow = defaultYellow
#                 signals[i].red = defaultRed

#             currentGreen = previousGreen
#             nextGreen = (currentGreen + 1) % noOfSignals
#             continue

#         print(f"\n→ Green for {directionNumbers[currentGreen]}")
#         while signals[currentGreen].green > 0:
#             printStatus()
#             updateValues()

#             if signals[nextGreen].red == detectionTime:
#                 thread = threading.Thread(target=setTime)
#                 thread.daemon = True
#                 thread.start()

#             time.sleep(1)

#         currentYellow = 1
#         print(f"→ Yellow for {directionNumbers[currentGreen]}")
#         while signals[currentGreen].yellow > 0:
#             printStatus()
#             updateValues()
#             time.sleep(1)

#         currentYellow = 0

#         signals[currentGreen].green = defaultGreen
#         signals[currentGreen].yellow = defaultYellow

#         currentGreen = nextGreen
#         nextGreen = (currentGreen + 1) % noOfSignals

# # Print the signal timers on cmd
# def printStatus():
#     for i in range(0, noOfSignals):
#         if(i==currentGreen):
#             if(currentYellow==0):
#                 print(" GREEN TS",i+1,"-> r:",signals[i].red," y:",signals[i].yellow," g:",signals[i].green)
#             else:
#                 print("YELLOW TS",i+1,"-> r:",signals[i].red," y:",signals[i].yellow," g:",signals[i].green)
#         else:
#             print(" RED TS",i+1,"-> r:",signals[i].red," y:",signals[i].yellow," g:",signals[i].green)
#     print()

# # Update values of the signal timers after every second
# def updateValues():
#     for i in range(0, noOfSignals):
#         if(i==currentGreen):
#             if(currentYellow==0):
#                 if signals[i].green > 0:
#                     signals[i].green -=1
#                 signals[i].totalGreenTime +=1
#             else:
#                 if signals[i].yellow > 0:
#                     signals[i].yellow -=1
#         else:
#             if signals[i].red > 0:
#                 signals[i].red -=1

# def generateVehicles():
#     global currentGreen, noOfSignals
#     while(True):
#         rand = random.randint(0,99)
#         if rand < 2:
#             vehicle_type = 5 # ambulance
#         else:
#             vehicle_type = random.randint(0,4) # normal vehicles
#         if(vehicle_type==4):
#             lane_number = 0
#         else:
#             lane_number = random.randint(0,1) + 1
#         will_turn = 0
#         if(lane_number==2):
#             temp = random.randint(0,4)
#             if(temp<=2):
#                 will_turn = 1
#             elif(temp>2):
#                 will_turn = 0
#         if vehicle_type == 5:
#             # For ambulance, choose current green or the previous direction (e.g., up when right is green)
#             direction_number = random.choice([currentGreen, (currentGreen - 1) % noOfSignals])
#         else:
#             direction_number = random.randint(0,3)
      
#         Vehicle(lane_number, vehicleTypes[vehicle_type], direction_number, directionNumbers[direction_number], will_turn)
#         time.sleep(2)

# def simulationTime():
#     global timeElapsed, simTime
#     while(True):
#         timeElapsed += 1
#         time.sleep(1)
#         if(timeElapsed==simTime):
#             totalVehicles = 0
#             print('Lane-wise Vehicle Counts')
#             for i in range(noOfSignals):
#                 print('Lane',i+1,':',vehicles[directionNumbers[i]]['crossed'])
#                 totalVehicles += vehicles[directionNumbers[i]]['crossed']
#             print('Total vehicles passed: ',totalVehicles)
#             print('Total time passed: ',timeElapsed)
#             print('No. of vehicles passed per unit time: ',(float(totalVehicles)/float(timeElapsed)))
#             os._exit(1)
   
# class Main:
#     thread4 = threading.Thread(name="simulationTime",target=simulationTime, args=())
#     thread4.daemon = True
#     thread4.start()
#     thread2 = threading.Thread(name="initialization",target=initialize, args=()) # initialization
#     thread2.daemon = True
#     thread2.start()
#     # Colours
#     black = (0, 0, 0)
#     white = (255, 255, 255)
#     # Screensize
#     screenWidth = 1400
#     screenHeight = 800
#     screenSize = (screenWidth, screenHeight)
#     # Setting background image i.e. image of intersection
#     background = pygame.image.load(os.path.join(BASE_DIR, 'images', 'mod_int.png'))
#     screen = pygame.display.set_mode(screenSize)
#     pygame.display.set_caption("SIMULATION")
#     # Loading signal images and font
#     redSignal = pygame.image.load(os.path.join(BASE_DIR, 'images', 'signals', 'red.png'))
#     yellowSignal = pygame.image.load(os.path.join(BASE_DIR, 'images', 'signals', 'yellow.png'))
#     greenSignal = pygame.image.load(os.path.join(BASE_DIR, 'images', 'signals', 'green.png'))
#     font = pygame.font.Font(None, 30)
#     emergencyFont = pygame.font.Font(None, 40)
#     thread3 = threading.Thread(name="generateVehicles",target=generateVehicles, args=()) # Generating vehicles
#     thread3.daemon = True
#     thread3.start()
#     while True:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 sys.exit()
#         screen.blit(background,(0,0)) # display background in simulation
#         for i in range(0,noOfSignals): # display signal and set timer according to current status: green, yello, or red
#             if(i==currentGreen):
#                 if(currentYellow==1):
#                     if(signals[i].yellow==0):
#                         signals[i].signalText = "STOP"
#                     else:
#                         signals[i].signalText = signals[i].yellow
#                     screen.blit(yellowSignal, signalCoods[i])
#                 else:
#                     if(signals[i].green==0):
#                         signals[i].signalText = "SLOW"
#                     else:
#                         signals[i].signalText = signals[i].green
#                     screen.blit(greenSignal, signalCoods[i])
#             else:
#                 if(signals[i].red<=10):
#                     if(signals[i].red==0):
#                         signals[i].signalText = "GO"
#                     else:
#                         signals[i].signalText = signals[i].red
#                 else:
#                     signals[i].signalText = "---"
#                 screen.blit(redSignal, signalCoods[i])
#         signalTexts = ["","","",""]
#         # display signal timer
#         for i in range(0,noOfSignals):
#             signalTexts[i] = font.render(str(signals[i].signalText), True, white, black)
#             screen.blit(signalTexts[i],signalTimerCoods[i])
#         timeElapsedText = font.render(("Time Elapsed: "+str(timeElapsed)), True, black, white)
#         screen.blit(timeElapsedText,(1100,50))
#         # 🚑 Draw Emergency Banners
#         if emergencyActive:
#             # Banner 1
#             emergencyText1 = emergencyFont.render(
#                 "🚑 EMERGENCY VEHICLE DETECTED!",
#                 True,
#                 (255, 0, 0),
#                 (255, 255, 255)
#                 )
#             text_rect1 = emergencyText1.get_rect(center=(700, 40))
#             screen.blit(emergencyText1, text_rect1)
#             # Banner 2
#             emergencyText2 = emergencyFont.render(
#                 "PRIORITY MODE ACTIVATED FOR " + directionNumbers[emergencyDirection].upper(),
#                 True,
#                 (255, 0, 0),
#                 (255, 255, 255)
#                 )
#             text_rect2 = emergencyText2.get_rect(center=(700, 80))
#             screen.blit(emergencyText2, text_rect2)
#             # Banner 3
#             ambWaiting = count_waiting_ambulances(emergencyDirection)
#             emergencyText3 = emergencyFont.render(
#                 f"AMBULANCES IN QUEUE: {ambWaiting}",
#                 True,
#                 (255, 0, 0),
#                 (255, 255, 255)
#                 )
#             text_rect3 = emergencyText3.get_rect(center=(700, 120))
#             screen.blit(emergencyText3, text_rect3)
#         # display the vehicles
#         for vehicle in simulation:
#             screen.blit(vehicle.currentImage, [vehicle.x, vehicle.y])
#             vehicle.move()
#         to_remove = []
#         for vehicle in simulation:
#             if vehicle.direction == 'right' and vehicle.x > 1400 + 100:
#                 to_remove.append(vehicle)
#             elif vehicle.direction == 'down' and vehicle.y > 800 + 100:
#                 to_remove.append(vehicle)
#             elif vehicle.direction == 'left' and vehicle.x < -100:
#                 to_remove.append(vehicle)
#             elif vehicle.direction == 'up' and vehicle.y < -100:
#                 to_remove.append(vehicle)
#         for vehicle in to_remove:
#             simulation.remove(vehicle)
#             vehicles[vehicle.direction][vehicle.lane].remove(vehicle)
#         for dir_num in range(4):
#             direction = directionNumbers[dir_num]
#             for lane in range(3):
#                 for i in range(len(vehicles[direction][lane])):
#                     vehicles[direction][lane][i].index = i
#         pygame.display.update()

# Main()




import random
import math
import time
import threading
import pygame
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Default signal timings
defaultRed = 120
defaultYellow = 5
defaultGreen = 25
defaultMinimum = 12
defaultMaximum = 55

signals = []
noOfSignals = 4
simTime = 600                      # simulation duration in seconds
timeElapsed = 0
currentGreen = 0
nextGreen = (currentGreen + 1) % noOfSignals
currentYellow = 0

# Emergency control
emergencyActive = False
emergencyDirection = None

# Warm-up phase control (to prevent too many ambulances at start)
simulation_warmup_seconds = 90     # ambulances very rare in first 90 seconds
ambulance_base_probability = 0.06   # 2%
ambulance_warmup_probability = 0.002  # 0.2% during warmup

# Average time per vehicle type to cross (seconds)
carTime     = 1.8
bikeTime    = 1.0
rickshawTime= 1.5
busTime     = 3.2
truckTime   = 3.5
ambulanceTime = 1.2

noOfLanes = 2
detectionTime = 5

speeds = {
    'car':       2.4,
    'bus':       1.9,
    'truck':     1.8,
    'rickshaw':  2.1,
    'bike':      2.7,
    'ambulance': 3.8
}

# Starting coordinates for each direction and lane
x = {'right': [0, 0, 0],       'down': [755, 727, 697], 'left': [1400,1400,1400], 'up': [602,627,657]}
y = {'right': [348,370,398],   'down': [0, 0, 0],       'left': [498,466,436],    'up': [800,800,800]}

vehicles = {
    'right': {0:[], 1:[], 2:[], 'crossed':0},
    'down':  {0:[], 1:[], 2:[], 'crossed':0},
    'left':  {0:[], 1:[], 2:[], 'crossed':0},
    'up':    {0:[], 1:[], 2:[], 'crossed':0}
}

vehicleTypes = {
    0:'car', 1:'bus', 2:'truck', 3:'rickshaw', 4:'bike', 5:'ambulance'
}

directionNumbers = {0:'right', 1:'down', 2:'left', 3:'up'}

signalCoods       = [(530,230), (810,230), (810,570), (530,570)]
signalTimerCoods  = [(530,210), (810,210), (810,550), (530,550)]

stopLines   = {'right': 590, 'down': 330, 'left': 800, 'up': 535}
defaultStop = {'right': 580, 'down': 320, 'left': 810, 'up': 545}
stops = {
    'right': [580,580,580],
    'down':  [320,320,320],
    'left':  [810,810,810],
    'up':    [545,545,545]
}

mid = {
    'right': {'x':705, 'y':445},
    'down':  {'x':695, 'y':450},
    'left':  {'x':695, 'y':425},
    'up':    {'x':695, 'y':400}
}

rotationAngle = 3
gap  = 30     # increased gap between stopped vehicles
gap2 = 25     # increased moving gap

pygame.init()
simulation = pygame.sprite.Group()

class TrafficSignal:
    def __init__(self, red, yellow, green, minimum, maximum):
        self.red = red
        self.yellow = yellow
        self.green = green
        self.minimum = minimum
        self.maximum = maximum
        self.signalText = "30"
        self.totalGreenTime = 0

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
        self.alerted = False

        vehicles[direction][lane].append(self)
        self.index = len(vehicles[direction][lane]) - 1

        path = os.path.join(BASE_DIR, 'images', direction, f'{vehicleClass}.png')
        self.originalImage = pygame.image.load(path)
        self.currentImage = pygame.image.load(path)

        # Set stop position dynamically
        prev_vehicle = vehicles[direction][lane][self.index-1] if self.index > 0 else None
        if prev_vehicle and prev_vehicle.crossed == 0:
            if direction == 'right':
                self.stop = prev_vehicle.stop - prev_vehicle.currentImage.get_rect().width - gap
            elif direction == 'left':
                self.stop = prev_vehicle.stop + prev_vehicle.currentImage.get_rect().width + gap
            elif direction == 'down':
                self.stop = prev_vehicle.stop - prev_vehicle.currentImage.get_rect().height - gap
            elif direction == 'up':
                self.stop = prev_vehicle.stop + prev_vehicle.currentImage.get_rect().height + gap
        else:
            self.stop = defaultStop[direction]

        # Adjust start position
        temp = self.currentImage.get_rect().width if direction in ['right', 'left'] else self.currentImage.get_rect().height
        temp += gap
        if direction == 'right':
            x[direction][lane] -= temp
            stops[direction][lane] -= temp
        elif direction == 'left':
            x[direction][lane] += temp
            stops[direction][lane] += temp
        elif direction == 'down':
            y[direction][lane] -= temp
            stops[direction][lane] -= temp
        elif direction == 'up':
            y[direction][lane] += temp
            stops[direction][lane] += temp

        simulation.add(self)

    def move(self):
        global emergencyActive, emergencyDirection

        # Check for emergency trigger
        if (self.vehicleClass == "ambulance" and self.crossed == 0 and self.direction_number != currentGreen):
            if not self.alerted:
                print(f"!!! EMERGENCY DETECTED - Ambulance waiting at RED from {self.direction.upper()} !!!")
                self.alerted = True
            if not emergencyActive:
                emergencyActive = True
                emergencyDirection = self.direction_number

        dir = self.direction
        is_green = (currentGreen == self.direction_number and currentYellow == 0)

        if dir == 'right':
            vehicle_dim = self.currentImage.get_rect().width
            mid_x = mid[dir]['x']
            stop_line = stopLines[dir] + 20

            if self.crossed == 0 and self.x + vehicle_dim > stop_line:
                self.crossed = 1
                vehicles[dir]['crossed'] += 1
                if self.vehicleClass == "ambulance":
                    print(f"Ambulance from {dir} has crossed → check if more")

            if self.willTurn:
                if self.crossed == 0 or self.x + vehicle_dim < mid_x:
                    if (self.x + vehicle_dim <= self.stop or is_green or self.crossed == 1) and \
                       (self.index == 0 or self.x + vehicle_dim < (vehicles[dir][self.lane][self.index-1].x - gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
                        self.x += self.speed
                else:
                    if self.turned == 0:
                        self.rotateAngle += rotationAngle
                        self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
                        self.x += 2
                        self.y += 1.8
                        if self.rotateAngle == 90:
                            self.turned = 1
                    else:
                        if self.index == 0 or self.y + self.currentImage.get_rect().height < (vehicles[dir][self.lane][self.index-1].y - gap2) or self.x + vehicle_dim < (vehicles[dir][self.lane][self.index-1].x - gap2):
                            self.y += self.speed
            else:
                if (self.x + vehicle_dim <= self.stop or self.crossed == 1 or is_green) and \
                   (self.index == 0 or self.x + vehicle_dim < (vehicles[dir][self.lane][self.index-1].x - gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
                    self.x += self.speed

        elif dir == 'down':
            vehicle_dim = self.currentImage.get_rect().height
            mid_y = mid[dir]['y']
            stop_line = stopLines[dir]

            if self.crossed == 0 and self.y + vehicle_dim > stop_line:
                self.crossed = 1
                vehicles[dir]['crossed'] += 1
                if self.vehicleClass == "ambulance":
                    print(f"Ambulance from {dir} has crossed → check if more")

            if self.willTurn:
                if self.crossed == 0 or self.y + vehicle_dim < mid_y:
                    if (self.y + vehicle_dim <= self.stop or is_green or self.crossed == 1) and \
                       (self.index == 0 or self.y + vehicle_dim < (vehicles[dir][self.lane][self.index-1].y - gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
                        self.y += self.speed
                else:
                    if self.turned == 0:
                        self.rotateAngle += rotationAngle
                        self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
                        self.x -= 2.5
                        self.y += 2
                        if self.rotateAngle == 90:
                            self.turned = 1
                    else:
                        if self.index == 0 or self.x > (vehicles[dir][self.lane][self.index-1].x + vehicles[dir][self.lane][self.index-1].currentImage.get_rect().width + gap2) or self.y < (vehicles[dir][self.lane][self.index-1].y - gap2):
                            self.x -= self.speed
            else:
                if (self.y + vehicle_dim <= self.stop or self.crossed == 1 or is_green) and \
                   (self.index == 0 or self.y + vehicle_dim < (vehicles[dir][self.lane][self.index-1].y - gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
                    self.y += self.speed

        elif dir == 'left':
            vehicle_dim = self.currentImage.get_rect().width
            mid_x = mid[dir]['x']
            stop_line = stopLines[dir]

            if self.crossed == 0 and self.x < stop_line:
                self.crossed = 1
                vehicles[dir]['crossed'] += 1
                if self.vehicleClass == "ambulance":
                    print(f"Ambulance from {dir} has crossed → check if more")

            if self.willTurn:
                if self.crossed == 0 or self.x > mid_x:
                    if (self.x >= self.stop or is_green or self.crossed == 1) and \
                       (self.index == 0 or self.x > (vehicles[dir][self.lane][self.index-1].x + vehicles[dir][self.lane][self.index-1].currentImage.get_rect().width + gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
                        self.x -= self.speed
                else:
                    if self.turned == 0:
                        self.rotateAngle += rotationAngle
                        self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
                        self.x -= 1.8
                        self.y -= 2.5
                        if self.rotateAngle == 90:
                            self.turned = 1
                    else:
                        if self.index == 0 or self.y > (vehicles[dir][self.lane][self.index-1].y + vehicles[dir][self.lane][self.index-1].currentImage.get_rect().height + gap2) or self.x > (vehicles[dir][self.lane][self.index-1].x + gap2):
                            self.y -= self.speed
            else:
                if (self.x >= self.stop or self.crossed == 1 or is_green) and \
                   (self.index == 0 or self.x > (vehicles[dir][self.lane][self.index-1].x + vehicles[dir][self.lane][self.index-1].currentImage.get_rect().width + gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
                    self.x -= self.speed

        elif dir == 'up':
            vehicle_dim = self.currentImage.get_rect().height
            mid_y = mid[dir]['y']
            stop_line = stopLines[dir]

            if self.crossed == 0 and self.y < stop_line:
                self.crossed = 1
                vehicles[dir]['crossed'] += 1
                if self.vehicleClass == "ambulance":
                    print(f"Ambulance from {dir} has crossed → check if more")

            if self.willTurn:
                if self.crossed == 0 or self.y > mid_y:
                    if (self.y >= self.stop or is_green or self.crossed == 1) and \
                       (self.index == 0 or self.y > (vehicles[dir][self.lane][self.index-1].y + vehicles[dir][self.lane][self.index-1].currentImage.get_rect().height + gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
                        self.y -= self.speed
                else:
                    if self.turned == 0:
                        self.rotateAngle += rotationAngle
                        self.currentImage = pygame.transform.rotate(self.originalImage, -self.rotateAngle)
                        self.x += 1
                        self.y -= 1
                        if self.rotateAngle == 90:
                            self.turned = 1
                    else:
                        if self.index == 0 or self.x < (vehicles[dir][self.lane][self.index-1].x - vehicles[dir][self.lane][self.index-1].currentImage.get_rect().width - gap2) or self.y > (vehicles[dir][self.lane][self.index-1].y + gap2):
                            self.x += self.speed
            else:
                if (self.y >= self.stop or self.crossed == 1 or is_green) and \
                   (self.index == 0 or self.y > (vehicles[dir][self.lane][self.index-1].y + vehicles[dir][self.lane][self.index-1].currentImage.get_rect().height + gap2) or vehicles[dir][self.lane][self.index-1].turned == 1):
                    self.y -= self.speed

def count_waiting_ambulances(dir_num):
    count = 0
    direction = directionNumbers[dir_num]
    for lane in range(3):
        for v in vehicles[direction][lane]:
            if v.crossed == 0 and v.vehicleClass == 'ambulance':
                count += 1
    return count

def count_waiting_vehicles(dir_num):
    count = 0
    direction = directionNumbers[dir_num]
    for lane in range(3):
        for v in vehicles[direction][lane]:
            if v.crossed == 0:
                count += 1
    return count

# Initialization
def initialize():
    minGreen = defaultGreen + defaultYellow
    ts1 = TrafficSignal(defaultRed - minGreen * 0, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
    signals.append(ts1)
    ts2 = TrafficSignal(ts1.red + minGreen, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
    signals.append(ts2)
    ts3 = TrafficSignal(ts2.red + minGreen, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
    signals.append(ts3)
    ts4 = TrafficSignal(ts3.red + minGreen, defaultYellow, defaultGreen, defaultMinimum, defaultMaximum)
    signals.append(ts4)
    print("→ Signals initialized")
    repeat()

# Adaptive timing calculation
def setTime():
    global emergencyActive
    if emergencyActive:
        print("  (Emergency active → skipping normal adaptive timing)")
        return

    print(f"→ Calculating green time for next direction: {directionNumbers[nextGreen]}")

    noOfCars = noOfBikes = noOfBuses = noOfTrucks = noOfRickshaws = noOfAmbulances = 0

    dir_name = directionNumbers[nextGreen]

    for lane in range(3):
        for v in vehicles[dir_name][lane]:
            if v.crossed == 0:
                vc = v.vehicleClass
                if vc == 'car':
                    noOfCars += 1
                elif vc == 'bus':
                    noOfBuses += 1
                elif vc == 'truck':
                    noOfTrucks += 1
                elif vc == 'rickshaw':
                    noOfRickshaws += 1
                elif vc == 'bike':
                    noOfBikes += 1
                elif vc == 'ambulance':
                    noOfAmbulances += 1

    total_time = (noOfCars * carTime + noOfRickshaws * rickshawTime + noOfBuses * busTime + noOfTrucks * truckTime + noOfBikes * bikeTime + noOfAmbulances * ambulanceTime)
    greenTime = math.ceil(total_time / 3)  # Divide by number of lanes (3)
    greenTime = max(defaultMinimum, min(defaultMaximum, greenTime))
    signals[nextGreen].green = greenTime
    print(f"  → Assigned green time = {greenTime} seconds  (vehicles: C:{noOfCars} Bk:{noOfBikes} Bs:{noOfBuses} T:{noOfTrucks} R:{noOfRickshaws} Amb:{noOfAmbulances})")

def repeat():
    global currentGreen, currentYellow, nextGreen, emergencyActive, emergencyDirection

    while True:
        # Check for pending emergencies in other directions even during normal operation
        for i in range(noOfSignals):
            if i != currentGreen and count_waiting_ambulances(i) > 0 and not emergencyActive:
                print(f"!!! EMERGENCY DETECTED in direction {directionNumbers[i].upper()} during normal operation !!!")
                emergencyActive = True
                emergencyDirection = i
                break

        if emergencyActive:
            print("\n" + "="*60)
            print("          EMERGENCY VEHICLE PRIORITY MODE ACTIVATED")
            print("="*60)
            print(f"Direction getting priority: {directionNumbers[emergencyDirection].upper()}")

            previousGreen = currentGreen
            currentGreen = emergencyDirection
            currentYellow = 0
            nextGreen = (currentGreen + 1) % noOfSignals

            for i in range(noOfSignals):
                if i != currentGreen:
                    signals[i].red = 300  # large value to prevent quick cycle
                    signals[i].green = 0
                    signals[i].yellow = 0

            num_amb = count_waiting_ambulances(emergencyDirection)
            initial_green = max(20, num_amb * 10)
            signals[currentGreen].green = initial_green
            signals[currentGreen].yellow = defaultYellow
            print(f"→ Setting emergency green to {initial_green}s for {num_amb} ambulances")

            while signals[currentGreen].green > 0 or count_waiting_ambulances(emergencyDirection) > 0:
                if signals[currentGreen].green <= 0 and count_waiting_ambulances(emergencyDirection) > 0:
                    num_amb_remaining = count_waiting_ambulances(emergencyDirection)
                    extension = max(10, num_amb_remaining * 10)
                    signals[currentGreen].green += extension
                    print(f"→ Extending emergency green by {extension}s for {num_amb_remaining} remaining ambulances")

                printStatus()
                updateValues()
                time.sleep(1)

            currentYellow = 1
            while signals[currentGreen].yellow > 0:
                printStatus()
                updateValues()
                time.sleep(1)

            currentYellow = 0
            print("\n→ Emergency cleared. Returning to normal adaptive control.")
            emergencyActive = False

            for i in range(noOfSignals):
                signals[i].green = defaultGreen
                signals[i].yellow = defaultYellow
                signals[i].red = defaultRed

            currentGreen = previousGreen
            nextGreen = (currentGreen + 1) % noOfSignals
            continue

        print(f"\n→ Green for {directionNumbers[currentGreen]}")
        while signals[currentGreen].green > 0:
            printStatus()
            updateValues()

            if signals[nextGreen].red == detectionTime:
                thread = threading.Thread(target=setTime)
                thread.daemon = True
                thread.start()

            time.sleep(1)

        currentYellow = 1
        print(f"→ Yellow for {directionNumbers[currentGreen]}")
        while signals[currentGreen].yellow > 0:
            printStatus()
            updateValues()
            time.sleep(1)

        currentYellow = 0

        signals[currentGreen].green = defaultGreen
        signals[currentGreen].yellow = defaultYellow

        currentGreen = nextGreen
        nextGreen = (currentGreen + 1) % noOfSignals

# Print the signal timers on cmd
def printStatus():
    for i in range(0, noOfSignals):
        if(i==currentGreen):
            if(currentYellow==0):
                print(" GREEN TS",i+1,"-> r:",signals[i].red," y:",signals[i].yellow," g:",signals[i].green)
            else:
                print("YELLOW TS",i+1,"-> r:",signals[i].red," y:",signals[i].yellow," g:",signals[i].green)
        else:
            print(" RED TS",i+1,"-> r:",signals[i].red," y:",signals[i].yellow," g:",signals[i].green)
    print()

# Update values of the signal timers after every second
def updateValues():
    for i in range(0, noOfSignals):
        if(i==currentGreen):
            if(currentYellow==0):
                if signals[i].green > 0:
                    signals[i].green -=1
                signals[i].totalGreenTime +=1
            else:
                if signals[i].yellow > 0:
                    signals[i].yellow -=1
        else:
            if signals[i].red > 0:
                signals[i].red -=1

def generateVehicles():
    global currentGreen, noOfSignals, timeElapsed
    while True:
        # Dynamic ambulance probability based on simulation time
        if timeElapsed < simulation_warmup_seconds:
            ambulance_prob = ambulance_warmup_probability
        else:
            ambulance_prob = ambulance_base_probability

        rand = random.random()  # 0.0 to 1.0

        if rand < ambulance_prob:
            vehicle_type = 5  # ambulance
        else:
            vehicle_type = random.randint(0,4)

        if vehicle_type == 4:  # bike
            lane_number = 0
        else:
            lane_number = random.randint(0,1) + 1

        will_turn = 0
        if lane_number == 2:
            temp = random.randint(0,4)
            will_turn = 1 if temp <= 2 else 0

        if vehicle_type == 5:
            # Ambulance prefers current green direction or the one just before it
            direction_number = random.choice([currentGreen, (currentGreen - 1) % noOfSignals])
        else:
            direction_number = random.randint(0,3)

        Vehicle(lane_number, vehicleTypes[vehicle_type], direction_number, directionNumbers[direction_number], will_turn)
        time.sleep(2)

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
   
class Main:
    thread4 = threading.Thread(name="simulationTime",target=simulationTime, args=())
    thread4.daemon = True
    thread4.start()
    thread2 = threading.Thread(name="initialization",target=initialize, args=()) # initialization
    thread2.daemon = True
    thread2.start()
    # Colours
    black = (0, 0, 0)
    white = (255, 255, 255)
    # Screensize
    screenWidth = 1400
    screenHeight = 800
    screenSize = (screenWidth, screenHeight)
    # Setting background image i.e. image of intersection
    background = pygame.image.load(os.path.join(BASE_DIR, 'images', 'mod_int.png'))
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("EMERGENCY MODEL")
    # Loading signal images and font
    redSignal = pygame.image.load(os.path.join(BASE_DIR, 'images', 'signals', 'red.png'))
    yellowSignal = pygame.image.load(os.path.join(BASE_DIR, 'images', 'signals', 'yellow.png'))
    greenSignal = pygame.image.load(os.path.join(BASE_DIR, 'images', 'signals', 'green.png'))
    font = pygame.font.Font(None, 30)
    emergencyFont = pygame.font.Font(None, 40)
    thread3 = threading.Thread(name="generateVehicles",target=generateVehicles, args=()) # Generating vehicles
    thread3.daemon = True
    thread3.start()
    flash_visible = True
    flash_timer = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.blit(background,(0,0)) # display background in simulation
        for i in range(0,noOfSignals): # display signal and set timer according to current status: green, yello, or red
            if(i==currentGreen):
                if(currentYellow==1):
                    if(signals[i].yellow==0):
                        signals[i].signalText = "STOP"
                    else:
                        signals[i].signalText = signals[i].yellow
                    screen.blit(yellowSignal, signalCoods[i])
                else:
                    if(signals[i].green==0):
                        signals[i].signalText = "SLOW"
                    else:
                        signals[i].signalText = signals[i].green
                    screen.blit(greenSignal, signalCoods[i])
            else:
                if(signals[i].red<=10):
                    if(signals[i].red==0):
                        signals[i].signalText = "GO"
                    else:
                        signals[i].signalText = signals[i].red
                else:
                    signals[i].signalText = "---"
                screen.blit(redSignal, signalCoods[i])
        signalTexts = ["","","",""]
        # display signal timer
        for i in range(0,noOfSignals):
            signalTexts[i] = font.render(str(signals[i].signalText), True, white, black)
            screen.blit(signalTexts[i],signalTimerCoods[i])
        timeElapsedText = font.render(("Time Elapsed: "+str(timeElapsed)), True, black, white)
        screen.blit(timeElapsedText,(1100,50))
        # 🚑 Draw Emergency Banners with flashing
        if emergencyActive:
            current_time = pygame.time.get_ticks()
            if current_time - flash_timer > 500:  # flash every 0.5 seconds
                flash_visible = not flash_visible
                flash_timer = current_time

            if flash_visible:
                # Banner 1
                emergencyText1 = emergencyFont.render(
                    "🚑 EMERGENCY VEHICLE DETECTED!",
                    True,
                    (255, 0, 0),
                    (255, 255, 255)
                    )
                text_rect1 = emergencyText1.get_rect(center=(700, 40))
                screen.blit(emergencyText1, text_rect1)
                # Banner 2
                emergencyText2 = emergencyFont.render(
                    "PRIORITY MODE ACTIVATED FOR " + directionNumbers[emergencyDirection].upper(),
                    True,
                    (255, 0, 0),
                    (255, 255, 255)
                    )
                text_rect2 = emergencyText2.get_rect(center=(700, 80))
                screen.blit(emergencyText2, text_rect2)
                # Banner 3
                ambWaiting = count_waiting_ambulances(emergencyDirection)
                emergencyText3 = emergencyFont.render(
                    f"AMBULANCES IN QUEUE: {ambWaiting}",
                    True,
                    (255, 0, 0),
                    (255, 255, 255)
                    )
                text_rect3 = emergencyText3.get_rect(center=(700, 120))
                screen.blit(emergencyText3, text_rect3)
        # display the vehicles
        for vehicle in simulation:
            screen.blit(vehicle.currentImage, [vehicle.x, vehicle.y])
            vehicle.move()
        to_remove = []
        for vehicle in simulation:
            if vehicle.direction == 'right' and vehicle.x > 1400 + 100:
                to_remove.append(vehicle)
            elif vehicle.direction == 'down' and vehicle.y > 800 + 100:
                to_remove.append(vehicle)
            elif vehicle.direction == 'left' and vehicle.x < -100:
                to_remove.append(vehicle)
            elif vehicle.direction == 'up' and vehicle.y < -100:
                to_remove.append(vehicle)
        for vehicle in to_remove:
            simulation.remove(vehicle)
            vehicles[vehicle.direction][vehicle.lane].remove(vehicle)
        for dir_num in range(4):
            direction = directionNumbers[dir_num]
            for lane in range(3):
                for i in range(len(vehicles[direction][lane])):
                    vehicles[direction][lane][i].index = i
        pygame.display.update()

Main()


