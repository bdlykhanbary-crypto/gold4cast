# Gold4Cast v1.0.3

## English

This release adds a provider-agnostic live-snapshot layer to the public Gold4Cast pipeline.

### Changes
- separates historical market data from current intraday inputs;
- overlays the current Gold18, USD/IRR and XAU/USD snapshot immediately before forecasting;
- adds fail-closed stale-data protection for live runs;
- shows the exact live inputs and optional quote times in the HTML report;
- keeps the public repository independent of any named third-party provider;
- documents the live-data contract in English and Persian.

The XGBoost Quantile forecasting architecture and the published model-selection benchmark are unchanged.

## فارسی

این نسخه یک لایه مستقل Snapshot لحظه‌ای به نسخه عمومی Gold4Cast اضافه می‌کند.

### تغییرات
- جداسازی داده تاریخی از ورودی‌های لحظه‌ای؛
- اضافه/جایگزین‌شدن آخرین Gold18، دلار و اونس درست قبل از پیش‌بینی؛
- جلوگیری از انتشار گزارش زنده با داده قدیمی؛
- نمایش مقدار و ساعت ورودی‌های همان اجرای مدل در HTML؛
- حفظ استقلال نسخه عمومی از هر Data Provider مشخص؛
- مستندسازی کامل به فارسی و انگلیسی.

معماری XGBoost Quantile و نتایج Benchmark انتخاب مدل تغییر نکرده‌اند.
