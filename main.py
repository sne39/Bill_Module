import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime

class BillingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Billing Software")

        # Basic Information About Firm
        self.firm_name = "XYZ Company"
        self.firm_address = "ABC Street, City"
        self.firm_phone = "1234567890"
        firm_info_label = tk.Label(root, text=f"Firm Name: {self.firm_name}\nAddress: {self.firm_address}\nPhone: {self.firm_phone}")
        firm_info_label.grid(row=0, column=0, columnspan=6)

        # Buttons
        tk.Button(root, text="Add Item", command=self.add_item).grid(row=1, column=0)
        tk.Button(root, text="Calculate", command=self.calculate_total).grid(row=1, column=1)
        tk.Button(root, text="Print", command=self.print_bill).grid(row=1, column=2)

        # Bill total with GST label
        self.bill_total_label = tk.Label(root, text="Bill total (with GST tax): ")
        self.bill_total_label.grid(row=2, column=0, columnspan=6)

        # Labels
        labels = ["Sr no", "Item/Particulars", "Item Code", "Quantity", "Price", "Taxes", "Total Without taxes"]
        for i, label_text in enumerate(labels):
            tk.Label(root, text=label_text).grid(row=3, column=i)

        # Entry fields
        self.entries = {}
        self.total_labels = {}  # Initialize total_labels dictionary
        self.item_count = 4  # To keep track of the number of items
        self.add_item()

        # Bill Information
        bill_info_label = tk.Label(root, text="Bill Information")
        bill_info_label.grid(row=self.item_count + 1, column=0, columnspan=6)

    def add_item(self):
        for j, label_text in enumerate(["Sr no", "Item/Particulars", "Item Code", "Quantity", "Price", "Taxes"]):
            entry_key = f"{label_text}{self.item_count}"
            self.entries[entry_key] = tk.Entry(self.root)
            self.entries[entry_key].grid(row=self.item_count, column=j)

        # Total Without Taxes Label
        total_without_tax_label = tk.Label(self.root, text="0.00")
        total_without_tax_label.grid(row=self.item_count, column=len(["Sr no", "Item/Particulars", "Item Code", "Quantity", "Price", "Taxes"]))
        self.total_labels[f'total_without_tax_{self.item_count}'] = total_without_tax_label

        self.item_count += 1

    def calculate_total(self):
        total_with_taxes = 0
        total_without_taxes = 0
        for i in range(4, self.item_count):
            try:
                price = float(self.entries[f"Price{i}"].get())
                quantity = float(self.entries[f"Quantity{i}"].get())
                taxes = float(self.entries[f"Taxes{i}"].get())
                total_without_tax = price * quantity
                total_without_taxes += total_without_tax
                total_with_taxes += total_without_tax * (1 + taxes / 100)
                self.total_labels[f'total_without_tax_{i}'].config(text=f"{total_without_tax:.2f}")
            except ValueError:
                pass
        self.bill_total_label.config(text=f"Bill total (with GST tax): {total_with_taxes:.2f}")

    def print_bill(self):
        bill_details = ""
        bill_details += "Sr no\tItem/Particulars\tItem Code\tQuantity\tPrice\tTaxes\n"
        for i in range(4, self.item_count):
            item_details = []
            for label_text in ["Sr no", "Item/Particulars", "Item Code", "Quantity", "Price", "Taxes"]:
                item_details.append(self.entries[f"{label_text}{i}"].get())
            bill_details += "\t".join(item_details) + "\n"

        # Display firm details
        bill_details += f"\nFirm Name: {self.firm_name}\n"
        bill_details += f"Address: {self.firm_address}\n"
        bill_details += f"Phone: {self.firm_phone}\n"

        # Display total amount
        total_amount = self.bill_total_label.cget("text")
        bill_details += f"\nTotal Amount: {total_amount}\n"

        # Display bill details in a messagebox
        messagebox.showinfo("Bill Details", bill_details)

        # Save bill in daily sales report
        self.save_daily_sales_report(bill_details)

    def save_daily_sales_report(self, bill_details):
        # Create or append to the daily sales report CSV file
        filename = "daily_sales_report.csv"
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Bill Number", "Firm Name", "Item/Particulars", "Item Code", "Quantity", "Price", "Taxes", "Total Without taxes", "Bill total(with gst tax)"])
            date_today = datetime.now().strftime("%Y-%m-%d")
            bill_number = datetime.now().strftime("%Y%m%d%H%M%S")
            firm_name = self.firm_name
            for i in range(4, self.item_count):
                item_details = []
                for label_text in ["Sr no", "Item/Particulars", "Item Code", "Quantity", "Price", "Taxes"]:
                    item_details.append(self.entries[f"{label_text}{i}"].get())
                writer.writerow([date_today, bill_number, firm_name] + item_details)

if __name__ == "__main__":
    root = tk.Tk()
    app = BillingApp(root)
    root.mainloop()
