
# 🐍 Snake Game with A* Algorithm

### 🎯 Introduction
A classic Snake game enhanced with the **A* pathfinding algorithm** to make the snake move intelligently toward the food while avoiding obstacles.

---

### 🧠 Technologies Used
- Python  
- Pygame  
- NumPy  

---

### ⚙️ Features
- Automatic snake movement using the **A*** algorithm  
- Random **obstacle generation**  
- **Dynamic scoring system**  
- **Game Over screen** showing final score  

---

### 🧩 A* Algorithm Overview
The A* algorithm finds the shortest path using:
```

f(n) = g(n) + h(n)

````
where  
- `g(n)` = actual distance from start  
- `h(n)` = estimated distance (Euclidean heuristic)

---

### 🚀 How to Run
1. Install dependencies:
   '''
   pip install pygame numpy

''''
2. Run the game:
'''
   python snake_game_astar.py
''''

### 📊 Result

* Snake automatically follows the shortest path to food.
* Smooth and responsive gameplay.
* Final score displayed at the end.


### 🏁 Conclusion

This project demonstrates the use of the **A* pathfinding algorithm** in real-time game development, making gameplay smarter and more interactive.



