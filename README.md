Here is a detailed and professional `README.md` file tailored specifically for your project. You can copy and paste this directly into your GitHub repository.

markdown
🚀 Dynamic Path-Finding Agent

An interactive Python/Pygame visualizer for A* and Greedy Best-First Search. It features a Dynamic Mode where obstacles spawn mid-transit, forcing the AI to instantly recalculate its route. Users can draw mazes, add terrain weights, and evaluate efficiency using live metrics like execution time, nodes visited, and path cost.

 ✨ Key Features

* **Multiple Search Algorithms:** * **A* (A-Star) Search:** Implemented with an *Expanded List* strategy to guarantee optimal pathfinding using $f(n) = g(n) + h(n)$.
  * **Greedy Best-First Search (GBFS):** Implemented with a *Strict Visited List* strategy, prioritizing speed by strictly exploring nodes based on $f(n) = h(n)$.
* **Heuristic Functions:** Toggle between **Manhattan** and **Euclidean** distance calculations in real-time.
* **Dynamic Simulation Mode:** Watch the agent traverse the grid step-by-step. In Dynamic Mode, random obstacles (walls and heavy terrain) spawn while the agent is moving. If the path is blocked, the agent autonomously recalculates a new optimal route from its current position.
* **Interactive Environment:** A sleek, "Midnight-themed" UI allows you to draw walls, place heavy terrain (weights cost 5x normal movement), reposition Start/Goal nodes, or instantly generate a 30% density maze.
* **Real-Time Metrics:** Live dashboard tracking:
  * **Visited Nodes:** To evaluate memory usage and algorithm efficiency.
  * **Path Cost:** To verify the optimality of the chosen route.
  * **Execution Time (ms):** To compare computational speed.

## 🛠️ Installation & Setup

This project requires **Python 3.x** and the **Pygame** library.

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/dynamic-path-finding-agent.git](https://github.com/your-username/dynamic-path-finding-agent.git)
   cd dynamic-path-finding-agent

```

2. 
**Install the required dependencies**:


```bash
pip install pygame

```


3. 
**Run the application**:


```bash
python main.py

```



## 🎮 How to Use (Controls)

### Grid Interaction

* **Left-Click:** Place a Wall, Weight, Start Node, or Goal Node on the grid (depending on the currently selected placement tool in the sidebar).
* **Right-Click:** Erase a node (turns it back into an empty, traversable cell).

### Sidebar Dashboard

* **ALGORITHM:** Choose between `A-STAR` and `GREEDY`.
* **HEURISTIC:** Choose between `MANHATTAN` and `EUCLIDEAN` distance.
* **SIMULATION:** * `STATIC`: Calculates and shows the path instantly.
* `DYNAMIC`: Agent physically moves along the path; new random obstacles spawn every 2 seconds.


* **PLACEMENT:** Select what your left-click will draw (`WALLS`, `WEIGHTS`, `START POS`, `GOAL POS`).
* **EXECUTION:**
* `START AGENT`: Begins the search and visualization.
* `GENERATE MAZE`: Wipes the grid and creates a random maze (30% wall density).
* `RESET SYSTEM`: Clears all walls, weights, and paths, keeping only the Start and Goal nodes.



## 🧠 Architectural Overview

The code is highly modular, split into logical components:

1. **Node Class:** Manages individual grid cells, their state (color/type), weight, and drawing logic.
2. **Heuristics & Search Logic:** Pure algorithmic implementations separating the expanded list logic of A* and the strict visited list logic of GBFS.
3. **UI Components:** Custom `NeonButton` class to handle hover states, glow effects, and clicks.
4. **Main Loop:** Handles Pygame events, mouse tracking, timing for dynamic mode, and grid rendering.

## 📝 License

This project is open-source and free to use for educational purposes.

```

```
