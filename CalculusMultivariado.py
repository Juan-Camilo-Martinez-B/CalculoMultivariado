import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sympy import symbols, diff, sympify, latex, lambdify
import random
from mpl_toolkits.mplot3d import Axes3D

class MultivariableCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GeoCalculus Multivariable")
        self.root.geometry("1200x800")
        self.setup_styles()
        self.setup_ui()
        
    def setup_styles(self):
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#2D2D2D")
        self.style.configure("TLabel", background="#2D2D2D", foreground="#FF7F00", font=("Arial", 10))
        self.style.configure("TButton", background="#FF7F00", foreground="black", font=("Arial", 10))
        self.style.configure("TEntry", fieldbackground="#2D2D2D", foreground="black", insertbackground="white")
        self.root.configure(bg="#2D2D2D")

    def setup_ui(self):
        # Main frames
        self.left_frame = ttk.Frame(self.root, width=400)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        self.right_frame = ttk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left Frame: Controls
        ttk.Label(self.left_frame, text="Función (ej: x**2 + y**2):").pack(pady=5)
        self.function_entry = ttk.Entry(self.left_frame, width=30)
        self.function_entry.pack(pady=5)
        
        # Calculator Keyboard
        self.setup_calculator_keyboard()
        
        ttk.Button(self.left_frame, text="Graficar", command=self.plot_function).pack(pady=5)
        ttk.Button(self.left_frame, text="Ejemplo Aleatorio", command=self.random_example).pack(pady=5)
        ttk.Button(self.left_frame, text="Derivadas Parciales", command=self.calculate_partial_derivatives).pack(pady=5)
        ttk.Button(self.left_frame, text="Gradiente", command=self.calculate_gradient).pack(pady=5)
        ttk.Button(self.left_frame, text="Corte 3D", command=self.open_slice_window).pack(pady=5)
        
        # Right Frame: Notebook for plots and derivatives
        self.notebook = ttk.Notebook(self.right_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.tab_2d = ttk.Frame(self.notebook)
        self.tab_3d = ttk.Frame(self.notebook)
        self.tab_partial = ttk.Frame(self.notebook)  # Pestaña para derivadas parciales
        self.tab_gradient = ttk.Frame(self.notebook) # Pestaña para gradiente
        self.notebook.add(self.tab_2d, text="Gráfica 2D")
        self.notebook.add(self.tab_3d, text="Gráfica 3D")
        self.notebook.add(self.tab_partial, text="Derivadas Parciales")
        self.notebook.add(self.tab_gradient, text="Gradiente")
        
        # Canvas for plots
        self.figure_2d = plt.figure(figsize=(6, 4), facecolor="#2D2D2D")
        self.canvas_2d = FigureCanvasTkAgg(self.figure_2d, master=self.tab_2d)
        self.canvas_2d.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.figure_3d = plt.figure(figsize=(6, 4), facecolor="#2D2D2D")
        self.canvas_3d = FigureCanvasTkAgg(self.figure_3d, master=self.tab_3d)
        self.canvas_3d.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Canvas for partial derivatives (LaTeX)
        self.figure_partial = plt.figure(figsize=(6, 4), facecolor="#2D2D2D")
        self.canvas_partial = FigureCanvasTkAgg(self.figure_partial, master=self.tab_partial)
        self.canvas_partial.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Canvas for gradient (LaTeX)
        self.figure_gradient = plt.figure(figsize=(6, 4), facecolor="#2D2D2D")
        self.canvas_gradient = FigureCanvasTkAgg(self.figure_gradient, master=self.tab_gradient)
        self.canvas_gradient.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def setup_calculator_keyboard(self):
        buttons = [
            '7', '8', '9', '+', 'x',
            '4', '5', '6', '-', 'y',
            '1', '2', '3', '*', 'z',
            '0', '(', ')', '/', '^',
            'π', 'sin', 'cos', 'exp', '⌫'
        ]
        
        keyboard_frame = ttk.Frame(self.left_frame)
        keyboard_frame.pack(pady=5)
        
        for i, btn in enumerate(buttons):
            if btn == '⌫':
                ttk.Button(
                    keyboard_frame, 
                    text=btn, 
                    width=3,
                    command=lambda: self.function_entry.delete(len(self.function_entry.get())-1, tk.END)
                ).grid(row=i//5, column=i%5, padx=2, pady=2)
            else:
                ttk.Button(
                    keyboard_frame, 
                    text=btn, 
                    width=3,
                    command=lambda b=btn: self.function_entry.insert(tk.END, b)
                ).grid(row=i//5, column=i%5, padx=2, pady=2)
    
    def random_example(self):
        examples = [
            "x**2 + y**2", 
            "sin(x) + cos(y)", 
            "x*y*z", 
            "exp(-x**2 - y**2)", 
            "sqrt(x**2 + y**2 + z**2)"
        ]
        func = random.choice(examples)
        self.function_entry.delete(0, tk.END)
        self.function_entry.insert(0, func)
        self.plot_function()
    
    def plot_function(self):
        try:
            func_str = self.function_entry.get()
            if not func_str:
                raise ValueError("Ingrese una función.")
            
            expr = sympify(func_str)
            variables = list(expr.free_symbols)
            variables.sort(key=lambda x: str(x))
            
            # Plot 2D (solo si es univariable)
            self.figure_2d.clf()
            if len(variables) == 1:
                x = np.linspace(-5, 5, 400)
                func_numeric = lambdify(variables[0], expr, "numpy")
                y = func_numeric(x)
                
                ax = self.figure_2d.add_subplot(111, facecolor="#2D2D2D")
                ax.plot(x, y, color="#FF7F00", linewidth=2)
                ax.set_title(f"Gráfica 2D: {func_str}", color="white")
                ax.set_xlabel(str(variables[0]), color="white")
                ax.set_ylabel(f"f({variables[0]})", color="white")
                ax.tick_params(colors="white")
                ax.grid(color="#555555")
            else:
                ax = self.figure_2d.add_subplot(111, facecolor="#2D2D2D")
                ax.text(0.5, 0.5, "La función no es univariable", ha="center", va="center", color="white")
            
            self.canvas_2d.draw()
            
            # Plot 3D (solo si es de 2 variables)
            self.figure_3d.clf()
            if len(variables) == 2:
                x = y = np.linspace(-5, 5, 20)  # Reducir puntos para visualización clara
                X, Y = np.meshgrid(x, y)
                func_numeric = lambdify((variables[0], variables[1]), expr, "numpy")
                Z = func_numeric(X, Y)
                
                ax = self.figure_3d.add_subplot(111, projection="3d", facecolor="#2D2D2D")
                ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.7)
                
                # Calcular gradiente en cada punto (opcional, si se desea visualizar aquí)
                grad_x = lambdify((variables[0], variables[1]), diff(expr, variables[0]), "numpy")(X, Y)
                grad_y = lambdify((variables[0], variables[1]), diff(expr, variables[1]), "numpy")(X, Y)
                grad_z = np.zeros_like(grad_x)
                
                # Dibujar vectores gradiente (opcional)
                ax.quiver(X, Y, Z, grad_x, grad_y, grad_z, color="red", length=1, normalize=True, label="Gradiente")
                
                ax.set_title(f"Gráfica 3D: {func_str}", color="white")
                ax.set_xlabel(str(variables[0]), color="white")
                ax.set_ylabel(str(variables[1]), color="white")
                ax.set_zlabel(f"f({variables[0]}, {variables[1]})", color="white")
                ax.tick_params(colors="white")
                ax.legend()
            elif len(variables) > 2:
                ax = self.figure_3d.add_subplot(111, facecolor="#2D2D2D")
                ax.text(0.5, 0.5, 
                        f"Función de {len(variables)} variables.\nUse 'Corte 3D' para visualizar.", 
                        ha="center", va="center", color="white")
            else:
                ax = self.figure_3d.add_subplot(111, facecolor="#2D2D2D")
                ax.text(0.5, 0.5, "La función no es multivariable", ha="center", va="center", color="white")
            
            self.canvas_3d.draw()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al graficar: {str(e)}")
    
    def calculate_partial_derivatives(self):
        try:
            func_str = self.function_entry.get()
            if not func_str:
                raise ValueError("Ingrese una función.")
                
            expr = sympify(func_str)
            variables = sorted(expr.free_symbols, key=lambda x: str(x))
            
            # Clear previous plot
            self.figure_partial.clf()
            ax = self.figure_partial.add_subplot(111, facecolor="#2D2D2D")
            ax.axis('off')
            
            # Display partial derivatives as LaTeX
            derivatives_text = "Derivadas parciales:\n\n"
            for var in variables:
                derivative = diff(expr, var)
                derivatives_text += f"$\\frac{{\\partial}}{{\\partial {var}}} ({latex(expr)}) = {latex(derivative)}$\n\n"
            
            ax.text(0.5, 0.5, derivatives_text, 
                    ha='center', va='center', 
                    color="white", fontsize=12)
            
            self.canvas_partial.draw()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en cálculo: {str(e)}")
    
    def calculate_gradient(self):
        try:
            func_str = self.function_entry.get()
            if not func_str:
                raise ValueError("Ingrese una función.")
                
            expr = sympify(func_str)
            variables = sorted(expr.free_symbols, key=lambda x: str(x))
            
            # Clear previous plot
            self.figure_gradient.clf()
            ax = self.figure_gradient.add_subplot(111, facecolor="#2D2D2D")
            ax.axis('off')
            
            # Display gradient as LaTeX
            gradient_components = [diff(expr, var) for var in variables]
            gradient_latex = r"$\nabla f = \left(" + ", ".join([latex(comp) for comp in gradient_components]) + r"\right)$"
            
            ax.text(0.5, 0.5, gradient_latex, 
                    ha='center', va='center', 
                    color="white", fontsize=14)
            
            self.canvas_gradient.draw()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error en cálculo: {str(e)}")
    
    def open_slice_window(self):
        try:
            func_str = self.function_entry.get()
            if not func_str:
                raise ValueError("Ingrese una función.")
            
            expr = sympify(func_str)
            variables = list(expr.free_symbols)
            if len(variables) < 3:
                messagebox.showinfo("Info", "La función debe tener al menos 3 variables.")
                return
            
            self.slice_window = tk.Toplevel(self.root)
            self.slice_window.title("Configurar Corte 3D")
            self.slice_window.configure(bg="#2D2D2D")
            
            ttk.Label(self.slice_window, text="Variable a fijar:", style="TLabel").pack(pady=5)
            self.var_combobox = ttk.Combobox(self.slice_window, values=[str(var) for var in variables])
            self.var_combobox.pack(pady=5)
            
            ttk.Label(self.slice_window, text="Valor:", style="TLabel").pack(pady=5)
            self.value_entry = ttk.Entry(self.slice_window)
            self.value_entry.pack(pady=5)
            
            ttk.Button(
                self.slice_window, 
                text="Graficar Corte", 
                command=lambda: self.plot_3d_slice(func_str)
            ).pack(pady=5)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def plot_3d_slice(self, func_str):
        try:
            fixed_var = self.var_combobox.get()
            fixed_value = float(self.value_entry.get())
            
            expr = sympify(func_str)
            variables = list(expr.free_symbols)
            variables.remove(sympify(fixed_var))
            variables.sort(key=lambda x: str(x))
            
            x = y = np.linspace(-5, 5, 20)
            X, Y = np.meshgrid(x, y)
            Z = lambdify((variables[0], variables[1]), expr.subs(fixed_var, fixed_value), "numpy")(X, Y)
            
            self.figure_3d.clf()
            ax = self.figure_3d.add_subplot(111, projection="3d", facecolor="#2D2D2D")
            ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.7)
            
            # Calcular gradiente en el corte (opcional)
            grad_x = lambdify((variables[0], variables[1]), diff(expr, variables[0]).subs(fixed_var, fixed_value), "numpy")(X, Y)
            grad_y = lambdify((variables[0], variables[1]), diff(expr, variables[1]).subs(fixed_var, fixed_value), "numpy")(X, Y)
            grad_z = np.zeros_like(grad_x)
            
            ax.quiver(X, Y, Z, grad_x, grad_y, grad_z, color="red", length=1, normalize=True, label="Gradiente")
            
            ax.set_title(f"Corte 3D: {func_str} con {fixed_var}={fixed_value}", color="white")
            ax.set_xlabel(str(variables[0]), color="white")
            ax.set_ylabel(str(variables[1]), color="white")
            ax.set_zlabel(f"f({variables[0]}, {variables[1]})", color="white")
            ax.tick_params(colors="white")
            ax.legend()
            
            self.canvas_3d.draw()
            self.slice_window.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al graficar corte: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MultivariableCalculatorApp(root)
    root.mainloop()
