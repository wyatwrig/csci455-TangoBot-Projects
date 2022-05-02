"""
Final Project Class. Implements robot actions
This class implements the robot and its possible actions, as well as managing user input
"""
import random
import sys, serial, time

class Robot:

    # TODO: The print statments need to be changed to be output by the speaker and the input needs to be text to speech.
    # TODO: need to add a condition to check if total moves are greater than some amount, if so the game is lost.

    def __init__(self):
        self.health = 200
        self.weapon = "basic sword"
        self.key = False
        self.damage = 10
        self.turns = 0
        self.bot = TangoBot()

    # prints the selection menu
    def menu(self):
        print("I can scout, rest, sharpen my weapon, or report")
        return input("What should I do? \n")

    
    # This method examines surrounding squares in the map and tells the user which ways are possible
    def scout(self, map):
        return self.getMovementChoice(map.getPossibleMoves())

    # This method rests in the current node and heals a random chunk of hp
    def rest(self):
        heal = random.randrange(3, 20, 3)
        self.health += heal
        self.turns += 1
        print(f"I healed for {heal} hp, bringing my total to {self.health}.\n")
    
    # This method works like rest but improves the current weapon
    def sharpen(self):
        sharp = random.randrange(3, 20, 3)
        self.damage += sharp
        self.turns += 1
        print(f"I sharpened my weapon for {sharp} damage, bringing my total to {self.damage} damage.\n")

    # not implemented yet, might not be necessary
    def fightChoice(self, type):
        if type == "fight":
            return self.ask(["fight", "retreat"])

    def getMovementChoice(self, possMovesArray):
        for i in possMovesArray:
            print("I can move {}".format(i))
        choice = input("Where should I go?\n")
        if choice not in possMovesArray and not "exit":
            choice = input("I can't do move there. Try a different movement.\n ") # TODO: might not be working correctly
        return choice

    def takeDamage(self, damage):
        self.health -= damage
    
    def getHealth(self):
        return self.health
    
    def getWeapon(self):
        return self.weapon
    
    def getKey(self):
        return self.key

    def getDamage(self):
        return self.damage

    def getTurns(self):
        return self.turns


    # executes the actual move on the map
    def move(self, choice, robomap):
        # update robot position on map
        if choice == "right":
            robomap.moveRight()
            time.sleep(1)
            self.bot.stop()
            time.sleep(1)
            self.bot.stop()
            self.bot.turnRight()
            time.sleep(1)
            self.bot.stop()
            time.sleep(1)
            self.bot.stop()
            time.sleep(1)
            self.bot.moveForward()
            time.sleep(1)
            self.bot.stop()
            time.sleep(1)
            self.bot.stop()
            time.sleep(1)
            self.bot.turnLeft()
            time.sleep(1)
            self.bot.stop()
            time.sleep(1)
            self.bot.stop()
        elif choice == "left":
            robomap.moveLeft()
            self.bot.stop()
            time.sleep(1)
            self.bot.stop()
            time.sleep(1)
            self.bot.turnLeft()
            time.sleep(1)
            self.bot.stop()
            time.sleep(1)
            self.bot.stop()
            time.sleep(1)
            self.bot.moveForward()
            self.bot.stop()
            time.sleep(1)
            self.bot.stop()
            time.sleep(1)
            self.bot.turnRight()
            self.bot.stop()
            time.sleep(1)
            self.bot.stop()
            time.sleep(1)
        elif choice == "up":
            robomap.moveUp()
            self.bot.stop()
            time.sleep(1)
            self.bot.stop()
            time.sleep(1)
            self.bot.moveForward()
            time.sleep(1)
            self.bot.stop()
        elif choice == "down":
            robomap.moveDown()
            self.bot.stop()
            time.sleep(1)
            self.bot.stop()
            time.sleep(1)
            self.bot.moveReverse()
            time.sleep(1)
            self.bot.stop()
        self.turns += 1
        

    # return info on current weapon, health, and whatever else we want to add.
    def report(self, nmap):
        print(f"I am in square {nmap.robotX}, {nmap.robotY}\n")
        print(f"I have {self.health} health\n")
        print(f"I have a {self.weapon} which does {self.damage} damage\n")
        if self.key:
            print(f"I have found the exit key\n")
        else:
            print(f"I have not found the exit key\n")
        print(f"I have used {self.turns} turns\n")
        print()
        print(nmap)


#TangoBot Class from other projects
class TangoBot:

    #initializes robot
    def __init__(self):

        self.waist = 6000
        self.headHorz  = 6000
        self.headVert = 6000
        self.motors = 6000
        self.turn = 6000

        self.message = "-1"

        try:
            self.usb = serial.Serial('/dev/ttyACM0')
            print(self.usb.name)
            print(self.usb.baudrate)
        except:
            try:
                self.usb = serial.Serial('/dev/ttyACM1')
                print(self.usb.name)
                print(self.usb.baudrate)
            except:
                print("No servo serial ports found")
                sys.exit(0)

        self.reset()

        #Ports: 0-1 motor controls, 2 waist, 3-4 head, arms after that

    def reset(self):
        self.waist = 6000
        self.headHorz  = 6000
        self.headVert = 6000
        self.motors = 6000
        self.turn = 6000
        self.makeCommand(self.headHorz, 0x03)
        self.makeCommand(self.headVert, 0x04)
        self.makeCommand(self.waist, 0x02)
        self.makeCommand(self.motors, 0x00)
        self.makeCommand(self.turn, 0x01)

    def moveReverse(self):
        if(self.motors < 7500):
            self.motors += 1000
            self.makeCommand(self.motors, 0x00)
            print("moving reverse")
        else:
            print("max speed")

    def moveForward(self):
        if(self.motors > 4500):
            self.motors -= 1000
            self.makeCommand(self.motors, 0x00)
            print("moving forward")
        else:
            print("max speed")

    def turnLeft(self):
        print('turning left')
#        self.motors = 6000
#        self.makeCommand(self.motors, 0x00)
        self.turn += 1300
        self.makeCommand(self.turn, 0x01)
        self.turn = 6000
#        time.sleep(1)
#        for i in range(3):
#            self.moveReverse(key)
#        for i in range(3):
#            self.moveForward(key)

    def turnRight(self):
        print('turning right')
#        self.motors = 6000
#        self.makeCommand(self.motors, 0x00)
        self.turn -= 1300
        self.makeCommand(self.turn, 0x01)
        self.turn = 6000
#        for i in range(3):
#            self.moveReverse(key)
#        for i in range(3):
#            self.moveForward(key)

    def stop(self):
        print("stopping")
        if(self.motors > 6000):
            while(self.motors > 6000):
                self.motors -= 250
                self.makeCommand(self.motors, 0x00)
        elif(self.motors < 6000):
            while(self.motors < 6000):
                self.motors += 250
                self.makeCommand(self.motors, 0x00)

    def moveWaistLeft(self):
        if(self.waist < 9000):
            self.waist += 500
            self.makeCommand(self.waist, 0x02)
            print("swiveling left")
        else:
            print("max swivel")

    def moveWaistRight(self):
        if(self.waist > 3000):
            self.waist -= 500
            self.makeCommand(self.waist, 0x02)
            print("swiveling right")
        else:
            print("max swivel")

    def moveHeadRight(self):
        if(self.headHorz > 5000):
            print("move head right")
            self.headHorz -= 500
            self.makeCommand(self.headHorz, 0x03)
        else:
            print("head too far right")

    def moveHeadLeft(self):
        if(self.headHorz < 7000):
            print("move head left")
            self.headHorz += 500
            self.makeCommand(self.headHorz, 0x03)
        else:
            print("head too far left")

    def moveHeadUp(self):
        if(self.headVert < 7000):
            print("move head up")
            self.headVert += 500
            self.makeCommand(self.headVert, 0x04)
        else:
            print("head too high")

    def moveHeadDown(self):
        if(self.headVert > 5000):
            print("move head down")
            self.headVert -= 500
            self.makeCommand(self.headVert, 0x04)
        else:
            print("head too low")

    def makeCommand(self, target, port):
        lsb = target &0x7F
        msb = (target >> 7) &0x7F
        cmd = chr(0xaa) + chr(0xC) + chr(0x04) + chr(port) + chr(lsb) + chr(msb)
        self.execute(cmd)

    def execute(self, cmd):
        print('Writing')
        self.usb.write(cmd.encode())
        print('Reading')

