
import tkinter as tk
from tkinter import ttk, messagebox

import networkx as nx
import matplotlib.pyplot as plt

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg
)

from iskit.graph import Graph


# إنشاء Graph تجريبي
g = Graph(directed=False)

g.add_edge("A", "B", 2)
g.add_edge("A", "C", 1)
g.add_edge("B", "D", 4)
g.add_edge("B", "E", 3)
g.add_edge("C", "D", 2)
g.add_edge("C", "F", 5)
g.add_edge("D", "E", 1)
g.add_edge("D", "F", 2)
g.add_edge("E", "G", 2)
g.add_edge("F", "G", 1)


# تحويل Graph إلى NetworkX
G = nx.DiGraph() if g.directed else nx.Graph()

for u in g.adj:

    G.add_node(u)

    for v, w in g.neighbors(u):
        G.add_edge(u, v, weight=w)


# تحديد مواقع ثابتة للـ Nodes
pos = nx.spring_layout(G, seed=42)


# Heuristic تجريبية
# القيم صفر حتى تضمن A* أقصر مسار
heuristics = {node: 0 for node in G.nodes}


def h(node):
    return heuristics[node]


# متغيرات الحركة
steps = []
step_index = 0
running = False
job = None
final_path = None
final_cost = None


# إنشاء النافذة
root = tk.Tk()

root.title("Graph Algorithm Visualizer")
root.geometry("1100x800")


# عناصر التحكم
controls = ttk.Frame(root, padding=15)
controls.pack(fill="x")


ttk.Label(
    controls,
    text="Algorithm:"
).grid(row=0, column=0, padx=5)


algorithm = ttk.Combobox(
    controls,
    values=["BFS", "Dijkstra", "A*"],
    state="readonly",
    width=15
)

algorithm.set("Dijkstra")
algorithm.grid(row=0, column=1, padx=5)


ttk.Label(
    controls,
    text="Start:"
).grid(row=0, column=2, padx=5)


start_box = ttk.Combobox(
    controls,
    values=list(G.nodes),
    state="readonly",
    width=8
)

start_box.set("A")
start_box.grid(row=0, column=3, padx=5)


ttk.Label(
    controls,
    text="Goal:"
).grid(row=0, column=4, padx=5)


goal_box = ttk.Combobox(
    controls,
    values=list(G.nodes),
    state="readonly",
    width=8
)

goal_box.set("G")
goal_box.grid(row=0, column=5, padx=5)


# إنشاء الرسم
fig, ax = plt.subplots(figsize=(10, 6))

canvas = FigureCanvasTkAgg(
    fig,
    master=root
)

canvas.get_tk_widget().pack(
    fill="both",
    expand=True
)


# معلومات الخطوة الحالية
info = tk.StringVar()

info.set("Choose an algorithm and press Start")

ttk.Label(
    root,
    textvariable=info,
    font=("Arial", 12),
    padding=10
).pack()


# دالة الرسم
def draw_graph(step=None, finished=False):

    ax.clear()

    # اللون الافتراضي للـ Nodes
    colors = ["lightgray" for _ in G.nodes]

    current = None
    visited = []
    path = []

    if step is not None:

        current = step["current"]
        visited = step["visited"]
        path = step["path"]

        colors = []

        for node in G.nodes:

            if node == current:
                colors.append("orange")

            elif node in visited:
                colors.append("lightblue")

            else:
                colors.append("lightgray")

    # عند الانتهاء نلون المسار النهائي بالأخضر
    if finished and final_path:

        colors = []

        for node in G.nodes:

            if node in final_path:
                colors.append("lightgreen")

            else:
                colors.append("lightgray")

        path = final_path

    nx.draw_networkx_nodes(
        G,
        pos,
        node_color=colors,
        node_size=1400,
        ax=ax
    )

    nx.draw_networkx_labels(
        G,
        pos,
        font_size=12,
        font_weight="bold",
        ax=ax
    )

    # رسم كل الـ Edges
    nx.draw_networkx_edges(
        G,
        pos,
        width=1.5,
        edge_color="gray",
        arrows=g.directed,
        ax=ax
    )

    # رسم أوزان الـ Edges
    edge_labels = nx.get_edge_attributes(
        G,
        "weight"
    )

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=edge_labels,
        font_size=10,
        ax=ax
    )

    # تلوين المسار الحالي بالأحمر
    if len(path) > 1:

        path_edges = list(
            zip(path[:-1], path[1:])
        )

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=path_edges,
            edge_color="red",
            width=4,
            arrows=g.directed,
            ax=ax
        )

    ax.set_title(
        "Graph Search Visualization",
        fontsize=16
    )

    ax.axis("off")

    canvas.draw()


# تشغيل الخوارزمية المختارة
def start_search():

    global steps
    global step_index
    global running
    global final_path
    global final_cost
    global job

    # إيقاف أي حركة قديمة
    running = False

    if job is not None:
        root.after_cancel(job)
        job = None

    start = start_box.get()
    goal = goal_box.get()

    selected = algorithm.get()

    if selected == "BFS":

        final_path, final_cost = g.bfs(
            start,
            goal
        )

    elif selected == "Dijkstra":

        final_path, final_cost = g.dijkstra(
            start,
            goal
        )

    else:

        final_path, final_cost = g.astar(
            start,
            goal,
            h
        )

    # نسخ خطوات البحث
    steps = list(g.steps)

    step_index = 0

    if not steps:

        messagebox.showinfo(
            "Result",
            "No steps found"
        )

        return

    # عرض أول خطوة
    show_step()


# عرض خطوة واحدة
def show_step():

    global step_index

    if not steps:
        return

    if step_index >= len(steps):

        draw_graph(
            steps[-1],
            finished=True
        )

        if final_path:

            result = " -> ".join(final_path)

            info.set(
                f"Finished | Path: {result} | "
                f"Result: {final_cost}"
            )

        else:

            info.set("No path found")

        return

    step = steps[step_index]

    draw_graph(step)

    current = step["current"]
    visited = step["visited"]
    path = step["path"]
    cost = step["cost"]

    info.set(
        f"Step: {step_index + 1}/{len(steps)}"
        f" | Current: {current}"
        f" | Visited: {visited}"
        f" | Path: {path}"
        f" | Cost: {cost}"
    )

    step_index += 1


# الانتقال للخطوة التالية
def next_step():

    global running
    global job

    running = False

    if job is not None:
        root.after_cancel(job)
        job = None

    show_step()


# تشغيل الحركة تلقائيًا
def auto_play():

    global running
    global job

    if not steps:
        start_search()

    if not steps:
        return

    running = True

    def animate():

        global running
        global job

        if not running:
            return

        if step_index <= len(steps):

            show_step()

            job = root.after(
                1000,
                animate
            )

        else:

            running = False
            job = None

    animate()


# إيقاف الحركة
def pause():

    global running
    global job

    running = False

    if job is not None:
        root.after_cancel(job)
        job = None


# إعادة العرض
def reset():

    global step_index
    global running
    global job

    pause()

    step_index = 0

    if steps:
        show_step()

    else:
        draw_graph()


# أزرار التحكم
buttons = ttk.Frame(
    root,
    padding=15
)

buttons.pack()


ttk.Button(
    buttons,
    text="Start",
    command=start_search
).pack(side="left", padx=5)


ttk.Button(
    buttons,
    text="Next Step",
    command=next_step
).pack(side="left", padx=5)


ttk.Button(
    buttons,
    text="Auto Play",
    command=auto_play
).pack(side="left", padx=5)


ttk.Button(
    buttons,
    text="Pause",
    command=pause
).pack(side="left", padx=5)


ttk.Button(
    buttons,
    text="Reset",
    command=reset
).pack(side="left", padx=5)


# عرض الرسم الأول
draw_graph()

root.mainloop()
