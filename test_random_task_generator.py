import unittest
import random
from datetime import datetime

class TestRandomTaskGenerator(unittest.TestCase):
    
    def setUp(self):
        self.default_tasks = [
            {"task": "Прочитать статью", "category": "Учёба"},
            {"task": "Сделать зарядку", "category": "Спорт"},
            {"task": "Пробежка 5 км", "category": "Спорт"},
            {"task": "Выучить 10 новых слов", "category": "Учёба"},
            {"task": "Написать код", "category": "Работа"},
        ]
        self.categories = ["Учёба", "Спорт", "Работа", "Дом", "Личное"]
        
    def test_validate_task_not_empty(self):
        """Проверка задачи (не должна быть пустой)"""
        def is_valid_task(task):
            return bool(task and task.strip())
        
        self.assertTrue(is_valid_task("Прочитать книгу"))
        self.assertTrue(is_valid_task(" Сделать зарядку "))
        self.assertFalse(is_valid_task(""))
        self.assertFalse(is_valid_task(" "))
        
    def test_validate_category(self):
        """Проверка категории (должна быть из списка)"""
        def is_valid_category(category):
            return category in self.categories
        
        self.assertTrue(is_valid_category("Учёба"))
        self.assertTrue(is_valid_category("Спорт"))
        self.assertTrue(is_valid_category("Работа"))
        self.assertFalse(is_valid_category(""))
        self.assertFalse(is_valid_category("Хобби"))
        self.assertFalse(is_valid_category(" "))
        
    def test_generate_random_task(self):
        """Проверка генерации случайной задачи"""
        def generate_random_task(tasks):
            return random.choice(tasks)
        
        task1 = generate_random_task(self.default_tasks)
        task2 = generate_random_task(self.default_tasks)
        
        self.assertIn(task1, self.default_tasks)
        self.assertIn(task2, self.default_tasks)
        
    def test_filter_by_category(self):
        """Проверка фильтрации по категории"""
        history = [
            {"task": "Чтение", "category": "Учёба"},
            {"task": "Бег", "category": "Спорт"},
            {"task": "Код", "category": "Работа"},
            {"task": "Книга", "category": "Учёба"},
        ]
        
        def filter_by_category(history, category):
            return [h for h in history if h["category"] == category]
        
        result = filter_by_category(history, "Учёба")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["task"], "Чтение")
        self.assertEqual(result[1]["task"], "Книга")
        
        result = filter_by_category(history, "Спорт")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["task"], "Бег")
        
        result = filter_by_category(history, "Дом")
        self.assertEqual(len(result), 0)
        
    def test_add_new_task(self):
        """Проверка добавления новой задачи"""
        tasks = self.default_tasks.copy()
        
        def add_new_task(tasks, new_task, category):
            tasks.append({"task": new_task, "category": category})
            return tasks
        
        tasks = add_new_task(tasks, "Помыть посуду", "Дом")
        
        self.assertEqual(len(tasks), 6)
        self.assertEqual(tasks[-1]["task"], "Помыть посуду")
        self.assertEqual(tasks[-1]["category"], "Дом")
        
    def test_task_uniqueness_in_history(self):
        """Проверка, что каждая сгенерированная задача добавляется в историю"""
        history = []
        
        def add_to_history(history, task, category):
            entry = {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "task": task,
                "category": category
            }
            history.append(entry)
            return history
        
        history = add_to_history(history, "Зарядка", "Спорт")
        history = add_to_history(history, "Чтение", "Учёба")
        
        self.assertEqual(len(history), 2)
        self.assertEqual(history[0]["task"], "Зарядка")
        self.assertEqual(history[1]["task"], "Чтение")
        
    def test_prevent_duplicate_in_custom_tasks(self):
        """Проверка предотвращения дублирования при добавлении (опционально)"""
        tasks = self.default_tasks.copy()
        existing_tasks = [t["task"] for t in tasks]
        
        def add_if_not_exists(tasks, new_task, category):
            if new_task not in [t["task"] for t in tasks]:
                tasks.append({"task": new_task, "category": category})
            return tasks
        
        tasks = add_if_not_exists(tasks, "Зарядка", "Спорт")
        self.assertEqual(len(tasks), 5)
        
        tasks = add_if_not_exists(tasks, "Новая задача", "Учёба")
        self.assertEqual(len(tasks), 6)

if __name__ == "__main__":
    unittest.main()
