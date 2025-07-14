import os.path
import datetime
import pickle
import time

import tkinter as tk
from tkinter import *
import cv2
from PIL import Image, ImageTk
import face_recognition

import util
import os


class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.geometry("1000x490+350+100")
        self.main_window.title("Sistema de Reconhecimento Facial")
        self.main_window.configure(bg='#1d1d20')

        self.db_dir = os.path.join(os.path.dirname(__file__), 'db')
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)

        self.log_path = os.path.join(os.path.dirname(__file__), 'log.txt')

        self.recognized_display_name = ""
        self.display_start_time = 0.0
        self.display_duration_seconds = 3

        self.recognition_active = False

        self.login_button_main_window = util.get_button(self.main_window, 'Identificar Rosto', '#77dd86', self.login)
        self.login_button_main_window.place(x=660, y=8)

        self.register_new_user_button_main_window = util.get_button(self.main_window, 'Registrar Rosto', '#523ba1',
                                                                    self.register_new_user)
        self.register_new_user_button_main_window.place(x=660, y=264)

        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=8, width=640, height=470)
        self.webcam_label.configure(bg='#1d1d20')

        self.add_webcam(self.webcam_label)

    def add_webcam(self, label):
        if not hasattr(self, 'cap') or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                util.msg_box('Erro', 'Não foi possível iniciar a webcam. Verifique a conexão e tente novamente.')
                return

        self._label = label
        self.process_webcam()

    def process_webcam(self):
        if not hasattr(self, 'cap') or not self.cap.isOpened():
            self._label.after(1000, self.add_webcam, self._label)
            return

        ret, frame = self.cap.read()
        if not ret:
            self._label.after(20, self.process_webcam)
            return

        self.most_recent_capture_arr = frame

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)

        current_time = time.time()

        # Lógica para limpar o nome exibido após o tempo limite
        if self.recognized_display_name and (current_time - self.display_start_time) > self.display_duration_seconds:
            self.recognized_display_name = ""
            self.display_start_time = 0.0
            self.recognition_active = False  # Garante que o reconhecimento volte ao estado inativo após a exibição

        name_to_draw = "Aguardando..."
        color_box = (255, 255, 0)  # Amarelo, para o estado "Aguardando..." ou sem reconhecimento ativo

        if face_locations:
            # Prioriza a exibição do nome reconhecido se ele estiver ativo e dentro do tempo
            if self.recognized_display_name and (
                    current_time - self.display_start_time) <= self.display_duration_seconds:
                name_to_draw = self.recognized_display_name
                color_box = (0, 255, 0)  # Verde para reconhecido
            else:
                # Se há rostos, mas nenhum reconhecimento ativo (ou tempo expirou)
                # E o reconhecimento não está no modo "ativo por clique"
                if not self.recognition_active:
                    name_to_draw = "Desconhecido"  # Exibe "Desconhecido" se não há reconhecimento ativo
                    color_box = (0, 0, 255)  # Vermelho para desconhecido
                else:  # Se está ativo por clique, mas ainda não reconheceu (ou é desconhecido)
                    name_to_draw = "Aguardando..."  # Ou poderia ser "Desconhecido"
                    color_box = (255, 255, 0)  # Amarelo
        else:
            name_to_draw = "Nenhum rosto"
            color_box = (255, 0, 0)  # Azul para nenhum rosto

        # Desenha os retângulos e texto
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), color_box, 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name_to_draw, (left + 6, bottom - 6), font, 0.7, (255, 255, 255), 1)

        img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        self.most_recent_capture_pil = img_pil.copy()

        img_pil_resized = img_pil.resize((640, 470), Image.Resampling.LANCZOS)
        imgtk = ImageTk.PhotoImage(image=img_pil_resized)

        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        self._label.after(20, self.process_webcam)

    def login(self):
        self.recognition_active = True
        start_time = time.time()

        if not hasattr(self, 'most_recent_capture_arr') or self.most_recent_capture_arr is None:
            util.msg_box('Erro', 'Nenhuma imagem da webcam disponível para reconhecimento. Tente novamente.')
            self.recognition_active = False
            return

        rgb_frame_login = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        face_locations_login = face_recognition.face_locations(rgb_frame_login)

        name = "unknown_person"
        if face_locations_login:
            name = util.recognize(rgb_frame_login, self.db_dir, face_locations_login)
        else:
            name = "no_persons_found"

        end_time = time.time()
        recognition_time_ms = (end_time - start_time) * 1000

        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box('Acesso Negado', 'Usuário não reconhecido. Tente Novamente.')
            self.recognized_display_name = ""  # Limpa o nome na tela se falhou
            self.display_start_time = 0.0
            self.recognition_active = False  # Desativa após falha no reconhecimento
        else:
            util.msg_box('Acesso Registrado',
                         f'Olá, {name}. Acesso registrado às {datetime.datetime.now().strftime("%H:%M:%S")}. Tempo de reconhecimento: {recognition_time_ms:.2f} ms')
            try:
                with open(self.log_path, 'a') as f:
                    f.write(
                        f'{name},{datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")},{recognition_time_ms:.2f}ms\n')

                # ATUALIZA AQUI: Define o nome e o tempo para exibição imediata na webcam
                self.recognized_display_name = name
                self.display_start_time = time.time()

            except Exception as e:
                print(f"ERRO: Não foi possível escrever no arquivo de log '{self.log_path}': {e}")
                self.recognition_active = False

    def register_new_user(self):
        self.recognition_active = False
        if not hasattr(self, 'most_recent_capture_arr') or self.most_recent_capture_arr is None:
            util.msg_box('Erro', 'Por favor, aguarde o feed da webcam iniciar para capturar uma imagem para cadastro.')
            return

        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.geometry("1000x490+350+100")
        self.register_new_user_window.title("Cadastro de Novo Usuário")
        self.register_new_user_window.configure(bg='#1d1d20')

        self.accept_button_register_new_user_window = util.get_buttontwo(self.register_new_user_window, 'Aceitar',
                                                                         '#77dd86', self.accept_register_new_user)
        self.accept_button_register_new_user_window.place(x=660, y=170)

        self.try_again_button_register_new_user_window = util.get_buttontwo(self.register_new_user_window,
                                                                            'Tentar novamente', '#523ba1',
                                                                            self.try_again_register_new_user)
        self.try_again_button_register_new_user_window.place(x=660, y=327)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=8, width=640, height=470)
        self.capture_label.configure(bg='#1d1d20')

        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=660, y=50)
        self.entry_text_register_new_user.configure(bg='#1d1d20', fg='white')

        self.text_label_register_new_user = util.get_text_label(self.register_new_user_window,
                                                                'Insira o nome do usuário:')
        self.text_label_register_new_user.place(x=720, y=8)
        self.text_label_register_new_user.configure(bg='#1d1d20', fg='white')
        self.entry_text_register_new_user.configure(bg='#1d1d20', fg='white')

    def try_again_register_new_user(self):
        if hasattr(self, 'register_new_user_window') and self.register_new_user_window.winfo_exists():
            self.register_new_user_window.destroy()
        if not self.recognized_display_name:
            self.recognition_active = False

    def add_img_to_label(self, label):
        if not hasattr(self, 'most_recent_capture_pil') or self.most_recent_capture_pil is None:
            util.msg_box('Erro', 'Nenhuma imagem disponível para exibição no formulário de cadastro.')
            return

        img_pil_resized = self.most_recent_capture_pil.resize((640, 470), Image.Resampling.LANCZOS)
        imgtk = ImageTk.PhotoImage(image=img_pil_resized)
        label.imgtk = imgtk
        label.configure(image=imgtk)

        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def start(self):
        self.main_window.mainloop()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get("1.0", "end-1c").strip()
        if not name:
            util.msg_box('Erro de Cadastro', 'Por favor, insira um nome para o usuário.')
            return

        if not hasattr(self, 'register_new_user_capture') or self.register_new_user_capture is None:
            util.msg_box('Erro de Cadastro', 'Nenhuma imagem capturada para cadastro.')
            return

        rgb_capture = cv2.cvtColor(self.register_new_user_capture, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_capture)

        if not face_locations:
            util.msg_box('Erro de Cadastro',
                         'Nenhum rosto detectado na imagem. Por favor, posicione-se melhor e tente novamente.')
            return

        try:
            embeddings = face_recognition.face_encodings(rgb_capture, face_locations)[0]

            file_path = os.path.join(self.db_dir, f'{name}.pickle')

            if os.path.exists(file_path):
                response = util.msg_box('Atenção', f'Já existe um usuário com o nome "{name}". Deseja substituir?',
                                        type='yesno')
                if response == 'no':
                    return

            with open(file_path, 'wb') as f:
                pickle.dump(embeddings, f)

            util.msg_box('Registrado com sucesso', f'Usuário "{name}" cadastrado com as características faciais.')

            self.recognized_display_name = name
            self.display_start_time = time.time()
            self.recognition_active = True

            self.register_new_user_window.destroy()

        except IndexError:
            util.msg_box('Erro de Codificação',
                         'Não foi possível extrair características do rosto para cadastro. Tente novamente.')
        except Exception as e:
            util.msg_box('Erro Inesperado', f'Ocorreu um erro ao cadastrar: {e}')


if __name__ == "__main__":
    app = App()
    app.start()