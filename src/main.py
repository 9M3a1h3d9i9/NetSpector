from tester import NetworkTester
from storage import ResultStorage

import argparse


# def main():
def console_main():
    """ Main function console mode."""
    """تابع اصلی که فرآیند تست و ذخیره‌سازی را هماهنگ می‌کند."""
    print("\n" + "="*50)
    # print("NetSpector - کنسول مانیتورینگ شبکه")
    print("NetSpector - Network Monitoring Console")

    print("="*50)

    # ۱. ایجاد نمونه‌ها
    tester = NetworkTester()
    storage = ResultStorage()

    # ۲. گرفتن نام اتصال از کاربر
    # connection_name = input("لطفاً یک نام برای این اتصال شبکه وارد کنید (مثلاً Irancell-NearWindow): ").strip()
    connection_name = input("Please enter a name for this network connection (e.g., Irancell-NearWindow): ").strip()
    if not connection_name:
        connection_name = "Unknown-Connection" # مقدار پیش‌فرض

    # ۳. اجرای تست پینگ
    # print("\n--- مرحله ۱: اجرای تست پینگ ---")
    print("--- Step 1: Running Ping Test ---")
    ping_results = tester.run_ping_test(count=10) # میتوانید count را افزایش دهید

    # ۴. اجرای تست سرعت
    # print("\n--- مرحله ۲: اجرای تست سرعت ---")
    print("\n--- Step 2: Running Speed Test ---")
    speed_results = tester.run_speed_test()

    # ۵. ذخیره نتایج
    # print("\n--- مرحله ۳: ذخیره نتایج ---")
    # print("[+] در حال ذخیره نتایج...")
    print("\n --- Step 3: Saving Results ---")
    print("[+] Saving results...")
    storage.save_result(connection_name, ping_results, speed_results)

    # ۶. نمایش خلاصه نتایج به کاربر

    # print("\n--- خلاصه نتایج ---")
    # print(f"اتصال: {connection_name}")
    # print(f"تأخیر متوسط: {ping_results['avg_latency']:.2f} ms")
    # print(f"جیتر: {ping_results['jitter']:.2f} ms")
    # print(f"از دست رفتن بسته: {ping_results['packet_loss']:.0f}%")
    # print(f"سرعت دانلود: {speed_results['download_speed']} Mbps")
    # print(f"سرعت آپلود: {speed_results['upload_speed']} Mbps")
    # print("\nبرنامه با موفقیت به پایان رسید!")

    print("\n--- SUMMARY RESULTS ---")
    print(f"Connection: {connection_name}")
    print(f"Average Latency: {ping_results['avg_latency']:.2f} ms")
    print(f"Jitter: {ping_results['jitter']:.2f} ms")
    print(f"Packet Loss: {ping_results['packet_loss']:.0f}%")
    print(f"Download Speed: {speed_results['download_speed']} Mbps")
    print(f"Upload Speed: {speed_results['upload_speed']} Mbps")
    print("\nProgram completed successfully!")

# نقطه ورود اسکریپت
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='NetSpector Network Monitoring Tool')
    parser.add_argument('--gui', action='store_true', help='Run in GUI mode')
    args = parser.parse_args()

    if args.gui:
        from gui import main
        main()
    else:
        console_main()