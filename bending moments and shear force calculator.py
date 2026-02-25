import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import numpy as np

class BeamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Beam Shear Force & Bending Moment Calculator")
        self.root.geometry("900x600")

        self.loads = []

        # Beam properties
        beam_frame = ttk.LabelFrame(root, text="Beam Properties")
        beam_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(beam_frame, text="Beam Length (m):").grid(row=0, column=0)
        self.length_entry = ttk.Entry(beam_frame)
        self.length_entry.grid(row=0, column=1)

        # Load input
        load_frame = ttk.LabelFrame(root, text="Add Load")
        load_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(load_frame, text="Type:").grid(row=0, column=0)
        self.load_type = ttk.Combobox(load_frame, values=["Point Load", "UDL"])
        self.load_type.grid(row=0, column=1)

        ttk.Label(load_frame, text="Magnitude (N or N/m):").grid(row=1, column=0)
        self.magnitude_entry = ttk.Entry(load_frame)
        self.magnitude_entry.grid(row=1, column=1)

        ttk.Label(load_frame, text="Position Start (m):").grid(row=2, column=0)
        self.start_entry = ttk.Entry(load_frame)
        self.start_entry.grid(row=2, column=1)

        ttk.Label(load_frame, text="Position End (m, for UDL):").grid(row=3, column=0)
        self.end_entry = ttk.Entry(load_frame)
        self.end_entry.grid(row=3, column=1)

        ttk.Button(load_frame, text="Add Load", command=self.add_load).grid(row=4, column=0, columnspan=2, pady=5)

        # Load list
        self.load_listbox = tk.Listbox(root)
        self.load_listbox.pack(fill="both", expand=True, padx=10, pady=5)

        ttk.Button(root, text="Calculate & Plot", command=self.calculate).pack(pady=10)

    def add_load(self):
        try:
            load_type = self.load_type.get()
            magnitude = float(self.magnitude_entry.get())
            start = float(self.start_entry.get())
            end = self.end_entry.get()

            if load_type == "Point Load":
                load = {"type": "point", "P": magnitude, "x": start}
                display = f"Point Load: {magnitude}N at {start}m"

            elif load_type == "UDL":
                end = float(end)
                load = {"type": "udl", "w": magnitude, "x1": start, "x2": end}
                display = f"UDL: {magnitude}N/m from {start}m to {end}m"

            else:
                raise ValueError

            self.loads.append(load)
            self.load_listbox.insert(tk.END, display)

        except:
            messagebox.showerror("Error", "Invalid load input")

    def calculate_reactions(self, L):
        total_force = 0
        moment_A = 0

        for load in self.loads:
            if load["type"] == "point":
                P = load["P"]
                x = load["x"]
                total_force += P
                moment_A += P * x

            elif load["type"] == "udl":
                w = load["w"]
                x1 = load["x1"]
                x2 = load["x2"]
                length = x2 - x1
                force = w * length
                centroid = x1 + length / 2
                total_force += force
                moment_A += force * centroid

        RB = moment_A / L
        RA = total_force - RB

        return RA, RB

    def calculate(self):
        try:
            L = float(self.length_entry.get())

            RA, RB = self.calculate_reactions(L)

            x_vals = np.linspace(0, L, 500)
            shear = np.zeros_like(x_vals)
            moment = np.zeros_like(x_vals)

            for i, x in enumerate(x_vals):
                V = RA
                M = RA * x

                for load in self.loads:
                    if load["type"] == "point":
                        if x >= load["x"]:
                            V -= load["P"]
                            M -= load["P"] * (x - load["x"])

                    elif load["type"] == "udl":
                        x1, x2 = load["x1"], load["x2"]
                        w = load["w"]

                        if x > x1:
                            length = min(x, x2) - x1
                            if length > 0:
                                V -= w * length
                                M -= w * length * (x - (x1 + length / 2))

                shear[i] = V
                moment[i] = M

            # Plot
            fig, axs = plt.subplots(2, 1, figsize=(8, 6))

            axs[0].plot(x_vals, shear)
            axs[0].set_title("Shear Force Diagram")
            axs[0].set_xlabel("Length (m)")
            axs[0].set_ylabel("Shear Force (N)")
            axs[0].grid()

            axs[1].plot(x_vals, moment)
            axs[1].set_title("Bending Moment Diagram")
            axs[1].set_xlabel("Length (m)")
            axs[1].set_ylabel("Moment (Nm)")
            axs[1].grid()

            plt.tight_layout()
            plt.show()

            messagebox.showinfo("Results", f"Reaction at A: {RA:.2f} N\nReaction at B: {RB:.2f} N")

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = BeamApp(root)
    root.mainloop()