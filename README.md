
# LiftOS — Elevator Scheduling Simulator

LiftOS is a small Operating Systems project that shows how **scheduling algorithms can be used to control an elevator** in a 10-floor building. I built it to make an OS concept easier to understand through a real-life example. Instead of watching a disk head move between requests, we can watch an elevator move between floors.

The project uses Python and Tkinter to display an animated building, handle floor calls, and compare three scheduling algorithms: **FCFS, SCAN, and LOOK**.

## Project Link

[View the LiftOS GitHub Repository](https://github.com/dineshkarri11-creator/LIFTOS)

**Note:** This link opens the source-code repository. LiftOS is a desktop application, so you can run it on your computer by following the instructions below.

## Features

- **10-Floor Building Simulation:** Watch the elevator move between floors in an animated building interface.
- **Floor Requests:** Click on any floor row to call the elevator.
- **Random Calls:** Generate random floor requests to test the simulation.
- **Automatic Requests:** Enable automatic call generation to keep the elevator busy.
- **Pause and Resume:** Control the simulation whenever needed.
- **Reset Option:** Restart the simulation and clear pending requests.
- **Adjustable Speed:** Change the elevator's speed from 0.5 to 5 floors per second.
- **Multiple Scheduling Algorithms:** Switch between FCFS, SCAN, and LOOK.
- **Algorithm Comparison:** Compare the performance of all three algorithms using the same randomly generated workload.
- **Performance Statistics:** Monitor floors travelled, requests served, average waiting time, longest waiting time, and pending requests.
- **Event Log:** View messages about floor calls, completed requests, and direction changes.

## Scheduling Algorithms Used

LiftOS demonstrates three operating-system scheduling algorithms.

| Algorithm | Description |
|---|---|
| **FCFS (First Come, First Served)** | Handles the oldest pending floor request first. |
| **SCAN** | Moves in one direction, serving requests along the way, until it reaches the end of the building before reversing direction. |
| **LOOK** | Moves in one direction and serves requests along the way, reversing direction when there are no more pending requests ahead. |

## Connection to Operating Systems

This project connects disk scheduling concepts with a real-world elevator system.

| Operating System Concept | Elevator Example |
|---|---|
| Disk head | Elevator cabin |
| Cylinder | Floor |
| I/O request | A person calling the elevator |
| Seek distance | Total floors travelled |
| Response time | Time a request waits before it is served |

This comparison helps explain how scheduling algorithms decide which request to handle and how their decisions affect travel distance and waiting time.

## Technologies Used

- **Python 3:** Implements the elevator simulation and scheduling logic.
- **Tkinter:** Creates the graphical user interface and animated building.
- **Python Standard Library:** Provides additional functionality through modules such as `math` and `random`.

## Requirements

Before running LiftOS, make sure you have:

- Python 3 installed on your computer.
- Tkinter available in your Python installation.
- Git installed if you want to clone the repository.

No third-party Python packages are required by the current source code.

## How to Run the Project

### Step 1: Clone the Repository

Open your terminal or VS Code terminal and run:

```bash
git clone https://github.com/dineshkarri11-creator/LIFTOS.git
```

### Step 2: Open the Project Folder

```bash
cd LIFTOS
```

### Step 3: Run the Application

Run the following command:

```bash
python elevator_scheduler.py
```

If your system uses `python3`, run:

```bash
python3 elevator_scheduler.py
```

### Step 4: Start Using LiftOS

Once the application window opens:

1. Click on any floor row to create an elevator request.
2. Select FCFS, SCAN, or LOOK from the scheduling algorithm menu.
3. Adjust the elevator speed using the slider.
4. Use Pause or Resume to control the simulation.
5. Click Random Call to generate a request automatically.
6. Enable Auto-generate calls to create requests continuously.
7. Click Compare algorithms to view a performance comparison.
8. Use Reset to restart the simulation.

**Note for Linux users:** If Tkinter is missing, install the appropriate Tkinter package using your Linux distribution's package manager.

## Understanding the Statistics

LiftOS displays useful statistics to help understand the elevator's performance.

- **Floors Travelled:** The total distance covered by the elevator, measured in floors.
- **Requests Served:** The number of floor requests completed.
- **Average Waiting Time:** The average time requests waited before being served.
- **Longest Waiting Time:** The longest recorded wait for a completed request.
- **Pending Floors:** The floors that currently have requests waiting.

The comparison window tests 40 randomly generated calls using each scheduling algorithm. It displays the results side by side, making it easier to understand how different algorithms perform.

Since the workload is random, the results may change each time the comparison is run. The most suitable algorithm depends on the requests and the performance metric being considered.

## Project Objective

The main objective of LiftOS is to demonstrate how operating-system scheduling concepts can be applied to a familiar, real-world situation.

By simulating an elevator, the project makes it easier to understand request handling, scheduling decisions, movement distance, and waiting time. It also provides a visual way to compare the behaviour of different algorithms.

## What I Learned

While developing LiftOS, I explored how scheduling algorithms work and how they affect the handling of multiple requests. I also gained practical experience with Python, Tkinter, graphical interfaces, simulation logic, and performance comparison.

Most importantly, this project helped me connect theoretical Operating Systems concepts with a practical application.

## Future Improvements

Some features that could be added in future versions include:

- Support for multiple elevators operating in the same building.
- Improved visual indicators for the current direction and destination.
- Saving comparison results for future analysis.
- Adding screenshots and a demonstration video to the repository.

## Author

**Dinesh Karri**

GitHub: [dineshkarri11-creator](https://github.com/dineshkarri11-creator)

---

*LiftOS — Bringing Operating Systems scheduling concepts to life through an interactive elevator simulator.*
