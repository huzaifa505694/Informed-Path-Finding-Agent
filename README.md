# 🚀 Dynamic Path-Finding Agent

An advanced, interactive Artificial Intelligence visualization tool built in Python using the Pygame library. This project demonstrates how autonomous agents navigate complex, grid-based environments using informed search algorithms.

Unlike standard visualizers that only solve static mazes, this agent features a **Dynamic Simulation Mode** where obstacles generate in real-time, forcing the AI to detect collisions and autonomously recalculate its optimal path mid-transit.

---

## 🧠 Core Search Algorithms

This tool allows you to compare two fundamental AI search strategies side-by-side. They are implemented strictly according to theoretical AI principles to highlight their differences in memory management and optimality:

* **A* (A-Star) Search (Optimal):**
* **Evaluation Function:** Uses `f(n) = g(n) + h(n)` (combining the exact cost to reach the node `g(n)` with the estimated cost to the goal `h(n)`).
* **Memory Strategy (Expanded List):** A* tracks paths dynamically and is allowed to "re-open" previously visited nodes if it discovers a cheaper path to reach them. This guarantees the mathematically shortest route.


* **Greedy Best-First Search / GBFS (Sub-optimal, but fast):**
* **Evaluation Function:** Uses strictly `f(n) = h(n)` (ignoring the travel cost entirely and only looking at the estimated distance to the goal).
* **Memory Strategy (Strict Visited List):** GBFS prioritizes speed and memory efficiency. Once it explores a node, it adds it to a strict "Closed Set" and will never re-evaluate it, even if a better path is possible.



## 📐 Heuristic Functions

Users can toggle between two distance estimation formulas in real-time to see how they affect the search frontier:

* **Manhattan Distance:** Calculates the distance based strictly on horizontal and vertical grid movements `(|x1 - x2| + |y1 - y2|)` without cutting corners.
* **Euclidean Distance:** Calculates the direct, straight-line "as the crow flies" distance between the current node and the goal using the Pythagorean theorem.

## ⚙️ Key Features & Simulation Modes

* **Dynamic Re-planning:** When the simulation is set to `DYNAMIC`, the agent physically traverses the grid. Every few seconds, random obstacles spawn. If an obstacle spawns directly on the agent's planned route, the agent halts, detects the blockage, and instantly calculates a new path from its exact current location.
* **Weighted Terrain:** Not all paths are equal. Alongside impenetrable walls, users can place "Weights" (Purple nodes). Weighted nodes simulate rough terrain (like mud or hills) and cost 5x more energy to traverse than an empty cell.
* **Instant Maze Generation:** A single click wipes the board and generates a complex, randomized maze with a 30% obstacle density for quick testing.
* **Cyber-Midnight UI:** A sleek, dark-mode user interface with glowing neon accents, logically organized into Algorithm, Heuristic, Simulation, and Placement panels.

## 🎮 Interactive Controls

### Mouse Interactions

* **Left-Click:** Draw on the grid based on your active selection in the `PLACEMENT` panel (Draw Walls, Draw Weights, Move Start Node, Move Goal Node).
* **Right-Click:** Erase any wall, weight, or search path from a cell, returning it to an empty state.

### Dashboard Operations

* **ALGORITHM:** Toggle between `A-STAR` and `GREEDY`.
* **HEURISTIC:** Toggle between `MANHATTAN` and `EUCLIDEAN`.
* **SIMULATION:**
* `STATIC`: The algorithm instantly calculates and displays the final path and frontier visually.
* `DYNAMIC`: The agent moves step-by-step. Random obstacles spawn automatically, and the agent reacts in real-time.


* **EXECUTION:**
* `START AGENT`: Triggers the selected algorithm and begins the search/movement.
* `GENERATE MAZE`: Instantly builds a random obstacle course.
* `RESET SYSTEM`: Wipes the entire grid clean, leaving only the Start and Goal nodes.



## 📊 Real-Time Metrics Dashboard

Located at the bottom of the sidebar, the metrics panel provides empirical data to help you compare algorithms:

* **Visited Nodes:** The total number of states the algorithm had to explore before finding the goal. (A* typically visits more nodes than GBFS).
* **Path Cost:** The mathematical weight of the final path. (A* guarantees the lowest possible cost; GBFS does not).
* **Execution Time:** The computational time required to find the solution, measured in milliseconds.

## 💻 Installation and Setup

To run this project locally on your machine, you will need **Python 3.x** installed.

**1. Clone the repository**
git clone [https://github.com/huzaifa505694/Informed-Path-Finding-Agent/tree/main](https://www.google.com/search?q=https://github.com/your-username/dynamic-path-finding-agent.git)
cd dynamic-path-finding-agent

**2. Install Dependencies**
This project relies on the Pygame library for rendering.
pip install pygame

**3. Run the Application**
python main.py
