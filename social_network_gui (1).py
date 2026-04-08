import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import subprocess

DATA_FILE = "network_data.txt"
C_EXECUTABLE = "social_network.exe" if os.name == "nt" else "./social_network"

class SocialNetworkGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Social Network Visualizer (Python GUI)")
        self.geometry("1100x720")
        self.minsize(900, 600)

        self.graph = nx.Graph()
        self.names = []
        self.adj_matrix = []
        self.data_loaded = False

        self.create_widgets()
        # load data (this will try using C executable --init if file missing)
        self.load_data()
        # draw initial
        self.initial_draw()

    # ----------------------- LOAD & SAVE DATA -----------------------
    def write_data_file(self):
        """Write current names + adj_matrix to DATA_FILE in same format C uses."""
        try:
            n = len(self.names)
            with open(DATA_FILE, "w") as f:
                f.write(str(n) + "\n")
                for name in self.names:
                    f.write(f"{name}\n")
                for i in range(n):
                    row = " ".join(str(self.adj_matrix[i][j]) for j in range(n))
                    f.write(row + "\n")
            self.text_output_insert("✅ Saved network to file.\n")
        except Exception as e:
            self.text_output_insert(f"❌ Error saving file: {e}\n")

    def create_default_data_and_save(self):
        """Create the same default network as the C program and save to disk."""
        default_names = ["Joshnavi", "Adarsh", "Geetesh", "Chandu", "Kavya"]
        n = len(default_names)
        matrix = [[0]*n for _ in range(n)]
        conns = [(0,1),(0,2),(1,2),(1,3),(2,4),(3,4)]
        for a,b in conns:
            matrix[a][b] = 1
            matrix[b][a] = 1
        self.names = default_names[:]
        self.adj_matrix = matrix
        self.build_graph_from_loaded()
        self.write_data_file()

    def text_output_insert(self, txt):
        self.text_output.configure(state=tk.NORMAL)
        self.text_output.insert(tk.END, txt)
        self.text_output.see(tk.END)
        self.text_output.configure(state=tk.DISABLED)

    def load_data(self):
        """Loads graph data from file, attempting to use C executable to create file
           if missing (but non-interactively using --init)."""
        self.text_output_insert("🔍 Checking network data...\n")

        if not os.path.exists(DATA_FILE):
            # if C executable exists, call it with --init (non-interactive)
            if os.path.exists(C_EXECUTABLE):
                try:
                    subprocess.run([C_EXECUTABLE, "--init"], check=True)
                    self.text_output_insert("⚙️ Created network_data.txt by running C executable.\n")
                except Exception as e:
                    self.text_output_insert(f"❌ Failed to run C executable: {e}\n")
                    # fallback to creating a default dataset
                    self.create_default_data_and_save()
                    self.text_output_insert("ℹ️ Created default network data (fallback).\n")
            else:
                # Create default file ourselves
                self.create_default_data_and_save()
                self.text_output_insert("⚠️ C executable not found. Created default network data locally.\n")

        # Now attempt to read file
        try:
            with open(DATA_FILE, "r") as f:
                lines = [line.rstrip() for line in f if line.strip() != ""]
            if not lines:
                raise ValueError("Empty data file.")
            n = int(lines[0])
            if n < 0:
                raise ValueError("Invalid node count.")
            self.names = lines[1:1+n]
            matrix_lines = lines[1+n:1+n+n]
            # if matrix lines are missing, fallback
            if len(matrix_lines) < n:
                raise ValueError("Adjacency matrix incomplete.")
            self.adj_matrix = []
            for row in matrix_lines:
                parts = row.split()
                # pad/truncate to n
                rowvals = [int(x) for x in parts[:n]] + [0]*(n - len(parts))
                self.adj_matrix.append(rowvals)
            self.build_graph_from_loaded()
            self.data_loaded = True
            self.text_output_insert("✅ Graph data loaded successfully.\n")
        except Exception as e:
            self.data_loaded = False
            self.text_output_insert(f"❌ Error loading data: {e}\n")

    def build_graph_from_loaded(self):
        """Build networkx graph from names and adj_matrix."""
        self.graph.clear()
        for name in self.names:
            self.graph.add_node(name)
        n = len(self.names)
        for i in range(n):
            for j in range(i+1, n):
                try:
                    if self.adj_matrix[i][j] == 1:
                        self.graph.add_edge(self.names[i], self.names[j])
                except IndexError:
                    continue

    # ----------------------- UI SETUP -----------------------
    def create_widgets(self):
        container = ttk.Frame(self, padding=8)
        container.pack(fill=tk.BOTH, expand=True)

        # left controls
        left = ttk.Frame(container, width=250)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0,8), pady=8)

        ttk.Label(left, text="📁 Data Controls", font=("Segoe UI", 11, "bold")).pack(pady=4)
        ttk.Button(left, text="Reload Data", command=self.reload_data).pack(fill=tk.X, pady=3)
        ttk.Button(left, text="Show Network Data", command=self.show_text_data).pack(fill=tk.X, pady=3)

        ttk.Separator(left).pack(fill=tk.X, pady=8)

        # Shortest path
        ttk.Label(left, text="🔗 Shortest Path", font=("Segoe UI", 11, "bold")).pack(pady=4)
        ttk.Label(left, text="Start:").pack(anchor="w")
        self.start_name = ttk.Entry(left, width=24)
        self.start_name.pack(pady=2)
        ttk.Label(left, text="End:").pack(anchor="w")
        self.end_name = ttk.Entry(left, width=24)
        self.end_name.pack(pady=2)
        ttk.Button(left, text="Find Path", command=self.find_shortest_path).pack(fill=tk.X, pady=5)

        ttk.Separator(left).pack(fill=tk.X, pady=8)

        # Mutual friends
        ttk.Label(left, text="👥 Mutual Friends", font=("Segoe UI", 11, "bold")).pack(pady=4)
        ttk.Label(left, text="User 1:").pack(anchor="w")
        self.mutual_user1 = ttk.Entry(left, width=24)
        self.mutual_user1.pack(pady=2)
        ttk.Label(left, text="User 2:").pack(anchor="w")
        self.mutual_user2 = ttk.Entry(left, width=24)
        self.mutual_user2.pack(pady=2)
        ttk.Button(left, text="Find Mutual Friends", command=self.find_mutual_friends).pack(fill=tk.X, pady=5)

        ttk.Separator(left).pack(fill=tk.X, pady=8)

        # Add user / friend
        ttk.Label(left, text="➕ Add User / Connect", font=("Segoe UI", 11, "bold")).pack(pady=4)
        ttk.Label(left, text="New user name:").pack(anchor="w")
        self.add_user_name = ttk.Entry(left, width=24)
        self.add_user_name.pack(pady=2)
        ttk.Label(left, text="Connect to (existing):").pack(anchor="w")
        self.add_connect_name = ttk.Entry(left, width=24)
        self.add_connect_name.pack(pady=2)
        ttk.Button(left, text="Add / Connect", command=self.add_user_and_connect).pack(fill=tk.X, pady=6)

        ttk.Separator(left).pack(fill=tk.X, pady=8)

        # Right: Graph + text output
        right = ttk.Frame(container)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Matplotlib figure embedded
        self.fig, self.ax = plt.subplots(figsize=(7.5, 6.5))
        plt.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Text output with scrollbar
        text_frame = ttk.Frame(right)
        text_frame.pack(fill=tk.X)
        self.text_output = tk.Text(text_frame, height=7, wrap=tk.WORD, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(text_frame, command=self.text_output.yview)
        self.text_output.configure(yscrollcommand=scrollbar.set)
        self.text_output.pack(side=tk.LEFT, fill=tk.X, expand=True)
        scrollbar.pack(side=tk.LEFT, fill=tk.Y)

        # initial message
        self.text_output_insert("Application ready.\n")

    # ----------------------- GRAPH DRAW -----------------------
    def initial_draw(self):
        if self.data_loaded:
            self.draw_graph()
            self.text_output_insert("📊 Initial graph displayed.\n")
        else:
            self.ax.clear()
            self.ax.text(0.5, 0.5, "No graph data available", fontsize=14, ha="center", va="center")
            self.ax.set_axis_off()
            self.canvas.draw()

    def draw_graph(self, path=None):
        self.ax.clear()
        if not self.data_loaded:
            self.ax.text(0.5, 0.5, "No graph data", fontsize=14, ha="center", va="center")
        else:
            try:
                pos = nx.spring_layout(self.graph, seed=42)
                nx.draw_networkx(self.graph, pos, ax=self.ax, with_labels=True, node_size=700, font_size=9)
                if path and len(path) > 1:
                    path_edges = list(zip(path[:-1], path[1:]))
                    nx.draw_networkx_edges(self.graph, pos, edgelist=path_edges, width=3)
            except Exception as e:
                self.text_output_insert(f"❌ Error drawing graph: {e}\n")
        self.ax.set_axis_off()
        self.canvas.draw()

    # ----------------------- BUTTON ACTIONS -----------------------
    def reload_data(self):
        self.load_data()
        self.draw_graph()
        self.text_output_insert("🔄 Reloaded data from file.\n")

    def show_text_data(self):
        if not self.data_loaded:
            self.text_output_insert("⚠️ No data to display.\n")
            return
        output = "\n--- Current Network Data ---\n"
        n = len(self.names)
        for i, name in enumerate(self.names):
            friends = []
            for j in range(n):
                try:
                    if self.adj_matrix[i][j] == 1:
                        friends.append(self.names[j])
                except IndexError:
                    continue
            output += f"{name}: {', '.join(friends) if friends else 'None'}\n"
        self.text_output_insert(output + "\n")

    def find_shortest_path(self):
        if not self.data_loaded:
            messagebox.showwarning("Warning", "Load graph data first.")
            return
        s = self.start_name.get().strip()
        e = self.end_name.get().strip()
        if s == "" or e == "":
            messagebox.showerror("Error", "Please enter both start and end names.")
            return
        if s not in self.graph or e not in self.graph:
            messagebox.showerror("Error", "Invalid names entered.")
            return
        try:
            path = nx.shortest_path(self.graph, source=s, target=e)
            self.text_output_insert(f"➡️ Shortest Path ({len(path)-1}): {' -> '.join(path)}\n")
            self.draw_graph(path)
        except nx.NetworkXNoPath:
            self.text_output_insert(f"❌ No connection found between {s} and {e}.\n")
        except Exception as ex:
            self.text_output_insert(f"❌ Error finding path: {ex}\n")

    def find_mutual_friends(self):
        if not self.data_loaded:
            messagebox.showwarning("Warning", "Load graph data first.")
            return
        u1 = self.mutual_user1.get().strip()
        u2 = self.mutual_user2.get().strip()
        if u1 == "" or u2 == "":
            messagebox.showerror("Error", "Please enter both user names.")
            return
        if u1 not in self.names or u2 not in self.names:
            messagebox.showerror("Error", "Invalid user names entered.")
            return
        i1, i2 = self.names.index(u1), self.names.index(u2)
        mutuals = [self.names[k] for k in range(len(self.names))
                   if self.adj_matrix[i1][k] == 1 and self.adj_matrix[i2][k] == 1]
        if mutuals:
            self.text_output_insert(f"👥 Mutual Friends of {u1} and {u2}: {', '.join(mutuals)}\n")
        else:
            self.text_output_insert(f"🙅 No mutual friends between {u1} and {u2}.\n")

    def add_user_and_connect(self):
        """Add a new user (if missing) and connect to an existing user (if provided)."""
        new_name = self.add_user_name.get().strip()
        connect_name = self.add_connect_name.get().strip()

        if new_name == "":
            messagebox.showerror("Error", "Please enter the new user name.")
            return

        # ensure data loaded in memory
        if not self.data_loaded:
            # Try to load or create default
            self.load_data()

        # if names not in memory, add to lists and expand matrix
        if new_name in self.names and connect_name == "":
            messagebox.showinfo("Info", f"{new_name} already exists. No connection specified.")
            return

        if new_name not in self.names:
            # add new user
            self.names.append(new_name)
            n = len(self.names)
            # expand adj_matrix
            for row in self.adj_matrix:
                row.extend([0])
            self.adj_matrix.append([0]*n)
            self.text_output_insert(f"➕ Added user: {new_name}\n")

        if connect_name != "":
            if connect_name not in self.names:
                # we auto-create the connect_name (matching C behavior noninteractive)
                self.names.append(connect_name)
                n = len(self.names)
                for row in self.adj_matrix:
                    row.extend([0])
                self.adj_matrix.append([0]*n)
                self.text_output_insert(f"➕ Also created user: {connect_name}\n")

            idx1 = self.names.index(new_name)
            idx2 = self.names.index(connect_name)
            if idx1 == idx2:
                messagebox.showerror("Error", "Cannot connect a user to themselves.")
                return
            if self.adj_matrix[idx1][idx2] == 1:
                messagebox.showinfo("Info", f"{new_name} and {connect_name} are already connected.")
            else:
                self.adj_matrix[idx1][idx2] = 1
                self.adj_matrix[idx2][idx1] = 1
                self.text_output_insert(f"🔗 Connected {new_name} with {connect_name}\n")

        # write file and update graph
        self.build_graph_from_loaded()
        try:
            self.write_data_file()
            # optionally call C noninteractive add to keep parity (not required)
            if os.path.exists(C_EXECUTABLE):
                try:
                    # call C to add too (noninteractive). It will load, add and save.
                    subprocess.run([C_EXECUTABLE, "--add", new_name, connect_name or new_name], check=True)
                    self.text_output_insert("⚙️ Synchronized change with C executable.\n")
                except Exception:
                    # ignore errors, Python already saved file
                    pass
        except Exception as e:
            self.text_output_insert(f"❌ Error while adding: {e}\n")
        self.draw_graph()

# ----------------------- Run -----------------------
if __name__ == "__main__":
    app = SocialNetworkGUI()
    app.mainloop()