class ToyRobot:
    def __init__(self):
        self.x = None
        self.y = None
        self.direction = None
        self.directions = ['NORTH', 'EAST', 'SOUTH', 'WEST']
        self.placed = False

    def place(self, x, y, direction):
        if 0 <= x < 5 and 0 <= y < 5 and direction in self.directions:
            self.x = x
            self.y = y
            self.direction = direction
            self.placed = True
            return True
        return False

    def move(self):
        if not self.placed:
            return False
        
        new_x, new_y = self.x, self.y
        if self.direction == 'NORTH' and self.y < 4:
            new_y += 1
        elif self.direction == 'SOUTH' and self.y > 0:
            new_y -= 1
        elif self.direction == 'EAST' and self.x < 4:
            new_x += 1
        elif self.direction == 'WEST' and self.x > 0:
            new_x -= 1
        
        if new_x != self.x or new_y != self.y:
            self.x, self.y = new_x, new_y
            return True
        return False

    def left(self):
        if not self.placed:
            return False
        current_index = self.directions.index(self.direction)
        self.direction = self.directions[(current_index - 1) % 4]
        return True

    def right(self):
        if not self.placed:
            return False
        current_index = self.directions.index(self.direction)
        self.direction = self.directions[(current_index + 1) % 4]
        return True

    def report(self):
        if not self.placed:
            return "Robot not placed yet."
        return f"{self.x},{self.y},{self.direction}"

class ToyRobotConsole:
    def __init__(self):
        self.robot = ToyRobot()

    def run(self):
        print("Welcome to the Toy Robot Simulator!")
        print("Available commands: PLACE X,Y,F | MOVE | LEFT | RIGHT | REPORT | EXIT")
        
        while True:
            command = input("Enter command: ").strip().upper()
            
            if command == "EXIT":
                print("Thank you for using the Toy Robot Simulator. Goodbye!")
                break
            
            self.process_command(command)

    def process_command(self, command):
        if command.startswith("PLACE"):
            try:
                _, position = command.split(" ")
                x, y, direction = position.split(",")
                if self.robot.place(int(x), int(y), direction):
                    print(f"Robot placed at {x},{y} facing {direction}")
                else:
                    print("Invalid placement")
            except ValueError:
                print("Invalid PLACE command. Format: PLACE X,Y,F")
        elif command == "MOVE":
            if self.robot.move():
                print("Robot moved")
            else:
                print("Cannot move")
        elif command == "LEFT":
            if self.robot.left():
                print("Robot turned left")
            else:
                print("Cannot turn left")
        elif command == "RIGHT":
            if self.robot.right():
                print("Robot turned right")
            else:
                print("Cannot turn right")
        elif command == "REPORT":
            print(self.robot.report())
        else:
            print("Invalid command")

def main():
    simulator = ToyRobotConsole()
    simulator.run()

if __name__ == "__main__":
    main()