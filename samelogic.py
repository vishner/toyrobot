import tkinter as tk
from tkinter import messagebox, scrolledtext

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

class ToyRobotGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Toy Robot Simulator")
        self.robot = ToyRobot()
        
        self.create_grid()
        self.create_controls()
        self.create_console()

    def create_grid(self):
        self.grid_frame = tk.Frame(self.master)
        self.grid_frame.pack(pady=20)
        
        self.cells = []
        for i in range(5):
            row = []
            for j in range(5):
                cell = tk.Frame(self.grid_frame, width=60, height=60, bg="white", relief="raised", borderwidth=1)
                cell.grid(row=i, column=j, padx=2, pady=2)
                row.append(cell)
            self.cells.append(row)

    def create_controls(self):
        control_frame = tk.Frame(self.master)
        control_frame.pack(pady=10)

        tk.Button(control_frame, text="PLACE", command=self.place_robot).grid(row=0, column=0, padx=5)
        tk.Button(control_frame, text="MOVE", command=self.move_robot).grid(row=0, column=1, padx=5)
        tk.Button(control_frame, text="LEFT", command=self.turn_left).grid(row=0, column=2, padx=5)
        tk.Button(control_frame, text="RIGHT", command=self.turn_right).grid(row=0, column=3, padx=5)
        tk.Button(control_frame, text="REPORT", command=self.report).grid(row=0, column=4, padx=5)

    def create_console(self):
        console_frame = tk.Frame(self.master)
        console_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.console_output = scrolledtext.ScrolledText(console_frame, wrap=tk.WORD, width=40, height=10)
        self.console_output.pack(pady=5, fill=tk.BOTH, expand=True)
        self.console_output.config(state=tk.DISABLED)

        self.console_input = tk.Entry(console_frame, width=40)
        self.console_input.pack(pady=5)
        self.console_input.bind('<Return>', self.process_command)

        tk.Button(console_frame, text="Execute", command=self.process_command).pack(pady=5)

    def process_command(self, event=None):
        command = self.console_input.get().strip().upper()
        self.console_input.delete(0, tk.END)
        
        if command.startswith("PLACE"):
            try:
                _, position = command.split(" ")
                x, y, direction = position.split(",")
                if self.robot.place(int(x), int(y), direction):
                    self.update_grid()
                    self.console_print(f"Robot placed at {x},{y} facing {direction}")
                else:
                    self.console_print("Invalid placement")
            except ValueError:
                self.console_print("Invalid PLACE command. Format: PLACE X,Y,F")
        elif command == "MOVE":
            if self.robot.move():
                self.update_grid()
                self.console_print("Robot moved")
            else:
                self.console_print("Cannot move")
        elif command == "LEFT":
            if self.robot.left():
                self.update_grid()
                self.console_print("Robot turned left")
            else:
                self.console_print("Cannot turn left")
        elif command == "RIGHT":
            if self.robot.right():
                self.update_grid()
                self.console_print("Robot turned right")
            else:
                self.console_print("Cannot turn right")
        elif command == "REPORT":
            self.console_print(self.robot.report())
        else:
            self.console_print("Invalid command")

    def console_print(self, message):
        self.console_output.config(state=tk.NORMAL)
        self.console_output.insert(tk.END, message + "\n")
        self.console_output.see(tk.END)
        self.console_output.config(state=tk.DISABLED)

    def place_robot(self):
        place_window = tk.Toplevel(self.master)
        place_window.title("Place Robot")

        tk.Label(place_window, text="X:").grid(row=0, column=0)
        x_entry = tk.Entry(place_window)
        x_entry.grid(row=0, column=1)

        tk.Label(place_window, text="Y:").grid(row=1, column=0)
        y_entry = tk.Entry(place_window)
        y_entry.grid(row=1, column=1)

        tk.Label(place_window, text="Direction:").grid(row=2, column=0)
        direction_var = tk.StringVar(place_window)
        direction_var.set("NORTH")
        direction_menu = tk.OptionMenu(place_window, direction_var, "NORTH", "EAST", "SOUTH", "WEST")
        direction_menu.grid(row=2, column=1)

        def submit():
            try:
                x = int(x_entry.get())
                y = int(y_entry.get())
                direction = direction_var.get()
                if self.robot.place(x, y, direction):
                    self.update_grid()
                    self.console_print(f"Robot placed at {x},{y} facing {direction}")
                    place_window.destroy()
                else:
                    messagebox.showerror("Invalid Placement", "The robot cannot be placed at this position.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid integer coordinates.")

        tk.Button(place_window, text="Place", command=submit).grid(row=3, column=0, columnspan=2)

    def move_robot(self):
        if self.robot.move():
            self.update_grid()
            self.console_print("Robot moved")
        else:
            self.console_print("Cannot move")

    def turn_left(self):
        if self.robot.left():
            self.update_grid()
            self.console_print("Robot turned left")
        else:
            self.console_print("Cannot turn left")

    def turn_right(self):
        if self.robot.right():
            self.update_grid()
            self.console_print("Robot turned right")
        else:
            self.console_print("Cannot turn right")

    def report(self):
        report = self.robot.report()
        self.console_print(report)

    def update_grid(self):
        for row in self.cells:
            for cell in row:
                for widget in cell.winfo_children():
                    widget.destroy()
                cell.config(bg="white")
        
        if self.robot.placed:
            robot_cell = self.cells[4 - self.robot.y][self.robot.x]
            robot_cell.config(bg="lightblue")
            
            label = tk.Label(robot_cell, text="🤖", font=("Arial", 20))
            label.place(relx=0.5, rely=0.5, anchor="center")
            
            arrow = "↑"
            if self.robot.direction == "EAST":
                arrow = "→"
            elif self.robot.direction == "SOUTH":
                arrow = "↓"
            elif self.robot.direction == "WEST":
                arrow = "←"
            
            arrow_label = tk.Label(robot_cell, text=arrow, font=("Arial", 16))
            arrow_label.place(relx=0.8, rely=0.2, anchor="ne")

def main():
    root = tk.Tk()
    ToyRobotGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()