# Telegram Spam Tozalagich Bot 🤖

Telegram guruhlarida spam va reklamalarni avtomatik tozalaydigan bot. Admin va guruh egalarining xabarlarini saqlab qoladi.

## ✨ Imkoniyatlar

- ✅ **Spam aniqlash**: URL, link, telefon raqamlari va reklama kalit so'zlarini aniqlaydi
- ✅ **Kanaldan forward**: Kanallardan forward qilingan xabarlarni o'chiradi
- ✅ **Emoji nazorati**: Haddan tashqari emoji ishlatilgan xabarlarni o'chiradi
- ✅ **Admin himoyasi**: Admin va guruh egalarining xabarlarini saqlab qoladi
- ✅ **Avtomatik**: Hech qanday buyruqsiz avtomatik ishlaydi

## 📋 Talablar

- Python 3.8 yoki yuqori
- Telegram Bot Token (@BotFather dan)

## 🚀 O'rnatish

Botni ikki usulda ishga tushirish mumkin: Docker bilan (tavsiya etiladi) yoki to'g'ridan-to'g'ri Python bilan.

### Usul 1: Docker bilan (Tavsiya etiladi) 🐳

#### Talablar
- Docker
- Docker Compose

#### 1. Repositoriyani klonlash

```bash
cd /home/shukurjon/PycharmProjects/Autoremover
```

#### 2. Environment faylini sozlash

```bash
cp .env.example .env
nano .env
```

`.env` faylga bot tokeningizni qo'shing:
```env
BOT_TOKEN=your_bot_token_here
MAX_EMOJIS=5
```

#### 3. Docker Compose bilan ishga tushirish

```bash
docker compose up -d
```

Bu buyruq:
- Docker image yaratadi
- Konteyner ishga tushiradi
- Avtomatik restart qiladi (server qayta ishga tushganda)
- Background rejimda ishlaydi

#### 4. Loglarni ko'rish

```bash
docker compose logs -f
```

#### 5. Botni to'xtatish

```bash
docker compose down
```

#### 6. Botni qayta ishga tushirish

```bash
docker compose restart
```

---

### Usul 2: Python bilan

#### 1. Repositoriyani yuklab olish

```bash
cd /home/shukurjon/PycharmProjects/Autoremover
```

#### 2. Virtual muhit yaratish

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

#### 3. Kerakli kutubxonalarni o'rnatish

```bash
pip install -r requirements.txt
```

### 4. Konfiguratsiya

`.env.example` faylidan `.env` fayl yarating:

```bash
cp .env.example .env
```

`.env` faylini tahrirlang va bot tokeningizni qo'shing:

```env
BOT_TOKEN=your_bot_token_here
MAX_EMOJIS=5
```

## 🤖 Bot yaratish

1. Telegramda [@BotFather](https://t.me/BotFather) ga o'ting
2. `/newbot` buyrug'ini yuboring
3. Bot uchun nom kiriting (masalan: "My Spam Cleaner")
4. Bot uchun username kiriting (masalan: "my_spam_cleaner_bot")
5. BotFather sizgaTokenni yuboradi, uni `.env` faylga qo'shing

## ▶️ Botni ishga tushirish

### Docker bilan

```bash
docker compose up -d
```

### Python bilan

```bash
python bot.py
```

Bot ishga tushgandan so'ng, quyidagi xabar ko'rinadi:

```
Bot initialized successfully!
Bot username: @your_bot_username
Bot is running. Press Ctrl+C to stop.
```

## 📱 Guruhda ishlatish

### 1. Botni guruhga qo'shish

1. Telegram guruhingizni oching
2. Guruh sozlamalaridan "Foydalanuvchi qo'shish"ni tanlang
3. Bot usernameni kiriting (@your_bot_username)

### 2. Botga admin huquqlarini berish

**MUHIM**: Bot to'g'ri ishlashi uchun admin huquqlari kerak!

1. Guruh sozlamalarini oching
2. "Administratorlar" bo'limiga o'ting
3. Botni tanlang
4. Quyidagi huquqni yoqing:
   - ✅ **Delete messages** (Xabarlarni o'chirish)

### 3. Tayyor!

Bot endi avtomatik ravishda spam xabarlarni aniqlaydi va o'chiradi.

## 🎯 Spam aniqlash qoidalari

Bot quyidagi holatlarni spam deb aniqlaydi:

1. **URL va linklar**: http://, https://, t.me/, www. kabi
2. **Telefon raqamlari**: +998, +7 va boshqa formatlar
3. **Haddan tashqari emoji**: 5 tadan ortiq emoji (sozlanishi mumkin)
4. **Reklama kalit so'zlari**: "chegirma", "aksiya", "tekin", "obuna" va boshqalar
5. **Kanaldan forward**: Kanallardan forward qilingan xabarlar

## ⚙️ Sozlamalar

`.env` faylida quyidagi parametrlarni sozlash mumkin:

- `BOT_TOKEN`: Bot tokeni (majburiy)
- `MAX_EMOJIS`: Maksimal ruxsat etilgan emoji soni (default: 5)
- `MAX_MESSAGE_LENGTH`: Tekshiriladigan maksimal xabar uzunligi (default: 4096)

`config.py` faylida qo'shimcha sozlamalar:

- `SPAM_KEYWORDS`: Spam kalit so'zlari ro'yxati
- `URL_PATTERNS`: URL aniqlash shablonlari
- `PHONE_PATTERNS`: Telefon raqam shablonlari

## 🔒 Xavfsizlik

- Admin va guruh egalarining xabarlari **hech qachon** o'chirilmaydi
- Bot faqat oddiy foydalanuvchilarning spam xabarlarini o'chiradi
- Barcha harakatlar log faylga yoziladi

## 📊 Loglar

Bot barcha harakatlarini konsolga chiqaradi:

```
2026-01-16 16:30:00 - INFO - Bot initialized successfully!
2026-01-16 16:30:05 - INFO - Deleted spam message from user 123456. Reason: URL/link mavjud
2026-01-16 16:30:10 - INFO - Skipping spam check for admin/owner 789012
```

## 🛠 Muammolarni hal qilish

### Bot xabarlarni o'chirmayapti

**Yechim**: Botga admin huquqlari berilganligini va "Delete messages" huquqi yoqilganligini tekshiring.

### Bot ishlamayapti

**Sabab 1**: `.env` faylda token noto'g'ri kiritilgan
**Yechim**: Tokenni qaytadan tekshiring va to'g'ri kiriting

**Sabab 2** (Python): Kerakli kutubxonalar o'rnatilmagan
**Yechim**: `pip install -r requirements.txt` buyrug'ini qayta ishga tushiring

**Sabab 3** (Docker): Konteyner ishlamayapti
**Yechim**: 
```bash
# Konteyner holatini tekshiring
docker compose ps

# Loglarni ko'ring
docker compose logs

# Konteynerni qayta ishga tushiring
docker compose restart
```

### Docker image qayta build qilish kerak

Agar kod o'zgartirilgan bo'lsa:

```bash
docker compose down
docker compose build --no-cache
docker compose up -d
```

### Bot ba'zi spamlarni o'tkazib yuboradi

**Yechim**: `config.py` faylida `SPAM_KEYWORDS` ro'yxatiga yangi kalit so'zlar qo'shing, keyin:

**Docker:**
```bash
docker compose restart
```

**Python:**
Botni qayta ishga tushiring

## 📝 Litsenziya

Bu loyiha ochiq kodli va bepul ishlatish uchun mo'ljallangan.

## 🤝 Hissa qo'shish

Kamchiliklar va takliflar uchun issue ochishingiz mumkin.

## 📧 Murojaat

Savollar bo'lsa, telegram orqali murojaat qiling.

---

**Eslatma**: Botdan faqat qonuniy maqsadlarda foydalaning va guruh qoidalariga rioya qiling! 🙏
