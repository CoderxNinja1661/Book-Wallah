import tkinter as tk
from tkinter import ttk
import time, random, heapq

# ------------------------------------------------------
# 🧠 ALGOQUEST — The Algorithm Visualizer
# Subject: Design and Analysis of Algorithms
# Algorithms: Quick Sort | Merge Sort | Dijkstra | Kruskal | 0/1 Knapsack
# ------------------------------------------------------

class AlgoQuest:
    def __init__(self, root):
        self.root = root
        self.root.title("⚔️ ALGOQUEST — The Algorithm Visualizer")
        self.root.geometry("1100x750")
        self.root.configure(bg="#0f172a")

        # Title
        title = tk.Label(root, text="🧩 ALGOQUEST — The Algorithm Visualizer",
                         font=("Arial", 22, "bold"), bg="#0f172a", fg="#38bdf8")
        title.pack(pady=10)

        # Top Frame
        top = tk.Frame(root, bg="#0f172a")
        top.pack(pady=5)

        # Algorithm Selection
        tk.Label(top, text="Choose Algorithm:", font=("Arial", 12),
                 fg="white", bg="#0f172a").grid(row=0, column=0, padx=10)
        self.algo = ttk.Combobox(top, values=[
            "Quick Sort", "Merge Sort", "Dijkstra", "Kruskal", "0/1 Knapsack"
        ], width=25, font=("Arial", 12))
        self.algo.grid(row=0, column=1)
        self.algo.set("Quick Sort")

        ttk.Button(top, text="Run", command=self.run_algo).grid(row=0, column=2, padx=10)
        ttk.Button(top, text="Reset", command=self.reset_canvas).grid(row=0, column=3, padx=10)

        # --- Custom Array Input Section ---
        tk.Label(top, text="Enter Numbers (comma-separated):", font=("Arial", 12),
                 fg="white", bg="#0f172a").grid(row=1, column=0, padx=10, pady=5)
        self.custom_entry = tk.Entry(top, width=40, font=("Arial", 12))
        self.custom_entry.grid(row=1, column=1, padx=10, pady=5)

        self.use_custom = tk.BooleanVar()
        tk.Checkbutton(top, text="Use My Numbers", variable=self.use_custom,
                       bg="#0f172a", fg="white", selectcolor="#1e293b").grid(row=1, column=2)

        # Canvas Area
        self.canvas = tk.Canvas(root, width=950, height=450, bg="#1e293b", highlightthickness=0)
        self.canvas.pack(pady=20)

        # Output Log
        self.output = tk.Text(root, height=8, width=120, bg="#0f172a", fg="#f8fafc", font=("Consolas", 10))
        self.output.pack(pady=5)

    # ---------- Reset ----------
    def reset_canvas(self):
        self.canvas.delete("all")
        self.output.delete("1.0", tk.END)

    # ---------- Log ----------
    def log_step(self, text):
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        self.root.update_idletasks()

    # ---------- Draw Bars ----------
    def draw_bars(self, data, colors):
        self.canvas.delete("all")
        c_w, c_h = 900, 400
        x_width = c_w / (len(data) + 1)
        offset = 30
        for i, height in enumerate(data):
            x0 = i * x_width + offset
            y0 = c_h - height * 3
            x1 = (i + 1) * x_width + offset + 10
            y1 = c_h
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=colors[i], outline="")
            self.canvas.create_text(x0 + 5, y0 - 10, text=str(height), fill="#e2e8f0", font=("Arial", 9))
        self.root.update()

    # ---------- Sorting ----------
    def visualize_sort(self, algo):
        # ✅ Custom or random array
        if self.use_custom.get():
            try:
                arr = list(map(int, self.custom_entry.get().split(',')))
                if not arr:
                    raise ValueError
                self.log_step(f"Using custom array: {arr}")
            except ValueError:
                self.log_step("⚠️ Invalid input! Using random array instead.")
                arr = [random.randint(10, 100) for _ in range(10)]
        else:
            arr = [random.randint(10, 100) for _ in range(10)]

        self.log_step(f"Initial array: {arr}")
        self.draw_bars(arr, ["#38bdf8"] * len(arr))
        time.sleep(0.5)

        if algo == "Quick Sort":
            self.quick_sort(arr, 0, len(arr)-1)
            self.log_step("Quick Sort Completed!")
        else:
            self.merge_sort(arr, 0, len(arr)-1)
            self.log_step("Merge Sort Completed!")

        self.draw_bars(arr, ["#22c55e"] * len(arr))
        self.log_step(f"Final Sorted Array: {arr}")

    def quick_sort(self, arr, low, high):
        if low < high:
            pi = self.partition(arr, low, high)
            self.quick_sort(arr, low, pi-1)
            self.quick_sort(arr, pi+1, high)

    def partition(self, arr, low, high):
        pivot = arr[high]
        self.log_step(f"Pivot chosen: {pivot}")
        i = low - 1
        for j in range(low, high):
            if arr[j] < pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
            self.draw_bars(arr, ["#f87171" if x == j else "#38bdf8" for x in range(len(arr))])
            time.sleep(0.15)
        arr[i+1], arr[high] = arr[high], arr[i+1]
        self.log_step(f"Pivot placed at index {i+1}")
        return i + 1

    def merge_sort(self, arr, l, r):
        if l < r:
            m = (l + r)//2
            self.merge_sort(arr, l, m)
            self.merge_sort(arr, m+1, r)
            self.merge(arr, l, m, r)
            self.draw_bars(arr, ["#fbbf24"] * len(arr))
            time.sleep(0.2)

    def merge(self, arr, l, m, r):
        left = arr[l:m+1]
        right = arr[m+1:r+1]
        self.log_step(f"Merging {left} and {right}")
        i = j = 0
        k = l
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                arr[k] = left[i]; i += 1
            else:
                arr[k] = right[j]; j += 1
            k += 1
            self.draw_bars(arr, ["#fbbf24"] * len(arr))
            time.sleep(0.1)
        while i < len(left):
            arr[k] = left[i]; i += 1; k += 1
        while j < len(right):
            arr[k] = right[j]; j += 1; k += 1

    # ---------- Dijkstra ----------
    def visualize_dijkstra(self):
        graph = {
            'A': [('B', 4), ('C', 2)],
            'B': [('A', 4), ('C', 1), ('D', 5)],
            'C': [('A', 2), ('B', 1), ('D', 8), ('E', 10)],
            'D': [('B', 5), ('C', 8), ('E', 2)],
            'E': [('C', 10), ('D', 2)]
        }
        pos = {'A': (100, 200), 'B': (250, 100), 'C': (250, 300), 'D': (450, 200), 'E': (600, 200)}

        for u in graph:
            for v, w in graph[u]:
                self.canvas.create_line(*pos[u], *pos[v], fill="#475569", width=2)
                mx, my = (pos[u][0]+pos[v][0])//2, (pos[u][1]+pos[v][1])//2
                self.canvas.create_text(mx, my, text=w, fill="white")
        for node, (x,y) in pos.items():
            self.canvas.create_oval(x-20, y-20, x+20, y+20, fill="#38bdf8")
            self.canvas.create_text(x, y, text=node, fill="white", font=("Arial", 12, "bold"))

        start = 'A'
        dist = {n: float('inf') for n in graph}; dist[start]=0
        pq = [(0, start)]
        self.log_step("Dijkstra’s Algorithm Steps:")
        while pq:
            d, node = heapq.heappop(pq)
            self.log_step(f"Visiting {node}, distance = {d}")
            for neigh, w in graph[node]:
                nd = d + w
                if nd < dist[neigh]:
                    dist[neigh] = nd
                    heapq.heappush(pq, (nd, neigh))
                    self.canvas.create_line(*pos[node], *pos[neigh], fill="#22c55e", width=4)
                    self.root.update(); time.sleep(0.3)
        self.log_step("Final shortest distances:")
        for k,v in dist.items():
            self.log_step(f"{k}: {v}")

    # ---------- Kruskal ----------
    def visualize_kruskal(self):
        nodes = ['A', 'B', 'C', 'D', 'E']
        edges = [
            ('A','B',2), ('A','C',3), ('B','C',1),
            ('B','D',4), ('C','D',5), ('C','E',6), ('D','E',7)
        ]
        pos = {'A':(100,200), 'B':(250,100), 'C':(250,300), 'D':(450,200), 'E':(600,200)}

        for u,v,w in edges:
            self.canvas.create_line(*pos[u], *pos[v], fill="#475569", width=2)
            mx,my=(pos[u][0]+pos[v][0])//2,(pos[u][1]+pos[v][1])//2
            self.canvas.create_text(mx,my,text=w,fill="white")
        for node,(x,y) in pos.items():
            self.canvas.create_oval(x-20,y-20,x+20,y+20,fill="#38bdf8")
            self.canvas.create_text(x,y,text=node,fill="white",font=("Arial",12,"bold"))

        parent={n:n for n in nodes}
        def find(n):
            while parent[n]!=n:n=parent[n]
            return n
        def union(a,b):
            parent[find(a)]=find(b)
        edges.sort(key=lambda x:x[2])
        mst=[]
        self.log_step("Kruskal’s Algorithm Steps:")
        for u,v,w in edges:
            if find(u)!=find(v):
                union(u,v)
                mst.append((u,v,w))
                self.canvas.create_line(*pos[u], *pos[v], fill="#22c55e", width=5)
                self.log_step(f"Edge {u}-{v} ({w}) added to MST")
                self.root.update(); time.sleep(0.4)
        total=sum(w for _,_,w in mst)
        self.log_step(f"Total MST weight = {total}")

    # ---------- Knapsack ----------
    def visualize_knapsack(self):
        weights=[2,3,4,5]; values=[3,4,5,8]; cap=8
        n=len(values)
        dp=[[0]*(cap+1) for _ in range(n+1)]
        self.log_step("0/1 Knapsack Steps:")
        for i in range(1,n+1):
            for w in range(1,cap+1):
                if weights[i-1]<=w:
                    dp[i][w]=max(values[i-1]+dp[i-1][w-weights[i-1]],dp[i-1][w])
                else:
                    dp[i][w]=dp[i-1][w]
                self.log_step(f"Item {i}, Capacity {w}: Value = {dp[i][w]}")
                self.root.update()
        max_val=dp[n][cap]
        bagx,bagy=400,150
        self.canvas.create_rectangle(bagx,bagy,bagx+200,bagy+250,outline="#38bdf8",width=4)
        self.canvas.create_text(bagx+100,bagy-20,text="Knapsack",fill="white",font=("Arial",14))
        y=bagy+220
        for i in range(n):
            self.canvas.create_rectangle(bagx+20,y-40,bagx+80,y,fill="#fbbf24")
            self.canvas.create_text(bagx+50,y-20,text=f"W:{weights[i]} V:{values[i]}",fill="black")
            y-=50; self.root.update(); time.sleep(0.3)
        self.log_step(f"Maximum Value: {max_val}")

    # ---------- Runner ----------
    def run_algo(self):
        algo=self.algo.get()
        self.reset_canvas()
        if algo in ["Quick Sort","Merge Sort"]:
            self.visualize_sort(algo)
        elif algo=="Dijkstra":
            self.visualize_dijkstra()
        elif algo=="Kruskal":
            self.visualize_kruskal()
        elif algo=="0/1 Knapsack":
            self.visualize_knapsack()
        else:
            self.log_step("Please select an algorithm.")

# ---------- RUN ----------
if __name__=="__main__":
    root=tk.Tk()
    app=AlgoQuest(root)
    root.mainloop()