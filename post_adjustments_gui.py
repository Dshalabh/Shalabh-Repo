import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
import os

class PostAdjustmentsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Post-Adjustments Data Manager")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f0f0f0')

        # Data storage
        self.data = []
        self.original_data = []
        self.headers = ["Account", "Description", "Debit", "Credit", "Balance", "Adjustment", "Final Balance"]

        # Initialize with sample data
        self.load_sample_data()

        # Create main interface
        self.create_widgets()
        self.populate_tree()

    def load_sample_data(self):
        """Load sample Post-Adjustments data"""
        self.data = [
            ["1001", "Cash", "5000.00", "", "5000.00", "500.00", "5500.00"],
            ["1100", "Accounts Receivable", "3200.00", "", "3200.00", "-200.00", "3000.00"],
            ["1200", "Inventory", "8500.00", "", "8500.00", "300.00", "8800.00"],
            ["2001", "Accounts Payable", "", "2500.00", "-2500.00", "100.00", "-2400.00"],
            ["2100", "Notes Payable", "", "5000.00", "-5000.00", "", "-5000.00"],
            ["3001", "Owner's Equity", "", "8000.00", "-8000.00", "200.00", "-7800.00"],
            ["4001", "Revenue", "", "15000.00", "-15000.00", "1000.00", "-14000.00"],
            ["5001", "Cost of Goods Sold", "6000.00", "", "6000.00", "-300.00", "6300.00"],
            ["6001", "Operating Expenses", "4200.00", "", "4200.00", "150.00", "4050.00"],
            ["6100", "Depreciation Expense", "800.00", "", "800.00", "50.00", "850.00"]
        ]
        self.original_data = [row[:] for row in self.data]  # Deep copy

    def create_widgets(self):
        """Create all GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Title
        title_label = ttk.Label(main_frame, text="Post-Adjustments Data Manager",
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Control panel
        control_frame = ttk.LabelFrame(main_frame, text="Controls", padding="10")
        control_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 10))

        # Buttons
        ttk.Button(control_frame, text="Add Entry", command=self.add_entry).grid(row=0, column=0, padx=5)
        ttk.Button(control_frame, text="Edit Entry", command=self.edit_entry).grid(row=0, column=1, padx=5)
        ttk.Button(control_frame, text="Delete Entry", command=self.delete_entry).grid(row=0, column=2, padx=5)
        ttk.Button(control_frame, text="Calculate Totals", command=self.calculate_totals).grid(row=0, column=3, padx=5)
        ttk.Button(control_frame, text="Export CSV", command=self.export_csv).grid(row=0, column=4, padx=5)
        ttk.Button(control_frame, text="Reset Data", command=self.reset_data).grid(row=0, column=5, padx=5)

        # Search frame
        search_frame = ttk.Frame(control_frame)
        search_frame.grid(row=1, column=0, columnspan=6, pady=(10, 0), sticky=(tk.W, tk.E))

        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=(0, 5))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_data)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.grid(row=0, column=1, padx=5)

        # Data display area
        data_frame = ttk.LabelFrame(main_frame, text="Account Data", padding="10")
        data_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))
        data_frame.columnconfigure(0, weight=1)
        data_frame.rowconfigure(0, weight=1)

        # Treeview for data display
        self.tree = ttk.Treeview(data_frame, columns=self.headers, show='headings', height=15)

        # Configure columns
        for col in self.headers:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c))
            if col in ['Debit', 'Credit', 'Balance', 'Adjustment', 'Final Balance']:
                self.tree.column(col, width=100, anchor='e')
            elif col == 'Account':
                self.tree.column(col, width=80, anchor='center')
            else:
                self.tree.column(col, width=150, anchor='w')

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(data_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(data_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Grid scrollbars and treeview
        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        v_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        h_scrollbar.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # Summary panel
        summary_frame = ttk.LabelFrame(main_frame, text="Summary", padding="10")
        summary_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))

        self.summary_labels = {}
        labels = ['Total Debits:', 'Total Credits:', 'Total Adjustments:', 'Net Balance:']
        for i, label in enumerate(labels):
            ttk.Label(summary_frame, text=label).grid(row=0, column=i*2, padx=(0, 5), sticky='w')
            self.summary_labels[label] = ttk.Label(summary_frame, text="$0.00", font=("Arial", 10, "bold"))
            self.summary_labels[label].grid(row=0, column=i*2+1, padx=(0, 20), sticky='w')

        # Calculate initial totals
        self.calculate_totals()

    def populate_tree(self):
        """Populate the treeview with data"""
        # Clear existing data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add data
        for row in self.data:
            self.tree.insert('', 'end', values=row)

    def filter_data(self, *args):
        """Filter data based on search term"""
        search_term = self.search_var.get().lower()

        # Clear tree
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Add filtered data
        for row in self.data:
            if search_term == "" or any(search_term in str(cell).lower() for cell in row):
                self.tree.insert('', 'end', values=row)

    def sort_column(self, col):
        """Sort data by column"""
        col_index = self.headers.index(col)

        # Sort data
        try:
            # Try numeric sort for financial columns
            if col in ['Debit', 'Credit', 'Balance', 'Adjustment', 'Final Balance']:
                self.data.sort(key=lambda x: float(x[col_index].replace(',', '') or 0))
            else:
                self.data.sort(key=lambda x: x[col_index])
        except ValueError:
            # Fall back to string sort
            self.data.sort(key=lambda x: x[col_index])

        self.populate_tree()

    def add_entry(self):
        """Add a new entry"""
        self.entry_dialog("Add New Entry")

    def edit_entry(self):
        """Edit selected entry"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Selection Required", "Please select an entry to edit.")
            return

        item = selection[0]
        values = self.tree.item(item, 'values')
        self.entry_dialog("Edit Entry", values)

    def entry_dialog(self, title, values=None):
        """Show dialog for adding/editing entries"""
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()

        # Center the dialog
        dialog.geometry("+%d+%d" % (self.root.winfo_rootx() + 50, self.root.winfo_rooty() + 50))

        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill='both', expand=True)

        # Entry fields
        entries = {}
        for i, header in enumerate(self.headers):
            ttk.Label(main_frame, text=f"{header}:").grid(row=i, column=0, sticky='w', pady=5)
            entry = ttk.Entry(main_frame, width=20)
            entry.grid(row=i, column=1, sticky='ew', padx=(10, 0), pady=5)
            entries[header] = entry

            # Fill with existing values if editing
            if values and i < len(values):
                entry.insert(0, values[i])

        main_frame.columnconfigure(1, weight=1)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=len(self.headers), column=0, columnspan=2, pady=20)

        def save_entry():
            # Get values from entries
            new_values = [entries[header].get() for header in self.headers]

            # Validate account number
            if not new_values[0]:
                messagebox.showerror("Error", "Account number is required.")
                return

            if values:  # Editing
                # Find and update the row
                for i, row in enumerate(self.data):
                    if row == list(values):
                        self.data[i] = new_values
                        break
            else:  # Adding
                self.data.append(new_values)

            self.populate_tree()
            self.calculate_totals()
            dialog.destroy()

        ttk.Button(button_frame, text="Save", command=save_entry).pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side='left', padx=5)

    def delete_entry(self):
        """Delete selected entry"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Selection Required", "Please select an entry to delete.")
            return

        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected entry?"):
            item = selection[0]
            values = list(self.tree.item(item, 'values'))

            # Remove from data
            for i, row in enumerate(self.data):
                if row == values:
                    del self.data[i]
                    break

            self.populate_tree()
            self.calculate_totals()

    def calculate_totals(self):
        """Calculate and display summary totals"""
        total_debits = 0
        total_credits = 0
        total_adjustments = 0
        net_balance = 0

        for row in self.data:
            try:
                # Debit (index 2)
                if row[2]:
                    total_debits += float(row[2].replace(',', ''))

                # Credit (index 3)
                if row[3]:
                    total_credits += float(row[3].replace(',', ''))

                # Adjustment (index 5)
                if row[5]:
                    total_adjustments += float(row[5].replace(',', ''))

                # Final Balance (index 6)
                if row[6]:
                    net_balance += float(row[6].replace(',', ''))

            except (ValueError, IndexError):
                continue

        # Update summary labels
        self.summary_labels['Total Debits:'].config(text=f"${total_debits:,.2f}")
        self.summary_labels['Total Credits:'].config(text=f"${total_credits:,.2f}")
        self.summary_labels['Total Adjustments:'].config(text=f"${total_adjustments:,.2f}")
        self.summary_labels['Net Balance:'].config(text=f"${net_balance:,.2f}")

    def export_csv(self):
        """Export data to CSV file"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export to CSV"
        )

        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(self.headers)  # Write headers
                    writer.writerows(self.data)    # Write data

                messagebox.showinfo("Export Successful", f"Data exported to {filename}")

            except Exception as e:
                messagebox.showerror("Export Error", f"Error exporting data: {str(e)}")

    def reset_data(self):
        """Reset data to original state"""
        if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset all data to original state?"):
            self.data = [row[:] for row in self.original_data]  # Deep copy
            self.populate_tree()
            self.calculate_totals()
            messagebox.showinfo("Reset Complete", "Data has been reset to original state.")

def main():
    root = tk.Tk()
    app = PostAdjustmentsGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()