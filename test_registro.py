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


class TestAppForRegistration:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.withdraw()

        self.db_dir = os.path.join(os.path.dirname(__file__), 'db')
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)

        self.log_path = os.path.join(os.path.dirname(__file__), 'log.txt')

        self.register_new_user_capture = None
        self.most_recent_capture_pil = None
        self.entry_text_register_new_user = util.get_entry_text(self.main_window)

        self.recognized_display_name = ""
        self.display_start_time = 0.0
        self.recognition_active = False

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get("1.0", "end-1c").strip()
        if not name:
            util.msg_box('Erro Cadastro', 'Insira um nome.')
            return

        if not hasattr(self, 'register_new_user_capture') or self.register_new_user_capture is None:
            util.msg_box('Erro Cadastro', 'Nenhuma imagem capturada.')
            return

        rgb_capture = cv2.cvtColor(self.register_new_user_capture, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_capture)

        if not face_locations:
            util.msg_box('Erro Cadastro',
                         'Nenhum rosto detectado. Posicione-se melhor e tente novamente.')
            return

        try:
            embeddings = face_recognition.face_encodings(rgb_capture, face_locations)[0]

            file_path = os.path.join(self.db_dir, f'{name}.pickle')

            if os.path.exists(file_path):
                print(f"AVISO: Usuario '{name}' ja existe. Sobrescrevendo para teste.")
                pass

            with open(file_path, 'wb') as f:
                pickle.dump(embeddings, f)

            util.msg_box('Registrado', f'Usuario "{name}" cadastrado.')

            self.recognized_display_name = name
            self.display_start_time = time.time()
            self.recognition_active = True


        except IndexError:
            util.msg_box('Erro Codificacao',
                         'Nao extraiu caracteristicas do rosto. Tente novamente.')
        except Exception as e:
            util.msg_box('Erro Inesperado', f'Erro ao cadastrar: {e}')


print("- INICIANDO TESTE 3: Simulacao Cadastro Usuario")
app_test_cadastro = None  # Inicializa como None para controle

try:
    app_test_cadastro = TestAppForRegistration()

    cap_test = cv2.VideoCapture(0)
    if not cap_test.isOpened():
        print("ERRO: Camera nao abriu para Teste 3.")
        print("STATUS: FALHOU [TESTE 3]")
    else:
        print("Webcam aberta para Teste 3. Pressione ENTER na janela 'Captura para Cadastro' para tirar a foto.")
        ret, frame_capture = cap_test.read()

        if ret:
            cv2.imshow('Captura para Cadastro', frame_capture)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            app_test_cadastro.register_new_user_capture = frame_capture.copy()

            nome_teste = input("Digite um nome UNICO para cadastro (Teste 3) e Enter: ").strip()
            if not nome_teste:
                nome_teste = "TesteUsuario" + str(int(time.time()))
                print(f"Nome vazio, usando nome padrao: {nome_teste}")

            app_test_cadastro.entry_text_register_new_user.delete(1.0, END)
            app_test_cadastro.entry_text_register_new_user.insert(1.0, nome_teste)

            print(f"Tentando cadastrar usuario: '{nome_teste}'...")
            app_test_cadastro.accept_register_new_user()

            expected_file_path = os.path.join(app_test_cadastro.db_dir, f'{nome_teste}.pickle')
            if os.path.exists(expected_file_path):
                print(f"SUCESSO: Arquivo '{nome_teste}.pickle' criado em '{app_test_cadastro.db_dir}'.")
                print("STATUS: PASSOU [TESTE 3] - Cadastro de usuario OK.")
                os.remove(expected_file_path)
                print(f"DEBUG: Arquivo '{nome_teste}.pickle' removido apos teste.")
            else:
                print(
                    f"AVISO: Arquivo '{nome_teste}.pickle' NAO criado. Verifique se um rosto foi detectado na captura.")
                print("STATUS: FALHOU [TESTE 3] - Cadastro de usuario com problema.")

            # Esta chamada aqui é a que provavelmente causa o erro se já foi destruída no final.
            # Vamos removê-la daqui e deixar apenas no finally.
            # app_test_cadastro.main_window.destroy()

        else:
            print("AVISO: Nenhuma imagem capturada para Teste 3. Pode ser problema na webcam.")
            print("STATUS: FALHOU [TESTE 3]")
    cap_test.release()
except Exception as e:
    print(f"ERRO GERAL no Teste 3 (Simulacao Cadastro): {e}")
    print("STATUS: FALHOU [TESTE 3]")
finally:
    # Adicionamos uma verificação antes de tentar destruir a janela
    if app_test_cadastro and hasattr(app_test_cadastro, 'main_window') and app_test_cadastro.main_window.winfo_exists():
        app_test_cadastro.main_window.destroy()
print("- FIM TESTE 3: Simulacao Cadastro Usuario")