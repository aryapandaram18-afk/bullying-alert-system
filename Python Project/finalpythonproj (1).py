import tkinter as tk
from tkinter import messagebox, scrolledtext, END
import re
from datetime import datetime
import os

# Configuration
BULlying_KEYWORDS = [
    'hate', 'stupid', 'ugly', 'fat', 'loser', 'idiot', 'freak', 'nerd', 'kill',
    'die', 'suicide', 'bully', 'harass', 'threat', 'abuse', 'trash', 'worthless',
    'disgusting', 'pathetic', 'failure', 'retard', 'cripple', 'bitch', 'asshole'
]
LOG_FILE = "bullying_incidents.log"
CHAT_HISTORY_FILE = "chat_history.log"

# Function to detect bullying
def detect_bullying(message):
    """Simple keyword-based detection for bullying language"""
    message_lower = message.lower()
    found_keywords = [word for word in BULlying_KEYWORDS if re.search(r'\b' + re.escape(word) + r'\b', message_lower)]
    return len(found_keywords) > 0, found_keywords

# Function to log incident
def log_incident(message, keywords, user):
    """Log bullying incident to file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"{timestamp} - Bullying detected from {user}: '{message}' (Keywords: {', '.join(keywords)})\n")

# Function to log chat history
def log_chat_message(user, message):
    """Log all chat messages to file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(CHAT_HISTORY_FILE, "a") as f:
        f.write(f"{timestamp} - {user}: {message}\n")

# Load chat history on startup
def load_chat_history(chat_log):
    """Load existing chat history into the chat log"""
    if os.path.exists(CHAT_HISTORY_FILE):
        try:
            with open(CHAT_HISTORY_FILE, "r") as f:
                for line in f:
                    parts = line.strip().split(" - ", 1)
                    if len(parts) == 2:
                        timestamp, msg = parts
                        user_msg = msg.split(": ", 1)
                        if len(user_msg) == 2:
                            user, message = user_msg
                            chat_log.config(state=tk.NORMAL)
                            chat_log.insert(END, f"[{timestamp.split()[1]}] {user}: {message}\n")
                            chat_log.config(state=tk.DISABLED)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load chat history: {e}")

# GUI Setup
class ChatMonitor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Anti-Cyberbullying Chat Monitor")
        self.root.geometry("600x500")
        self.root.configure(bg="#f0f4f8")  # Light blue-gray background
        
        # Main frame
        main_frame = tk.Frame(self.root, bg="#f0f4f8")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Chat display area
        self.chat_log = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=70, height=18, 
                                                bg="#ffffff", fg="#333333", font=("Arial", 12))
        self.chat_log.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.chat_log.config(state=tk.DISABLED)
        
        # Input frame with username
        input_frame = tk.Frame(main_frame, bg="#f0f4f8")
        input_frame.pack(padx=5, pady=5, fill=tk.X)
        
        tk.Label(input_frame, text="User:", bg="#f0f4f8", fg="#333333", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        self.user_entry = tk.Entry(input_frame, width=10, bg="#ffffff", fg="#333333", font=("Arial", 12))
        self.user_entry.pack(side=tk.LEFT, padx=5)
        self.user_entry.insert(0, "User1")  # Default user
        
        self.message_entry = tk.Entry(input_frame, width=40, bg="#ffffff", fg="#333333", 
                                   font=("Arial", 12), insertbackground="black")
        self.message_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.message_entry.bind('<Return>', self.send_message)
        
        send_btn = tk.Button(input_frame, text="Send", command=self.send_message, 
                           bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), 
                           activebackground="#45a049", padx=10, pady=2)
        send_btn.pack(side=tk.LEFT, padx=5)
        
        # Control frame
        control_frame = tk.Frame(main_frame, bg="#f0f4f8")
        control_frame.pack(padx=5, pady=5, fill=tk.X)
        
        clear_btn = tk.Button(control_frame, text="Clear Chat", command=self.clear_chat, 
                            bg="#f44336", fg="white", font=("Arial", 10, "bold"), 
                            activebackground="#da190b", padx=10, pady=2)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        report_btn = tk.Button(control_frame, text="View Reports", command=self.view_reports, 
                             bg="#2196F3", fg="white", font=("Arial", 10, "bold"), 
                             activebackground="#1976D2", padx=10, pady=2)
        report_btn.pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status = tk.Label(main_frame, text="Monitoring active...", bg="#e0e0e0", 
                             fg="#333333", font=("Arial", 10), anchor="w", pady=2)
        self.status.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        # Admin Console
        self.admin_window = tk.Toplevel(self.root)
        self.admin_window.title("Admin Monitor")
        self.admin_window.geometry("500x300")
        self.admin_window.configure(bg="#f0f4f8")
        
        self.admin_log = scrolledtext.ScrolledText(self.admin_window, wrap=tk.WORD, width=60, height=15, 
                                                 bg="#ffffff", fg="#333333", font=("Arial", 12))
        self.admin_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.admin_log.config(state=tk.DISABLED)
        
        # Load chat history
        load_chat_history(self.chat_log)
        self.add_to_chat("System", "Chat monitoring started. Welcome!")
    
    def add_to_chat(self, user, message, is_bullying=False):
        """Add message to chat log with color coding"""
        self.chat_log.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        color = "red" if is_bullying else "black"
        
        if is_bullying:
            self.chat_log.insert(END, f"[{timestamp}] {user}: {message} (🚨 BULLYING DETECTED 🚨)\n", color)
            self.admin_log.config(state=tk.NORMAL)
            self.admin_log.insert(END, f"[{timestamp}] ALERT: {user}: {message} (Keywords detected)\n", "red")
            self.admin_log.tag_config("red", foreground="red")
            self.admin_log.config(state=tk.DISABLED)
            messagebox.showwarning("Admin Alert", f"Bullying detected from {user}: {message}")
        else:
            self.chat_log.insert(END, f"[{timestamp}] {user}: {message}\n")
        
        self.chat_log.tag_config("red", foreground="red")
        self.chat_log.config(state=tk.DISABLED)
        self.chat_log.see(END)
        log_chat_message(user, message)
        self.status.config(text=f"Last update: {timestamp}")
    
    def send_message(self, event=None):
        """Send message and check for bullying"""
        message = self.message_entry.get().strip()
        user = self.user_entry.get().strip()
        if not message or not user:
            messagebox.showwarning("Input Error", "Please enter a user name and message!")
            return
        
        is_bullying, keywords = detect_bullying(message)
        
        if is_bullying:
            log_incident(message, keywords, user)
            self.add_to_chat(user, message, is_bullying=True)
        else:
            self.add_to_chat(user, message)
        
        self.message_entry.delete(0, END)
    
    def clear_chat(self):
        """Clear the chat log"""
        self.chat_log.config(state=tk.NORMAL)
        self.chat_log.delete(1.0, END)
        self.chat_log.config(state=tk.DISABLED)
        self.status.config(text="Chat cleared...")
    
    def view_reports(self):
        """View logged bullying incidents"""
        try:
            with open(LOG_FILE, "r") as f:
                logs = f.read()
            if logs:
                report_window = tk.Toplevel(self.root)
                report_window.title("Bullying Reports")
                report_window.geometry("450x350")
                report_window.configure(bg="#f0f4f8")
                
                report_text = scrolledtext.ScrolledText(report_window, wrap=tk.WORD, width=50, height=15,
                                                      bg="#ffffff", fg="#333333", font=("Arial", 12))
                report_text.pack(padx=10, pady=10)
                report_text.insert(END, logs)
                report_text.config(state=tk.DISABLED)
            else:
                messagebox.showinfo("Reports", "No bullying incidents logged yet.")
        except FileNotFoundError:
            messagebox.showinfo("Reports", "No bullying incidents logged yet.")
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()

# Run the application
if __name__ == "__main__":
    app = ChatMonitor()
    app.run()