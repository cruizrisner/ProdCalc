# Production Calculator v1.3
# Features: Calculate production targets, clear button, integer display, color-coded percentages
# Last updated: Debugging clear button visibility issue

import tkinter as tk
from tkinter import ttk
import math

class ProductionCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Production Calculator")
        self.root.geometry("700x500")
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Input section
        ttk.Label(main_frame, text="Input Parameters", font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Cycle Time
        ttk.Label(main_frame, text="Cycle Time (seconds):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.cycle_time_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.cycle_time_var, width=15).grid(row=1, column=1, sticky=tk.W, pady=2)
        
        # Number of Heads
        ttk.Label(main_frame, text="Number of Heads:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.num_heads_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.num_heads_var, width=15).grid(row=2, column=1, sticky=tk.W, pady=2)
        
        # Unit Value
        ttk.Label(main_frame, text="Unit Value:").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.unit_value_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.unit_value_var, width=15).grid(row=3, column=1, sticky=tk.W, pady=2)
        
        # 8 Hourly Values
        ttk.Label(main_frame, text="Hourly Values", font=("Arial", 10, "bold")).grid(row=4, column=0, columnspan=3, pady=(15, 5))
        
        self.hourly_vars = []
        for i in range(8):
            ttk.Label(main_frame, text=f"Hour {i+1}:").grid(row=5+i//2, column=(i%2)*2, sticky=tk.W, pady=2, padx=(0 if i%2==0 else 20, 0))
            var = tk.StringVar()
            self.hourly_vars.append(var)
            ttk.Entry(main_frame, textvariable=var, width=12).grid(row=5+i//2, column=(i%2)*2+1, sticky=tk.W, pady=2)
        
        # Buttons section - Calculate and Clear buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=9, column=0, columnspan=3, pady=20)
        
        calculate_btn = ttk.Button(button_frame, text="Calculate", command=self.calculate)
        calculate_btn.pack(side=tk.LEFT, padx=5)
        
        clear_btn = ttk.Button(button_frame, text="Clear", command=self.clear_all)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        # Results section
        ttk.Label(main_frame, text="Results", font=("Arial", 12, "bold")).grid(row=10, column=0, columnspan=3, pady=(10, 5))
        
        # Hourly Target display
        ttk.Label(main_frame, text="Hourly Target:").grid(row=11, column=0, sticky=tk.W, pady=2)
        self.target_label = ttk.Label(main_frame, text="", font=("Arial", 10, "bold"))
        self.target_label.grid(row=11, column=1, sticky=tk.W, pady=2)
        
        # Results frame with scrollable area
        results_frame = ttk.LabelFrame(main_frame, text="Hourly Calculations", padding="10")
        results_frame.grid(row=12, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        results_frame.columnconfigure(0, weight=1)
        
        # Create headers
        headers_frame = ttk.Frame(results_frame)
        headers_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 5))
        headers_frame.columnconfigure(0, weight=1)
        headers_frame.columnconfigure(1, weight=1)
        headers_frame.columnconfigure(2, weight=1)
        headers_frame.columnconfigure(3, weight=1)
        
        ttk.Label(headers_frame, text="Hour", font=("Arial", 9, "bold")).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(headers_frame, text="Actual Value", font=("Arial", 9, "bold")).grid(row=0, column=1, sticky=tk.W)
        ttk.Label(headers_frame, text="% of Target", font=("Arial", 9, "bold")).grid(row=0, column=2, sticky=tk.W)
        ttk.Label(headers_frame, text="Difference", font=("Arial", 9, "bold")).grid(row=0, column=3, sticky=tk.W)
        
        # Results display area
        self.results_frame = ttk.Frame(results_frame)
        self.results_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
        self.results_frame.columnconfigure(0, weight=1)
        self.results_frame.columnconfigure(1, weight=1)
        self.results_frame.columnconfigure(2, weight=1)
        self.results_frame.columnconfigure(3, weight=1)
        
        # Configure main frame row weights
        main_frame.rowconfigure(12, weight=1)
    
    def clear_all(self):
        """Clear all input fields and results"""
        # Clear input fields
        self.cycle_time_var.set("")
        self.num_heads_var.set("")
        self.unit_value_var.set("")
        
        # Clear hourly values
        for var in self.hourly_vars:
            var.set("")
        
        # Clear results
        self.target_label.config(text="")
        for widget in self.results_frame.winfo_children():
            widget.destroy()
    
    def calculate(self):
        try:
            # Get input values
            cycle_time = float(self.cycle_time_var.get())
            num_heads = float(self.num_heads_var.get())
            unit_value = float(self.unit_value_var.get())
            
            # Calculate hourly target: (3600/cycle_time) * num_heads, rounded to nearest whole number
            hourly_target = round((3600 / cycle_time) * num_heads)
            
            # Display hourly target
            self.target_label.config(text=str(hourly_target))
            
            # Clear previous results
            for widget in self.results_frame.winfo_children():
                widget.destroy()
            
            # Calculate and display results for each hourly value
            total_actual = 0
            completed_hours = 0
            for i, hourly_var in enumerate(self.hourly_vars):
                hourly_value_str = hourly_var.get().strip()
                if hourly_value_str:  # Only process non-empty values
                    hourly_value = float(hourly_value_str)
                    
                    # Calculate actual value: unit_value * hourly_value
                    actual_value = unit_value * hourly_value
                    total_actual += actual_value
                    completed_hours += 1
                    
                    # Calculate percentage of target, rounded to nearest whole number
                    percentage = round((actual_value / hourly_target) * 100)

                    # Calculate difference from target
                    difference = round(actual_value - hourly_target)
                    
                    # Determine background color based on percentage
                    bg_color = "#90EE90" if percentage >= 92 else "#FFB6C1"  # Light green or light red
                    
                    # Display results
                    row = i
                    ttk.Label(self.results_frame, text=f"Hour {i+1}:").grid(row=row, column=0, sticky=tk.W, pady=1)
                    ttk.Label(self.results_frame, text=f"{int(actual_value)}").grid(row=row, column=1, sticky=tk.W, pady=1)
                    ttk.Label(self.results_frame, text=f"{difference:+d}").grid(row=row, column=3, sticky=tk.W, pady=1)
                    
                    # Create percentage label with colored background
                    percentage_label = tk.Label(self.results_frame, text=f"{percentage}%", background=bg_color, 
                                              relief="solid", borderwidth=1)
                    percentage_label.grid(row=row, column=2, sticky=tk.W, pady=1, padx=2)

            if completed_hours:
                total_target = hourly_target * completed_hours
                total_difference = round(total_actual - total_target)
                total_percentage = round((total_actual / total_target) * 100)
                total_bg_color = "#90EE90" if total_percentage >= 92 else "#FFB6C1"
                total_row = len(self.hourly_vars)

                ttk.Separator(self.results_frame, orient=tk.HORIZONTAL).grid(
                    row=total_row, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(6, 3)
                )
                ttk.Label(self.results_frame, text="Totals", font=("Arial", 9, "bold")).grid(
                    row=total_row + 1, column=0, sticky=tk.W, pady=1
                )
                ttk.Label(self.results_frame, text=f"{int(total_actual)}", font=("Arial", 9, "bold")).grid(
                    row=total_row + 1, column=1, sticky=tk.W, pady=1
                )
                total_percentage_label = tk.Label(
                    self.results_frame,
                    text=f"{total_percentage}%",
                    background=total_bg_color,
                    relief="solid",
                    borderwidth=1,
                    font=("Arial", 9, "bold"),
                )
                total_percentage_label.grid(row=total_row + 1, column=2, sticky=tk.W, pady=1, padx=2)
                ttk.Label(self.results_frame, text=f"{total_difference:+d}", font=("Arial", 9, "bold")).grid(
                    row=total_row + 1, column=3, sticky=tk.W, pady=1
                )
                    
        except ValueError as e:
            # Clear results and show error
            self.target_label.config(text="Error: Please enter valid numbers")
            for widget in self.results_frame.winfo_children():
                widget.destroy()
            ttk.Label(self.results_frame, text="Invalid input values", foreground="red").grid(row=0, column=0, pady=5)
        except ZeroDivisionError:
            # Handle division by zero
            self.target_label.config(text="Error: Cycle time cannot be zero")
            for widget in self.results_frame.winfo_children():
                widget.destroy()
            ttk.Label(self.results_frame, text="Cycle time must be greater than 0", foreground="red").grid(row=0, column=0, pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = ProductionCalculator(root)
    root.mainloop()
