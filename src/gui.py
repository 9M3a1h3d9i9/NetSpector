# In the name of Allah 

# این کد یک رابط کاربری کامل با قابلیت اجرای تست، نمایش نتایج و مدیریت threadها ایجاد می‌کند.

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
from datetime import datetime

# Import our own modules
from tester import NetworkTester
from storage import ResultStorage

class NetSpectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NetSpector - Network Monitoring Tool")
        self.root.geometry("800x700")  # Set initial window size

        self.tester = NetworkTester()
        self.storage = ResultStorage()
        self.is_testing = False

        self.setup_gui()
        self.load_history()

    def setup_gui(self):
        # Create main frames
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Input Frame
        input_frame = ttk.LabelFrame(main_frame, text="Test Configuration", padding="5")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(input_frame, text="Connection Name:").grid(row=0, column=0, sticky=tk.W, padx=5)
        self.connection_var = tk.StringVar(value="My-Connection")
        connection_entry = ttk.Entry(input_frame, textvariable=self.connection_var, width=30)
        connection_entry.grid(row=0, column=1, padx=5)

        ttk.Label(input_frame, text="Ping Count:").grid(row=1, column=0, sticky=tk.W, padx=5)
        self.ping_count_var = tk.IntVar(value=10)
        ping_spinbox = ttk.Spinbox(input_frame, from_=5, to=50, textvariable=self.ping_count_var, width=10)
        ping_spinbox.grid(row=1, column=1, sticky=tk.W, padx=5)

        # Button Frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        self.test_button = ttk.Button(button_frame, text="Run Full Test", command=self.start_test_thread)
        self.test_button.pack(side=tk.LEFT, padx=5)

        self.ping_only_button = ttk.Button(button_frame, text="Ping Test Only", command=lambda: self.start_test_thread(ping_only=True))
        self.ping_only_button.pack(side=tk.LEFT, padx=5)

        # Progress Frame
        self.progress_frame = ttk.Frame(main_frame)
        self.progress_frame.grid(row=2, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        # 
        self.progress_frame.grid_remove()  # Hide initially

        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X)

        # Results Frame
        results_frame = ttk.LabelFrame(main_frame, text="Test Results", padding="5")
        results_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        # Create text widget for results
        self.results_text = scrolledtext.ScrolledText(results_frame, height=12, width=75)
        self.results_text.pack(fill=tk.BOTH, expand=True)

        # History Frame
        history_frame = ttk.LabelFrame(main_frame, text="Test History", padding="5")
        history_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        # Create treeview for history
        columns = ('timestamp', 'connection', 'latency', 'download', 'upload')
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show='headings', height=6)

        # Define headings
        self.history_tree.heading('timestamp', text='Timestamp')
        self.history_tree.heading('connection', text='Connection')
        self.history_tree.heading('latency', text='Latency (ms)')
        self.history_tree.heading('download', text='Download (Mbps)')
        self.history_tree.heading('upload', text='Upload (Mbps)')

        # Define columns
        self.history_tree.column('timestamp', width=150)
        self.history_tree.column('connection', width=120)
        self.history_tree.column('latency', width=100)
        self.history_tree.column('download', width=100)
        self.history_tree.column('upload', width=100)

        # Add scrollbar
        history_scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=history_scrollbar.set)

        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        history_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure grid weights for resizing
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        main_frame.rowconfigure(4, weight=1)

    def start_test_thread(self, ping_only=False):
        """Start the test in a separate thread to prevent GUI freezing."""
        if self.is_testing:
            messagebox.showwarning("Warning", "A test is already running!")
            return

        self.is_testing = True
        # self.progress_frame.pack()  # Show progress bar
        self.progress_frame.grid() # Show progress bar
        self.progress_bar.start()
        self.test_button.config(state='disabled')
        self.ping_only_button.config(state='disabled')

        # Start the test in a new thread
        thread = threading.Thread(target=self.run_test, args=(ping_only,))
        thread.daemon = True
        thread.start()

    def run_test(self, ping_only):
        """Run the network test (called from the thread)."""
        try:
            connection_name = self.connection_var.get()
            ping_count = self.ping_count_var.get()

            # Run ping test
            self.update_results("Running ping test...\n")
            ping_results = self.tester.run_ping_test(count=ping_count)

            speed_results = None
            if not ping_only:
                # Run speed test
                self.update_results("Running speed test...\n")
                speed_results = self.tester.run_speed_test()
            else:
                speed_results = {'download_speed': 0.0, 'upload_speed': 0.0}

            # Save results
            self.update_results("Saving results...\n")
            self.storage.save_result(connection_name, ping_results, speed_results)

            # Display results
            self.update_results("\n=== TEST RESULTS ===\n")
            self.update_results(f"Connection: {connection_name}\n")
            self.update_results(f"Avg Latency: {ping_results['avg_latency']:.2f} ms\n")
            self.update_results(f"Min Latency: {ping_results['min_latency']:.2f} ms\n")
            self.update_results(f"Max Latency: {ping_results['max_latency']:.2f} ms\n")
            self.update_results(f"Jitter: {ping_results['jitter']:.2f} ms\n")
            self.update_results(f"Packet Loss: {ping_results['packet_loss']:.0f}%\n")
            
            if not ping_only:
                self.update_results(f"Download Speed: {speed_results['download_speed']} Mbps\n")
                self.update_results(f"Upload Speed: {speed_results['upload_speed']} Mbps\n")

            # Reload history
            self.load_history()

        except Exception as e:
            error_msg = f"Error during test: {str(e)}\n"
            self.update_results(error_msg)
            messagebox.showerror("Error", error_msg)
        finally:
            # Schedule GUI updates in the main thread
            self.root.after(0, self.test_complete)

    def test_complete(self):
        """Clean up after test completion."""
        self.progress_bar.stop()
        # self.progress_frame.pack_forget()  # Hide progress bar
        self.progress_frame.grid_remove() # Hide progress bar
        self.test_button.config(state='normal')
        self.ping_only_button.config(state='normal')
        self.is_testing = False

    def update_results(self, message):
        """Update the results text widget (thread-safe)."""
        def _update():
            self.results_text.insert(tk.END, message)
            self.results_text.see(tk.END)
        self.root.after(0, _update)

    def load_history(self):
        """Load and display test history."""
        # Clear current treeview
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        # Load results from storage
        results = self.storage.load_results()

        # Add results to treeview (show latest first)
        for result in reversed(results[-10:]):  # Show last 10 results
            timestamp = result['timestamp']
            try:
                # Format timestamp for display
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                formatted_time = dt.strftime("%Y-%m-%d %H:%M")
            except:
                formatted_time = timestamp[:16]  # Fallback

            self.history_tree.insert('', tk.END, values=(
                formatted_time,
                result['connection_name'],
                f"{result['ping']['avg_latency']:.1f}",
                f"{result['speed']['download_speed']}",
                f"{result['speed']['upload_speed']}"
            ))

def main():
    """Main function to run the GUI application."""
    root = tk.Tk()
    app = NetSpectorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()