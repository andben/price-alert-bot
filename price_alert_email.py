"""
Price Alert Bot — Email via Gmail
==================================
Controlla i prezzi degli ISIN configurati e invia email di alert.
Pensato per girare su GitHub Actions (gratis, ogni ora).

Setup:
  1. Configura gli alert in ALERTS qui sotto
  2. Crea un App Password Gmail (vedi README)
  3. Su GitHub: Settings → Secrets → aggiungi GMAIL_USER e GMAIL_APP_PASSWORD
"""

import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ─── CONFIGURAZIONE ────────────────────────────────────────────────────────────

GMAIL_USER     = os.environ.get("GMAIL_USER", "")           # es. tuaemail@gmail.com
GMAIL_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")   # App Password Gmail
NOTIFY_EMAIL   = os.environ.get("NOTIFY_EMAIL", GMAIL_USER) # chi riceve l'alert

# ─── I TUOI ALERT ──────────────────────────────────────────────────────────────
# Modifica questa lista con i tuoi strumenti finanziari.
# direction: "above"  → alert se prezzo SALE sopra il target
#            "below"  → alert se prezzo SCENDE sotto il target
# ticker: simbolo Yahoo Finance corrispondente all'ISIN
#   - Azioni USA:      ticker diretto (es. AAPL, MSFT)
#   - Borsa italiana:  ticker.MI (es. ENI.MI, ISP.MI)
#   - Borsa tedesca:   ticker.DE
#   - ETF irlandesi:   ISIN diretto spesso funziona

ALERTS = [
    {
        "isin":      "US0378331005",
        "ticker":    "AAPL",
        "name":      "Apple Inc.",
        "price":     200.00,
        "direction": "above",   # avvisami se SALE sopra 200$
    },
    {
        "isin":      "IE00B4L5Y983",
        "ticker":    "IWDA.AS",
        "name":      "iShares MSCI World ETF",
        "price":     90.00,
        "direction": "below",   # avvisami se SCENDE sotto 90€
    },
    # Aggiungi altri alert qui...
    # {
    #     "isin":      "IT0003128367",
    #     "ticker":    "ENI.MI",
    #     "name":      "Eni S.p.A.",
    #     "price":     14.50,
    #     "direction": "below",
    # },
]

# ──────────────────────────────────────────────────────────────────────────────


def get_price(ticker: str) -> float | None:
    """Recupera il prezzo corrente tramite Yahoo Finance."""
    try:
        import yfinance as yf
        t = yf.Ticker(ticker)
        price = t.fast_info.last_price
        if price and price > 0:
            return round(float(price), 4)
    except Exception as e:
        print(f"  ⚠️  Errore prezzo {ticker}: {e}")
    return None


def send_email(subject: str, body_html: str) -> bool:
    """Invia una email tramite Gmail SMTP."""
    if not GMAIL_USER or not GMAIL_PASSWORD:
        print("❌ Credenziali Gmail non configurate.")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = f"Price Alert Bot <{GMAIL_USER}>"
    msg["To"]      = NOTIFY_EMAIL
    msg.attach(MIMEText(body_html, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_USER, NOTIFY_EMAIL, msg.as_string())
        print(f"  ✅ Email inviata a {NOTIFY_EMAIL}")
        return True
    except Exception as e:
        print(f"  ❌ Errore invio email: {e}")
        return False


def build_email_html(triggered: list[dict]) -> str:
    """Costruisce il corpo HTML dell'email di alert."""
    now = datetime.now().strftime("%d/%m/%Y %H:%M")
    rows = ""
    for a in triggered:
        color  = "#16a34a" if a["direction"] == "above" else "#dc2626"
        symbol = "↑" if a["direction"] == "above" else "↓"
        cond   = "salito sopra" if a["direction"] == "above" else "sceso sotto"
        rows += f"""
        <tr>
          <td style="padding:12px;border-bottom:1px solid #e5e7eb">
            <strong>{a['name']}</strong><br>
            <span style="color:#6b7280;font-size:13px">{a['isin']} · {a['ticker']}</span>
          </td>
          <td style="padding:12px;border-bottom:1px solid #e5e7eb;text-align:center">
            <span style="color:{color};font-size:20px;font-weight:bold">{symbol} {a['current']:,.4f}</span>
          </td>
          <td style="padding:12px;border-bottom:1px solid #e5e7eb;text-align:center;color:#6b7280">
            Target: <strong>{a['price']:,.4f}</strong><br>
            <span style="font-size:12px">È {cond} il target</span>
          </td>
        </tr>"""

    return f"""
    <html><body style="font-family:sans-serif;background:#f9fafb;padding:24px">
      <div style="max-width:600px;margin:0 auto;background:white;border-radius:12px;
                  box-shadow:0 1px 3px rgba(0,0,0,.1);overflow:hidden">
        <div style="background:#1d4ed8;padding:24px">
          <h1 style="color:white;margin:0;font-size:22px">🔔 Price Alert</h1>
          <p style="color:#bfdbfe;margin:4px 0 0">{now}</p>
        </div>
        <div style="padding:24px">
          <p style="color:#374151">
            {len(triggered)} strument{'o ha' if len(triggered)==1 else 'i hanno'} raggiunto
            {'il target' if len(triggered)==1 else 'i rispettivi target'}:
          </p>
          <table style="width:100%;border-collapse:collapse">
            <thead>
              <tr style="background:#f3f4f6">
                <th style="padding:10px 12px;text-align:left;font-size:13px;color:#6b7280">STRUMENTO</th>
                <th style="padding:10px 12px;text-align:center;font-size:13px;color:#6b7280">PREZZO</th>
                <th style="padding:10px 12px;text-align:center;font-size:13px;color:#6b7280">TARGET</th>
              </tr>
            </thead>
            <tbody>{rows}</tbody>
          </table>
        </div>
        <div style="padding:16px 24px;background:#f9fafb;border-top:1px solid #e5e7eb">
          <p style="margin:0;font-size:12px;color:#9ca3af">
            Price Alert Bot · Dati da Yahoo Finance · Aggiornato ogni ora
          </p>
        </div>
      </div>
    </body></html>"""


def main():
    print(f"\n{'='*50}")
    print(f"  Price Alert Bot  —  {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"{'='*50}")

    triggered = []

    for alert in ALERTS:
        print(f"\n📊 Controllo {alert['name']} ({alert['ticker']})...")
        current = get_price(alert["ticker"])

        if current is None:
            print(f"  ⚠️  Prezzo non disponibile, salto.")
            continue

        direction_label = ">" if alert["direction"] == "above" else "<"
        print(f"  Prezzo attuale: {current:,.4f}  |  Target: {alert['price']:,.4f}  ({direction_label})")

        is_triggered = (
            alert["direction"] == "above" and current >= alert["price"]
        ) or (
            alert["direction"] == "below" and current <= alert["price"]
        )

        if is_triggered:
            print(f"  🚨 ALERT SCATTATO!")
            triggered.append({**alert, "current": current})
        else:
            print(f"  ✅ Nessun alert.")

    if triggered:
        print(f"\n📧 Invio email con {len(triggered)} alert...")
        subject = f"🚨 Price Alert — {len(triggered)} strumento{'o' if len(triggered)==1 else 'i'} ha raggiunto il target"
        html = build_email_html(triggered)
        send_email(subject, html)
    else:
        print("\n✅ Nessun alert scattato. Nessuna email inviata.")

    print(f"\n{'='*50}\n")


if __name__ == "__main__":
    main()
