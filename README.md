# Rexona Node

**دیتاپلین (data plane) نسخهٔ ری‌برندشدهٔ Nexora Node v0.0.5** — باینری‌های آماده برای `amd64` و `arm64`.

مخزن بالاسری: [`Nexora-VPN/node`](https://github.com/Nexora-VPN/node) (تگ `v0.0.5`)

---

## چه چیزی تغییر کرده؟

فقط **ری‌برند**. هیچ تغییری در منطق، پروتکل، یا مسیر داده انجام نشده:

- `nexora` → `rexona`، `Nexora` → `Rexona`، `NEXORA` → `REXONA`
- **۹۳۳۹ جایگزینی هم‌طول** (بدون تغییر حجم باینری، بدون تغییر آفست‌ها)
- مسیر state: `/var/opt/nexora` → `/var/opt/rexona`
- نام باینری و یونیت systemd: `rexona-node`
- صفر رشتهٔ `nexora` در باینری نهایی

**تأیید سلامت:** `rexona-node 0.0.5` روی amd64 اجرا و تست شده.

---

## نصب

### الف) از پنل (خودکار، توصیه‌شده)

پنل خودش اسکریپت `install-node.sh` را می‌سرو می‌کند و باینری را از این مخزن می‌کشد:

```bash
curl -fsSL https://<PANEL>:2095/install-node.sh | bash -s -- --panel <PANEL>:2095 --token <TOKEN>
```

> ⚠️ این مخزن **خصوصی** است. برای نصب خودکار، یا باید باینری از سمت پنل staged شده باشد
> (`--source panel`)، یا توکن GitHub در دسترس باشد.

### ب) دستی از ریلیز

```bash
# دانلود
curl -fL -o node.tar.gz \
  https://github.com/frank0live/node/releases/download/v0.0.5/rexona-node-linux-amd64.tar.gz

# استخراج
tar xzf node.tar.gz          # → rexona-node/rexona-node + .service

# نصب
install -d /opt/rexona-node /var/opt/rexona
install -m 0755 rexona-node/rexona-node /opt/rexona-node/
install -m 0644 rexona-node/rexona-node.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable --now rexona-node
```

سپس در پنل، نود را با آدرس و توکن وصل کنید.

---

## فایل‌ها

```
rexona-node-linux-amd64.tar.gz   # x86_64  (28 MB)
rexona-node-linux-arm64.tar.gz   # aarch64 (26 MB)
```

هر آرشیو شامل:
```
rexona-node/rexona-node          # باینری پچ‌شده
rexona-node/rexona-node.service  # یونیت systemd
```

---

## SHA256

```
amd64 tarball : e9e4291d35995fef45a1923a22a6066cc0de29794759b680c029098e76e2e554
amd64 binary  : 33bac5afbfe490274579897296672fd3911170a9a0f06af7e7091e9209102852
arm64 tarball : c49d6c5c3068354687036d101d06a29a81d578afaca9a39304778f1d44177b05
arm64 binary  : 86bd3cf499634d493d5656d0c607ca2c8b284bf170e31c9c88f002bf1a6a3590
```

---

## بازسازی پچ

```bash
python3 patch_node.py rexona-node.orig rexona-node.patched
```

اسکریپت جایگزینی‌های هم‌طول را انجام می‌دهد و اگر حجم باینری تغییر کند، متوقف می‌شود.

---

## نکته‌های عملیاتی

- **پورت پیش‌فرض نود:** `62050` (TLS با گواهی خودامضا که پنل روی اولین اتصال پین می‌کند)
- **گواهی نود را حذف نکنید:** اگر بازتولید شود، پنل دیگر به نود وصل نمی‌شود
- **آپدیت:** باینری جدید را جایگزین کنید، `systemctl restart rexona-node` — کانفیگ و گواهی حفظ می‌شوند
- **Docker:** ایمیج `ghcr.io/nexora-vpn/node` همچنان بالاسری است (ری‌برند نشده)

---

## مجوز

همان مجوز بالاسری (`Nexora Node`). این مخزن فقط باینری پچ‌شده را بازتوزیع می‌کند.
