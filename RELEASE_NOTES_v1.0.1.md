# Gold4Cast v1.0.1

## English

This patch release hardens the public open-source package without changing the
v1.0 forecasting model:

- provider-agnostic CSV market-data input,
- no hard-coded third-party market-data endpoint,
- least-privilege GitHub Actions permissions,
- no automatic commits of forecast history from the public workflow,
- constrained baseline dependencies,
- bilingual data-input documentation.

The forecasting model remains XGBoost Quantile with the same 3M / 6M / 12M
endpoint design.

## فارسی

این نسخه اصلاحی، بسته عمومی Open Source را بدون تغییر مدل پیش‌بینی v1.0
ایمن‌تر و عمومی‌تر می‌کند:

- ورودی CSV مستقل از ارائه‌دهنده داده،
- حذف endpoint اختصاصی سرویس‌های شخص ثالث از کد عمومی،
- کاهش دسترسی GitHub Actions به `contents: read`,
- حذف commit خودکار تاریخچه پیش‌بینی از Workflow عمومی،
- تعیین محدوده نسخه dependencyها،
- مستندات ورودی داده به فارسی و انگلیسی.

مدل پیش‌بینی همچنان XGBoost Quantile با افق‌های ۳، ۶ و ۱۲ ماهه است.
