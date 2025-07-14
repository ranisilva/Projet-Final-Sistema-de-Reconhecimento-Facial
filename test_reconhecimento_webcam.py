import os
import cv2
import face_recognition
import pickle
import util

print("- INICIANDO TESTE 5: Reconhecimento Facial em Tempo Real (Câmera)")
db_dir_test = os.path.join(os.path.dirname(__file__), 'db')

if not os.path.exists(db_dir_test):
    print(f"ERRO: Pasta '{db_dir_test}' não encontrada. Crie-a ou ajuste o caminho.")
    print("Por favor, certifique-se de que seu banco de dados de faces esteja disponível.")
else:
    # Initialize webcam
    cap = cv2.VideoCapture(0)  # 0 represents the default webcam

    if not cap.isOpened():
        print("ERRO: Não foi possível abrir a câmera. Verifique se ela está conectada e disponível.")
    else:
        print("Câmera aberta com sucesso. Pressione 'q' para sair.")
        print("Aguardando detecção e reconhecimento de rosto...")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("ERRO: Não foi possível ler o frame da câmera. Encerrando.")
                break

            # Convert the BGR image (OpenCV default) to RGB (face_recognition requires RGB)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Find all face locations and face encodings in the current frame
            face_locations = face_recognition.face_locations(rgb_frame)

            name_recognized = "no_persons_found"

            if face_locations:
                # Recognize faces in the current frame
                name_recognized = util.recognize(rgb_frame, db_dir_test, face_locations)

                # Draw bounding boxes and names on the frame
                for (top, right, bottom, left) in face_locations:
                    # Draw a box around the face
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

                    # Draw a label with a name below the face
                    cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
                    font = cv2.FONT_HERSHEY_DUPLEX
                    cv2.putText(frame, name_recognized, (left + 6, bottom - 6), font, 0.7, (0, 0, 0), 1)

                if name_recognized == 'unknown_person':
                    print("OBS: Rosto detectado mas não cadastrado no DB.")
                elif name_recognized != 'no_persons_found':
                    print(f"SUCESSO: Sistema identificou o rosto '{name_recognized}'.")
            # else: # This else statement is commented out to avoid excessive console output if no faces are continuously detected.
            #     print("OBS: Não detectou nenhum rosto no frame.")

            # Display the resulting frame
            cv2.imshow('Reconhecimento Facial (Pressione Q para Sair)', frame)

            # Break the loop on 'q' key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Encerrando o reconhecimento facial...")
                break

        # Release the webcam and destroy all OpenCV windows
        cap.release()
        cv2.destroyAllWindows()
        print("STATUS: Teste 2 Encerrado.")

print("- FIM TESTE 5: Reconhecimento Facial em Tempo Real (Câmera)")