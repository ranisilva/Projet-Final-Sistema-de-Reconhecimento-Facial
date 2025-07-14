import tkinter as tk
from tkinter import messagebox
import face_recognition
import os
import pickle
import numpy as np


def get_button(window, text, color, command, fg='white'):
    button = tk.Button(
        window,
        text=text,
        activebackground='#03032e',
        activeforeground='#00fff0',
        fg=fg,
        bg=color,
        command=command,
        height=6,
        width=20,
        font=('helvetica bold', 20)
    )
    return button


def get_buttontwo(window, text, color, command, fg='white'):
    buttontwo = tk.Button(
        window,
        text=text,
        activebackground='#03032e',  # Cor de fundo quando apertado
        activeforeground='#00fff0',  # Cor do texto quando clicado
        fg=fg,
        bg=color,
        command=command,
        height=4,
        width=20,
        font=('helvetica bold', 20)
    )
    return buttontwo


def get_img_label(window):
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label


def get_text_label(window, text):
    label = tk.Label(window, text=text, width=20)
    label.config(font=("sans-serif", 15), justify="center")
    return label


def get_entry_text(window):
    inputtxt = tk.Text(window,
                       height=1,
                       width=22, font=("Arial", 20))
    return inputtxt


def msg_box(title, description):
    messagebox.showinfo(title, description)


def recognize(img, db_path, face_locations=None):
    if face_locations is None:
        face_locations = face_recognition.face_locations(img)

    embeddings_unknown = face_recognition.face_encodings(img, face_locations)
    if len(embeddings_unknown) == 0:
        print("LOG: Nenhum rosto detectado na imagem para comparação.")
        return 'no_persons_found'
    else:
        embeddings_unknown = embeddings_unknown[0]

    db_dir = sorted(os.listdir(db_path))

    match = False
    j = 0
    while not match and j < len(db_dir):
        path_ = os.path.join(db_path, db_dir[j])

        if not os.path.exists(path_):
            print(f"LOG: recognize - Arquivo de embedding não encontrado: {path_}. Pulando.")
            j += 1
            continue

        try:
            with open(path_, 'rb') as file:
                embeddings = pickle.load(file)
                name_from_file = db_dir[j][:-7]  # Extrai o nome do arquivo (removendo '.pickle')
                print(f"LOG: Comparando com o arquivo pickle de: {name_from_file} ({db_dir[j]})")
        except Exception as e:
            print(f"ERRO: recognize - Não foi possível carregar o arquivo pickle '{path_}': {e}. Pulando.")
            j += 1
            continue

        match = face_recognition.compare_faces([embeddings], embeddings_unknown)[0]

        if match:
            print(f"LOG: Correspondência encontrada com: {name_from_file}")
        else:
            print(f"LOG: Nenhuma correspondência com: {name_from_file}")

        j += 1

    if match:
        # Quando um match é encontrado, 'j' já foi incrementado, então voltamos 1 para pegar o nome correto.
        # db_dir[j-1] contém o nome do arquivo que deu match.
        final_recognized_name = db_dir[j - 1][:-7]
        print(f"LOG: Reconhecimento finalizado. Pessoa identificada: {final_recognized_name}")
        return final_recognized_name
    else:
        print("LOG: Reconhecimento finalizado. Nenhuma pessoa conhecida encontrada.")
        return 'unknown_person'