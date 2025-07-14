import cv2

print("- INICIANDO TESTE 1: Webcam (Abertura)")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERRO: Camera nao abriu. Teste 1 falhou.")
else:
    print("Webcam aberta. Aperte 'q' para fechar.")
    for _ in range(30):
        ret, frame = cap.read()
        if ret:
            cv2.imshow('Webcam - Teste 1', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            print("AVISO: Falha ao ler frame da webcam no Teste 1.")
            break
    cap.release()
    cv2.destroyAllWindows()
    if not cap.isOpened():
        print("SUCESSO: Webcam abriu e fechou corretamente. Teste 1 passou.")
    else:
        print("AVISO: Webcam pode nao ter sido completamente liberada. Teste 1 com ressalvas.")
print("- FIM TESTE 1: Webcam (Abertura)")