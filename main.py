import os
import csv
import tkinter as tk
from tkinter import messagebox

main_path = "C:/Users/ASUS/OneDrive/Desktop/Text"
folders = ["Spam", "Ham"]

def ensure_setup():
    os.makedirs(main_path, exist_ok=True)
    sample_texts = {
        "Spam": ["Win a free iPhone!", "You've been selected!", "Claim your reward now!"],
        "Ham": ["Meeting at 10?", "Can you send the file?", "I'll call you later."]
    }
    for folder in folders:
        folder_path = os.path.join(main_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        csv_path = os.path.join(folder_path, f"{folder.lower()}_data.csv")
        if not os.path.exists(csv_path):
            with open(csv_path, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(["Serial", "Text"])
                for i, msg in enumerate(sample_texts[folder], start=1):
                    writer.writerow([i, msg])

def show_training(category):
    csv_path = os.path.join(main_path, category, f"{category.lower()}_data.csv")
    if not os.path.exists(csv_path):
        messagebox.showerror("Error", f"{category} CSV not found.")
        return
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        messages = [row["Text"] for row in reader]

    win = tk.Toplevel()
    win.title(f"Training - {category}")
    tk.Label(win, text=f"Training on {category} Messages", font=("Arial", 14)).pack(pady=10)
    lb = tk.Listbox(win, width=50)
    lb.pack(padx=10, pady=10)
    for msg in messages:
        lb.insert(tk.END, msg)
    tk.Button(win, text="Close", command=win.destroy).pack(pady=10)

def train_window():
    win = tk.Toplevel()
    win.title("Choose Training Category")
    tk.Label(win, text="Select what to train:", font=("Arial", 12)).pack(pady=10)
    for folder in folders:
        tk.Button(win, text=f"Train {folder}", font=("Arial", 11),
                  command=lambda f=folder: show_training(f)).pack(pady=5)

def enter_text():
    def save_text():
        msg = text_box.get().strip()
        category = var.get()
        if not msg:
            messagebox.showwarning("Empty", "Please enter a message.")
            return
        csv_path = os.path.join(main_path, category, f"{category.lower()}_data.csv")
        try:
            with open(csv_path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                next_id = sum(1 for _ in reader)
        except:
            next_id = 1
        with open(csv_path, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([next_id, msg])
        answer = messagebox.askquestion("Saved", f"Saved to {category}. Add another?")
        if answer == 'yes':
            text_box.delete(0, tk.END)
        else:
            entry_win.destroy()

    entry_win = tk.Toplevel()
    entry_win.title("Add Text Message")
    tk.Label(entry_win, text="Enter message:", font=("Arial", 12)).pack(pady=5)
    text_box = tk.Entry(entry_win, width=40)
    text_box.pack(pady=5)
    var = tk.StringVar(entry_win)
    var.set(folders[0])
    tk.OptionMenu(entry_win, var, *folders).pack(pady=5)
    tk.Button(entry_win, text="Save", command=save_text).pack(pady=10)

def test_message():
    def classify_message():
        msg = input_box.get().strip()
        if not msg:
            messagebox.showwarning("Empty", "Enter text to classify.")
            return
        prediction = "Spam" if any(word in msg.lower() for word in ["win", "reward", "selected"]) else "Ham"
        messagebox.showinfo("Result", f"Prediction: {prediction}")
        test_win.destroy()

    test_win = tk.Toplevel()
    test_win.title("Test Message")
    tk.Label(test_win, text="Enter message to test:", font=("Arial", 12)).pack(pady=5)
    input_box = tk.Entry(test_win, width=40)
    input_box.pack(pady=5)
    tk.Button(test_win, text="Classify", command=classify_message).pack(pady=10)

ensure_setup()
root = tk.Tk()
root.title("Spam Detection System")
root.geometry("360x270")

tk.Button(root, text="Train", font=("Arial", 12), command=train_window).pack(pady=10)
tk.Button(root, text="Text", font=("Arial", 12), command=enter_text).pack(pady=10)
tk.Button(root, text="Test", font=("Arial", 12), command=test_message).pack(pady=10)

root.mainloop()
