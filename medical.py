import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
import random
import os
import tempfile


class MedicalBillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("💊 Medical Billing System")
        self.root.geometry("700x500")

        # Variables
        self.customer_name = tk.StringVar()
        self.customer_phone = tk.StringVar()
        self.total_price = 0
        self.items = []
        self.bill_number = random.randint(1000, 9999)

        # 🧍 Customer Frame
        customer_frame = tk.LabelFrame(root, text="Customer Details", padx=10, pady=10, font=("Arial", 12))
        customer_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(customer_frame, text="Name:").grid(row=0, column=0, sticky=tk.W)
        tk.Entry(customer_frame, textvariable=self.customer_name, width=30).grid(row=0, column=1)

        tk.Label(customer_frame, text="Phone:").grid(row=1, column=0, sticky=tk.W)
        tk.Entry(customer_frame, textvariable=self.customer_phone, width=30).grid(row=1, column=1)

        # 💊 Item Frame
        item_frame = tk.LabelFrame(root, text="Add Medicine", padx=10, pady=10, font=("Arial", 12))
        item_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(item_frame, text="Item Name:").grid(row=0, column=0, sticky=tk.W)
        self.item_name = tk.Entry(item_frame)
        self.item_name.grid(row=0, column=1)

        tk.Label(item_frame, text="Price (₹):").grid(row=1, column=0, sticky=tk.W)
        self.item_price = tk.Entry(item_frame)
        self.item_price.grid(row=1, column=1)

        tk.Label(item_frame, text="Quantity:").grid(row=2, column=0, sticky=tk.W)
        self.item_quantity = tk.Entry(item_frame)
        self.item_quantity.grid(row=2, column=1)

        tk.Button(item_frame, text="➕ Add Item", command=self.add_item, bg="#4CAF50", fg="white").grid(row=3, column=1, pady=10)

        # 🔘 Action Buttons
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="🧾 Generate Bill", command=self.generate_bill, bg="#2196F3", fg="white", width=15).grid(row=0, column=0, padx=10)
        tk.Button(button_frame, text="💾 Save Bill", command=self.save_bill, bg="#FF9800", fg="white", width=15).grid(row=0, column=1, padx=10)
        tk.Button(button_frame, text="♻️ Reset", command=self.reset_all, bg="#f44336", fg="white", width=15).grid(row=0, column=2, padx=10)
        tk.Button(button_frame, text="🖨️ Print", command=self.print_bill, bg="#9C27B0", fg="white", width=15).grid(row=0, column=3, padx=10)

        # ⏱️ Date-Time Label
        self.date_time_label = tk.Label(root, text=datetime.now().strftime('%d-%m-%Y %H:%M:%S'), font=("Arial", 10))
        self.date_time_label.pack()

        # 🧮 Total
        self.total_price_label = tk.Label(root, text="Total Price: ₹ 0.00", font=("Arial", 14, "bold"))
        self.total_price_label.pack(pady=5)

        # 📜 Scrollable Bill Output
        bill_frame = tk.Frame(root)
        bill_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        self.bill_text = tk.Text(bill_frame, font=("Courier", 10))
        self.bill_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(bill_frame, command=self.bill_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.bill_text.config(yscrollcommand=scrollbar.set)

    # ➕ Add Item Function
    def add_item(self):
        name = self.item_name.get()
        price = self.item_price.get()
        qty = self.item_quantity.get()

        if name and price and qty:
            try:
                price = float(price)
                qty = int(qty)
                total = price * qty
                self.items.append((name, price, qty))
                self.total_price += total
                self.total_price_label.config(text=f"Total Price: ₹ {self.total_price:.2f}")
                self.item_name.delete(0, tk.END)
                self.item_price.delete(0, tk.END)
                self.item_quantity.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Input Error", "Please enter valid numbers for price and quantity.")
        else:
            messagebox.showerror("Missing Info", "Please fill in all item fields.")

    # 🧾 Generate Bill
    def generate_bill(self):
        if not self.customer_name.get() or not self.customer_phone.get() or not self.items:
            messagebox.showerror("Missing Info", "Please fill customer details and add at least one item.")
            return

        self.bill_text.delete("1.0", tk.END)
        self.bill_text.insert(tk.END, f"===== Medical Bill =====\n")
        self.bill_text.insert(tk.END, f"Bill No: {self.bill_number}\n")
        self.bill_text.insert(tk.END, f"Name: {self.customer_name.get()}\n")
        self.bill_text.insert(tk.END, f"Phone: {self.customer_phone.get()}\n")
        self.bill_text.insert(tk.END, f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n\n")
        self.bill_text.insert(tk.END, f"{'Item':<20}{'Price':<10}{'Qty':<10}{'Total':<10}\n")
        self.bill_text.insert(tk.END, "-"*60 + "\n")

        for item in self.items:
            name, price, qty = item
            total = price * qty
            self.bill_text.insert(tk.END, f"{name:<20}₹{price:<10.2f}{qty:<10}₹{total:<10.2f}\n")

        self.bill_text.insert(tk.END, "-"*60 + "\n")
        self.bill_text.insert(tk.END, f"{'Total':<40} ₹ {self.total_price:.2f}\n")
        self.bill_text.insert(tk.END, "="*60 + "\n")
        self.bill_text.insert(tk.END, f"Thank you! Visit again. 🙏\n")

    # 💾 Save Bill
    def save_bill(self):
        if not self.bill_text.get("1.0", tk.END).strip():
            messagebox.showerror("No Bill", "Please generate a bill first.")
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", title="Save Bill As", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w") as f:
                f.write(self.bill_text.get("1.0", tk.END))
            messagebox.showinfo("Saved", "Bill saved successfully!")

    # 🖨️ Print Bill
    def print_bill(self):
        if not self.bill_text.get("1.0", tk.END).strip():
            messagebox.showerror("No Bill", "Please generate a bill first.")
            return
        temp_file = tempfile.mktemp(".txt")
        with open(temp_file, "w") as f:
            f.write(self.bill_text.get("1.0", tk.END))
        os.startfile(temp_file, "print")  # Windows only

    # ♻️ Reset All
    def reset_all(self):
        self.customer_name.set("")
        self.customer_phone.set("")
        self.item_name.delete(0, tk.END)
        self.item_price.delete(0, tk.END)
        self.item_quantity.delete(0, tk.END)
        self.items = []
        self.total_price = 0
        self.bill_number = random.randint(1000, 9999)
        self.total_price_label.config(text="Total Price: ₹ 0.00")
        self.bill_text.delete("1.0", tk.END)


# 🔘 Start App
if __name__ == "__main__":
    root = tk.Tk()
    app = MedicalBillingApp(root)
    root.mainloop()














































