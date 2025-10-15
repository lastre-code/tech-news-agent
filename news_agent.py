import feedparser
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from dotenv import load_dotenv
import os

# Cargar variables de entorno (correo y clave)
load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
TO_EMAIL = os.getenv("TO_EMAIL")

# Leer las fuentes RSS
with open("feeds.txt", "r", encoding="utf-8") as f:
    feeds = [line.strip() for line in f.readlines() if line.strip()]

# Crear mensaje
subject = f" Noticias de Tecnología por Iconic Digital- {datetime.now().strftime('%d/%m/%Y')}"
body = ""

for url in feeds:
    feed = feedparser.parse(url)
    if 'title' in feed.feed:
        body += f"\n\n🔹 {feed.feed.title}\n"
        body += "-" * len(feed.feed.title) + "\n"
    for entry in feed.entries[:5]:
        title = entry.title
        link = entry.link
        body += f"• {title}\n  {link}\n"

# Enviar correo
msg = MIMEMultipart()
msg["From"] = EMAIL
msg["To"] = TO_EMAIL
msg["Subject"] = subject
msg.attach(MIMEText(body, "plain", "utf-8"))

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.send_message(msg)
    server.quit()
    print("✅ Correo enviado con las noticias tecnológicas.")
except Exception as e:
    print(f"❌ Error al enviar el correo: {e}")
