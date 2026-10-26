# LiftOS — Elevator Scheduling Simulator

## About the Project

LiftOS is an Operating Systems project that demonstrates how scheduling algorithms can be used to control an elevator in a 10-floor building.

I developed this project to understand how operating system concepts can be applied to real-life situations. Instead of studying disk scheduling only through theory, LiftOS provides a visual simulation where an elevator moves between floors and handles different requests.

The project is built using Python and Tkinter. It allows users to control an animated elevator, generate floor requests, adjust its speed, and compare three scheduling algorithms: FCFS, SCAN, and LOOK.

## Features

- **10-Floor Building Simulation:** Watch the elevator move between floors in an animated building interface.
- **Floor Requests:** Click on any floor row to call the elevator.
- **Random Calls:** Generate random floor requests to test the simulation.
- **Automatic Requests:** Enable automatic call generation to create requests continuously.
- **Pause and Resume:** Pause or resume the simulation whenever needed.
- **Reset Option:** Restart the simulation and clear pending requests.
- **Adjustable Speed:** Change the elevator speed from 0.5 to 5 floors per second.
- **Multiple Scheduling Algorithms:** Switch between FCFS, SCAN, and LOOK.
- **Algorithm Comparison:** Compare all three algorithms using the same randomly generated workload.
- **Performance Statistics:** Monitor floors travelled, requests served, average waiting time, longest waiting time, and pending requests.
- **Event Log:** View information about floor calls, completed requests, and direction changes.

## Scheduling Algorithms Used

LiftOS demonstrates three operating system scheduling algorithms.

### 1. FCFS (First Come, First Served)

FCFS handles the oldest pending request first. The elevator prioritizes requests according to the order in which they were received.

### 2. SCAN

SCAN moves in one direction and serves requests along the way. It continues to the end of the building before reversing direction.

### 3. LOOK

LOOK moves in one direction and serves requests along the way. When there are no more pending requests ahead, the elevator reverses direction instead of travelling unnecessarily to the end of the building.

## Connection to Operating Systems

This project connects disk scheduling concepts with a real-world elevator system.

| Operating System Concept | Elevator Example |
|---|---|
| Disk head | Elevator cabin |
| Cylinder | Floor |
| I/O request | A person calling the elevator |
| Seek distance | Floors travelled |
| Response time | Passenger waiting time |

This comparison helps explain how scheduling algorithms decide which request to handle and how those decisions affect travel distance and waiting time.

## Technologies Used

- **Python 3:** Implements the simulation logic and scheduling algorithms.
- **Tkinter:** Creates the graphical user interface and animated building.
- **Math Module:** Supports calculations for elevator movement.
- **Random Module:** Generates random floor requests and workloads.

## Requirements

Before running LiftOS, make sure you have:

- Python 3 installed on your computer.
- Tkinter available in your Python installation.
- The project source file, `elevator_scheduler.py`.

The project uses Python's standard library and does not require third-party Python packages.

## How to Run the Project

### Step 1: Open the Project

Open the LiftOS project folder in VS Code or your preferred terminal.

### Step 2: Open the Terminal

Open the terminal inside your project folder, where the `elevator_scheduler.py` file is located.

### Step 3: Run the Application

Execute the following command:

```bash
python elevator_scheduler.py
```

If your system uses `python3`, run:

```bash
python3 elevator_scheduler.py
```

### Step 4: Use the Application

Once the application window opens:

1. Click on any floor row to create an elevator request.
2. Select FCFS, SCAN, or LOOK from the scheduling algorithm menu.
3. Adjust the elevator speed using the slider.
4. Use Pause or Resume to control the simulation.
5. Click **Random Call** to generate a floor request.
6. Enable **Auto-generate calls** to create requests automatically.
7. Click **Compare algorithms** to view a performance comparison.
8. Use **Reset** to restart the simulation.

## Understanding the Statistics

LiftOS displays several statistics to help users understand the elevator's performance.

- **Floors Travelled:** The total distance covered by the elevator, measured in floors.
- **Requests Served:** The number of floor requests completed.
- **Average Waiting Time:** The average time requests waited before being served.
- **Longest Waiting Time:** The longest recorded waiting time for a completed request.
- **Pending Floors:** The floors with requests that are still waiting.

The comparison window tests 40 randomly generated calls using each scheduling algorithm. It displays the results side by side, making it easier to understand how the algorithms perform.

Since the workload is random, the results may change each time the comparison is run. The most suitable algorithm depends on the requests and the performance metric being considered.

## Project Objective

The main objective of LiftOS is to demonstrate how operating system scheduling concepts can be applied to a familiar, real-world situation.

By simulating an elevator, the project makes it easier to understand request handling, scheduling decisions, movement distance, and waiting time. It also provides a visual way to compare different scheduling algorithms.

## What I Learned

While developing LiftOS, I learned how scheduling algorithms work and how they affect the handling of multiple requests. I also gained practical experience with Python programming, Tkinter, graphical user interfaces, simulation logic, and performance comparison.

Most importantly, this project helped me connect theoretical Operating Systems concepts with a practical application.

## Future Improvements

Some features that could be added in future versions include:

- Support for multiple elevators in the same building.
- Improved visual indicators for the current direction and destination.
- Saving algorithm comparison results for future analysis.
- Adding screenshots and a demonstration video.
- Introducing more scheduling strategies for comparison.

## Author

**Dinesh Karri And Charan** 

Project: LiftOS — Elevator Scheduling Simulator

## Conclusion

LiftOS demonstrates how operating system scheduling algorithms can be applied to an everyday system like an elevator. Through an animated interface and performance statistics, the project makes it easier to understand how different scheduling methods handle requests and influence waiting time and travel distance.

**LiftOS — Bringing Operating Systems scheduling concepts to life through an interactive elevator simulator.**
