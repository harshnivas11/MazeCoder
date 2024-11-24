import sqlite3

def init_database():
    conn = sqlite3.connect('questions.db')
    cursor = conn.cursor()
    
    # Create questions table with difficulty level
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY,
        question TEXT NOT NULL,
        option_a TEXT NOT NULL,
        option_b TEXT NOT NULL,
        option_c TEXT NOT NULL,
        option_d TEXT NOT NULL,
        correct_answer TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        used INTEGER DEFAULT 0
    )
    ''')
    
    # Questions for different difficulty levels
    questions = [
        # Easy Questions (exactly 10)
        ("What is the time complexity of searching for an element in a balanced binary search tree?",
         "O(n)", "O(log n)", "O(1)", "O(n log n)", "B", "easy"),
        ("Which data structure uses FIFO (First In First Out)?",
         "Stack", "Queue", "Linked List", "Tree", "B", "easy"),
        ("What is the best-case time complexity of bubble sort?",
         "O(n^2)", "O(n log n)", "O(n)", "O(log n)", "C", "easy"),
        ("Which data structure is used for implementing recursion?",
         "Queue", "Stack", "Array", "Linked List", "B", "easy"),
        ("What is the full form of BFS?",
         "Binary Forward Search", "Breadth First Search", "Best First Search", "Backward First Search", "B", "easy"),
        ("What is the time complexity of searching an element in a hash table?",
         "O(log n)", "O(n)", "O(1)", "O(n log n)", "C", "easy"),
        ("Which of the following is not a linear data structure?",
         "Array", "Queue", "Stack", "Binary Tree", "D", "easy"),
        ("What is the time complexity of accessing an element in an array?",
         "O(n)", "O(1)", "O(log n)", "O(n log n)", "B", "easy"),
        ("In a binary tree, how many children can a node have at most?",
         "1", "2", "3", "Unlimited", "B", "easy"),
        ("Which sorting algorithm is the fastest for small data sets?",
         "Bubble Sort", "Insertion Sort", "Quick Sort", "Merge Sort", "B", "easy"),
        
        # Medium Questions (exactly 8)
        ("What is the time complexity of merging two sorted arrays?",
         "O(n)", "O(log n)", "O(m + n)", "O(n^2)", "C", "medium"),
        ("Which traversal is used for Depth First Search (DFS)?",
         "Pre-order", "Post-order", "In-order", "Any of the above", "D", "medium"),
        ("What is the space complexity of recursive Quick Sort?",
         "O(1)", "O(log n)", "O(n)", "O(n log n)", "B", "medium"),
        ("Which of the following graph algorithms uses a min-heap?",
         "Kruskal's", "Dijkstra's", "Bellman-Ford", "Floyd-Warshall", "B", "medium"),
        ("What is the maximum number of nodes at level k of a binary tree?",
         "2^k", "2^(k-1)", "k", "k^2", "A", "medium"),
        ("Which of the following is used to detect cycles in a graph?",
         "DFS", "BFS", "Kruskal's", "Floyd-Warshall", "A", "medium"),
        ("What is the auxiliary space complexity of Merge Sort?",
         "O(n)", "O(1)", "O(log n)", "O(n^2)", "A", "medium"),
        ("What is the average case time complexity of searching in a skip list?",
         "O(log n)", "O(n)", "O(1)", "O(n log n)", "A", "medium"),
        
        # Hard Questions (exactly 7)
        ("Which algorithm is used to find articulation points in a graph?",
         "Tarjan's", "Dijkstra's", "Floyd-Warshall", "Kruskal's", "A", "hard"),
        ("What is the amortized time complexity of union-find with path compression?",
         "O(n)", "O(log n)", "O(α(n))", "O(1)", "C", "hard"),
        ("What is the time complexity of the Bellman-Ford algorithm?",
         "O(V + E)", "O(VE)", "O(E log V)", "O(V^2)", "B", "hard"),
        ("Which data structure is best for implementing A* pathfinding?",
         "Stack", "Priority Queue", "Queue", "Linked List", "B", "hard"),
        ("What is the minimum height of a B-Tree of order m with n keys?",
         "⌈logm(n+1)⌉", "⌈logm n⌉", "m^⌈n/m⌉", "n/m", "A", "hard"),
        ("What is the time complexity of building a max-heap?",
         "O(log n)", "O(n log n)", "O(n)", "O(n^2)", "C", "hard"),
        ("Which algorithm solves the all-pairs shortest path problem?",
         "Dijkstra's", "Floyd-Warshall", "Bellman-Ford", "Prim's", "B", "hard")
    ]
    
    cursor.execute('DELETE FROM questions')
    cursor.executemany('''
    INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_answer, difficulty)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', questions)
    
    conn.commit()
    conn.close()