# Artificial Intelligence – Multi-Agent Pacman Project

## Project Overview

This project implements **Artificial Intelligence multi-agent search techniques** in the classic **Pacman game environment**. The objective is to design intelligent agents capable of making optimal decisions while interacting with other agents such as ghosts.

Pacman must determine the best possible action by considering the behavior of ghost agents. To achieve this, several AI search algorithms are implemented, including **Minimax** and **Expectimax**, along with a custom **evaluation function** to analyze game states.

This project demonstrates key AI concepts such as:

* Multi-agent search
* Adversarial decision making
* Probabilistic decision making
* Game state evaluation

---

#  Game Environment

The Pacman environment simulates a **grid-based maze** where multiple agents interact.

**Pacman**

* Attempts to eat all food pellets
* Tries to maximize the total score
* Must avoid ghosts

**Ghosts**

* Attempt to catch Pacman
* Move according to specific strategies or randomness

The **GameState** contains important information such as:

* Pacman position
* Ghost positions
* Remaining food pellets
* Capsules
* Current score

Agents use this information to determine the best next action.

---

#  Implemented AI Algorithms

## 1️⃣ Minimax Algorithm

The **Minimax algorithm** is used for adversarial search where Pacman assumes ghosts act optimally to minimize Pacman’s score.

The algorithm works by:

1. Exploring possible future game states.
2. Alternating between **max nodes (Pacman)** and **min nodes (ghosts)**.
3. Selecting the action that maximizes Pacman’s guaranteed outcome.

This allows Pacman to plan strategically against intelligent ghost behavior.

---

## 2️⃣ Expectimax Algorithm

The **Expectimax algorithm** models ghost behavior as **random rather than adversarial**.

Instead of assuming ghosts always choose the worst move for Pacman, their actions are treated as **probabilistic events**.

The algorithm:

1. Expands possible game states
2. Calculates the **expected value** of ghost actions
3. Selects the move with the **highest expected utility**

This approach is more suitable when ghost movements are unpredictable.

---

## 3️⃣ Evaluation Function

An **evaluation function** is used to estimate the quality of a game state when the search depth limit is reached.

The evaluation considers factors such as:

* Distance to the nearest food
* Distance to ghosts
* Remaining food pellets
* Current game score

A well-designed evaluation function helps Pacman make strong decisions without needing to search too deeply.


## 📄 File Descriptions

### pacman.py

This is the **main file that runs the Pacman game**.
It also defines the **GameState class**, which represents the current state of the game.

Responsibilities include:

* Running the game loop
* Managing agent turns
* Updating game states
* Tracking scores

---

### game.py

This file contains the **core logic of the Pacman world**.

It defines several important classes:

* `Agent` – Base class for Pacman and ghosts
* `AgentState` – Stores the state of each agent
* `Direction` – Possible movement directions
* `Grid` – Representation of the maze layout

---

### util.py

This file provides useful **data structures and helper utilities** for implementing search algorithms.

Examples include:

* Stack
* Queue
* PriorityQueue

These structures may simplify algorithm implementation.

---

### multiAgents.py

This file contains the **AI agent implementations**, including:

* Reflex Agent
* Minimax Agent
* Expectimax Agent
* Evaluation Function

Each agent determines the best action for Pacman based on different decision-making strategies.

---

# ▶️ Running the Program

Run the default Pacman game:

```
python pacman.py
```

Run Pacman with the **Minimax Agent**:

```
python pacman.py -p MinimaxAgent
```

Run with a specific search depth:

```
python pacman.py -p MinimaxAgent -a depth=3
```

Run using **Expectimax Agent**:

```
python pacman.py -p ExpectimaxAgent
```

---

# 🎯 Learning Outcomes

Through this project, students gain experience with:

* AI multi-agent systems
* Adversarial search algorithms
* Decision making under uncertainty
* Heuristic evaluation design
* Game AI implementation

---

# 👨‍💻 Author

**Student:** Nguyen Thi Hong Hanh
**Course:** Artificial Intelligence
**Institution:** RMIT University
