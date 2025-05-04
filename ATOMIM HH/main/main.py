import customtkinter as ctk
from g4f.client import Client
import pyttsx3
import speech_recognition as sr
import tkinter as tk

r=sr.Recognizer()
mic=sr.Microphone()

sr.LANGAUGE="ru-RU"

# Создание клиента G4F
client = Client()
engine=pyttsx3.init('sapi5')

# Настройки интерфейса
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Голосовой Помощник")
app.geometry("900x500")

# Заголовок
label_title = ctk.CTkLabel(app, text="𝓐𝓣𝓞𝓜𝓘𝓜 𝓗", font=('Arial', 35))
label_title.pack(pady=10)

#Ввести
label = ctk.CTkLabel(app, text="Введи свой вопрос ниже и получи ответ", font=("Arial", 14))
label.pack(pady=5)

# Поле для ввода
entry = ctk.CTkEntry(app, placeholder_text="Напиши свой вопрос...")
entry.pack(pady=10)

# Место для вывода ответа
output_label = ctk.CTkLabel(app, text="", font=("Arial", 13), wraplength=800, justify="left")
output_label.pack(pady=10)

def resize(event):
    # Получаем новый размер окна
    width, height = event.width, event.height

    # Масштабируем шрифт названия
    label_title.config(font=("Orbitron", int(height * 0.08)))

    # Масштабируем шрифт заголовка
    label.config(font=("Arial", int(height * 0.06)))

    # Масштабируем размеры кнопки
    button.config(width=int(width * 0.4), height=int(height * 0.1))

    # Масштабируем размеры поля ввода
    entry.config(width=int(width * 0.6))

    # Масштабируем размеры текстового поля
    text_display.config(width=int(width * 0.6), height=int(height * 0.2))


#смена темы
def switch_theme():
    current_mode = ctk.get_appearance_mode()
    new_mode = "light" if current_mode == "Dark" else "dark"
    ctk.set_appearance_mode(new_mode)
    
    theme_button.configure(text=f"Тема: {new_mode.capitalize()}")

    if new_mode == "light":
        label_title.configure(text_color="gray")
        label.configure(text_color="gray")
        entry.configure(text_color="black")
    else:
        label_title.configure(text_color="lightgray")
        label.configure(text_color="white")
        entry.configure(text_color="lightgray")
    
    if current_mode=='light':
        label_title.configure(text_color="gray")
        label.configure(text_color="gray")
        entry.configure(text_color="black")

theme_button = ctk.CTkButton(app, text="Тема: Dark", command=switch_theme)
theme_button.pack(pady=10)

# Функция обработки ввода
with mic as source:
    r.adjust_for_ambient_noise(source)
    def listen_and_process():
        with mic as source:
            r.adjust_for_ambient_noise(source)
            print("Слушаю...")
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio, language='ru-RU')
                entry.delete(0, 'end')  # Clear entry field
                entry.insert(0, text)   # Show recognized text
                handle_input()          # Process the input
            except sr.UnknownValueError:
                output_label.configure(text="Извините, я не понял что вы сказали")
            except sr.RequestError:
                output_label.configure(text="Ошибка сервиса распознавания речи")
 
    # Add a voice input button
    voice_button = ctk.CTkButton(app, text="🎤 Голосовой ввод", command=listen_and_process)
    voice_button.pack(pady=10)

def handle_input(event=None):
    text = entry.get()
    if text.strip() == "":
        output_label.configure(text="⚠️ Ты ничего не ввёл!")
        # Early return for empty input 
        return
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Можно заменить на "gpt-3.5-turbo"
            messages=[{"role": "user", "content": text}],
            web_search=False
        )
        answer = response.choices[0].message.content
    except Exception as e:
        answer = f"Ошибка: {e}"

    engine=pyttsx3.init('sapi5')

    output_label.configure(text=answer)

# Enter = запуск
entry.bind("<Return>", handle_input)

# Кнопка
button = ctk.CTkButton(app, text="Отправить", command=handle_input)
button.pack(pady=10)


app.mainloop()

input("Нажмите любую кнопку...")
