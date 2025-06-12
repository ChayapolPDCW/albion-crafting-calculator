import tkinter as tk
from tkinter import ttk, messagebox

FAME_TABLE = {
    "T4":      [180, 180, 180, 360, 540, 720],
    "T4.1":    [360, 360, 360, 720, 1080, 1440],
    "T4.2":    [720, 720, 720, 1440, 2160, 2880],
    "T4.3":    [1440, 1440, 1440, 2880, 4320, 5760],
    "T5":      [720, 720, 720, 1440, 2160, 2880],
    "T5.1":    [1440, 1440, 1440, 2880, 4320, 5760],
    "T5.2":    [2880, 2880, 2880, 5760, 8640, 11520],
    "T5.3":    [5760, 5760, 5760, 11520, 17280, 23040],
    "T6":      [2160, 2160, 2160, 4320, 6480, 8640],
    "T6.1":    [4320, 4320, 4320, 8640, 12960, 17280],
    "T6.2":    [8640, 8640, 8640, 17280, 25920, 34560],
    "T6.3":    [17280, 17280, 17280, 34560, 51840, 69120],
    "T7":      [5160, 5160, 5160, 10320, 15480, 20640],
    "T7.1":    [10320, 10320, 10320, 20640, 30960, 41280],
    "T7.2":    [20640, 20640, 20640, 41280, 61920, 82560],
    "T7.3":    [41280, 41280, 41280, 82560, 123840, 165120],
    "T8":      [11160, 11160, 11160, 22320, 33480, 44640],
    "T8.1":    [22320, 22320, 22320, 44640, 66860, 89280],
    "T8.2":    [44640, 44640, 44640, 89280, 133920, 178560],
    "T8.3":    [89280, 89280, 89280, 178560, 267840, 357120],
}
ITEM_TYPES = ["Helmet", "Shoes", "Offhand/Capes", "Armor/Bags", "Weapon 1H", "Weapon 2H"]
TIERS = list(FAME_TABLE.keys())

EMPTY_BOOK_FAME_TABLE = {
    "T4": 3600,
    "T5": 7200,
    "T6": 14400,
    "T7": 28380,
    "T8": 58590,
}

def get_fame_from_table(tier, item_type):
    idx = ITEM_TYPES.index(item_type)
    return FAME_TABLE[tier][idx]

def calculate_cost(res1_p, res1_q, res2_p, res2_q, res3_p, res3_q, nutrition_cost, item_value, rrr, full_book_price, empty_book_price, fame_from_craft, empty_book_fame):
    tax = ((nutrition_cost * item_value) / 44.44) / 20
    book_filled = fame_from_craft / empty_book_fame if empty_book_fame else 0
    total_resource_cost = (
        res1_p * res1_q +
        res2_p * res2_q +
        res3_p * res3_q
    ) * ((100 - rrr) / 100)
    book_profit = book_filled * (full_book_price - empty_book_price)
    cc = total_resource_cost + tax - book_profit
    return cc

class AlbionCraftGUI:
    def __init__(self, root):
        self.root = root
        root.title("Albion Crafting Calculator")

        # Resource Inputs
        for i in range(1, 4):
            tk.Label(root, text=f"Resource{i}_Price:").grid(row=i-1, column=0)
            setattr(self, f"res{i}_p", tk.Entry(root))
            getattr(self, f"res{i}_p").grid(row=i-1, column=1)
            tk.Label(root, text=f"Resource{i}_Qty:").grid(row=i-1, column=2)
            setattr(self, f"res{i}_q", tk.Entry(root))
            getattr(self, f"res{i}_q").grid(row=i-1, column=3)

        # Nutrition cost, item value, RRR
        tk.Label(root, text="Nutrition_cost:").grid(row=3, column=0)
        self.nutrition_cost = tk.Entry(root)
        self.nutrition_cost.grid(row=3, column=1)

        tk.Label(root, text="Item_value:").grid(row=3, column=2)
        self.item_value = tk.Entry(root)
        self.item_value.grid(row=3, column=3)

        tk.Label(root, text="RRR (%):").grid(row=4, column=0)
        self.rrr = tk.Entry(root)
        self.rrr.grid(row=4, column=1)

        # Drop-downs for Tier and Item Type
        tk.Label(root, text="Tier:").grid(row=5, column=0)
        self.tier_var = tk.StringVar(value=TIERS[0])
        self.tier_menu = ttk.Combobox(root, textvariable=self.tier_var, values=TIERS, state="readonly")
        self.tier_menu.grid(row=5, column=1)

        tk.Label(root, text="Item Type:").grid(row=5, column=2)
        self.item_type_var = tk.StringVar(value=ITEM_TYPES[0])
        self.item_type_menu = ttk.Combobox(root, textvariable=self.item_type_var, values=ITEM_TYPES, state="readonly")
        self.item_type_menu.grid(row=5, column=3)

        # Book prices and fame
        tk.Label(root, text="Full_book_price:").grid(row=6, column=0)
        self.full_book_price = tk.Entry(root)
        self.full_book_price.grid(row=6, column=1)

        tk.Label(root, text="Empty_book_price:").grid(row=6, column=2)
        self.empty_book_price = tk.Entry(root)
        self.empty_book_price.grid(row=6, column=3)

        # เพิ่ม drop-down สำหรับ empty_book_fame (แสดงเป็น T4-T8)
        tk.Label(root, text="Empty_book_fame:").grid(row=7, column=0)
        self.empty_book_fame_var = tk.StringVar()
        self.empty_book_fame_menu = ttk.Combobox(
            root,
            textvariable=self.empty_book_fame_var,
            values=list(EMPTY_BOOK_FAME_TABLE.keys()),
            state="readonly"
        )
        self.empty_book_fame_menu.grid(row=7, column=1)

        # Fame from craft (auto)
        tk.Label(root, text="Fame from craft:").grid(row=7, column=2)
        self.fame_from_craft = tk.StringVar()
        self.fame_label = tk.Label(root, textvariable=self.fame_from_craft)
        self.fame_label.grid(row=7, column=3)

        # Update fame and empty_book_fame when dropdown changes
        self.tier_menu.bind("<<ComboboxSelected>>", self.update_fame_and_journal)
        self.item_type_menu.bind("<<ComboboxSelected>>", self.update_fame_and_journal)
        self.update_fame_and_journal()

        # Calculate button
        self.calc_btn = tk.Button(root, text="Calculate", command=self.calculate)
        self.calc_btn.grid(row=8, column=0, columnspan=2)

        # Result
        self.result_var = tk.StringVar()
        tk.Label(root, textvariable=self.result_var, font=("Arial", 14)).grid(row=8, column=2, columnspan=2)

    def update_fame_and_journal(self, event=None):
        try:
            fame = get_fame_from_table(self.tier_var.get(), self.item_type_var.get())
            self.fame_from_craft.set(str(fame))
        except Exception:
            self.fame_from_craft.set("0")
        
        tier_main = self.tier_var.get().split('.')[0]
        if tier_main in EMPTY_BOOK_FAME_TABLE:
            self.empty_book_fame_var.set(tier_main)
        else:
            self.empty_book_fame_var.set("T4")

    def calculate(self):
        try:
            res1_p = float(self.res1_p.get() or 0)
            res1_q = float(self.res1_q.get() or 0)
            res2_p = float(self.res2_p.get() or 0)
            res2_q = float(self.res2_q.get() or 0)
            res3_p = float(self.res3_p.get() or 0)
            res3_q = float(self.res3_q.get() or 0)
            nutrition_cost = float(self.nutrition_cost.get() or 0)
            item_value = float(self.item_value.get() or 0)
            rrr = float(self.rrr.get() or 0)
            full_book_price = float(self.full_book_price.get() or 0)
            empty_book_price = float(self.empty_book_price.get() or 0)
            fame_from_craft = float(self.fame_from_craft.get() or 0)
            empty_book_fame_key = self.empty_book_fame_var.get()
            empty_book_fame = EMPTY_BOOK_FAME_TABLE.get(empty_book_fame_key, 1)
            cc = calculate_cost(
                res1_p, res1_q, res2_p, res2_q, res3_p, res3_q,
                nutrition_cost, item_value, rrr,
                full_book_price, empty_book_price,
                fame_from_craft, empty_book_fame
            )
            self.result_var.set(f"Crafting Cost: {cc:.2f}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = AlbionCraftGUI(root)
    root.mainloop()
