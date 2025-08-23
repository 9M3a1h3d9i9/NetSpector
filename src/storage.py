import json
import os
from datetime import datetime

class ResultStorage:
    """
    یک کلاس برای ذخیره و بازیابی نتایج تست‌های شبکه در یک فایل JSON.
    """

    def __init__(self, data_dir='../data', filename='network_results.json'):
        """
        مقداردهی اولیه ذخیره‌سازی.

        Args:
            data_dir (str): مسیر نسبی پوشه‌ای که فایل نتایج در آن ذخیره می‌شود.
            filename (str): نام فایل JSON.
        """
        self.data_dir = data_dir
        self.filename = filename
        self.filepath = os.path.join(data_dir, filename)

        # مطمئن شویم پوشه data وجود دارد
        os.makedirs(data_dir, exist_ok=True)

    def save_result(self, connection_name, ping_results, speed_results):
        """
        نتیجه یک تست را به انتهای فایل JSON اضافه می‌کند.

        Args:
            connection_name (str): نام توصیفی برای اتصال (مثلاً 'Irancell-Hotspot').
            ping_results (dict): نتایج بازگشتی از متد run_ping_test.
            speed_results (dict): نتایج بازگشتی از متد run_speed_test.
        """
        # ساخت یک رکورد جدید از داده‌ها
        new_entry = {
            'timestamp': datetime.now().isoformat(), # زمان دقیق تست
            'connection_name': connection_name,
            'ping': ping_results,
            'speed': speed_results
        }

        # خواندن داده‌های موجود از فایل (اگر وجود دارد)
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # اگر فایل وجود نداشت یا خالی/خراب بود، یک لیست جدید شروع کن
            existing_data = []

        # اضافه کردن رکورد جدید به لیست موجود
        existing_data.append(new_entry)

        # نوشتن کل لیست به فایل
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False)

        # print(f"[+] نتایج با موفقیت در '{self.filepath}' ذخیره شد.")
        print(f"[+] Results successfully saved to '{self.filepath}'.")

    def load_results(self):
        """
        تمام نتایج تاریخی را از فایل JSON بارگذاری می‌کند.

        Returns:
            list: لیستی از دیکشنری‌های حاوی تمام نتایج.
        """
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []  # اگر فایل وجود نداشت، یک لیست خالی برگردان

# بخشی برای تست مستقل ماژول
if __name__ == "__main__":
    storage = ResultStorage()
    # نمونه داده برای تست
    test_ping = {'avg_latency': 45.6, 'jitter': 12.3, 'packet_loss': 0.0}
    test_speed = {'download_speed': 32.1, 'upload_speed': 5.7}
    storage.save_result("Test-Connection", test_ping, test_speed)
    all_data = storage.load_results()
    # print("همه داده‌های ذخیره شده:", all_data)
    print("All stored data:", all_data)