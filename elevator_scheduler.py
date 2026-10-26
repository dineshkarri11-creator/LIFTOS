"""
Elevator Controller Simulator  -  Operating Systems project
===========================================================
Real-life use case : an elevator serving a 10-floor building.
OS concept         : disk scheduling (FCFS vs SCAN vs LOOK).

    disk head      ->  elevator cabin
    cylinder       ->  floor
    I/O request    ->  person pressing a call button
    seek distance  ->  floors travelled
    response time  ->  passenger waiting time

Run:  python elevator_scheduler.py      (only needs Python 3 with tkinter)
Use : click on any floor row to call the elevator.
"""

import math
import random
import tkinter as tk
from tkinter import ttk

FLOORS = 10
FLOOR_H = 52
TOP_PAD = 24
CANVAS_W = 470
DOOR_TIME = 1.2          # seconds the doors stay open while serving a floor
TICK_MS = 30             # animation tick
ALGOS = ("FCFS", "SCAN", "LOOK")


# --------------------------------------------------------------------------
#  Simulation core (no GUI code here, so it can also run headless for stats)
# --------------------------------------------------------------------------
class ElevatorSim:
    def __init__(self):
        self.reset()

    def reset(self):
        self.pos = 0.0            # floor position (float while moving)
        self.dir = 1              # +1 up, -1 down
        self.requests = {}        # floor -> sim time when requested (insertion = arrival order)
        self.time = 0.0
        self.door_t = None        # None = doors closed, else seconds since opening
        self.reset_stats()

    def reset_stats(self):
        self.traveled = 0.0       # total "seek distance" in floors
        self.served = 0
        self.total_wait = 0.0
        self.max_wait = 0.0

    @property
    def avg_wait(self):
        return self.total_wait / self.served if self.served else 0.0

    def add_request(self, floor):
        if floor in self.requests:
            return False
        self.requests[floor] = self.time
        return True

    def door_open_fraction(self):
        if self.door_t is None:
            return 0.0
        ramp = 0.3
        return max(0.0, min(1.0, self.door_t / ramp, (DOOR_TIME - self.door_t) / ramp))

    def _should_stop(self, floor, algo):
        if algo == "FCFS":                       # FCFS only stops for the oldest request
            return floor == next(iter(self.requests))
        return True                              # SCAN / LOOK serve everything on the way

    def _choose_direction(self, algo, msgs):
        cur, old = self.pos, self.dir
        if algo == "FCFS":
            target = next(iter(self.requests))
            self.dir = 1 if target > cur else -1
        elif algo == "LOOK":
            ahead = [f for f in self.requests if (f - cur) * self.dir > 1e-9]
            behind = [f for f in self.requests if (f - cur) * self.dir < -1e-9]
            if not ahead and behind:             # nothing further this way -> turn around
                self.dir = -self.dir
        else:  # SCAN: go all the way to the end of the building, then reverse
            if self.dir == 1 and cur >= FLOORS - 1 - 1e-9:
                self.dir = -1
            elif self.dir == -1 and cur <= 1e-9:
                self.dir = 1
        if self.dir != old and algo != "FCFS":
            msgs.append(f"[{self.time:5.1f}s] {algo}: reversing direction "
                        f"({'up' if self.dir == 1 else 'down'}) at floor {cur:.0f}")

    def step(self, dt, algo, speed):
        """Advance the simulation by dt seconds. Returns a list of log messages."""
        msgs = []
        self.time += dt

        # doors currently open -> wait
        if self.door_t is not None:
            self.door_t += dt
            if self.door_t >= DOOR_TIME:
                self.door_t = None
            return msgs

        at_floor = abs(self.pos - round(self.pos)) < 1e-9
        if at_floor:
            f = int(round(self.pos))
            if f in self.requests and self._should_stop(f, algo):
                wait = self.time - self.requests.pop(f)
                self.served += 1
                self.total_wait += wait
                self.max_wait = max(self.max_wait, wait)
                self.door_t = 0.0
                msgs.append(f"[{self.time:5.1f}s] Served floor {f} (waited {wait:.1f}s)")
                return msgs

        if not self.requests:                    # idle
            return msgs

        self._choose_direction(algo, msgs)

        # move towards the next whole floor in the current direction
        if self.dir == 1:
            nxt = math.floor(self.pos + 1e-9) + 1
        else:
            nxt = math.ceil(self.pos - 1e-9) - 1
        if nxt < 0 or nxt > FLOORS - 1:
            self.dir = -self.dir
            return msgs
        dist = abs(nxt - self.pos)
        move = min(speed * dt, dist)
        self.pos = float(nxt) if move >= dist - 1e-12 else self.pos + self.dir * move
        self.traveled += move
        return msgs


def benchmark(n_requests=40, seed=None, speed=2.0):
    """Run the SAME random workload through every algorithm and compare."""
    rng = random.Random(seed)
    t, workload = 0.0, []
    for _ in range(n_requests):
        t += rng.expovariate(1 / 1.5)
        workload.append((t, rng.randrange(FLOORS)))

    results = {}
    for algo in ALGOS:
        sim, i = ElevatorSim(), 0
        while i < len(workload) or sim.requests or sim.door_t is not None:
            while i < len(workload) and workload[i][0] <= sim.time:
                sim.add_request(workload[i][1])
                i += 1
            sim.step(0.05, algo, speed)
            if sim.time > 3600:
                break
        results[algo] = (sim.traveled, sim.avg_wait, sim.max_wait, sim.served)
    return results


# --------------------------------------------------------------------------
#  GUI
# --------------------------------------------------------------------------
class App:
    def __init__(self, root):
        self.root = root
        root.title("Elevator Controller - OS Scheduling Simulator")
        root.resizable(False, False)

        self.sim = ElevatorSim()
        self.paused = False
        self.auto_timer = 0.0
        self.algo = tk.StringVar(value="LOOK")
        self.speed = tk.DoubleVar(value=2.0)
        self.auto = tk.BooleanVar(value=False)

        # ---- building window -------------------------------------------------
        self.canvas = tk.Canvas(root, width=CANVAS_W, height=TOP_PAD * 2 + FLOORS * FLOOR_H,
                                bg="#f4f6f8", highlightthickness=0)
        self.canvas.grid(row=0, column=0, padx=8, pady=8)
        self.canvas.bind("<Button-1>", self.on_click)

        # ---- control panel ---------------------------------------------------
        side = ttk.Frame(root, padding=8)
        side.grid(row=0, column=1, sticky="ns")

        ttk.Label(side, text="Scheduling algorithm", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        box = ttk.Combobox(side, textvariable=self.algo, values=ALGOS, state="readonly", width=12)
        box.pack(anchor="w", pady=(0, 6))
        box.bind("<<ComboboxSelected>>", self.on_algo_change)

        tk.Scale(side, from_=0.5, to=5, resolution=0.5, orient="horizontal", length=220,
                 variable=self.speed, label="Elevator speed (floors/sec)").pack(anchor="w")

        row = ttk.Frame(side)
        row.pack(anchor="w", pady=4)
        self.pause_btn = ttk.Button(row, text="Pause", command=self.toggle_pause, width=9)
        self.pause_btn.pack(side="left", padx=(0, 4))
        ttk.Button(row, text="Random call", command=self.random_request, width=12).pack(side="left", padx=(0, 4))
        ttk.Button(row, text="Reset", command=self.reset_all, width=7).pack(side="left")

        ttk.Checkbutton(side, text="Auto-generate calls", variable=self.auto).pack(anchor="w")
        ttk.Button(side, text="Compare algorithms (new window)", command=self.show_benchmark).pack(
            anchor="w", pady=6)

        ttk.Separator(side).pack(fill="x", pady=4)
        self.stats = {k: tk.StringVar() for k in ("traveled", "served", "avg", "max", "pending")}
        for label, key in (("Floors travelled (seek distance)", "traveled"),
                           ("Requests served", "served"),
                           ("Average wait (s)", "avg"),
                           ("Longest wait (s)", "max"),
                           ("Pending floors", "pending")):
            r = ttk.Frame(side)
            r.pack(fill="x")
            ttk.Label(r, text=label + ":").pack(side="left")
            ttk.Label(r, textvariable=self.stats[key], font=("Segoe UI", 9, "bold")).pack(side="right")

        ttk.Separator(side).pack(fill="x", pady=4)
        ttk.Label(side, text="Event log", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        self.log_box = tk.Text(side, width=44, height=12, state="disabled", font=("Consolas", 9))
        self.log_box.pack()

        self.log("Click a floor row to call the elevator.")
        self.tick()

    # ---- events --------------------------------------------------------------
    def log(self, msg):
        self.log_box.config(state="normal")
        self.log_box.insert("end", msg + "\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")

    def on_click(self, event):
        floor = FLOORS - 1 - int((event.y - TOP_PAD) // FLOOR_H)
        if 0 <= floor < FLOORS and self.sim.add_request(floor):
            self.log(f"[{self.sim.time:5.1f}s] Call from floor {floor}")

    def random_request(self):
        floor = random.randrange(FLOORS)
        if self.sim.add_request(floor):
            self.log(f"[{self.sim.time:5.1f}s] Call from floor {floor}")

    def on_algo_change(self, _=None):
        self.sim.reset_stats()
        self.log(f"--- Switched to {self.algo.get()} (statistics reset) ---")

    def toggle_pause(self):
        self.paused = not self.paused
        self.pause_btn.config(text="Resume" if self.paused else "Pause")

    def reset_all(self):
        self.sim.reset()
        self.log_box.config(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.config(state="disabled")
        self.log("Simulation reset.")

    # ---- comparison window ---------------------------------------------------
    def show_benchmark(self):
        win = tk.Toplevel(self.root)
        win.title("Algorithm comparison - same workload for all")
        cols = ("Algorithm", "Floors travelled", "Avg wait (s)", "Max wait (s)", "Served")
        tree = ttk.Treeview(win, columns=cols, show="headings", height=3)
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=120, anchor="center")
        tree.pack(padx=10, pady=10)
        note = ttk.Label(win, text="", wraplength=560, justify="left")
        note.pack(padx=10, pady=(0, 6))

        def run():
            tree.delete(*tree.get_children())
            res = benchmark(n_requests=40)
            for algo, (trav, avg, mx, served) in res.items():
                tree.insert("", "end", values=(algo, f"{trav:.0f}", f"{avg:.1f}", f"{mx:.1f}", served))
            best = min(res, key=lambda a: res[a][0])
            note.config(text=f"40 random calls, identical for every algorithm. "
                             f"Least travel: {best}. Lower is better for all columns.")

        ttk.Button(win, text="Run again with new random workload", command=run).pack(pady=(0, 10))
        run()

    # ---- main loop -----------------------------------------------------------
    def tick(self):
        dt = TICK_MS / 1000
        if not self.paused:
            if self.auto.get():
                self.auto_timer -= dt
                if self.auto_timer <= 0:
                    self.random_request()
                    self.auto_timer = random.uniform(1.0, 3.0)
            for m in self.sim.step(dt, self.algo.get(), self.speed.get()):
                self.log(m)
        self.draw()
        self.update_stats()
        self.root.after(TICK_MS, self.tick)

    def update_stats(self):
        s = self.sim
        self.stats["traveled"].set(f"{s.traveled:.1f}")
        self.stats["served"].set(str(s.served))
        self.stats["avg"].set(f"{s.avg_wait:.1f}")
        self.stats["max"].set(f"{s.max_wait:.1f}")
        self.stats["pending"].set(", ".join(map(str, sorted(s.requests))) or "-")

    # ---- drawing -------------------------------------------------------------
    def y_top(self, floor):
        return TOP_PAD + (FLOORS - 1 - floor) * FLOOR_H

    def draw(self):
        c, s = self.canvas, self.sim
        c.delete("all")
        sx1, sx2 = 190, 270

        # floors + waiting passengers
        for f in range(FLOORS):
            y = self.y_top(f)
            pending = f in s.requests
            c.create_rectangle(0, y, sx1 - 4, y + FLOOR_H,
                               fill="#ffe3e3" if pending else "#f4f6f8", outline="#c8d0d8")
            c.create_text(10, y + FLOOR_H / 2, anchor="w", text="Ground" if f == 0 else f"Floor {f}",
                          font=("Segoe UI", 9, "bold"))
            if pending:
                px, py = 105, y + FLOOR_H / 2
                c.create_oval(px - 6, py - 16, px + 6, py - 4, fill="#e67e22", outline="")
                c.create_line(px, py - 4, px, py + 10, width=3, fill="#e67e22")
                c.create_line(px - 8, py, px + 8, py, width=3, fill="#e67e22")
                c.create_text(px + 14, py, anchor="w", fill="#c0392b", font=("Segoe UI", 8),
                              text=f"{s.time - s.requests[f]:.1f}s")

        # shaft
        c.create_rectangle(sx1 - 4, TOP_PAD, sx2 + 4, TOP_PAD + FLOORS * FLOOR_H,
                           fill="#dfe4ea", outline="#7f8c8d", width=2)
        for f in range(FLOORS + 1):
            y = TOP_PAD + f * FLOOR_H
            c.create_line(0, y, CANVAS_W, y, fill="#c8d0d8")

        # cabin + sliding doors
        y = TOP_PAD + (FLOORS - 1 - s.pos) * FLOOR_H
        cx1, cx2, cy1, cy2 = sx1 + 2, sx2 - 2, y + 3, y + FLOOR_H - 3
        c.create_rectangle(cx1, cy1, cx2, cy2, fill="#fff3bf", outline="#2c3e50", width=2)
        panel_w = (cx2 - cx1) / 2 * (1 - s.door_open_fraction())
        c.create_rectangle(cx1, cy1, cx1 + panel_w, cy2, fill="#546e7a", outline="#2c3e50")
        c.create_rectangle(cx2 - panel_w, cy1, cx2, cy2, fill="#546e7a", outline="#2c3e50")

        # indicator panel (like the display above an elevator door)
        idle = not s.requests and s.door_t is None
        arrow = "■" if idle else ("▲" if s.dir == 1 else "▼")
        c.create_rectangle(300, 30, 450, 120, fill="#111", outline="#555", width=3)
        c.create_text(345, 75, text=str(int(round(s.pos))), fill="#2ecc71", font=("Consolas", 40, "bold"))
        c.create_text(415, 75, text=arrow, fill="#2ecc71", font=("Consolas", 28, "bold"))
        c.create_text(375, 145, text=f"Algorithm: {self.algo.get()}", font=("Segoe UI", 11, "bold"))
        c.create_text(375, 170, text="Doors open" if s.door_open_fraction() > 0 else
                      ("Idle" if idle else "Moving"), font=("Segoe UI", 10))
        c.create_text(375, 215, width=150, font=("Segoe UI", 9), fill="#555", justify="center",
                      text="FCFS: oldest call first\nSCAN: sweep to the ends\nLOOK: sweep, turn at last call")


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()