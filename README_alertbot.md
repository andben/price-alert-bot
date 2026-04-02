# 📊 Telegram Price Alert Bot

Bot Telegram che monitora prezzi di strumenti finanziari tramite ISIN e invia notifiche quando superano o scendono sotto una soglia.

---

## ⚡ Setup rapido

### 1. Crea il bot su Telegram
1. Apri Telegram e cerca **@BotFather**
2. Invia `/newbot` e segui le istruzioni
3. Copia il **TOKEN** che ti viene fornito

### 2. Installa le dipendenze
```bash
pip install python-telegram-bot yfinance
```

### 3. Configura il token
**Opzione A** — variabile d'ambiente (consigliata):
```bash
export TELEGRAM_BOT_TOKEN="il_tuo_token_qui"
python telegram_alert_bot.py
```

**Opzione B** — modifica il file:
Apri `telegram_alert_bot.py` e sostituisci la riga:
```python
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "IL_TUO_TOKEN_QUI")
```
con:
```python
BOT_TOKEN = "il_tuo_token_qui"
```

### 4. Avvia il bot
```bash
python telegram_alert_bot.py
```

---

## 💬 Comandi Telegram

| Comando | Descrizione |
|---------|-------------|
| `/start` | Avvia il bot e mostra i comandi |
| `/alert` | Crea un nuovo alert (ISIN → Prezzo → Direzione) |
| `/lista` | Visualizza tutti gli alert attivi |
| `/cancella` | Rimuovi un alert esistente |
| `/annulla` | Annulla l'operazione corrente |

---

## 🔄 Come funziona

```
/alert
  └─► Inserisci ISIN (es: US0378331005)
        └─► Inserisci prezzo target (es: 185.50)
              └─► Scegli direzione:
                    ├─► 📈 SOPRA  → alert se prezzo ≥ target
                    └─► 📉 SOTTO  → alert se prezzo ≤ target
```

Il bot controlla i prezzi ogni **60 secondi** e invia una notifica quando la condizione è soddisfatta.

---

## 📝 Note importanti

### Dati di mercato
Il bot usa **Yahoo Finance** tramite `yfinance`. Yahoo Finance **non supporta nativamente gli ISIN** ma accetta alcuni ticker europei con suffisso (`.MI` per Milano, `.DE` per Francoforte, ecc.).

Per dati professionali usa API dedicate:
- **OpenFIGI** (gratuita) — converte ISIN in ticker
- **Alpha Vantage** — dati di mercato con free tier
- **Twelve Data** — supporto ISIN nativo
- **Bloomberg / Refinitiv** — soluzioni enterprise

### Persistenza dati
Gli alert sono salvati **in memoria**: si perdono al riavvio del bot. Per produzione usa un database (SQLite, PostgreSQL, Redis).

---

## 🚀 Deploy su server (opzionale)

Con **systemd** su Linux:
```ini
# /etc/systemd/system/alertbot.service
[Unit]
Description=Telegram Price Alert Bot

[Service]
ExecStart=/usr/bin/python3 /path/to/telegram_alert_bot.py
Environment=TELEGRAM_BOT_TOKEN=il_tuo_token
Restart=always

[Install]
WantedBy=multi-user.target
```
```bash
sudo systemctl enable alertbot && sudo systemctl start alertbot
```

---

## 🛠 Personalizzazione

| Parametro | Posizione | Default | Descrizione |
|-----------|-----------|---------|-------------|
| `CHECK_INTERVAL` | riga 22 | `60` | Secondi tra i controlli prezzi |
| `BOT_TOKEN` | riga 19 | — | Token del bot Telegram |
