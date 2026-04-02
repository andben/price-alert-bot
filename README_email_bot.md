# 📧 Price Alert Bot — Email

Ricevi email automatiche quando un titolo finanziario supera o scende sotto il prezzo target.
**100% gratuito** — usa Gmail + GitHub Actions.

---

## Come funziona

```
GitHub Actions (ogni ora)
        │
        ▼
  price_alert_email.py
        │
        ├── Legge gli ALERTS configurati
        ├── Recupera prezzi da Yahoo Finance
        └── Se un target è raggiunto → invia email via Gmail
```

Niente server, niente abbonamenti, niente PC acceso. GitHub fa tutto.

---

## Setup (10 minuti)

### 1. Crea un App Password Gmail

> ⚠️ NON usare la tua password Gmail normale — crea un'App Password dedicata.

1. Vai su [myaccount.google.com/security](https://myaccount.google.com/security)
2. Attiva la **Verifica in 2 passaggi** (se non l'hai già)
3. Cerca **"App Password"** nella barra di ricerca dell'account
4. Seleziona app: **Posta** → dispositivo: **Altro** → nome: `PriceAlertBot`
5. Copia la password di 16 caratteri generata (es. `abcd efgh ijkl mnop`)

---

### 2. Crea il repository GitHub

1. Vai su [github.com/new](https://github.com/new)
2. Nome: `price-alert-bot` → **Create repository**
3. Carica questi file:
   ```
   price-alert-bot/
   ├── price_alert_email.py          ← il bot
   └── .github/
       └── workflows/
           └── price-alert.yml       ← lo scheduler
   ```

---

### 3. Aggiungi i Secrets su GitHub

Nel tuo repository: **Settings → Secrets and variables → Actions → New repository secret**

| Nome secret | Valore |
|-------------|--------|
| `GMAIL_USER` | `tuaemail@gmail.com` |
| `GMAIL_APP_PASSWORD` | `abcd efgh ijkl mnop` (senza spazi: `abcdefghijklmnop`) |
| `NOTIFY_EMAIL` | Email dove ricevere gli alert (può essere la stessa) |

---

### 4. Configura i tuoi alert

Apri `price_alert_email.py` e modifica la lista `ALERTS`:

```python
ALERTS = [
    {
        "isin":      "IT0003128367",
        "ticker":    "ENI.MI",          # suffisso .MI per Borsa Italiana
        "name":      "Eni S.p.A.",
        "price":     14.50,
        "direction": "below",           # email se scende SOTTO 14.50€
    },
    {
        "isin":      "US0378331005",
        "ticker":    "AAPL",            # ticker diretto per azioni USA
        "name":      "Apple Inc.",
        "price":     200.00,
        "direction": "above",           # email se sale SOPRA 200$
    },
]
```

**Suffissi ticker per mercato:**
| Mercato | Suffisso | Esempio |
|---------|----------|---------|
| Borsa Italiana | `.MI` | `ENI.MI` |
| Borsa tedesca (Xetra) | `.DE` | `BMW.DE` |
| Borsa francese | `.PA` | `LVMH.PA` |
| Borsa USA | nessuno | `AAPL` |
| Amsterdam (ETF) | `.AS` | `IWDA.AS` |

---

### 5. Fai partire il bot

Dopo aver caricato i file su GitHub:
1. Vai su **Actions** nel tuo repository
2. Clicca su **Price Alert Check**
3. Clicca **Run workflow** → **Run workflow** ✅

Da quel momento gira in automatico ogni ora.

---

## Frequenza di controllo

Modifica il cron nel file `price-alert.yml`:

| Frequenza | Cron |
|-----------|------|
| Ogni ora | `0 * * * *` |
| Ogni 30 min | `*/30 * * * *` |
| Solo ore di mercato (9-18) | `0 9-18 * * 1-5` |
| Una volta al giorno (ore 9) | `0 9 * * 1-5` |

> **Nota:** GitHub Actions usa il fuso orario UTC. L'Italia è UTC+1 (inverno) o UTC+2 (estate).

---

## Costo

| Componente | Costo |
|------------|-------|
| GitHub Actions | **Gratis** (2.000 minuti/mese) |
| Gmail SMTP | **Gratis** |
| Yahoo Finance | **Gratis** |
| **Totale** | **0 €** |

Un controllo ogni ora su 30 giorni = 720 esecuzioni × ~30 secondi = ~360 minuti/mese. Ampiamente nel piano gratuito.
