# Social Network Graph

## Overview
A graph-based social network application that models user connections, mutual friendships, and shortest connection paths using the BFS algorithm.

## Features
- Add users and create friendships
- Display complete network
- Find mutual friends between any two users
- Find shortest path using BFS algorithm
- Persistent data storage using file handling

## Technologies Used
- **Language:** C
- **Algorithm:** Breadth-First Search (BFS)
- **Data Structure:** Adjacency Matrix

## How It Works
1. Users are stored as nodes in a graph
2. Friendships are represented as edges
3. BFS algorithm finds the shortest path between users
4. Data is saved locally for persistence

## Sample Output

![command prompt output](https://github.com/user-attachments/assets/85d35cce-e8dd-4d9b-a39f-e57bd370fb80)

**Main Menu**

1.Add 2.Show 3.Mutual 4.Shortest 5.Exit
Choice: 2

**Network Display**

--- Current Network ---
Joshnavi   : Adarsh, Geetesh
Adarsh     : Joshnavi, Geetesh, Chandu
Geetesh    : Joshnavi, Adarsh, Kavya
Chandu     : Adarsh, Kavya
Kavya      : Geetesh, Chandu

![graph visual output](https://github.com/user-attachments/assets/6cd6fec0-44e1-445b-be05-c4c5bfb30088)

**Adding a Friend**

Choice: 1
Enter your name: Kavya
Connect with: Geetesh
Connection added!

**Shortest Path Using BFS**

Choice: 4
Start: Joshnavi
End: Kavya

Path: Joshnavi -> Geetesh -> Kavya
Cost: 2

![Data loaded output](https://github.com/user-attachments/assets/11db74e0-0493-4648-ac7e-e2fb2f80dce3)


## Algorithms Used
- **BFS (Breadth-First Search)** for shortest path finding
- **Adjacency Matrix** for graph representation

## Authors
- B. Geetesh
- G. Chandu
- K. Joshnavi
- P. Adarsh

## Guide
**Mr. B. Mahesh** M.Tech, (Ph.D)

## Institution
Department of Computer Science and Engineering
ANIL NEERUKONDA INSTITUTE OF TECHNOLOGY & SCIENCES (A)
Sangivalasa, Bheemunipatnam, Visakhapatnam Dist.

## License
Academic Project
