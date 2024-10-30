import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF
import datetime

# Base de datos simulada
usuarios_db = {}
habitaciones_db = {}
reservas_db = {}

# Clase Usuario
class Usuario:
    def __init__(self, nombre, email, contraseña):
        self.nombre = nombre
        self.email = email
        self.contraseña = contraseña

    @classmethod
    def crear_cuenta(cls, nombre, email, contraseña):
        if email in usuarios_db:
            messagebox.showerror("Error", "Ya existe una cuenta con este correo.")
        else:
            nuevo_usuario = cls(nombre, email, contraseña)
            usuarios_db[email] = nuevo_usuario
            messagebox.showinfo("Éxito", f"Cuenta creada exitosamente para {nombre}.")

    @classmethod
    def iniciar_sesion(cls, email, contraseña):
        usuario = usuarios_db.get(email)
        if usuario and usuario.contraseña == contraseña:
            messagebox.showinfo("Bienvenido", f"Inicio de sesión exitoso. Bienvenido {usuario.nombre}!")
            return True
        else:
            messagebox.showerror("Error", "Correo o contraseña incorrectos.")
            return False

    @classmethod
    def cambiar_contraseña(cls, email, contraseña_actual, nueva_contraseña):
        usuario = usuarios_db.get(email)
        if usuario and usuario.contraseña == contraseña_actual:
            usuario.contraseña = nueva_contraseña
            messagebox.showinfo("Éxito", "Contraseña cambiada exitosamente.")
        else:
            messagebox.showerror("Error", "La contraseña actual es incorrecta.")

# Clase Habitación
class Habitacion:
    def __init__(self, numero, tipo, precio, descripcion):
        self.numero = numero
        self.tipo = tipo
        self.precio = precio
        self.descripcion = descripcion

    @classmethod
    def registrar_habitacion(cls, numero, tipo, precio, descripcion):
        if numero in habitaciones_db:
            messagebox.showerror("Error", "Ya existe una habitación con ese número.")
        else:
            nueva_habitacion = cls(numero, tipo, precio, descripcion)
            habitaciones_db[numero] = nueva_habitacion
            messagebox.showinfo("Éxito", "Habitación registrada exitosamente.")

    @classmethod
    def buscar_habitaciones_disponibles(cls):
        if habitaciones_db:
            lista_habitaciones = [f"Habitación {num}: {hab.tipo}, Precio: {hab.precio}" for num, hab in habitaciones_db.items()]
            return "\n".join(lista_habitaciones)
        else:
            return "No hay habitaciones disponibles."

# Clase Reserva
from datetime import datetime

class Reserva:
    def __init__(self, habitacion, fecha_inicio, fecha_fin):
        self.habitacion = habitacion
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin


    @classmethod
    def realizar_reserva(cls, email, numero_habitacion, fecha_inicio, fecha_fin):
        if numero_habitacion not in habitaciones_db:
            messagebox.showerror("Error", "Habitación no disponible.")
        elif any(reserva.numero_habitacion == numero_habitacion for reserva in reservas_db.values()):
            messagebox.showerror("Error", "La habitación ya está reservada en esas fechas.")
        else:
            nueva_reserva = cls(email, numero_habitacion, fecha_inicio, fecha_fin)
            reservas_db[email] = nueva_reserva
            messagebox.showinfo("Éxito", "Reserva realizada exitosamente.")

    @classmethod
    def modificar_reserva(cls, email, nueva_fecha_inicio, nueva_fecha_fin):
        reserva = reservas_db.get(email)
        if reserva:
            reserva.fecha_inicio = nueva_fecha_inicio
            reserva.fecha_fin = nueva_fecha_fin
            messagebox.showinfo("Éxito", "Reserva modificada exitosamente.")
        else:
            messagebox.showerror("Error", "No se encontró una reserva para ese usuario.")

    @classmethod
    def cancelar_reserva(cls, email):
        if email in reservas_db:
            del reservas_db[email]
            messagebox.showinfo("Éxito", "Reserva cancelada exitosamente.")
        else:
            messagebox.showerror("Error", "No se encontró una reserva para ese usuario.")

    @classmethod
    def generar_reporte(cls, fecha_inicio, fecha_fin):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Reporte de Reservas", ln=True, align="C")

        for reserva in reservas_db.values():
            if fecha_inicio <= reserva.fecha_inicio <= fecha_fin:
                texto = f"Usuario: {reserva.usuario_email}, Habitación: {reserva.numero_habitacion}, " \
                        f"Fecha Inicio: {reserva.fecha_inicio}, Fecha Fin: {reserva.fecha_fin}"
                pdf.cell(200, 10, txt=texto, ln=True)
        
        pdf.output("reporte_reservas.pdf")
        messagebox.showinfo("Éxito", "Reporte generado exitosamente en reporte_reservas.pdf")

# Interfaz gráfica
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Hotel")

        # Pestañas
        self.tab_control = tk.Frame(self.root)
        self.tab_control.pack()

        self.boton_crear_cuenta = tk.Button(self.tab_control, text="Crear Cuenta", command=self.mostrar_crear_cuenta)
        self.boton_crear_cuenta.grid(row=0, column=0)

        self.boton_iniciar_sesion = tk.Button(self.tab_control, text="Iniciar Sesión", command=self.mostrar_iniciar_sesion)
        self.boton_iniciar_sesion.grid(row=0, column=1)

        self.boton_cambiar_contraseña = tk.Button(self.tab_control, text="Cambiar Contraseña", command=self.mostrar_cambiar_contraseña)
        self.boton_cambiar_contraseña.grid(row=0, column=2)

        self.boton_registrar_habitacion = tk.Button(self.tab_control, text="Registrar Habitación", command=self.mostrar_registrar_habitacion)
        self.boton_registrar_habitacion.grid(row=0, column=3)

        self.boton_buscar_habitaciones = tk.Button(self.tab_control, text="Buscar Habitaciones", command=self.mostrar_buscar_habitaciones)
        self.boton_buscar_habitaciones.grid(row=0, column=4)

        self.boton_realizar_reserva = tk.Button(self.tab_control, text="Realizar Reserva", command=self.mostrar_realizar_reserva)
        self.boton_realizar_reserva.grid(row=0, column=5)

        self.boton_modificar_reserva = tk.Button(self.tab_control, text="Modificar Reserva", command=self.mostrar_modificar_reserva)
        self.boton_modificar_reserva.grid(row=0, column=6)

        self.boton_cancelar_reserva = tk.Button(self.tab_control, text="Cancelar Reserva", command=self.mostrar_cancelar_reserva)
        self.boton_cancelar_reserva.grid(row=0, column=7)

        self.boton_generar_reporte = tk.Button(self.tab_control, text="Generar Reporte", command=self.mostrar_generar_reporte)
        self.boton_generar_reporte.grid(row=0, column=8)

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()

        self.mostrar_crear_cuenta()

    def limpiar_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def mostrar_crear_cuenta(self):
        self.limpiar_frame()
        tk.Label(self.main_frame, text="Nombre").grid(row=0, column=0)
        tk.Label(self.main_frame, text="Email").grid(row=1, column=0)
        tk.Label(self.main_frame, text="Contraseña").grid(row=2, column=0)

        nombre_entry = tk.Entry(self.main_frame)
        email_entry = tk.Entry(self.main_frame)
        contraseña_entry = tk.Entry(self.main_frame, show="*")

        nombre_entry.grid(row=0, column=1)
        email_entry.grid(row=1, column=1)
        contraseña_entry.grid(row=2, column=1)

        def crear_cuenta():
            Usuario.crear_cuenta(nombre_entry.get(), email_entry.get(), contraseña_entry.get())

        tk.Button(self.main_frame, text="Crear Cuenta", command=crear_cuenta).grid(row=3, column=1)

    def mostrar_iniciar_sesion(self):
        self.limpiar_frame()
        tk.Label(self.main_frame, text="Email").grid(row=0, column=0)
        tk.Label(self.main_frame, text="Contraseña").grid(row=1, column=0)

        email_entry = tk.Entry(self.main_frame)
        contraseña_entry = tk.Entry(self.main_frame, show="*")

        email_entry.grid(row=0, column=1)
        contraseña_entry.grid(row=1, column=1)

        def iniciar_sesion():
            Usuario.iniciar_sesion(email_entry.get(), contraseña_entry.get())

        tk.Button(self.main_frame, text="Iniciar Sesión", command=iniciar_sesion).grid(row=2, column=1)

    def mostrar_cambiar_contraseña(self):
        self.limpiar_frame()
        tk.Label(self.main_frame, text="Email").grid(row=0, column=0)
        tk.Label(self.main_frame, text="Contraseña Actual").grid(row=1, column=0)
        tk.Label(self.main_frame, text="Nueva Contraseña").grid(row=2, column=0)

        email_entry = tk.Entry(self.main_frame)
        contraseña_actual_entry = tk.Entry(self.main_frame, show="*")
        nueva_contraseña_entry = tk.Entry(self.main_frame, show="*")

        email_entry.grid(row=0, column=1)
        contraseña_actual_entry.grid(row=1, column=1)
        nueva_contraseña_entry.grid(row=2, column=1)

        def cambiar_contraseña():
            Usuario.cambiar_contraseña(email_entry.get(), contraseña_actual_entry.get(), nueva_contraseña_entry.get())

        tk.Button(self.main_frame, text="Cambiar Contraseña", command=cambiar_contraseña).grid(row=3, column=1)

    def mostrar_registrar_habitacion(self):
        self.limpiar_frame()
        tk.Label(self.main_frame, text="Número").grid(row=0, column=0)
        tk.Label(self.main_frame, text="Tipo").grid(row=1, column=0)
        tk.Label(self.main_frame, text="Precio").grid(row=2, column=0)
        tk.Label(self.main_frame, text="Descripción").grid(row=3, column=0)

        numero_entry = tk.Entry(self.main_frame)
        tipo_entry = tk.Entry(self.main_frame)
        precio_entry = tk.Entry(self.main_frame)
        descripcion_entry = tk.Entry(self.main_frame)

        numero_entry.grid(row=0, column=1)
        tipo_entry.grid(row=1, column=1)
        precio_entry.grid(row=2, column=1)
        descripcion_entry.grid(row=3, column=1)

        def registrar_habitacion():
            Habitacion.registrar_habitacion(numero_entry.get(), tipo_entry.get(), precio_entry.get(), descripcion_entry.get())

        tk.Button(self.main_frame, text="Registrar Habitación", command=registrar_habitacion).grid(row=4, column=1)

    def mostrar_buscar_habitaciones(self):
        self.limpiar_frame()
        habitaciones_disponibles = Habitacion.buscar_habitaciones_disponibles()
        tk.Label(self.main_frame, text="Habitaciones Disponibles").pack()
        tk.Label(self.main_frame, text=habitaciones_disponibles).pack()

    def mostrar_realizar_reserva(self):
        self.limpiar_frame()
        tk.Label(self.main_frame, text="Email").grid(row=0, column=0)
        tk.Label(self.main_frame, text="Número de Habitación").grid(row=1, column=0)
        tk.Label(self.main_frame, text="Fecha Inicio (YYYY-MM-DD)").grid(row=2, column=0)
        tk.Label(self.main_frame, text="Fecha Fin (YYYY-MM-DD)").grid(row=3, column=0)

        email_entry = tk.Entry(self.main_frame)
        habitacion_entry = tk.Entry(self.main_frame)
        fecha_inicio_entry = tk.Entry(self.main_frame)
        fecha_fin_entry = tk.Entry(self.main_frame)

        email_entry.grid(row=0, column=1)
        habitacion_entry.grid(row=1, column=1)
        fecha_inicio_entry.grid(row=2, column=1)
        fecha_fin_entry.grid(row=3, column=1)

        def realizar_reserva():
            Reserva.realizar_reserva(email_entry.get(), habitacion_entry.get(), fecha_inicio_entry.get(), fecha_fin_entry.get())

        tk.Button(self.main_frame, text="Realizar Reserva", command=realizar_reserva).grid(row=4, column=1)

    def mostrar_modificar_reserva(self):
        self.limpiar_frame()
        tk.Label(self.main_frame, text="Email").grid(row=0, column=0)
        tk.Label(self.main_frame, text="Nueva Fecha Inicio (YYYY-MM-DD)").grid(row=1, column=0)
        tk.Label(self.main_frame, text="Nueva Fecha Fin (YYYY-MM-DD)").grid(row=2, column=0)

        email_entry = tk.Entry(self.main_frame)
        nueva_fecha_inicio_entry = tk.Entry(self.main_frame)
        nueva_fecha_fin_entry = tk.Entry(self.main_frame)

        email_entry.grid(row=0, column=1)
        nueva_fecha_inicio_entry.grid(row=1, column=1)
        nueva_fecha_fin_entry.grid(row=2, column=1)

        def modificar_reserva():
            Reserva.modificar_reserva(email_entry.get(), nueva_fecha_inicio_entry.get(), nueva_fecha_fin_entry.get())

        tk.Button(self.main_frame, text="Modificar Reserva", command=modificar_reserva).grid(row=3, column=1)

    def mostrar_cancelar_reserva(self):
        self.limpiar_frame()
        tk.Label(self.main_frame, text="Email").grid(row=0, column=0)

        email_entry = tk.Entry(self.main_frame)
        email_entry.grid(row=0, column=1)

        def cancelar_reserva():
            Reserva.cancelar_reserva(email_entry.get())

        tk.Button(self.main_frame, text="Cancelar Reserva", command=cancelar_reserva).grid(row=1, column=1)

    def mostrar_generar_reporte(self):
        self.limpiar_frame()
        tk.Label(self.main_frame, text="Fecha Inicio (YYYY-MM-DD)").grid(row=0, column=0)
        tk.Label(self.main_frame, text="Fecha Fin (YYYY-MM-DD)").grid(row=1, column=0)

        fecha_inicio_entry = tk.Entry(self.main_frame)
        fecha_fin_entry = tk.Entry(self.main_frame)

        fecha_inicio_entry.grid(row=0, column=1)
        fecha_fin_entry.grid(row=1, column=1)

        def generar_reporte():
            Reserva.generar_reporte(fecha_inicio_entry.get(), fecha_fin_entry.get())

        tk.Button(self.main_frame, text="Generar Reporte", command=generar_reporte).grid(row=2, column=1)

# Ejecutar la aplicación
root = tk.Tk()
app = App(root)
root.mainloop()
