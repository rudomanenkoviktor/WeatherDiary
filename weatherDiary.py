import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary - Дневник погоды")
        self.root.geometry("850x650")
        
        self.entries = []
        self.current_filter = "all"
        self.filter_temp_min = None
        self.filter_temp_max = None
        self.filter_date_value = None
        
        self.create_input_frame()
        self.create_list_frame()
        self.create_filter_frame()
        self.create_button_frame()
        
        self.load_from_file()
        
    def create_input_frame(self):
        input_frame = ttk.LabelFrame(self.root, text="Добавить новую запись", padding=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.date_entry = ttk.Entry(input_frame, width=20)
        self.date_entry.grid(row=0, column=1, padx=5, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        ttk.Label(input_frame, text="Температура (°C):").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.temp_entry = ttk.Entry(input_frame, width=10)
        self.temp_entry.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(input_frame, text="Описание:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.desc_entry = ttk.Entry(input_frame, width=50)
        self.desc_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5)
        
        self.precip_var = tk.BooleanVar()
        ttk.Checkbutton(input_frame, text="Осадки", variable=self.precip_var).grid(row=2, column=0, columnspan=2, sticky="w", padx=5, pady=5)
        
        ttk.Button(input_frame, text="Добавить запись", command=self.add_entry).grid(row=2, column=2, columnspan=2, pady=5)
        
    def create_filter_frame(self):
        filter_frame = ttk.LabelFrame(self.root, text="Фильтрация записей", padding=10)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Фильтр по дате:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_date = ttk.Entry(filter_frame, width=15)
        self.filter_date.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(filter_frame, text="Применить", command=self.filter_by_date).grid(row=0, column=2, padx=5)
        ttk.Button(filter_frame, text="Сбросить", command=self.reset_filter).grid(row=0, column=3, padx=5)
        
        ttk.Label(filter_frame, text="Фильтр по температуре:").grid(row=1, column=0, padx=5, pady=5)
        self.filter_temp_min_entry = ttk.Entry(filter_frame, width=8)
        self.filter_temp_min_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Label(filter_frame, text="до").grid(row=1, column=2)
        self.filter_temp_max_entry = ttk.Entry(filter_frame, width=8)
        self.filter_temp_max_entry.grid(row=1, column=3, padx=5, pady=5)
        ttk.Button(filter_frame, text="Применить", command=self.filter_by_temp).grid(row=1, column=4, padx=5)
        
    def create_list_frame(self):
        list_frame = ttk.LabelFrame(self.root, text="Список записей", padding=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        columns = ("date", "temperature", "description", "precipitation")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        self.tree.heading("date", text="Дата")
        self.tree.heading("temperature", text="Температура (°C)")
        self.tree.heading("description", text="Описание")
        self.tree.heading("precipitation", text="Осадки")
        
        self.tree.column("date", width=120)
        self.tree.column("temperature", width=100)
        self.tree.column("description", width=350)
        self.tree.column("precipitation", width=80)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
    def create_button_frame(self):
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Button(button_frame, text="Сохранить в JSON", command=self.save_to_file).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Загрузить из JSON", command=self.load_from_file).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Очистить всё", command=self.clear_all).pack(side="left", padx=5)
        
        self.status_label = ttk.Label(button_frame, text="Готов", relief="sunken")
        self.status_label.pack(side="right", padx=5, fill="x", expand=True)
        
    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
            
    def add_entry(self):
        date = self.date_entry.get().strip()
        temp = self.temp_entry.get().strip()
        description = self.desc_entry.get().strip()
        precipitation = "Да" if self.precip_var.get() else "Нет"
        
        if not self.validate_date(date):
            messagebox.showerror("Ошибка", "Неверный формат даты!\nИспользуйте ГГГГ-ММ-ДД")
            return
            
        try:
            temp_float = float(temp)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом!")
            return
            
        if not description:
            messagebox.showerror("Ошибка", "Описание не может быть пустым!")
            return
            
        entry = {
            "date": date,
            "temperature": temp_float,
            "description": description,
            "precipitation": precipitation
        }
        
        self.entries.append(entry)
        self.update_display()
        
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precip_var.set(False)
        
        self.status_label.config(text=f"Добавлена запись за {date}")
        
    def update_display(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        filtered_entries = self.get_filtered_entries()
        
        for entry in filtered_entries:
            self.tree.insert("", "end", values=(
                entry["date"],
                entry["temperature"],
                entry["description"],
                entry["precipitation"]
            ))
            
        self.status_label.config(text=f"Показано записей: {len(filtered_entries)} из {len(self.entries)}")
        
    def get_filtered_entries(self):
        if self.current_filter == "by_date":
            return [e for e in self.entries if e["date"] == self.filter_date_value]
        elif self.current_filter == "by_temp":
            result = self.entries
            if self.filter_temp_min is not None:
                result = [e for e in result if e["temperature"] >= self.filter_temp_min]
            if self.filter_temp_max is not None:
                result = [e for e in result if e["temperature"] <= self.filter_temp_max]
            return result
        else:
            return self.entries
            
    def filter_by_date(self):
        date = self.filter_date.get().strip()
        if not date:
            messagebox.showwarning("Предупреждение", "Введите дату для фильтрации")
            return
            
        if not self.validate_date(date):
            messagebox.showerror("Ошибка", "Неверный формат даты для фильтра!")
            return
            
        self.filter_date_value = date
        self.current_filter = "by_date"
        self.update_display()
        self.status_label.config(text=f"Фильтр по дате: {date}")
        
    def filter_by_temp(self):
        min_temp_str = self.filter_temp_min_entry.get().strip()
        max_temp_str = self.filter_temp_max_entry.get().strip()
        
        if not min_temp_str and not max_temp_str:
            messagebox.showwarning("Предупреждение", "Введите хотя бы одно значение температуры")
            return
            
        try:
            self.filter_temp_min = float(min_temp_str) if min_temp_str else None
            self.filter_temp_max = float(max_temp_str) if max_temp_str else None
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом!")
            return
            
        self.current_filter = "by_temp"
        self.update_display()
        
        if self.filter_temp_min is not None and self.filter_temp_max is not None:
            self.status_label.config(text=f"Фильтр по температуре: от {self.filter_temp_min} до {self.filter_temp_max}")
        elif self.filter_temp_min is not None:
            self.status_label.config(text=f"Фильтр по температуре: выше {self.filter_temp_min}")
        else:
            self.status_label.config(text=f"Фильтр по температуре: ниже {self.filter_temp_max}")
        
    def reset_filter(self):
        self.current_filter = "all"
        self.filter_date.delete(0, tk.END)
        self.filter_temp_min_entry.delete(0, tk.END)
        self.filter_temp_max_entry.delete(0, tk.END)
        self.filter_date_value = None
        self.filter_temp_min = None
        self.filter_temp_max = None
        self.update_display()
        self.status_label.config(text="Фильтры сброшены")
        
    def save_to_file(self):
        filename = "weather_data.json"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.entries, f, ensure_ascii=False, indent=2)
            self.status_label.config(text=f"Сохранено в {filename}")
            messagebox.showinfo("Успех", f"Данные сохранены в {filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")
            
    def load_from_file(self):
        filename = "weather_data.json"
        if not os.path.exists(filename):
            messagebox.showwarning("Предупреждение", f"Файл {filename} не найден")
            return
            
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    messagebox.showwarning("Предупреждение", "Файл пуст, создана новая запись")
                    self.entries = []
                else:
                    self.entries = json.loads(content)
            self.reset_filter()
            self.status_label.config(text=f"Загружено из {filename}")
            messagebox.showinfo("Успех", f"Загружено {len(self.entries)} записей")
        except json.JSONDecodeError:
            messagebox.showerror("Ошибка", "Файл JSON повреждён! Создана новая запись.")
            self.entries = []
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить: {e}")
            
    def clear_all(self):
        if messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить ВСЕ записи?"):
            self.entries = []
            self.reset_filter()
            self.status_label.config(text="Все записи удалены")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
