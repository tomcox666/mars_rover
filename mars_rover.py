#Create the robot to assign information, commands and movement operations
class Robot:
    #for each robot thats created set the initial coordinates, orientation and commands from the user input, set "lost" to be false initially
    def __init__(self, x, y, orientation, commands):
        self.x = x
        self.y = y
        self.orientation = orientation
        self.commands = commands
        self.lost = False
    
    #change robot orientation when the command is a left or right turn, including modulo 4 (list length) will allow to essentially wrap the list
    direction = ["N", "E", "S", "W"]
    def turn_left(self):
        self.orientation = self.direction[(self.direction.index(self.orientation) - 1) % 4]

    def turn_right(self):
        self.orientation = self.direction[(self.direction.index(self.orientation) + 1) % 4]
    
    #change robots current x,y coordinates by +/-1 depending on current orientation
    def move_forward(self, grid_size):
        if self.orientation == "N":
            self.y += 1
        elif self.orientation == "E":
            self.x += 1
        elif self.orientation == "S":
            self.y -= 1
        elif self.orientation == "W":
            self.x -= 1

        #if outside grid dimensions, set robot to be lost
        if not (0 <= self.x < grid_size[0] and 0 <= self.y < grid_size[1]):
            self.lost = True
    
    #string representation of Robot object, when we print robot this will be how the information is returned as a string
    def __str__(self):
        return f"({self.x}, {self.y}, {self.orientation})" + (" LOST" if self.lost else "")

def main():
    # Get the input string from the user, allows for multi line input and will break when a blank line is entered
    def get_user_input():
        user_input = [] 
        while True: 
            line = input() 
            if not line: # If line is blank 
                break 
            else: 
                user_input.append(line)
        return user_input
    # Flag to track whether the user is happy with their input
    input_confirmed = False

    # Ask for input with grid, robot information and comands
    while not input_confirmed:
        print("\nInput grid size 'n m' as well as initial robot conditons and commands on a new line for each robot '(x, y, O) COMMANDS'. To end input enter an blank line.")
        user_input = get_user_input()

        # Ask the user if they are happy with their input
        confirmation = input("\nAre you happy with this input?  (y/n) ")

        # If the user is happy with their input, set the flag to True and run the final print statement
        if confirmation.lower() == "y":
            input_confirmed = True
    
    # Parse the grid size from user input, maps input string elements to integers in a tuple
    try:
        grid_size = tuple(map(int, user_input[0].split()))
    except ValueError:
        print("Invalid grid size")
        return
    
    # Parse the robot information and commands, update robot with the given information, add to robots list
    robots = []
    for robot_information in user_input[1:]:
        try:
            robot_info, command = robot_information.strip("(").split(") ")
            x, y, orientation = robot_info.split(", ")
            x, y = int(x), int(y)
            commands = []
            commands[:0] = command
        except ValueError:
            print("Invalid robot information")
            return
        robot = Robot(x, y, orientation, commands)
        robots.append(robot)
        
    # Execute the commands for each robot and print out robot in final state
    for robot in robots:
        for command in robot.commands:
            if command == "L":
                robot.turn_left()
            elif command == "R":
                robot.turn_right()
            elif command == "F":
                robot.move_forward(grid_size)
        print(robot)

#best practice for running main in a python script, allows for the script to be used as standalone program or a reuseable module in the future
if __name__ == "__main__":
    main()