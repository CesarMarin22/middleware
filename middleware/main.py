import serial
import tkinter as tk
from tkinter import ttk, Scrollbar, Text
import threading

# Configuración de la comunicación serial para COM1 (ajusta según tus necesidades)
puerto_com1 = serial.Serial('COM6', baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=False, rtscts=False, dsrdtr=False)

# Función para enviar un mensaje limitado a 30 caracteres y sin espacios en blanco
def enviar_mensaje():
    mensaje = entrada_enviar.get().strip()  # Obtiene el mensaje desde el área de texto y quita espacios en blanco
    mensaje = mensaje[:30]  # Limita el mensaje a 30 caracteres
    if mensaje:
        puerto_com1.write(mensaje.encode('ascii'))    # Envía el mensaje
        entrada_enviar.delete(0, tk.END)          # Borra el mensaje enviado
        mensaje = "Yo: " + mensaje  # Agregar "Yo: " al mensaje enviado
        agregar_mensaje_enviado(mensaje)              # Agrega el mensaje enviado a la sección de mensajes enviados

# Función para agregar un mensaje a la sección de mensajes recibidos
def agregar_mensaje_recibido(mensaje):
    if mensaje.strip().endswith('>'):
        mensaje += '\n'  # Agrega un salto de línea si el mensaje termina con '>'
    salida_recibir.config(state=tk.NORMAL)        # Habilita la edición del área de texto
    salida_recibir.insert(tk.END, mensaje)        # Agrega el mensaje al final
    salida_recibir.config(state=tk.DISABLED)      # Deshabilita la edición del área de texto
    salida_recibir.see(tk.END)                    # Hace scroll para mostrar el mensaje más reciente

# Función para agregar un mensaje a la sección de mensajes enviados
def agregar_mensaje_enviado(mensaje):
    salida_enviar.config(state=tk.NORMAL)          # Habilita la edición del área de texto
    salida_enviar.insert(tk.END, mensaje)          # Agrega el mensaje al final
    salida_enviar.insert(tk.END, '\n')             # Agrega un salto de línea
    salida_enviar.config(state=tk.DISABLED)        # Deshabilita la edición del área de texto
    salida_enviar.see(tk.END)                      # Hace scroll para mostrar el mensaje más reciente

# Función para leer mensajes en segundo plano
def leer_mensajes():
    while True:
        mensaje = puerto_com1.read_all().decode('ascii')
        if mensaje:
            agregar_mensaje_recibido(mensaje)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Comunicación Serial (COM6)")

# Dividir la ventana en dos partes verticales
frame_izquierdo = tk.Frame(ventana, width=200)
frame_izquierdo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

frame_derecho = tk.Frame(ventana)
frame_derecho.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Área de entrada para enviar mensajes limitados a 30 caracteres
entrada_enviar = tk.Entry(frame_izquierdo)
entrada_enviar.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

boton_enviar = tk.Button(frame_izquierdo, text="Enviar", command=enviar_mensaje)
boton_enviar.pack(pady=5)

# Área de salida para mensajes recibidos
frame_recibir = ttk.LabelFrame(frame_derecho, text="Mensajes Recibidos")
frame_recibir.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

salida_recibir = Text(frame_recibir, height=10, width=40, state=tk.DISABLED)
salida_recibir.pack(fill=tk.BOTH, expand=True)

scrollbar_recibir = Scrollbar(frame_recibir, command=salida_recibir.yview)
scrollbar_recibir.pack(side=tk.RIGHT, fill=tk.Y)
salida_recibir.config(yscrollcommand=scrollbar_recibir.set)

# Área de salida para mensajes enviados
frame_enviar = ttk.LabelFrame(frame_derecho, text="Mensajes Enviados")
frame_enviar.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

salida_enviar = Text(frame_enviar, height=5, width=40, state=tk.DISABLED)
salida_enviar.pack(fill=tk.BOTH, expand=True)

scrollbar_enviar = Scrollbar(frame_enviar, command=salida_enviar.yview)
scrollbar_enviar.pack(side=tk.RIGHT, fill=tk.Y)
salida_enviar.config(yscrollcommand=scrollbar_enviar.set)

# Iniciar el hilo para leer mensajes en segundo plano
thread = threading.Thread(target=leer_mensajes)
thread.daemon = True
thread.start()

# Iniciar la interfaz gráfica
ventana.mainloop()