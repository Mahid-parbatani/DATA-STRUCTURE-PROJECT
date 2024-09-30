import tkinter as tk
from tkinter import messagebox
from collections import deque
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class EventNode:
    def __init__(self, event_name, event_time):
        self.event_name = event_name
        self.event_time = event_time
        self.prev = None
        self.next = None

class EventList:
    def __init__(self):
        self.head = None
        self.tail = None
    
    def add_event(self, event_name, event_time):
        new_event = EventNode(event_name, event_time)
        if self.head is None:
            self.head = new_event
            self.tail = new_event
        else:
            current = self.head
            while current and current.event_time < event_time:
                current = current.next
            
            if current is None:
                new_event.prev = self.tail
                self.tail.next = new_event
                self.tail = new_event
            elif current == self.head:
                new_event.next = self.head
                self.head.prev = new_event
                self.head = new_event
            else:
                prev_node = current.prev
                prev_node.next = new_event
                new_event.prev = prev_node
                new_event.next = current
                current.prev = new_event
    
    def remove_event(self, event_name):
        current = self.head
        while current:
            if current.event_name == event_name:
                if current == self.head:
                    self.head = current.next
                    if self.head:
                        self.head.prev = None
                elif current == self.tail:
                    self.tail = current.prev
                    if self.tail:
                        self.tail.next = None
                else:
                    current.prev.next = current.next
                    current.next.prev = current.prev
                return True
            current = current.next
        return False

    def view_events(self):
        current = self.head
        events = []
        while current:
            events.append((current.event_name, current.event_time))
            current = current.next
        return events

class EventNotificationQueue:
    def __init__(self):
        self.queue = deque()
    
    def add_notification(self, event_name):
        self.queue.append(event_name)
    
    def notify_next_event(self):
        if self.queue:
            return self.queue.popleft()
        else:
            return None

class EventScheduler:
    def __init__(self):
        self.event_list = EventList()
        self.notification_queue = EventNotificationQueue()
    
    def schedule_event(self, event_name, event_time):
        self.event_list.add_event(event_name, event_time)
        self.notification_queue.add_notification(event_name)
    
    def cancel_event(self, event_name):
        return self.event_list.remove_event(event_name)
    
    def show_events(self):
        return self.event_list.view_events()
    
    def notify_upcoming_event(self):
        return self.notification_queue.notify_next_event()

class EventSchedulerGUI:
    def __init__(self, root):
        self.scheduler = EventScheduler()
        root.title("Event Scheduler")
        root.configure(bg="#ecf0f1")
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)
        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        button_style = {'font': ("Arial", 14), 'width': 15, 'height': 2}

        self.schedule_button = tk.Button(root, text="Schedule Event", command=self.open_schedule_window,
                                          bg="#3498db", fg="black", **button_style)
        self.schedule_button.grid(row=0, column=0, padx=5, pady=20)

        self.view_button = tk.Button(root, text="View Events", command=self.view_events,
                                      bg="#2ecc71", fg="black", **button_style)
        self.view_button.grid(row=0, column=1, padx=5, pady=20)

        self.cancel_button = tk.Button(root, text="Cancel Event", command=self.open_cancel_window,
                                       bg="#e74c3c", fg="black", **button_style)
        self.cancel_button.grid(row=1, column=0, padx=5, pady=20)

        self.notify_button = tk.Button(root, text="Notify Next Event", command=self.notify_event,
                                       bg="#f39c12", fg="black", **button_style)
        self.notify_button.grid(row=1, column=1, padx=5, pady=20)

        self.graph_button = tk.Button(root, text="Show Event Graph", command=self.show_graph,
                                       bg="#9b59b6", fg="black", **button_style)
        self.graph_button.grid(row=2, column=0, padx=5, pady=5)

    def open_schedule_window(self):
        schedule_window = tk.Toplevel()
        schedule_window.title("Schedule Event")
        schedule_window.configure(bg="#ecf0f1")
        event_name_label = tk.Label(schedule_window, text="Event Name:", bg="#ecf0f1")
        event_name_label.grid(row=0, column=0, padx=10, pady=10)
        event_name_entry = tk.Entry(schedule_window)
        event_name_entry.grid(row=0, column=1, padx=10, pady=10)
        event_time_label = tk.Label(schedule_window, text="Event Time (DD-MM-YYYY HH:MM):", bg="#ecf0f1")
        event_time_label.grid(row=1, column=0, padx=10, pady=10)
        event_time_entry = tk.Entry(schedule_window)
        event_time_entry.grid(row=1, column=1, padx=10, pady=10)

        def schedule_event_action():
            event_name = event_name_entry.get()
            event_time_str = event_time_entry.get()
            try:
                event_time = datetime.strptime(event_time_str, '%d-%m-%Y %H:%M')
                self.scheduler.schedule_event(event_name, event_time)
                messagebox.showinfo("Success", f"Event '{event_name}' scheduled for {event_time}.")
                schedule_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid date and time format (DD-MM-YYYY HH:MM).")

        schedule_button = tk.Button(schedule_window, text="Schedule", command=schedule_event_action,
                                    bg="#3498db", fg="black", font=("Arial", 14))
        schedule_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def open_cancel_window(self):
        cancel_window = tk.Toplevel()
        cancel_window.title("Cancel Event")
        cancel_window.configure(bg="#ecf0f1")
        cancel_event_label = tk.Label(cancel_window, text="Event Name to Cancel:", bg="#ecf0f1")
        cancel_event_label.grid(row=0, column=0, padx=10, pady=10)
        cancel_event_entry = tk.Entry(cancel_window)
        cancel_event_entry.grid(row=0, column=1, padx=10, pady=10)

        def cancel_event_action():
            event_name = cancel_event_entry.get()
            if self.scheduler.cancel_event(event_name):
                messagebox.showinfo("Success", f"Event '{event_name}' has been canceled.")
                cancel_window.destroy()
            else:
                messagebox.showerror("Error", f"Event '{event_name}' not found.")

        cancel_button = tk.Button(cancel_window, text="Cancel Event", command=cancel_event_action,
                                  bg="#e74c3c", fg="black", font=("Arial", 14))
        cancel_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def view_events(self):
        events = self.scheduler.show_events()
        if events:
            event_list = "\n".join([f"{name} at {time.strftime('%d-%m-%Y %H:%M')}" for name, time in events])
            messagebox.showinfo("Scheduled Events", event_list)
        else:
            messagebox.showinfo("Scheduled Events", "No events scheduled.")

    def notify_event(self):
        next_event = self.scheduler.notify_upcoming_event()
        if next_event:
            messagebox.showinfo("Notification", f"Upcoming event: '{next_event}' is happening soon!")
        else:
            messagebox.showinfo("Notification", "No upcoming events.")

    def show_graph(self):
        events = self.scheduler.show_events()
        if not events:
            messagebox.showinfo("No Events", "No events to display.")
            return

        event_names = [name for name, _ in events]
        event_times = [time for _, time in events]

        plt.figure(figsize=(10, 5))
        plt.barh(event_names, range(len(event_names)), color='skyblue')
        plt.xlabel('Event Index')
        plt.title('Scheduled Events')
        plt.xticks(range(len(event_names)), [time.strftime('%d-%m-%Y %H:%M') for time in event_times], rotation=45)
        
        plt.tight_layout()
        
        graph_window = tk.Toplevel()
        graph_window.title("Event Graph")
        canvas = FigureCanvasTkAgg(plt.gcf(), master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

root = tk.Tk()
app = EventSchedulerGUI(root)
root.mainloop()
import tkinter as tk
from tkinter import messagebox
from collections import deque
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class EventNode:
    def __init__(self, event_name, event_time):
        self.event_name = event_name
        self.event_time = event_time
        self.prev = None
        self.next = None

class EventList:
    def __init__(self):
        self.head = None
        self.tail = None
    
    def add_event(self, event_name, event_time):
        new_event = EventNode(event_name, event_time)
        if self.head is None:
            self.head = new_event
            self.tail = new_event
        else:
            current = self.head
            while current and current.event_time < event_time:
                current = current.next
            
            if current is None:
                new_event.prev = self.tail
                self.tail.next = new_event
                self.tail = new_event
            elif current == self.head:
                new_event.next = self.head
                self.head.prev = new_event
                self.head = new_event
            else:
                prev_node = current.prev
                prev_node.next = new_event
                new_event.prev = prev_node
                new_event.next = current
                current.prev = new_event
    
    def remove_event(self, event_name):
        current = self.head
        while current:
            if current.event_name == event_name:
                if current == self.head:
                    self.head = current.next
                    if self.head:
                        self.head.prev = None
                elif current == self.tail:
                    self.tail = current.prev
                    if self.tail:
                        self.tail.next = None
                else:
                    current.prev.next = current.next
                    current.next.prev = current.prev
                return True
            current = current.next
        return False

    def view_events(self):
        current = self.head
        events = []
        while current:
            events.append((current.event_name, current.event_time))
            current = current.next
        return events

class EventNotificationQueue:
    def __init__(self):
        self.queue = deque()
    
    def add_notification(self, event_name):
        self.queue.append(event_name)
    
    def notify_next_event(self):
        if self.queue:
            return self.queue.popleft()
        else:
            return None

class EventScheduler:
    def __init__(self):
        self.event_list = EventList()
        self.notification_queue = EventNotificationQueue()
    
    def schedule_event(self, event_name, event_time):
        self.event_list.add_event(event_name, event_time)
        self.notification_queue.add_notification(event_name)
    
    def cancel_event(self, event_name):
        return self.event_list.remove_event(event_name)
    
    def show_events(self):
        return self.event_list.view_events()
    
    def notify_upcoming_event(self):
        return self.notification_queue.notify_next_event()

class EventSchedulerGUI:
    def __init__(self, root):
        self.scheduler = EventScheduler()
        root.title("Event Scheduler")
        root.configure(bg="#ecf0f1")
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)
        root.grid_rowconfigure(2, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        button_style = {'font': ("Arial", 14), 'width': 15, 'height': 2}

        self.schedule_button = tk.Button(root, text="Schedule Event", command=self.open_schedule_window,
                                          bg="#3498db", fg="black", **button_style)
        self.schedule_button.grid(row=0, column=0, padx=5, pady=20)

        self.view_button = tk.Button(root, text="View Events", command=self.view_events,
                                      bg="#2ecc71", fg="black", **button_style)
        self.view_button.grid(row=0, column=1, padx=5, pady=20)

        self.cancel_button = tk.Button(root, text="Cancel Event", command=self.open_cancel_window,
                                       bg="#e74c3c", fg="black", **button_style)
        self.cancel_button.grid(row=1, column=0, padx=5, pady=20)

        self.notify_button = tk.Button(root, text="Notify Next Event", command=self.notify_event,
                                       bg="#f39c12", fg="black", **button_style)
        self.notify_button.grid(row=1, column=1, padx=5, pady=20)

        self.graph_button = tk.Button(root, text="Show Event Graph", command=self.show_graph,
                                       bg="#9b59b6", fg="black", **button_style)
        self.graph_button.grid(row=2, column=0, padx=5, pady=5)

    def open_schedule_window(self):
        schedule_window = tk.Toplevel()
        schedule_window.title("Schedule Event")
        schedule_window.configure(bg="#ecf0f1")
        event_name_label = tk.Label(schedule_window, text="Event Name:", bg="#ecf0f1")
        event_name_label.grid(row=0, column=0, padx=10, pady=10)
        event_name_entry = tk.Entry(schedule_window)
        event_name_entry.grid(row=0, column=1, padx=10, pady=10)
        event_time_label = tk.Label(schedule_window, text="Event Time (DD-MM-YYYY HH:MM):", bg="#ecf0f1")
        event_time_label.grid(row=1, column=0, padx=10, pady=10)
        event_time_entry = tk.Entry(schedule_window)
        event_time_entry.grid(row=1, column=1, padx=10, pady=10)

        def schedule_event_action():
            event_name = event_name_entry.get()
            event_time_str = event_time_entry.get()
            try:
                event_time = datetime.strptime(event_time_str, '%d-%m-%Y %H:%M')
                self.scheduler.schedule_event(event_name, event_time)
                messagebox.showinfo("Success", f"Event '{event_name}' scheduled for {event_time}.")
                schedule_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid date and time format (DD-MM-YYYY HH:MM).")

        schedule_button = tk.Button(schedule_window, text="Schedule", command=schedule_event_action,
                                    bg="#3498db", fg="black", font=("Arial", 14))
        schedule_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def open_cancel_window(self):
        cancel_window = tk.Toplevel()
        cancel_window.title("Cancel Event")
        cancel_window.configure(bg="#ecf0f1")
        cancel_event_label = tk.Label(cancel_window, text="Event Name to Cancel:", bg="#ecf0f1")
        cancel_event_label.grid(row=0, column=0, padx=10, pady=10)
        cancel_event_entry = tk.Entry(cancel_window)
        cancel_event_entry.grid(row=0, column=1, padx=10, pady=10)

        def cancel_event_action():
            event_name = cancel_event_entry.get()
            if self.scheduler.cancel_event(event_name):
                messagebox.showinfo("Success", f"Event '{event_name}' has been canceled.")
                cancel_window.destroy()
            else:
                messagebox.showerror("Error", f"Event '{event_name}' not found.")

        cancel_button = tk.Button(cancel_window, text="Cancel Event", command=cancel_event_action,
                                  bg="#e74c3c", fg="black", font=("Arial", 14))
        cancel_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    def view_events(self):
        events = self.scheduler.show_events()
        if events:
            event_list = "\n".join([f"{name} at {time.strftime('%d-%m-%Y %H:%M')}" for name, time in events])
            messagebox.showinfo("Scheduled Events", event_list)
        else:
            messagebox.showinfo("Scheduled Events", "No events scheduled.")

    def notify_event(self):
        next_event = self.scheduler.notify_upcoming_event()
        if next_event:
            messagebox.showinfo("Notification", f"Upcoming event: '{next_event}' is happening soon!")
        else:
            messagebox.showinfo("Notification", "No upcoming events.")

    def show_graph(self):
        events = self.scheduler.show_events()
        if not events:
            messagebox.showinfo("No Events", "No events to display.")
            return

        event_names = [name for name, _ in events]
        event_times = [time for _, time in events]

        plt.figure(figsize=(10, 5))
        plt.barh(event_names, range(len(event_names)), color='skyblue')
        plt.xlabel('Event Index')
        plt.title('Scheduled Events')
        plt.xticks(range(len(event_names)), [time.strftime('%d-%m-%Y %H:%M') for time in event_times], rotation=45)
        
        plt.tight_layout()
        
        graph_window = tk.Toplevel()
        graph_window.title("Event Graph")
        canvas = FigureCanvasTkAgg(plt.gcf(), master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack()

root = tk.Tk()
app = EventSchedulerGUI(root)
root.mainloop()


