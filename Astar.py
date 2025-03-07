import heapq
import time
import folium
import tkinter as tk
from tkinter import ttk, messagebox
from geopy.geocoders import Nominatim
from haversine import haversine

# List of major cities in Tamil Nadu
tamil_nadu_cities = [
    "Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem", "Erode", "Vellore", "Tirunelveli",
    "Thoothukudi", "Thanjavur", "Dindigul", "Nagercoil", "Karur", "Kanchipuram", "Namakkal", "Cuddalore"
]

class AStarGraph:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="TamilNaduAStar")
        self.locations = {}
        self.edges = {}

    def add_city(self, city_name):
        """Fetch latitude & longitude for a city and add it to the graph"""
        time.sleep(1)  # Prevent API blocking
        location = self.geolocator.geocode(city_name + ", Tamil Nadu, India", timeout=10)
        if location:
            self.locations[city_name] = (location.latitude, location.longitude)
        else:
            messagebox.showerror("Error", f"Could not find location for {city_name}")

    def calculate_distance(self, city1, city2):
        """Calculate Haversine distance between two cities"""
        if city1 in self.locations and city2 in self.locations:
            return round(haversine(self.locations[city1], self.locations[city2]), 2)
        return None

    def add_road(self, city1, city2):
        """Store distances between cities"""
        distance = self.calculate_distance(city1, city2)
        if distance:
            self.edges.setdefault(city1, {})[city2] = distance
            self.edges.setdefault(city2, {})[city1] = distance  # Undirected graph
        else:
            messagebox.showerror("Error", f"Could not calculate distance between {city1} and {city2}")

    def heuristic(self, city, goal):
        """Heuristic function: Haversine distance to the goal city"""
        return self.calculate_distance(city, goal) or float("inf")

    def a_star_search(self, start, goal):
        """A* Algorithm for shortest path"""
        if start not in self.edges or goal not in self.edges:
            messagebox.showerror("Error", "Start or goal city not found in roads.")
            return None

        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {city: float("inf") for city in self.edges}
        g_score[start] = 0
        f_score = {city: float("inf") for city in self.edges}
        f_score[start] = self.heuristic(start, goal)

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                path.reverse()
                return path

            for neighbor, distance in self.edges[current].items():
                tentative_g_score = g_score[current] + distance
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None

    def draw_map(self, path=None):
        """Visualize the graph on a map using Folium"""
        if not self.locations:
            messagebox.showerror("Error", "No locations to map.")
            return

        first_city = next(iter(self.locations.values()))
        city_map = folium.Map(location=first_city, zoom_start=7)

        # Add city markers
        for city, coords in self.locations.items():
            folium.Marker(coords, popup=city, icon=folium.Icon(color="blue")).add_to(city_map)

        # Draw roads
        for city1, neighbors in self.edges.items():
            for city2 in neighbors:
                folium.PolyLine([self.locations[city1], self.locations[city2]], color="gray").add_to(city_map)

        # Highlight shortest path
        if path:
            path_coords = [self.locations[city] for city in path]
            folium.PolyLine(path_coords, color="red", weight=5, opacity=0.7).add_to(city_map)

        city_map.save("tamil_nadu_map.html")
        messagebox.showinfo("Map Saved", "Map has been saved as tamil_nadu_map.html. Open it in a browser.")

# Tkinter GUI
def run_gui():
    graph = AStarGraph()

    def submit_cities():
        selected_cities = [dropdowns[i].get() for i in range(7)]
        for city in selected_cities:
            graph.add_city(city)
        messagebox.showinfo("Cities Added", "Cities have been added successfully.")

    def submit_roads():
        city1 = road_city1.get()
        city2 = road_city2.get()
        graph.add_road(city1, city2)
        messagebox.showinfo("Road Added", f"Road added between {city1} and {city2}")

    def find_path():
        start = start_city.get()
        goal = goal_city.get()
        path = graph.a_star_search(start, goal)
        if path:
            messagebox.showinfo("Shortest Path", " → ".join(path))
            graph.draw_map(path)
        else:
            messagebox.showerror("Error", "No path found.")

    root = tk.Tk()
    root.title("Tamil Nadu A* Pathfinding")

    tk.Label(root, text="Select 7 Cities:").grid(row=0, column=0, columnspan=2)

    dropdowns = []
    for i in range(7):
        dropdown = ttk.Combobox(root, values=tamil_nadu_cities, state="readonly")
        dropdown.grid(row=i + 1, column=1)
        dropdowns.append(dropdown)

    tk.Button(root, text="Add Cities", command=submit_cities).grid(row=8, column=1)

    tk.Label(root, text="Enter Road Connection:").grid(row=9, column=0, columnspan=2)
    road_city1 = ttk.Combobox(root, values=tamil_nadu_cities, state="readonly")
    road_city1.grid(row=10, column=0)
    road_city2 = ttk.Combobox(root, values=tamil_nadu_cities, state="readonly")
    road_city2.grid(row=10, column=1)

    tk.Button(root, text="Add Road", command=submit_roads).grid(row=11, column=1)

    tk.Label(root, text="Select Start and Goal Cities:").grid(row=12, column=0, columnspan=2)
    start_city = ttk.Combobox(root, values=tamil_nadu_cities, state="readonly")
    start_city.grid(row=13, column=0)
    goal_city = ttk.Combobox(root, values=tamil_nadu_cities, state="readonly")
    goal_city.grid(row=13, column=1)

    tk.Button(root, text="Find Shortest Path", command=find_path).grid(row=14, column=1)

    root.mainloop()

# Run GUI
if __name__ == "__main__":
    run_gui()
