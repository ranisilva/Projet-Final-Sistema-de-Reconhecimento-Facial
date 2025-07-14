import os
import datetime
import tkinter as tk

class TestAppForLog:
    def __init__(self):
        self.log_path = os.path.join(os.path.dirname(__file__), 'log.txt')
        self.main_window = tk.Tk()
        self.main_window.withdraw()

print("- INICIANDO TESTE 4: Verificacao Log Acesso")
app_test_log = TestAppForLog()

log_file_exists_before = os.path.exists(app_test_log.log_path)
if log_file_exists_before:
    os.remove(app_test_log.log_path)
    print(f"DEBUG: Log '{app_test_log.log_path}' removido para limpeza antes do teste.")

test_user = "UsuarioLog"
test_time_ms = 123.45
current_datetime_str = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

print(f"Simulando gravacao de log para usuario: '{test_user}' com tempo: {test_time_ms:.2f}ms")

try:
    with open(app_test_log.log_path, 'a') as f:
        f.write(f'{test_user},{current_datetime_str},{test_time_ms:.2f}ms\n')

    if os.path.exists(app_test_log.log_path):
        with open(app_test_log.log_path, 'r') as f:
            logged_content = f.read()
            print(f"Conteudo do log:\n{logged_content.strip()}")

            assert test_user in logged_content
            assert current_datetime_str in logged_content
            assert f"{test_time_ms:.2f}ms" in logged_content
            print("SUCESSO: Log gravado e verificado corretamente.")
            print("STATUS: PASSOU [TESTE 4] - Log de acesso OK.")
    else:
        print("ERRO: Arquivo de log nao foi criado.")
        print("STATUS: FALHOU [TESTE 4] - Log de acesso.")

except Exception as e:
    print(f"ERRO no Teste 4 (Log Acesso): {e}")
    print("STATUS: FALHOU [TESTE 4] - Erro no log de acesso.")
finally:
    if os.path.exists(app_test_log.log_path):
        os.remove(app_test_log.log_path)
        print(f"DEBUG: Log '{app_test_log.log_path}' removido apos teste.")
    if 'app_test_log' in locals() and hasattr(app_test_log, 'main_window'):
        app_test_log.main_window.destroy()
print("- FIM TESTE 4: Verificacao Log Acesso")