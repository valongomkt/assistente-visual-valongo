
import pyautogui
import requests
import time
import io
import threading
from tkinter import Tk, Button, Label, Text, END
from playsound import playsound

# CONFIGURAÇÕES
WEBHOOK_URL = 'https://valongo.app.n8n.cloud/webhook-test/screen-analyzer'
INTERVALO = 15
ARQUIVO_AUDIO = 'resposta.mp3'

capturando = False
thread = None

def log(msg):
    log_box.insert(END, f"{msg}\n")
    log_box.see(END)

def capturar_e_enviar():
    global capturando
    while capturando:
        log("[📸] Capturando tela...")
        screenshot = pyautogui.screenshot()
        buffer = io.BytesIO()
        screenshot.save(buffer, format='PNG')
        buffer.seek(0)
        files = {'file': ('screenshot.png', buffer, 'image/png')}
        try:
            log("[⏫] Enviando imagem para n8n...")
            r = requests.post(WEBHOOK_URL, files=files)
            if r.status_code == 200:
                with open(ARQUIVO_AUDIO, 'wb') as f:
                    f.write(r.content)
                log("[🔊] Tocando resposta da IA...")
                playsound(ARQUIVO_AUDIO)
            else:
                log(f"[⚠] Erro ao enviar imagem: {r.status_code}")
        except Exception as e:
            log(f"[ERRO] {e}")
        time.sleep(INTERVALO)

def iniciar():
    global capturando, thread
    if not capturando:
        capturando = True
        log("[▶] Captura iniciada.")
        thread = threading.Thread(target=capturar_e_enviar)
        thread.start()

def parar():
    global capturando
    capturando = False
    log("[⏸] Captura pausada.")

# GUI
app = Tk()
app.title("Assistente Visual por Voz")
app.geometry("420x300")
Label(app, text="Suporte Visual com n8n + GPT-4o").pack()

Button(app, text="▶ Iniciar Captura", command=iniciar, bg="green", fg="white").pack(pady=5)
Button(app, text="⏸ Pausar Captura", command=parar, bg="red", fg="white").pack(pady=5)

log_box = Text(app, height=12, width=55)
log_box.pack(padx=10, pady=10)

app.mainloop()
