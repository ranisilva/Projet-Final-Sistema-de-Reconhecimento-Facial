import os
import pickle
import face_recognition
import numpy as np


def serializar_embeddings_de_rostos():
    # Caminhos fornecidos por você
    caminho_pasta_origem_lfw = r'C:\Users\Admin\Documents\TCC-RANI\lfw\lfw'
    caminho_pasta_destino_pickle = r'C:\Users\Admin\Documents\TCC-RANI\lfw\pickle'

    # Garante que a pasta de destino exista
    if not os.path.exists(caminho_pasta_destino_pickle):
        os.makedirs(caminho_pasta_destino_pickle)

    for nome_pasta_pessoa in os.listdir(caminho_pasta_origem_lfw):
        caminho_pasta_pessoa = os.path.join(caminho_pasta_origem_lfw, nome_pasta_pessoa)

        if os.path.isdir(caminho_pasta_pessoa):
            for nome_arquivo_imagem in os.listdir(caminho_pasta_pessoa):
                caminho_completo_imagem = os.path.join(caminho_pasta_pessoa, nome_arquivo_imagem)

                # Verifica se é um arquivo de imagem JPG/JPEG
                if os.path.isfile(caminho_completo_imagem) and \
                        (nome_arquivo_imagem.lower().endswith('.jpg') or \
                         nome_arquivo_imagem.lower().endswith('.jpeg')):

                    try:
                        # Carrega a imagem
                        # face_recognition espera imagens RGB
                        imagem = face_recognition.load_image_file(caminho_completo_imagem)

                        # Obtém todas as codificações faciais na imagem
                        # Se houver várias faces, pegamos apenas a primeira para esta finalidade
                        face_encodings = face_recognition.face_encodings(imagem)

                        if face_encodings:
                            embedding_da_pessoa = face_encodings[0]  # Pega o primeiro embedding encontrado

                            # Cria o nome do arquivo .pkl baseado no nome da pasta da pessoa
                            nome_para_pickle = nome_pasta_pessoa.replace(" ", "_")
                            caminho_arquivo_pickle = os.path.join(caminho_pasta_destino_pickle,
                                                                  f"{nome_para_pickle}.pkl")

                            # Serializa o embedding (array numpy)
                            with open(caminho_arquivo_pickle, 'wb') as f:
                                pickle.dump(embedding_da_pessoa, f)

                            # Interrompe para a próxima pessoa, pois já pegamos a primeira imagem
                            break
                        else:
                            # Se não encontrou face na primeira imagem, tenta a próxima imagem na pasta
                            # ou a próxima pasta de pessoa se não houver mais imagens
                            continue  # Continua o loop para a próxima imagem dentro da mesma pasta

                    except Exception:
                        # Ignora erros de leitura ou processamento e tenta a próxima imagem
                        continue


serializar_embeddings_de_rostos()