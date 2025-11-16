# NetSpector - Network Monitoring & Analysis Framework

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Network](https://img.shields.io/badge/Network-Monitoring-green.svg)
![Status](https://img.shields.io/badge/Status-Stable%20Core-orange.svg)

**پلتفرم پایه برای مانیتورینگ و تحلیل شبکه - قابل توسعه به سیستم‌های هوشمند**

</div>

##  Overview

NetSpector یک فریم‌ورک ماژولار برای مانیتورینگ و تحلیل شبکه است که به عنوان **پایه‌ای قوی** برای توسعه سیستم‌های پیشرفته شبکه‌ای طراحی شده است. این پروژه نشان‌دهنده توانایی پیاده‌سازی مفاهیم پایه شبکه و قابلیت گسترش به حوزه‌های پیشرفته است.

##  ویژگی‌های فعلی

###  قابلیت‌های پایه
- **مانیتورینگ Real-time** شبکه
- **تست پینگ پیشرفته** با محاسبه latency, jitter, packet loss
- **تست سرعت اینترنت** (Download/Upload)
- **ذخیره‌سازی ساختاریافته** نتایج
- **رابط دوگانه** (Console + GUI)

###  معماری ماژولار
```python
NetSpector/
├── core/
│   ├── NetworkTester.py    # ماژول تست شبکه
│   ├── ResultStorage.py    # مدیریت ذخیره‌سازی
│   └── GUI.py             # رابط گرافیکی
└── examples/              # نمونه‌های استفاده
