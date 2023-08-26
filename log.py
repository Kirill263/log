import tkinter as tk
from tkinter import ttk
import win32evtlog
import win32evtlogutil

def view_event_log():
    event_type = event_type_entry.get()
    error_code = error_code_entry.get()
    selected_log = log_choice.get()

    hand = win32evtlog.OpenEventLog(None, selected_log)
    num_records = win32evtlog.GetNumberOfEventLogRecords(hand)

    flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
    total_records = 0
    record_number = 1

    while True:
        events = win32evtlog.ReadEventLog(hand, flags, 0)
        if not events:
            break

        for event in events:
            total_records += 1

            if event_type and event.EventType != int(event_type):
                continue

            if error_code and event.EventID != int(error_code):
                continue

            if selected_log == "System":
                event_dict = win32evtlogutil.SafeFormatMessage(event, "System")
            elif selected_log == "Application":
                event_dict = win32evtlogutil.SafeFormatMessage(event, "Application")
            elif selected_log == "Security":
                event_dict = win32evtlogutil.SafeFormatMessage(event, "Security")

            log_text.insert(tk.END, f"Запись #{record_number}:\n")
            log_text.insert(tk.END, f"Источник: {event_dict}\n")
            log_text.insert(tk.END, f"Идентификатор события: {event_dict}\n")
            log_text.insert(tk.END, f"Описание: {event_dict}\n")
            log_text.insert(tk.END, "-----------------\n")
            record_number += 1

    win32evtlog.CloseEventLog(hand)
    log_text.insert(tk.END, f"Всего записей: {total_records}\n")

window = tk.Tk()
window.title("Просмотр журнала событий")
window.geometry("1280x800")

input_frame = tk.Frame(window)
input_frame.pack(pady=10, anchor="w")

output_frame = tk.Frame(window, bg="white", bd=1, relief=tk.SOLID)
output_frame.pack(fill=tk.BOTH, expand=True)

log_text = tk.Text(output_frame, height=30, width=80, font=("Courier New", 10))
log_text.pack(fill=tk.BOTH, expand=True)

log_choice_label = tk.Label(input_frame, text="Журнал событий:")
log_choice_label.grid(row=0, column=0, sticky="w")
log_choice = tk.StringVar()
log_dropdown = ttk.Combobox(input_frame, textvariable=log_choice, values=["System", "Application", "Security"])
log_dropdown.grid(row=0, column=1, sticky="w")

event_type_label = tk.Label(input_frame, text="Тип события:")
event_type_label.grid(row=1, column=0, sticky="w")
event_type_entry = tk.Entry(input_frame)
event_type_entry.grid(row=1, column=1, sticky="w")

error_code_label = tk.Label(input_frame, text="Код ошибки:")
error_code_label.grid(row=2, column=0, sticky="w")
error_code_entry = tk.Entry(input_frame)
error_code_entry.grid(row=2, column=1, sticky="w")

view_button = tk.Button(input_frame, text="Просмотреть", command=view_event_log)
view_button.grid(row=3, column=0, columnspan=2)

window.mainloop()
