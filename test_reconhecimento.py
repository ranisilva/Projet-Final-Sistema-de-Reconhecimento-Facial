import os
import cv2
import face_recognition
import pickle
import util

print("- INICIANDO TESTE 2: Reconhecimento Imagem Local")
db_dir_test = os.path.join(os.path.dirname(__file__), 'db')

if not os.path.exists(db_dir_test):
    print(f"ERRO: Pasta '{db_dir_test}' nao encontrada. Crie ou ajuste.")
else:
    test_image_path = os.path.join(os.path.dirname(__file__), 'teste_rosto.jpg')
    if not os.path.exists(test_image_path):
        print(f"ERRO: Imagem de teste '{test_image_path}' nao encontrada. Crie uma com um rosto conhecido e um desconhecido.")
        print("Para este teste, tente com uma imagem de rosto que VOCÊ JÁ CADASTROU e outra com um rosto NÃO CADASTRADO.")
    else:
        try:
            img = cv2.imread(test_image_path)
            if img is None:
                print(f"ERRO: Nao carregou imagem '{test_image_path}'. Verifique caminho/formato ou se esta corrompida.")
            else:
                print(f"Tentando reconhecer rosto em '{test_image_path}'...")

                rgb_test_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                face_locations_test = face_recognition.face_locations(rgb_test_img)

                name_recognized = "no_persons_found"
                if face_locations_test:
                    name_recognized = util.recognize(rgb_test_img, db_dir_test, face_locations_test)
                else:
                    print("OBS: Nao detectou nenhum rosto na imagem de teste.")

                print(f"RESULTADO: Rosto reconhecido: {name_recognized}")
                if name_recognized == 'unknown_person':
                    print("OBS: Rosto detectado mas nao cadastrado no DB.")
                    print("STATUS: PASSOU [TESTE 2] para rosto Desconhecido (se esperado).")
                elif name_recognized == 'no_persons_found':
                    print("OBS: Nenhum rosto detectado na imagem ou no DB.")
                    print("STATUS: PASSOU [TESTE 2] para nenhum rosto (se esperado).")
                else:
                    print(f"SUCESSO: Sistema identificou o rosto '{name_recognized}'.")
                    print("STATUS: PASSOU [TESTE 2] para rosto Conhecido.")
        except Exception as e:
            print(f"ERRO CRITICO no reconhecimento facial do Teste 2: {e}")
            print("STATUS: FALHOU [TESTE 2]")
print("- FIM TESTE 2: Reconhecimento Imagem Local")