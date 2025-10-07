import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib
matplotlib.use('Agg') # Use non-interactive backend for environments without a display
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import threading
from bias_generator import BiasGenerator
from stats_engine import StatisticalEngine
import json
import argparse
from datetime import datetime

class RandomnessReverseEngine:
    def __init__(self, root):
        self.root = root
        self.root.title("Stochastic Process Visualization Engine")
        self.root.geometry("1200x850")
        self.root.configure(bg='#1a1a2e')

        # Data storage
        self.data = []
        self.current_bias_id = None
        self.current_bias_name = ""
        self.statistical_results = {}
        self.bias_revealed = False

        # Initialize components
        self.bias_generator = BiasGenerator()
        self.stats_engine = StatisticalEngine()

        # Setup GUI
        self.setup_styles()
        self.create_widgets()

    def setup_styles(self):
        """Configure modern styling for ttk widgets"""
        style = ttk.Style()
        style.theme_use('clam')

        # Main styles
        style.configure('TLabel', background='#1a1a2e', foreground='white', font=('Segoe UI', 10))
        style.configure('Header.TLabel', background='#16213e', foreground='#ffffff', font=('Segoe UI', 14, 'bold'))
        style.configure('Stats.TLabel', font=('Segoe UI', 10), foreground='#ffffff', background='#16213e')
        style.configure('Title.TLabel', font=('Segoe UI', 24, 'bold'), foreground='#ffffff', background='#1a1a2e')

        # Button styling
        style.configure('TButton', background='#16213e', foreground='white', font=('Segoe UI', 10, 'bold'), padding=6)
        style.map('TButton', background=[('active', '#101828')], foreground=[('active', 'white')])

        # Result pass/fail styles
        style.configure('Pass.TLabel', background='#0f1419', foreground='#00b894', font=('Segoe UI', 10, 'bold'))
        style.configure('Fail.TLabel', background='#0f1419', foreground='#e17055', font=('Segoe UI', 10, 'bold'))

    def create_widgets(self):
        """Create and layout all GUI components"""
        main_frame = tk.Frame(self.root, bg='#1a1a2e')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        title_label = ttk.Label(main_frame, text="Stochastic Process Visualization Engine", style='Title.TLabel')
        title_label.pack(pady=(0, 20))

        self.create_control_panel(main_frame)
        content_frame = tk.Frame(main_frame, bg='#1a1a2e')
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.create_chart_panel(content_frame)
        self.create_stats_panel(content_frame)
        self.create_inference_panel(main_frame)

    def create_control_panel(self, parent):
        """Create the top control panel"""
        control_frame = tk.Frame(parent, bg='#16213e', relief=tk.RAISED, bd=2)
        control_frame.pack(fill=tk.X, pady=(0, 10))
        inner_frame = tk.Frame(control_frame, bg='#16213e')
        inner_frame.pack(fill=tk.X, padx=20, pady=15)

        self.generate_btn = ttk.Button(inner_frame, text="Generate Biased Data", command=self.generate_data)
        self.generate_btn.pack(side=tk.LEFT)

        self.bias_status_frame = tk.Frame(inner_frame, bg='#16213e')
        self.bias_status_frame.pack(side=tk.RIGHT)
        ttk.Label(self.bias_status_frame, text="Current Bias:", style='Header.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        self.bias_label = ttk.Label(self.bias_status_frame, text="None Generated", style='Header.TLabel')
        self.bias_label.pack(side=tk.LEFT)
        self.toggle_btn = ttk.Button(self.bias_status_frame, text="Reveal", command=self.toggle_bias_visibility, state=tk.DISABLED)
        self.toggle_btn.pack(side=tk.LEFT, padx=(10, 0))

    def create_chart_panel(self, parent):
        """Create the data visualization panel"""
        chart_frame = tk.Frame(parent, bg='#16213e', relief=tk.RAISED, bd=2)
        chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        header_frame = tk.Frame(chart_frame, bg='#16213e')
        header_frame.pack(fill=tk.X, padx=15, pady=10)
        ttk.Label(header_frame, text="Data Distribution", style='Header.TLabel').pack(side=tk.LEFT)
        self.chart_frame = tk.Frame(chart_frame, bg='#16213e')
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        self.create_empty_chart()

    def create_stats_panel(self, parent):
        """Create the statistical tests panel"""
        stats_frame = tk.Frame(parent, bg='#16213e', relief=tk.RAISED, bd=2)
        stats_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        header_frame = tk.Frame(stats_frame, bg='#16213e')
        header_frame.pack(fill=tk.X, padx=15, pady=10)
        ttk.Label(header_frame, text="Statistical Analysis", style='Header.TLabel').pack(side=tk.LEFT)
        self.stats_count_label = ttk.Label(header_frame, text="0/15 tests passed", style='Stats.TLabel')
        self.stats_count_label.pack(side=tk.RIGHT)
        self.create_stats_scrollable_area(stats_frame)

    def create_stats_scrollable_area(self, parent):
        """Create scrollable area for statistical test results"""
        container = tk.Frame(parent, bg='#16213e')
        container.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        canvas = tk.Canvas(container, bg='#16213e', highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        self.stats_scrollable_frame = tk.Frame(canvas, bg='#16213e')
        window = canvas.create_window((0, 0), window=self.stats_scrollable_frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self.stats_scrollable_frame.bind("<Configure>", on_frame_configure)

        def resize_canvas(event):
            canvas.itemconfig(window, width=event.width)
        container.bind("<Configure>", resize_canvas)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind("<MouseWheel>", _on_mousewheel)
        
        placeholder = tk.Label(self.stats_scrollable_frame, text="Generate data to see statistical analysis", font=('Segoe UI', 12), fg='#888888', bg='#16213e')
        placeholder.pack(pady=50)

    def create_inference_panel(self, parent):
        """Create the bias inference panel"""
        inference_frame = tk.Frame(parent, bg='#16213e', relief=tk.RAISED, bd=2)
        inference_frame.pack(fill=tk.X, pady=(10, 0))
        inner_frame = tk.Frame(inference_frame, bg='#16213e')
        inner_frame.pack(fill=tk.X, padx=20, pady=15)
        ttk.Label(inner_frame, text="Bias Inference Challenge", style='Header.TLabel').pack(anchor=tk.W, pady=(0, 10))
        
        controls_frame = tk.Frame(inner_frame, bg='#16213e')
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(controls_frame, text="Select your guess:", style='Stats.TLabel').pack(side=tk.LEFT, padx=(0, 10))
        
        self.bias_var = tk.StringVar()
        self.bias_dropdown = ttk.Combobox(controls_frame, textvariable=self.bias_var, values=self.bias_generator.get_bias_names(), state="readonly", width=40)
        self.bias_dropdown.pack(side=tk.LEFT, padx=(0, 10))
        self.bias_dropdown.set("Select bias pattern...")
        
        self.submit_btn = ttk.Button(controls_frame, text="Submit Guess", command=self.submit_inference, state=tk.DISABLED)
        self.submit_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        self.results_frame = tk.Frame(inner_frame, bg='#16213e')
        self.results_frame.pack(fill=tk.X, pady=(10, 0))

    def create_empty_chart(self):
        """Create an empty chart placeholder"""
        fig = Figure(figsize=(8, 6), facecolor='#16213e')
        ax = fig.add_subplot(111, facecolor='#16213e')
        ax.text(0.5, 0.5, "Generate data to see visualization", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes, fontsize=16, color='#888888')
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
        self.canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def generate_data(self):
        """Generate biased data and run analysis"""
        self.generate_btn.config(state=tk.DISABLED, text="Generating...")
        self.root.update()
        thread = threading.Thread(target=self._generate_data_thread)
        thread.daemon = True
        thread.start()

    def _generate_data_thread(self):
        """Thread function for data generation"""
        try:
            self.data, self.current_bias_id, self.current_bias_name = self.bias_generator.generate_biased_data()
            self.statistical_results = self.stats_engine.run_all_tests(self.data)
            self.root.after(0, self._update_gui_after_generation)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Data generation failed: {str(e)}"))
            self.root.after(0, lambda: self.generate_btn.config(state=tk.NORMAL, text="Generate Biased Data"))

    def _update_gui_after_generation(self):
        """Update GUI after data generation is complete"""
        self.bias_revealed = False
        self.generate_btn.config(state=tk.NORMAL, text="Generate Biased Data")
        self.toggle_btn.config(state=tk.NORMAL)
        self.submit_btn.config(state=tk.NORMAL)
        self.bias_label.config(text="Hidden")
        self.update_chart()
        self.update_statistics()
        for widget in self.results_frame.winfo_children():
            widget.destroy()

    def update_chart(self):
        """Update the data visualization chart"""
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        fig = Figure(figsize=(8, 6), facecolor='#16213e')
        ax = fig.add_subplot(111, facecolor='#16213e')
        ax.hist(self.data, bins=50, alpha=0.7, color='#6c5ce7', edgecolor='#a29bfe')
        ax.set_title('Data Distribution Histogram', color='white', fontsize=14, fontweight='bold')
        ax.set_xlabel('Value Range', color='white')
        ax.set_ylabel('Frequency', color='white')
        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('white')
            spine.set_alpha(0.3)
        fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_statistics(self):
        """Update the statistical test results display"""
        for widget in self.stats_scrollable_frame.winfo_children():
            widget.destroy()
        passed_tests = sum(1 for result in self.statistical_results.values() if result.get('passed', False))
        total_tests = len(self.statistical_results)
        self.stats_count_label.config(text=f"{passed_tests}/{total_tests} tests passed")
        for i, (test_name, result) in enumerate(self.statistical_results.items()):
            self.create_test_result_widget(self.stats_scrollable_frame, test_name, result, i)

    def create_test_result_widget(self, parent, test_name, result, index: int):
        """Create a widget for displaying a single test result"""
        bg_color = '#0f1419' if index % 2 == 0 else '#16213e'
        test_frame = tk.Frame(parent, bg=bg_color, relief=tk.FLAT, bd=1)
        test_frame.pack(fill=tk.X, padx=5, pady=2)
        info_frame = tk.Frame(test_frame, bg=bg_color)
        info_frame.pack(fill=tk.X, padx=10, pady=8)

        status_icon = "✔" if result.get('passed', False) else "✖"
        status_color = "#00b894" if result.get('passed', False) else "#e17055"
        
        name_label = tk.Label(info_frame, text=f"{status_icon} {test_name}", font=('Segoe UI', 10, 'bold'), fg='white', bg=bg_color)
        name_label.pack(side=tk.LEFT)
        
        value_text = f"{result.get('value', 'N/A')}"
        if isinstance(result.get('value'), float):
            value_text = f"{result.get('value'):.4f}"

        value_label = tk.Label(info_frame, text=value_text, font=('Segoe UI', 10, 'bold'), fg=status_color, bg=bg_color)
        value_label.pack(side=tk.RIGHT)
        
        if 'description' in result:
            desc_label = tk.Label(test_frame, text=result['description'], font=('Segoe UI', 8), fg='#888888', bg=bg_color, justify=tk.LEFT)
            desc_label.pack(side=tk.LEFT, padx=10, pady=(0, 8))

    def toggle_bias_visibility(self):
        """Toggle visibility of the current bias"""
        if self.bias_revealed:
            self.bias_label.config(text="Hidden")
            self.toggle_btn.config(text="Reveal")
            self.bias_revealed = False
        else:
            self.bias_label.config(text=self.current_bias_name)
            self.toggle_btn.config(text="Hide")
            self.bias_revealed = True

    def submit_inference(self):
        """Process the user's bias inference"""
        if not self.data:
            messagebox.showwarning("Warning", "Please generate data first!")
            return
        selected_bias = self.bias_var.get()
        if selected_bias == "Select bias pattern..." or not selected_bias:
            messagebox.showwarning("Warning", "Please select a bias pattern!")
            return
        results = self.calculate_inference_results(selected_bias)
        self.display_inference_results(results)
        self.bias_revealed = True
        self.bias_label.config(text=self.current_bias_name)
        self.toggle_btn.config(text="Hide")

    def calculate_inference_results(self, guessed_bias):
        """Calculate similarity score and inference quality"""
        bias_names = self.bias_generator.get_bias_names()
        guessed_bias_id = bias_names.index(guessed_bias) + 1
        is_correct = (guessed_bias_id == self.current_bias_id)

        if is_correct:
            similarity_score = 10.0
        else:
            passed_tests = sum(1 for result in self.statistical_results.values() if result.get('passed', False))
            total_tests = len(self.statistical_results)
            pass_rate = passed_tests / total_tests if total_tests > 0 else 0
            bias_distance = abs(guessed_bias_id - self.current_bias_id)
            distance_factor = max(0, 1 - bias_distance / 8)
            similarity_score = (distance_factor * 6) + (pass_rate * 4)
            similarity_score = max(0, min(10, similarity_score))

        if similarity_score >= 9:
            confidence = "Excellent"; confidence_color = "#00b894"
        elif similarity_score >= 7:
            confidence = "Good"; confidence_color = "#0984e3"
        elif similarity_score >= 5:
            confidence = "Fair"; confidence_color = "#fdcb6e"
        else:
            confidence = "Weak"; confidence_color = "#e17055"
            
        return {'guessed_bias': guessed_bias, 'actual_bias': self.current_bias_name, 'is_correct': is_correct, 'similarity_score': similarity_score, 'confidence': confidence, 'confidence_color': confidence_color}

    def display_inference_results(self, results):
        """Display the inference results"""
        for widget in self.results_frame.winfo_children():
            widget.destroy()

        results_container = tk.Frame(self.results_frame, bg='#0f1419', relief=tk.RAISED, bd=2)
        results_container.pack(fill=tk.X, pady=10)

        header_frame = tk.Frame(results_container, bg='#0f1419')
        header_frame.pack(fill=tk.X, padx=20, pady=(15, 10))

        result_text = "Correct!" if results['is_correct'] else "Incorrect"
        result_color = "#00b894" if results['is_correct'] else "#e17055"
        result_label = tk.Label(header_frame, text=f"Result: {result_text}", font=('Segoe UI', 14, 'bold'), fg=result_color, bg='#0f1419')
        result_label.pack(side=tk.LEFT)

        grid_frame = tk.Frame(results_container, bg='#0f1419')
        grid_frame.pack(fill=tk.X, padx=20, pady=10)
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)

        # Left Column
        left_frame = tk.Frame(grid_frame, bg='#0f1419')
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        ttk.Label(left_frame, text="Your Guess:", style='Stats.TLabel').pack(anchor=tk.W)
        tk.Label(left_frame, text=results['guessed_bias'], font=('Segoe UI', 10), fg='white', bg='#0f1419', wraplength=250, justify=tk.LEFT).pack(anchor=tk.W, pady=(2, 10))

        ttk.Label(left_frame, text="Actual Bias:", style='Stats.TLabel').pack(anchor=tk.W)
        tk.Label(left_frame, text=results['actual_bias'], font=('Segoe UI', 10), fg='white', bg='#0f1419', wraplength=250, justify=tk.LEFT).pack(anchor=tk.W, pady=(2, 10))

        # Right Column
        right_frame = tk.Frame(grid_frame, bg='#0f1419')
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        ttk.Label(right_frame, text="Similarity Score:", style='Stats.TLabel').pack(anchor=tk.W)
        score_text = f"{results['similarity_score']:.1f} / 10.0"
        tk.Label(right_frame, text=score_text, font=('Segoe UI', 10), fg='white', bg='#0f1419').pack(anchor=tk.W, pady=(2, 10))

        ttk.Label(right_frame, text="Inference Confidence:", style='Stats.TLabel').pack(anchor=tk.W)
        tk.Label(right_frame, text=results['confidence'], font=('Segoe UI', 10, 'bold'), fg=results['confidence_color'], bg='#0f1419').pack(anchor=tk.W, pady=(2, 10))

        # Separator
        separator = ttk.Separator(results_container, orient='horizontal')
        separator.pack(fill='x', padx=20, pady=10)

        # Save Button
        button_frame = tk.Frame(results_container, bg='#0f1419')
        button_frame.pack(pady=(0, 15))
        save_btn = ttk.Button(button_frame, text="Save Result", command=lambda: self.save_result(results))
        save_btn.pack()


    def save_result(self, results):
        """Save the inference result to a JSON file"""
        try:
            result_data = {
                'timestamp': datetime.now().isoformat(),
                'data_size': len(self.data),
                'guessed_bias': results['guessed_bias'],
                'actual_bias': results['actual_bias'],
                'is_correct': results['is_correct'],
                'similarity_score': results['similarity_score'],
                'confidence': results['confidence'],
                'statistical_tests': self.statistical_results
            }
            filename = f"inference_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, 'w') as f:
                json.dump(result_data, f, indent=2, default=str)
            messagebox.showinfo("Success", f"Result saved to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save result: {str(e)}")

def run_cli_mode(args):
    """Runs the application in command-line interface mode."""
    print("Running in Command-Line Interface (CLI) mode.")
    
    bias_gen = BiasGenerator()
    stats_eng = StatisticalEngine()

    if args.list_biases:
        print("\nAvailable bias patterns:")
        for i, name in bias_gen.BIAS_PATTERNS.items():
            print(f"  ID {i}: {name}")
        return

    print(f"\nGenerating {args.count} data points...")
    data, bias_id, bias_name = bias_gen.generate_biased_data(count=args.count, bias_id=args.bias_id)
    print(f"Generated data with bias: '{bias_name}' (ID: {bias_id})")

    print("\nRunning statistical analysis...")
    results = stats_eng.run_all_tests(data)

    print("\n--- Statistical Analysis Results ---")
    for test_name, result in results.items():
        passed = "PASSED" if result['passed'] else "FAILED"
        value = f"{result['value']:.4f}" if isinstance(result['value'], float) else result['value']
        print(f"  - {test_name:<25} | Value: {value:<15} | Status: {passed}")
    print("------------------------------------")

def main():
    """Main function to run GUI or CLI."""
    parser = argparse.ArgumentParser(description="Stochastic Process Visualization Engine")
    parser.add_argument('--cli', action='store_true', help='Run in command-line (headless) mode.')
    parser.add_argument('--count', type=int, default=1000, help='Number of data points to generate in CLI mode.')
    parser.add_argument('--bias-id', type=int, choices=range(1, 9), help='Specific bias ID to generate (1-8). Random if not specified.')
    parser.add_argument('--list-biases', action='store_true', help='List all available bias patterns and their IDs.')
    args = parser.parse_args()

    if args.cli or args.list_biases:
        run_cli_mode(args)
    else:
        try:
            # Attempt to create the main window. This will fail in a headless environment.
            root = tk.Tk()
            app = RandomnessReverseEngine(root)
            root.mainloop()
        except tk.TclError as e:
            if "no display name" in str(e):
                print("No display available. For headless operation, use the --cli flag.")
            else:
                raise

if __name__ == "__main__":
    main()
