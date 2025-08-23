import speedtest
from ping3 import ping
import time
import statistics

class NetworkTester:
    """
    یک کلاس برای انجام تست‌های مختلف شبکه شامل پینگ و سرعت.
    """

    def __init__(self, test_server='8.8.8.8'):
        """
        مقداردهی اولیه تستر.

        Args:
            test_server (str): آدرس IP یا hostname سروری که برای تست پینگ استفاده می‌شود. پیش‌فرض '8.8.8.8' (DNS گوگل) است.
        """
        self.test_server = test_server

    def run_ping_test(self, count=10):
        """
        یک تست پینگ انجام می‌دهد و آمار آن را محاسبه می‌کند.

        Args:
            count (int): تعداد پینگ‌های ارسالی. پیش‌فرض 10.

        Returns:
            dict: یک دیکشنری حاوی نتایج تست پینگ شامل:
                - avg_latency (float): میانگین تاخیر (میلی‌ثانیه)
                - min_latency (float): کمترین تاخیر
                - max_latency (float): بیشترین تاخیر
                - jitter (float): انحراف معیار تاخیرها (میلی‌ثانیه)
                - packet_loss (float): درصد بسته‌های از دست رفته
        """
        delays = []  # لیست برای ذخیره زمان‌های پاسخ موفق
        lost = 0     # شمارنده پینگ‌های از دست رفته

        # print(f"[+] در حال ارسال {count} پینگ به {self.test_server}...")
        print(f" Sending {count} pings to {self.test_server}...")

        for i in range(count):
            try:
                # ارسال پینگ و دریافت پاسخ بر حسب میلی‌ثانیه
                delay = ping(self.test_server, unit='ms', timeout=1)
                if delay is None or delay is False:
                    # اگر پاسخی دریافت نشد (Timeout یا خطای دیگر)
                    # print(f"  پینگ {i+1}: timeout")
                    print(f"  Ping {i+1}: timeout")
                    lost += 1
                else:
                    # اگر پاسخ موفقیت‌آمیز بود
                    # print(f"  پینگ {i+1}: {delay:.2f} ms")
                    print(f"  Ping {i+1}: {delay:.2f} ms")
                    delays.append(delay)
            except Exception as e:
                # گرفتن هرگونه استثنای دیگر
                # print(f"  پینگ {i+1}: خطا - {e}")
                print(f"  Ping {i+1}: error - {e}")
                lost += 1
            time.sleep(0.5)  # مکث نیم ثانیه بین هر پینگ

        # محاسبه آمار
        if delays:  # اگر حداقل یک پاسخ موفق داشتیم
            avg_delay = statistics.mean(delays)
            min_delay = min(delays)
            max_delay = max(delays)
            jitter = statistics.stdev(delays) if len(delays) > 1 else 0.0
            loss_percent = (lost / count) * 100
        else:
            # اگر هیچ پاسخی دریافت نشد
            avg_delay = min_delay = max_delay = jitter = 0.0
            loss_percent = 100.0

        results = {
            'avg_latency': avg_delay,
            'min_latency': min_delay,
            'max_latency': max_delay,
            'jitter': jitter,
            'packet_loss': loss_percent
        }

        # print("[+] تست پینگ تکمیل شد.")
        print("[+] Ping test completed.")
        return results

    def run_speed_test(self):
        """
        تست سرعت اینترنت (دانلود و آپلود) را اجرا می‌کند.

        Returns:
            dict: یک دیکشنری حاوی نتایج تست سرعت شامل:
                - download_speed (float): سرعت دانلود (Mbps)
                - upload_speed (float): سرعت آپلود (Mbps)
        """
        # print("[+] در حال اجرای تست سرعت (این ممکن است چند لحظه طول بکشد)...")
        print("[+] Running speed test (this may take a while)...")  
        try:
            st = speedtest.Speedtest()
            # پیدا کردن بهترین سرور
            st.get_best_server()
            # اجرای تست دانلود
            st.download()
            # اجرای تست آپلود
            st.upload()
            # گرفتن نتایج
            results = st.results.dict()

            # تبدیل بیت بر ثانیه به مگابیت بر ثانیه و گرد کردن
            download_mbps = results['download'] / 1_000_000
            upload_mbps = results['upload'] / 1_000_000

            speed_results = {
                'download_speed': round(download_mbps, 2),
                'upload_speed': round(upload_mbps, 2)
            }

            # print(f"[+] تست سرعت تکمیل شد: دانلود: {download_mbps:.2f} Mbps, آپلود: {upload_mbps:.2f} Mbps")
            print(f"[+] Speed test completed: Download: {download_mbps:.2f} Mbps, Upload: {upload_mbps:.2f} Mbps")
            return speed_results

        except Exception as e:
            # print(f"[-] خطا در اجرای تست سرعت: {e}")
            print(f"[-] Error running speed test: {e}")
            # بازگرداندن مقادیر صفر در صورت خطا
            return {'download_speed': 0.0, 'upload_speed': 0.0}

# بخشی برای تست مستقل ماژول (اگر فایل مستقیماً اجرا شد)
if __name__ == "__main__":
    tester = NetworkTester()
    ping_results = tester.run_ping_test(count=5)
    # print("نتایج پینگ:", ping_results)
    print("Ping Results:", ping_results)
    speed_results = tester.run_speed_test()
    # print("نتایج سرعت:", speed_results)
    print("Speed Results:", speed_results)