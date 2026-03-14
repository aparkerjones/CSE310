import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk
from typing import Optional

from fishing_tracker.database import FishingRepository


DATE_HELPER = "Use a real date in YYYY-MM-DD (example: 2026-03-14)"


class FishingApp:
    def __init__(self) -> None:
        """Set up the window, wire up the database, and load the initial catch list."""
        self.repo = FishingRepository()
        self.selected_id: Optional[int] = None

        self.root = tk.Tk()
        self.root.title("Idaho Fishing Catch Tracker")
        self.root.geometry("1080x640")

        self._build_layout()
        self._refresh_records()

    def _build_layout(self) -> None:
        """Set up the tabbed layout with Catches and Records tabs."""
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)

        # --- Catches tab ---
        catches_tab = ttk.Frame(notebook, padding=12)
        notebook.add(catches_tab, text="Catches")

        left = ttk.Frame(catches_tab)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 12))

        right = ttk.Frame(catches_tab)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.catch_date_var = tk.StringVar()
        self.water_body_var = tk.StringVar()
        self.county_var = tk.StringVar()
        self.species_var = tk.StringVar()
        self.size_in_var = tk.StringVar()
        self.notes_var = tk.StringVar()

        self.filter_start_var = tk.StringVar()
        self.filter_end_var = tk.StringVar()

        self.total_label_var = tk.StringVar(value="Total catches in current view: 0")

        self._build_form(left)
        self._build_filter(right)
        self._build_grid(right)

        # --- Records tab ---
        records_tab = ttk.Frame(notebook, padding=12)
        notebook.add(records_tab, text="Records")
        self._build_records_tab(records_tab)

    def _build_form(self, parent: ttk.Frame) -> None:
        """Build the left-side entry form and action buttons."""
        ttk.Label(parent, text="Catch Entry", font=("Segoe UI", 12, "bold")).pack(anchor=tk.W)

        form = ttk.Frame(parent)
        form.pack(fill=tk.X, pady=(8, 12))

        self._labeled_entry(form, "Catch date", self.catch_date_var)
        ttk.Label(form, text=DATE_HELPER, foreground="#555555").pack(anchor=tk.W, pady=(0, 8))

        self._labeled_entry(form, "Water body", self.water_body_var)
        self._labeled_entry(form, "County", self.county_var)
        self._labeled_entry(form, "Species", self.species_var)
        self._labeled_entry(form, "Size in inches (whole number)", self.size_in_var)
        self._labeled_entry(form, "Notes", self.notes_var)

        actions = ttk.Frame(parent)
        actions.pack(fill=tk.X)

        ttk.Button(actions, text="Insert", command=self._insert_record).pack(fill=tk.X, pady=2)
        ttk.Button(actions, text="Update", command=self._update_record).pack(fill=tk.X, pady=2)
        ttk.Button(actions, text="Delete", command=self._delete_record).pack(fill=tk.X, pady=2)
        ttk.Button(actions, text="Clear Form", command=self._clear_form).pack(fill=tk.X, pady=2)

    def _build_filter(self, parent: ttk.Frame) -> None:
        """Build the date filter controls and the total fish count label at the top of the results panel."""
        filter_card = ttk.Frame(parent)
        filter_card.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(filter_card, text="Date Filter", font=("Segoe UI", 11, "bold")).grid(row=0, column=0, columnspan=3, sticky=tk.W)

        ttk.Label(filter_card, text="Start date").grid(row=1, column=0, sticky=tk.W, pady=(8, 4))
        ttk.Entry(filter_card, textvariable=self.filter_start_var, width=16).grid(row=1, column=1, sticky=tk.W, pady=(8, 4), padx=(6, 0))

        ttk.Label(filter_card, text="End date").grid(row=2, column=0, sticky=tk.W, pady=4)
        ttk.Entry(filter_card, textvariable=self.filter_end_var, width=16).grid(row=2, column=1, sticky=tk.W, pady=4, padx=(6, 0))

        ttk.Label(filter_card, text=DATE_HELPER, foreground="#555555").grid(row=3, column=0, columnspan=2, sticky=tk.W, pady=(2, 6))

        ttk.Button(filter_card, text="Apply Filter", command=self._refresh_records).grid(row=1, column=2, rowspan=2, padx=(10, 0), sticky=tk.NS)
        ttk.Button(filter_card, text="Reset Filter", command=self._clear_filter).grid(row=3, column=2, padx=(10, 0), sticky=tk.EW)

        ttk.Label(filter_card, textvariable=self.total_label_var, font=("Segoe UI", 10, "bold")).grid(row=4, column=0, columnspan=3, sticky=tk.W, pady=(8, 0))

    def _build_grid(self, parent: ttk.Frame) -> None:
        """Set up the catch table with columns, widths, and a row-click binding."""
        columns = ("id", "date", "water", "county", "species", "size", "notes")
        self.tree = ttk.Treeview(parent, columns=columns, show="headings", height=20)

        headings = {
            "id": "ID",
            "date": "Date",
            "water": "Water Body",
            "county": "County",
            "species": "Species",
            "size": "Size (in)",
            "notes": "Notes",
        }

        widths = {
            "id": 52,
            "date": 98,
            "water": 180,
            "county": 130,
            "species": 140,
            "size": 72,
            "notes": 300,
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(col, width=widths[col], anchor=tk.W)

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self._on_row_select)

    def _labeled_entry(self, parent: ttk.Frame, label: str, var: tk.StringVar) -> None:
        """Add a label + text entry pair to the form."""
        ttk.Label(parent, text=label).pack(anchor=tk.W)
        ttk.Entry(parent, textvariable=var, width=30).pack(anchor=tk.W, pady=(0, 8))

    def _insert_record(self) -> None:
        """Validate the form and add the new catch to the database."""
        payload = self._validated_payload()
        if payload is None:
            return

        self.repo.add_catch(*payload)
        self._clear_form()
        self._refresh_records()

    def _update_record(self) -> None:
        """Validate the form and save changes to the selected catch."""
        if self.selected_id is None:
            messagebox.showwarning("No selection", "Select a row before trying to update.")
            return

        payload = self._validated_payload()
        if payload is None:
            return

        self.repo.update_catch(self.selected_id, *payload)
        self._clear_form()
        self._refresh_records()

    def _delete_record(self) -> None:
        """Ask for confirmation, then remove the selected catch."""
        if self.selected_id is None:
            messagebox.showwarning("No selection", "Select a row before trying to delete.")
            return

        should_delete = messagebox.askyesno("Delete record", "Delete selected catch record?")
        if not should_delete:
            return

        self.repo.delete_catch(self.selected_id)
        self._clear_form()
        self._refresh_records()

    def _validated_payload(self) -> Optional[tuple]:
        """Check that all required fields are filled in and valid, then return them as a tuple."""
        catch_date = self.catch_date_var.get().strip()
        water_body = self.water_body_var.get().strip()
        county = self.county_var.get().strip()
        species = self.species_var.get().strip()
        size_text = self.size_in_var.get().strip()
        notes = self.notes_var.get().strip()

        if not catch_date or not water_body or not county or not species or not size_text:
            messagebox.showerror("Missing fields", "Fill in date, water body, county, species, and size.")
            return None

        if not self._looks_like_date(catch_date):
            messagebox.showerror("Bad date", "Date must use YYYY-MM-DD format.")
            return None

        if not size_text.isdigit() or int(size_text) < 1:
            messagebox.showerror("Bad size", "Size must be a whole number in inches (example: 18).")
            return None

        size_in = int(size_text)

        return catch_date, water_body, county, species, size_in, notes

    def _refresh_records(self) -> None:
        """Reload the catch list from the database and update the total fish count."""
        start_date = self.filter_start_var.get().strip() or None
        end_date = self.filter_end_var.get().strip() or None

        if start_date and not self._looks_like_date(start_date):
            messagebox.showerror("Bad start date", "Start date must use YYYY-MM-DD.")
            return
        if end_date and not self._looks_like_date(end_date):
            messagebox.showerror("Bad end date", "End date must use YYYY-MM-DD.")
            return

        records = self.repo.list_catches(start_date, end_date)

        # Wipe the existing rows before filling in fresh results.
        for row in self.tree.get_children():
            self.tree.delete(row)

        for record in records:
            self.tree.insert(
                "",
                tk.END,
                iid=str(record.id),
                values=(
                    record.id,
                    record.catch_date,
                    record.water_body,
                    record.county,
                    record.species,
                    str(int(record.size_in)),
                    record.notes,
                ),
            )

        total = self.repo.total_catches(start_date, end_date)
        self.total_label_var.set(f"Total catches in current view: {total}")

    def _on_row_select(self, _event: object) -> None:
        """When a row is clicked, copy its data into the entry form."""
        selected = self.tree.selection()
        if not selected:
            return

        # Pull the row values and populate each form field.
        row = self.tree.item(selected[0], "values")
        self.selected_id = int(row[0])
        self.catch_date_var.set(row[1])
        self.water_body_var.set(row[2])
        self.county_var.set(row[3])
        self.species_var.set(row[4])
        self.size_in_var.set(row[5])
        self.notes_var.set(row[6])

    def _clear_form(self) -> None:
        """Blank out the form and deselect any highlighted row."""
        self.selected_id = None
        self.catch_date_var.set("")
        self.water_body_var.set("")
        self.county_var.set("")
        self.species_var.set("")
        self.size_in_var.set("")
        self.notes_var.set("")
        self.tree.selection_remove(self.tree.selection())

    def _clear_filter(self) -> None:
        """Clear the date filters and show all records again."""
        self.filter_start_var.set("")
        self.filter_end_var.set("")
        self._refresh_records()

    @staticmethod
    def _looks_like_date(value: str) -> bool:
        """Return True only for real calendar dates in YYYY-MM-DD format."""
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def _build_records_tab(self, parent: ttk.Frame) -> None:
        """Build the records viewer with water body / date filters and a results table."""
        self.rec_water_var = tk.StringVar()
        self.rec_start_var = tk.StringVar()
        self.rec_end_var = tk.StringVar()

        filter_card = ttk.Frame(parent)
        filter_card.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(filter_card, text="Records", font=("Segoe UI", 12, "bold")).grid(row=0, column=0, columnspan=5, sticky=tk.W, pady=(0, 8))

        ttk.Label(filter_card, text="Water body (blank = state-wide)").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(filter_card, textvariable=self.rec_water_var, width=24).grid(row=1, column=1, sticky=tk.W, padx=(6, 16))

        ttk.Label(filter_card, text="Start date").grid(row=1, column=2, sticky=tk.W)
        ttk.Entry(filter_card, textvariable=self.rec_start_var, width=14).grid(row=1, column=3, sticky=tk.W, padx=(6, 0))

        ttk.Label(filter_card, text="End date").grid(row=2, column=2, sticky=tk.W, pady=(6, 0))
        ttk.Entry(filter_card, textvariable=self.rec_end_var, width=14).grid(row=2, column=3, sticky=tk.W, padx=(6, 0), pady=(6, 0))

        ttk.Label(filter_card, text=DATE_HELPER, foreground="#555555").grid(row=3, column=2, columnspan=2, sticky=tk.W, padx=(6, 0), pady=(2, 0))

        ttk.Button(filter_card, text="Check Records", command=self._check_records).grid(row=1, column=4, rowspan=2, padx=(14, 0), sticky=tk.NS)

        self._build_records_grid(parent)

    def _build_records_grid(self, parent: ttk.Frame) -> None:
        """Set up the records results table."""
        cols = ("water", "species", "size")
        self.rec_tree = ttk.Treeview(parent, columns=cols, show="headings", height=22)

        self.rec_tree.heading("water", text="Water Body")
        self.rec_tree.heading("species", text="Species")
        self.rec_tree.heading("size", text="Record Size (in)")

        self.rec_tree.column("water", width=240, anchor=tk.W)
        self.rec_tree.column("species", width=200, anchor=tk.W)
        self.rec_tree.column("size", width=140, anchor=tk.W)

        self.rec_tree.pack(fill=tk.BOTH, expand=True)

    def _check_records(self) -> None:
        """Query for the biggest fish per species and populate the records table."""
        water_body = self.rec_water_var.get().strip() or None
        start_date = self.rec_start_var.get().strip() or None
        end_date = self.rec_end_var.get().strip() or None

        if start_date and not self._looks_like_date(start_date):
            messagebox.showerror("Bad start date", "Start date must use YYYY-MM-DD.")
            return
        if end_date and not self._looks_like_date(end_date):
            messagebox.showerror("Bad end date", "End date must use YYYY-MM-DD.")
            return

        records = self.repo.get_records(water_body, start_date, end_date)

        for row in self.rec_tree.get_children():
            self.rec_tree.delete(row)

        for entry in records:
            self.rec_tree.insert(
                "",
                tk.END,
                values=(entry.water_body, entry.species, str(int(entry.record_size_in))),
            )

    def run(self) -> None:
        """Hand control to Tkinter and show the window."""
        self.root.mainloop()
