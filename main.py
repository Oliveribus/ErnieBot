import os
from tkinter import filedialog, StringVar, DISABLED, NORMAL
import threading
import customtkinter as customtkinter
import openai
from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
import sys
import platform
from gradio import Interface
from gradio.components import Textbox
from PIL import Image

f = open('key.txt')
APIKey = f.read()

os.environ["OPENAI_API_KEY"] = APIKey
thread = None

_IS_MAC = platform.system() == 'Darwin'

def resource_path(relative_path):  # needed for bundling
    """Get absolute path to resource, works for dev and for PyInstaller"""
    if not _IS_MAC:
        return relative_path
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
            os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def open_directory_dialog():
    global directory_path
    directory_path = filedialog.askdirectory()
    status_label.configure(text=directory_path)

def nachricht():
    status_label.configure(text="Bitte eine der Optionen wählen!")

def check_button():
    # Überprüfen Sie, welcher Radiobutton ausgewählt ist
    if selected_button.get() == "Lokalen Index erzeugen":
        # Aktivieren Sie den Button, wenn "Lokalen Index erzeugen" ausgewählt ist
        tton2.configure(state=NORMAL)
        button.configure(command=VectorConstruct)
    else:
        # Deaktivieren Sie den Button, wenn "Lokalen Index verwenden" ausgewählt ist
        tton2.configure(state=DISABLED)
        button.configure(command=Bot)
def VectorConstruct():
    try:
        input = directory_path
        documents = SimpleDirectoryReader(input).load_data()
        index = GPTVectorStoreIndex.from_documents(documents)
        index.storage_context.persist(f'{directory_path}/storage')
        status_label.configure(text="Index gespeichert! \n"
                                    "Server kann gestartet werden. \n"
                                    "Bitte wähle oben die Verwendung des lokalen Index")
        return index
    except NameError:
        status_label.configure(text="Input-Datei wählen!")
def VectorLoader():
    # # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir=f'{directory_path}/storage')
    # # load index
    return load_index_from_storage(storage_context)


def query(input, index):
    query_engine = index.as_query_engine()
    return query_engine.query(input)


def GPT(input, hidden):
    vector = VectorLoader()
    querry = query(input, vector)
    input4gpt = input + str(querry) + f' {hidden}'
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
            {"role": "assistant", "content": input4gpt},
        ]
    )
    return (response["choices"][0]["message"]["content"]), str(querry)


# Chatbot starten
def Bot():
        global thread
        thread = threading.Thread(target=iface.launch, kwargs={'inbrowser': True}, daemon=True)
        status_label.configure(text="Server läuft")
        thread.start()


def on_close():
    global thread
    thread = None

    # Gradio stoppen


def stop_gradio():
    iface.close()  # Schließt das Interface
    status_label.configure(text="Server ist gestoppt")


def on_closing():
    root.quit()  # Beenden Sie das Hauptereignis-Loop
    root.destroy()  #


# Frontend initalisieren
iface = Interface(
    fn=GPT,
    inputs=[
        Textbox(lines=7, label="Enter your text"),
        Textbox(lines=3, label="Hidden Prompt", value='Erstelle eine systematische Lösungsskizze, in der du nacheinnander ' \
             'die zu prüfenden Tatbestandsmerkmale voranstellst und dann darunter subsumierst.')
    ],
    outputs=[
        Textbox(label='Antwort mit Hidden Prompt'),
        Textbox(label='Antwort ohne Hidden Prompt')
    ],
    title="ErnieBot",
    allow_flagging='never'
)


iface.close(on_close)



##### GUI LOKAL #######

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

root = customtkinter.CTk()
root.geometry("550x500")
root.title("ErnieBot")

root.protocol("WM_DELETE_WINDOW", on_closing)


frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=20, fill="both", expand="True")

logo = Image.open(resource_path('Ernie.png'))
logo_ctk = customtkinter.CTkImage(light_image=logo, size=(90, 90))
logo_label = customtkinter.CTkLabel(master=frame, image=logo_ctk, text=None)
logo_label.pack(padx=10, pady=10)

title = customtkinter.CTkLabel(master=frame, text="ErnieBot", font=("Arial", 24, "bold"))
title.pack(padx=10, pady=10)

tton2 = customtkinter.CTkButton(master=frame, text="Ordner wählen", command=open_directory_dialog, state=NORMAL)
tton2.pack(padx=10, pady=10)

selected_button = StringVar()

button1 = customtkinter.CTkRadioButton(master=frame, text="Lokalen Index erzeugen", variable=selected_button, value="Lokalen Index erzeugen", command=check_button)
button1.pack(padx=10, pady=10)
button2 = customtkinter.CTkRadioButton(master=frame, text="Lokalen Index verwenden", variable=selected_button, value="Lokalen Index verwenden", command=check_button)
button2.pack(padx=10, pady=10)

button = customtkinter.CTkButton(master=frame, text="Start", command=nachricht)
button.pack(padx=10, pady=10)

stop_button = customtkinter.CTkButton(master=frame, text="Stop", command=stop_gradio, fg_color="red")
stop_button.pack(padx=10, pady=10)

status_label = customtkinter.CTkLabel(master=frame, text="Server Status: Stopped")
status_label.pack(padx=10, pady=10)
root.mainloop()

