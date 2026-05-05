import unittest
from datetime import datetime

class TestWeatherDiary(unittest.TestCase):
    
    def test_validate_date(self):
        """Проверка формата даты"""
        def validate_date(date_str):
            try:
                datetime.strptime(date_str, "%Y-%m-%d")
                return True
            except ValueError:
                return False
        
        self.assertTrue(validate_date("2026-05-05"))
        self.assertTrue(validate_date("2024-12-31"))
        self.assertTrue(validate_date("2025-01-01"))
        self.assertFalse(validate_date("05.05.2026"))
        self.assertFalse(validate_date("2026/05/05"))
        self.assertFalse(validate_date("2026-13-05"))
        self.assertFalse(validate_date("2026-05-32"))
        self.assertFalse(validate_date("invalid"))
        self.assertFalse(validate_date(""))
    
    def test_validate_temperature(self):
        """Проверка температуры (должна быть числом)"""
        def validate_temperature(temp_str):
            try:
                float(temp_str)
                return True
            except ValueError:
                return False
        
        self.assertTrue(validate_temperature("25"))
        self.assertTrue(validate_temperature("-5"))
        self.assertTrue(validate_temperature("10.5"))
        self.assertTrue(validate_temperature("-3.7"))
        self.assertTrue(validate_temperature("0"))
        self.assertFalse(validate_temperature("abc"))
        self.assertFalse(validate_temperature("20c"))
        self.assertFalse(validate_temperature(""))
        self.assertFalse(validate_temperature("10.5.5"))
    
    def test_validate_description(self):
        """Проверка описания (не должно быть пустым)"""
        def is_valid_description(desc):
            return bool(desc and desc.strip())
        
        self.assertTrue(is_valid_description("Солнечно"))
        self.assertTrue(is_valid_description("  Дождь с грозой  "))
        self.assertTrue(is_valid_description("Облачно"))
        self.assertFalse(is_valid_description(""))
        self.assertFalse(is_valid_description("   "))
    
    def test_precipitation_format(self):
        """Проверка формата осадков (Да или Нет)"""
        def format_precipitation(value):
            return "Да" if value else "Нет"
        
        self.assertEqual(format_precipitation(True), "Да")
        self.assertEqual(format_precipitation(False), "Нет")
        self.assertIn(format_precipitation(True), ["Да", "Нет"])
        self.assertIn(format_precipitation(False), ["Да", "Нет"])
    
    def test_filter_by_date(self):
        """Проверка фильтрации по дате"""
        entries = [
            {"date": "2026-05-01", "temperature": 15},
            {"date": "2026-05-02", "temperature": 18},
            {"date": "2026-05-03", "temperature": 22},
            {"date": "2026-05-04", "temperature": 20},
            {"date": "2026-05-05", "temperature": 17},
        ]
        
        def filter_by_date(entries, filter_date):
            return [e for e in entries if e["date"] == filter_date]
        
        result = filter_by_date(entries, "2026-05-03")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["temperature"], 22)
        
        result = filter_by_date(entries, "2026-05-01")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["temperature"], 15)
        
        result = filter_by_date(entries, "2026-06-01")
        self.assertEqual(len(result), 0)
    
    def test_filter_by_temperature(self):
        """Проверка фильтрации по температуре"""
        entries = [
            {"date": "2026-05-01", "temperature": -5},
            {"date": "2026-05-02", "temperature": 0},
            {"date": "2026-05-03", "temperature": 10},
            {"date": "2026-05-04", "temperature": 15},
            {"date": "2026-05-05", "temperature": 25},
        ]
        
        def filter_by_temperature(entries, min_temp=None, max_temp=None):
            result = entries
            if min_temp is not None:
                result = [e for e in result if e["temperature"] >= min_temp]
            if max_temp is not None:
                result = [e for e in result if e["temperature"] <= max_temp]
            return result
        
        # Фильтр выше 10 градусов
        result = filter_by_temperature(entries, min_temp=10)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["temperature"], 10)
        self.assertEqual(result[1]["temperature"], 15)
        self.assertEqual(result[2]["temperature"], 25)
        
        # Фильтр ниже 10 градусов
        result = filter_by_temperature(entries, max_temp=10)
        self.assertEqual(len(result), 3)
        
        # Фильтр диапазон от 0 до 15
        result = filter_by_temperature(entries, min_temp=0, max_temp=15)
        self.assertEqual(len(result), 3)
        
        # Фильтр вне диапазона
        result = filter_by_temperature(entries, min_temp=30, max_temp=40)
        self.assertEqual(len(result), 0)
    
    def test_filter_above_10(self):
        """Проверка фильтрации записей выше +10°C (по требованию)"""
        entries = [
            {"date": "2026-05-01", "temperature": 5},
            {"date": "2026-05-02", "temperature": 8},
            {"date": "2026-05-03", "temperature": 12},
            {"date": "2026-05-04", "temperature": 15},
            {"date": "2026-05-05", "temperature": 10},
        ]
        
        def filter_above_10(entries):
            return [e for e in entries if e["temperature"] > 10]
        
        result = filter_above_10(entries)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["temperature"], 12)
        self.assertEqual(result[1]["temperature"], 15)
    
    def test_calculate_average_temperature(self):
        """Проверка вычисления средней температуры"""
        entries = [
            {"temperature": 10},
            {"temperature": 20},
            {"temperature": 30},
        ]
        
        def average_temperature(entries):
            if not entries:
                return 0
            return sum(e["temperature"] for e in entries) / len(entries)
        
        self.assertEqual(average_temperature(entries), 20)
        self.assertEqual(average_temperature([]), 0)
        self.assertEqual(average_temperature([{"temperature": 15}]), 15)
    
    def test_sort_by_date(self):
        """Проверка сортировки записей по дате"""
        entries = [
            {"date": "2026-05-03", "temperature": 22},
            {"date": "2026-05-01", "temperature": 15},
            {"date": "2026-05-04", "temperature": 20},
            {"date": "2026-05-02", "temperature": 18},
        ]
        
        def sort_by_date(entries):
            return sorted(entries, key=lambda x: x["date"])
        
        sorted_entries = sort_by_date(entries)
        self.assertEqual(sorted_entries[0]["date"], "2026-05-01")
        self.assertEqual(sorted_entries[1]["date"], "2026-05-02")
        self.assertEqual(sorted_entries[2]["date"], "2026-05-03")
        self.assertEqual(sorted_entries[3]["date"], "2026-05-04")
    
    def test_count_rainy_days(self):
        """Проверка подсчёта дней с осадками"""
        entries = [
            {"precipitation": "Да"},
            {"precipitation": "Нет"},
            {"precipitation": "Да"},
            {"precipitation": "Нет"},
            {"precipitation": "Да"},
        ]
        
        def count_rainy_days(entries):
            return sum(1 for e in entries if e["precipitation"] == "Да")
        
        self.assertEqual(count_rainy_days(entries), 3)
        self.assertEqual(count_rainy_days([]), 0)

if __name__ == "__main__":
    unittest.main()
