import mysql.connector
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime

class TallerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Taller Mecánico - Login")
        self.conexion = None
        self.cursor = None
        self.admin_id = None  
        self.admin_name = None
        self.rol = None
        self.create_login_screen()

    def create_connection(self):
        try:
            self.conexion = mysql.connector.connect(
                host="127.0.0.1",
                user="root",
                password="server",
                database="dbtaller_mecanico",
                charset="utf8mb4",
                collation="utf8mb4_general_ci"
            )
            self.cursor = self.conexion.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al conectar con la base de datos: {err}")

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.conexion:
            self.conexion.close()

    def create_login_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.login_label = tk.Label(self.root, text="Inicio de Sesión", font=("Arial", 16))
        self.login_label.pack(pady=20)

        self.username_label = tk.Label(self.root, text="Correo electronico:")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self.root, text="Contraseña:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self.root, text="Iniciar Sesión", command=self.login)
        self.login_button.pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        self.create_connection()

        if not self.cursor:
            return

        query = "SELECT * FROM usuarios WHERE correo_electronico = %s AND contrasena = %s"
        self.cursor.execute(query, (username, password))
        result = self.cursor.fetchone()

        if result:
            self.admin_id = result[0]  # Guardar el ID del administrador
            self.admin_name = result[3]  # Guardar el nombre del administrador
            self.rol = result[4]
            messagebox.showinfo("Inicio de Sesión", "¡Inicio de sesión exitoso!")
            self.create_menu_screen()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

        self.close_connection()

    def create_menu_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.menu_label = tk.Label(self.root, text="Menú Principal", font=("Arial", 16))
        self.menu_label.pack(pady=20)

        self.users_button = tk.Button(self.root, text="Administrar Usuarios", command=self.create_user_management_screen)
        self.users_button.pack(pady=10)

        self.boton_clientes = tk.Button(self.root, text="Administrar Clientes", command=self.crear_pantalla_clientes)
        self.boton_clientes.pack(pady=10)

        self.boton_vehiculos = tk.Button(self.root, text="Administrar vehiculos", command=self.crear_pantalla_vehiculos)
        self.boton_vehiculos.pack(pady=10)

        self.boton_piezas = tk.Button(self.root, text="Piezas", command=self.crear_pantalla_piezas)
        self.boton_piezas.pack(pady=10)

        self.boton_reparar = tk.Button(self.root, text="Reparaciones", command=self.crear_pantalla_reparacion)
        self.boton_reparar.pack(pady=10)

        self.logout_button = tk.Button(self.root, text="Cerrar Sesión", command=self.create_login_screen)
        self.logout_button.pack(pady=10)

        if self.rol == "secretaria" or self.rol == "mecanico":
            self.users_button.config(state="disabled")
        if self.rol == "mecanico":
            self.boton_clientes.config(state="disabled")
        if self.rol == "secretaria" or self.rol == "mecanico":
            self.boton_piezas.config(state="disabled")
        if self.rol == "secretaria":
            self.boton_reparar.config(state="disabled")

    def create_user_management_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.user_management_label = tk.Label(self.root, text="Administración de Usuarios", font=("Arial", 16))
        self.user_management_label.pack(pady=20)

        self.add_user_button = tk.Button(self.root, text="Agregar Usuario", command=self.add_user)
        self.add_user_button.pack(pady=10)

        self.edit_user_button = tk.Button(self.root, text="Editar Usuario", command=self.edit_user)
        self.edit_user_button.pack(pady=10)

        self.search_user_button = tk.Button(self.root, text="Buscar Usuario", command=self.search_user)
        self.search_user_button.pack(pady=10)

        self.back_button = tk.Button(self.root, text="Volver al Menú", command=self.create_menu_screen)
        self.back_button.pack(pady=20)

    def crear_pantalla_clientes(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.leyenda_administrador_clientes = tk.Label(self.root, text="Administración de Clientes", font=("Arial", 16))
        self.leyenda_administrador_clientes.pack(pady=20)

        self.add_user_button = tk.Button(self.root, text="Agregar Cliente", command=self.agregar_cliente)
        self.add_user_button.pack(pady=10)

        self.edit_user_button = tk.Button(self.root, text="Editar Cliente", command=self.editar_cliente)
        self.edit_user_button.pack(pady=10)

        self.search_user_button = tk.Button(self.root, text="Buscar Cliente", command=self.buscar_cliente)
        self.search_user_button.pack(pady=10)

        self.back_button = tk.Button(self.root, text="Volver al Menú", command=self.create_menu_screen)
        self.back_button.pack(pady=20)

        if self.rol == "secretaria":
            self.edit_user_button.config(state="disabled")

    def crear_pantalla_vehiculos(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.leyenda_administrador_vehiculos = tk.Label(self.root, text="Administración de Vehiculos", font=("Arial", 16))
        self.leyenda_administrador_vehiculos.pack(pady=20)
        
        self.boton_agregar_vehiculo = tk.Button(self.root, text="Agregar vehiculo", command=self.agregar_vehiculo)
        self.boton_agregar_vehiculo.pack(pady=10)

        self.boton_editar_vehiculo = tk.Button(self.root, text="Editar vehiculo", command=self.editar_vehiculo)
        self.boton_editar_vehiculo.pack(pady=10)

        self.boton_buscar_vehiculo = tk.Button(self.root, text="Buscar vehiculo", command=self.buscar_vehiculo)
        self.boton_buscar_vehiculo.pack(pady=10)

        self.back_button = tk.Button(self.root, text="Volver al Menú", command=self.create_menu_screen)
        self.back_button.pack(pady=20)

        if self.rol == "mecanico":
            self.boton_agregar_vehiculo.config(state="disabled")
            self.boton_editar_vehiculo.config(state="disabled")
        if self.rol == "secretaria":
            self.boton_editar_vehiculo.config(state="disabled")

    def crear_pantalla_piezas(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.leyenda_administrar_piezas = tk.Label(self.root, text="Administrar Piezas", font=("Arial", 16))
        self.leyenda_administrar_piezas.pack(pady=20)

        self.boton_agregar_pieza = tk.Button(self.root, text="Agregar nueva pieza", command=self.agregar_pieza)
        self.boton_agregar_pieza.pack(pady=10)

        self.boton_editar_pieza = tk.Button(self.root, text="Editar pieza", command=self.editar_pieza)
        self.boton_editar_pieza.pack(pady=10)

        self.boton_buscar_pieza = tk.Button(self.root, text="Buscar pieza", command=self.buscar_pieza)
        self.boton_buscar_pieza.pack(pady=10)

        self.back_button = tk.Button(self.root, text="Volver al Menú", command=self.create_menu_screen)
        self.back_button.pack(pady=20)

    def crear_pantalla_reparacion(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.leyenda_reparacion = tk.Label(self.root, text="Administrar Reparaciones", font=("Arial", 16))
        self.leyenda_reparacion.pack(pady=20)

        self.boton_agregar_reparacion= tk.Button(self.root, text="Agregar nueva reparacion", command=self.agregar_reparacion)
        self.boton_agregar_reparacion.pack(pady=10)

        self.boton_editar_reparacion = tk.Button(self.root, text="Editar reparacion", command=self.editar_reparacion)
        self.boton_editar_reparacion.pack(pady=10)

        self.boton_buscar_reparacion = tk.Button(self.root, text="Buscar reparacion", command=self.buscar_reparacion)
        self.boton_buscar_reparacion.pack(pady=10)

        self.back_button = tk.Button(self.root, text="Volver al Menú", command=self.create_menu_screen)
        self.back_button.pack(pady=20) 

        if self.rol == "mecanico":
            self.boton_editar_reparacion.config(state="disabled")       

    def agregar_reparacion(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.create_connection()
        
        query = "SELECT matricula FROM vehiculos"
        self.cursor.execute(query)
        result_matricula = self.cursor.fetchall()

        query = "SELECT id_pieza FROM piezas"
        self.cursor.execute(query)
        result_idPieza = self.cursor.fetchall()

        self.close_connection()

        self.leyenda_agregar_reparacion = tk.Label(self.root, text="Agregar Reparacion", font=("Arial", 16))
        self.leyenda_agregar_reparacion.pack(pady=20)

        self.leyenda_matricula_reparacion = tk.Label(self.root, text="Matricula:")
        self.leyenda_matricula_reparacion.pack(pady=5)
        matriculas = [row[0] for row in result_matricula]
        self.combobox_matricula_reparacion = ttk.Combobox(self.root, values=matriculas)
        self.combobox_matricula_reparacion.pack(pady=5)

        self.leyenda_pieza_reparacion = tk.Label(self.root, text="ID de la pieza:")
        self.leyenda_pieza_reparacion.pack(pady=5)
        piezas = [row[0] for row in result_idPieza]
        self.combobox_pieza_reparacion = ttk.Combobox(self.root, values=piezas)
        self.combobox_pieza_reparacion.pack(pady=5)

        self.leyenda_piezas_utilizadas = tk.Label(self.root, text="Ingresa piezas utilizadas:")
        self.leyenda_piezas_utilizadas.pack(pady=5)
        self.entrada_piezas_utilizadas = tk.Entry(self.root)
        self.entrada_piezas_utilizadas.pack(pady=5)

        self.leyenda_fecha_entrada = tk.Label(self.root, text="Ingresa la fecha del ingreso del vehiculo:")
        self.leyenda_fecha_entrada.pack(pady=5)
        self.entrada_fecha_entrada = tk.Entry(self.root)
        self.entrada_fecha_entrada.pack(pady=5)

        self.leyenda_fecha_salida = tk.Label(self.root, text="Ingresa la fecha de salida del vehiculo:")
        self.leyenda_fecha_salida.pack(pady=5)
        self.entrada_fecha_salida = tk.Entry(self.root)
        self.entrada_fecha_salida.pack(pady=5)

        self.leyenda_falla = tk.Label(self.root, text="Ingresa la falla:")
        self.leyenda_falla.pack(pady=5)
        self.entrada_falla = tk.Entry(self.root)
        self.entrada_falla.pack(pady=5)

        self.leyenda_precio = tk.Label(self.root, text="Costo:")
        self.leyenda_precio.pack(pady=5)
        self.entrada_precio = tk.Entry(self.root)
        self.entrada_precio.pack(pady=5)

        self.save_button = tk.Button(self.root, text="Guardar", command=self.guardar_reparacion)
        self.save_button.pack(pady=20)

        self.back_button = tk.Button(self.root, text="Volver", command=self.crear_pantalla_reparacion)
        self.back_button.pack(pady=10)

    def guardar_reparacion(self):
        matricula = self.combobox_matricula_reparacion.get()
        pieza_id = self.combobox_pieza_reparacion.get()
        piezas_utilizadas = self.entrada_piezas_utilizadas.get()
        fecha_entrada = self.entrada_fecha_entrada.get()
        fecha_salida = self.entrada_fecha_salida.get()
        falla = self.entrada_falla.get()
        precio = self.entrada_precio.get()

        if not (matricula and pieza_id and piezas_utilizadas and fecha_entrada and fecha_salida and falla and precio):
            messagebox.showerror("Error", "Todos los campos deben ser llenados.")
            return

        try:
            piezas_utilizadas = int(piezas_utilizadas)
            precio = float(precio)
        except ValueError:
            messagebox.showerror("Error", "Cantidad de piezas y precio deben ser numéricos.")
            return

        try:
            fecha_entrada_dt = datetime.strptime(fecha_entrada, '%Y-%m-%d')
            fecha_salida_dt = datetime.strptime(fecha_salida, '%Y-%m-%d')

            if fecha_salida_dt < fecha_entrada_dt:
                messagebox.showerror("Error", "La fecha de salida no puede ser anterior a la fecha de entrada.")
                return
        except ValueError:
            messagebox.showerror("Error", "Las fechas deben estar en el formato AAAA-MM-DD.")
            return

        self.create_connection()

        try:
            query = "SELECT cantidad FROM piezas WHERE id_pieza = %s"
            self.cursor.execute(query, (pieza_id,))
            result = self.cursor.fetchone()

            if not result:
                messagebox.showerror("Error", f"No se encontró la pieza con ID {pieza_id}")
                self.close_connection()
                return

            cantidad_actual = result[0]

            if piezas_utilizadas > cantidad_actual:
                messagebox.showerror("Error", "No hay suficientes piezas disponibles.")
                self.close_connection()
                return

            nueva_cantidad = cantidad_actual - piezas_utilizadas
            query = "UPDATE piezas SET cantidad = %s WHERE id_pieza = %s"
            self.cursor.execute(query, (nueva_cantidad, pieza_id))

            query = """
                INSERT INTO reparaciones (matricula, pieza, fecha_entrada, fecha_salida, falla, precio)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (matricula, pieza_id, fecha_entrada, fecha_salida, falla, precio))

            self.conexion.commit()

            messagebox.showinfo("Éxito", "Reparación agregada exitosamente.")

        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al agregar la reparación: {str(e)}")

        finally:
            self.close_connection()
            self.crear_pantalla_reparacion()

    def editar_reparacion(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.leyenda_editar_reparacion = tk.Label(self.root, text="Editar Reparación", font=("Arial", 16))
        self.leyenda_editar_reparacion.pack(pady=20)

        self.leyenda_folio_buscar = tk.Label(self.root, text="Folio de Reparación:")
        self.leyenda_folio_buscar.pack(pady=5)
        self.entrada_folio_buscar = tk.Entry(self.root)
        self.entrada_folio_buscar.pack(pady=5)

        self.find_edit_button = tk.Button(self.root, text="Buscar", command=self.buscar_reparacion_a_editar)
        self.find_edit_button.pack(pady=20)

        self.back_button = tk.Button(self.root, text="Volver", command=self.crear_pantalla_reparacion)
        self.back_button.pack(pady=10)


    def buscar_reparacion_a_editar(self):
        folio = self.entrada_folio_buscar.get()

        if not folio:
            messagebox.showerror("Error", "El folio no puede estar vacío.")
            return

        try:
            folio = int(folio)  # Asegurarse que el folio sea un número
        except ValueError:
            messagebox.showerror("Error", "El folio debe ser numérico.")
            return

        self.create_connection()

        try:
            query = "SELECT * FROM reparaciones WHERE folio = %s"
            self.cursor.execute(query, (folio,))
            result = self.cursor.fetchone()

            if result:
                self.leyenda_matricula_editar = tk.Label(self.root, text="Matricula:")
                self.leyenda_matricula_editar.pack(pady=5)
                self.entrada_matricula_editar = tk.Entry(self.root)
                self.entrada_matricula_editar.insert(0, result[1])  # Matrícula
                self.entrada_matricula_editar.pack(pady=5)

                self.leyenda_pieza_editar = tk.Label(self.root, text="ID de la pieza:")
                self.leyenda_pieza_editar.pack(pady=5)
                self.entrada_pieza_editar = tk.Entry(self.root)
                self.entrada_pieza_editar.insert(0, result[2])  # Pieza
                self.entrada_pieza_editar.pack(pady=5)

                self.leyenda_fecha_entrada_editar = tk.Label(self.root, text="Fecha de entrada:")
                self.leyenda_fecha_entrada_editar.pack(pady=5)
                self.entrada_fecha_entrada_editar = tk.Entry(self.root)
                self.entrada_fecha_entrada_editar.insert(0, result[3])  # Fecha de entrada
                self.entrada_fecha_entrada_editar.pack(pady=5)

                self.leyenda_fecha_salida_editar = tk.Label(self.root, text="Fecha de salida:")
                self.leyenda_fecha_salida_editar.pack(pady=5)
                self.entrada_fecha_salida_editar = tk.Entry(self.root)
                self.entrada_fecha_salida_editar.insert(0, result[4])  # Fecha de salida
                self.entrada_fecha_salida_editar.pack(pady=5)

                self.leyenda_falla_editar = tk.Label(self.root, text="Falla:")
                self.leyenda_falla_editar.pack(pady=5)
                self.entrada_falla_editar = tk.Entry(self.root)
                self.entrada_falla_editar.insert(0, result[5])  # Falla
                self.entrada_falla_editar.pack(pady=5)

                self.leyenda_precio_editar = tk.Label(self.root, text="Precio:")
                self.leyenda_precio_editar.pack(pady=5)
                self.entrada_precio_editar = tk.Entry(self.root)
                self.entrada_precio_editar.insert(0, result[6])  # Precio
                self.entrada_precio_editar.pack(pady=5)

                self.save_button = tk.Button(self.root, text="Guardar Cambios", command=lambda: self.actualizar_reparacion(folio))
                self.save_button.pack(pady=20)

                self.back_button = tk.Button(self.root, text="Volver", command=self.crear_pantalla_reparacion)
                self.back_button.pack(pady=10)
            else:
                messagebox.showerror("Error", f"No se encontró la reparación con folio {folio}")

        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al buscar la reparación: {str(e)}")

        finally:
            self.close_connection()

    def actualizar_reparacion(self, folio):
        matricula = self.entrada_matricula_editar.get()
        pieza_id = self.entrada_pieza_editar.get()
        fecha_entrada = self.entrada_fecha_entrada_editar.get()
        fecha_salida = self.entrada_fecha_salida_editar.get()
        falla = self.entrada_falla_editar.get()
        precio = self.entrada_precio_editar.get()

        if not (matricula and pieza_id and fecha_entrada and fecha_salida and falla and precio):
            messagebox.showerror("Error", "Todos los campos deben ser llenados.")
            return

        try:
            precio = float(precio)
            fecha_entrada_dt = datetime.strptime(fecha_entrada, '%Y-%m-%d')
            fecha_salida_dt = datetime.strptime(fecha_salida, '%Y-%m-%d')

            if fecha_salida_dt < fecha_entrada_dt:
                messagebox.showerror("Error", "La fecha de salida no puede ser anterior a la fecha de entrada.")
                return
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha incorrecto o precio no numérico.")
            return

        self.create_connection()

        try:
            query = "SELECT matricula FROM vehiculos WHERE matricula = %s"
            self.cursor.execute(query, (matricula,))
            result_matricula = self.cursor.fetchone()

            if not result_matricula:
                messagebox.showerror("Error", f"No se encontró el vehículo con matrícula {matricula}")
                self.close_connection()
                return

            query = "SELECT id_pieza FROM piezas WHERE id_pieza = %s"
            self.cursor.execute(query, (pieza_id,))
            result_pieza = self.cursor.fetchone()

            if not result_pieza:
                messagebox.showerror("Error", f"No se encontró la pieza con ID {pieza_id}")
                self.close_connection()
                return

            query = """
                UPDATE reparaciones 
                SET matricula = %s, pieza = %s, fecha_entrada = %s, fecha_salida = %s, falla = %s, precio = %s
                WHERE folio = %s
            """
            self.cursor.execute(query, (matricula, pieza_id, fecha_entrada, fecha_salida, falla, precio, folio))
            self.conexion.commit()

            messagebox.showinfo("Éxito", "Reparación actualizada exitosamente.")

        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al actualizar la reparación: {str(e)}")

        finally:
            self.close_connection()
            self.crear_pantalla_reparacion()

    def buscar_reparacion(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.leyenda_buscar_reparacion = tk.Label(self.root, text="Buscar Reparación", font=("Arial", 16))
        self.leyenda_buscar_reparacion.pack(pady=20)

        self.leyenda_folio_buscar = tk.Label(self.root, text="Ingrese el folio de la reparación:")
        self.leyenda_folio_buscar.pack(pady=5)
        self.entrada_folio_buscar = tk.Entry(self.root)
        self.entrada_folio_buscar.pack(pady=5)

        self.buscar_button = tk.Button(self.root, text="Buscar", command=self.encontrar_reparacion)
        self.buscar_button.pack(pady=20)

        self.back_button = tk.Button(self.root, text="Volver", command=self.crear_pantalla_reparacion)
        self.back_button.pack(pady=10)


    def encontrar_reparacion(self):
        folio = self.entrada_folio_buscar.get()

        if not folio:
            messagebox.showerror("Error", "El folio no puede estar vacío.")
            return

        try:
            folio = int(folio)  # Validar que el folio sea un número
        except ValueError:
            messagebox.showerror("Error", "El folio debe ser numérico.")
            return

        self.create_connection()

        try:
            query = "SELECT * FROM reparaciones WHERE folio = %s"
            self.cursor.execute(query, (folio,))
            result = self.cursor.fetchone()

            if result:
                self.leyenda_resultado = tk.Label(self.root, text="Resultado de la búsqueda", font=("Arial", 14))
                self.leyenda_resultado.pack(pady=10)

                self.leyenda_matricula_resultado = tk.Label(self.root, text=f"Matrícula: {result[1]}")
                self.leyenda_matricula_resultado.pack(pady=5)

                self.leyenda_pieza_resultado = tk.Label(self.root, text=f"ID de la pieza: {result[2]}")
                self.leyenda_pieza_resultado.pack(pady=5)

                self.leyenda_fecha_entrada_resultado = tk.Label(self.root, text=f"Fecha de entrada: {result[3]}")
                self.leyenda_fecha_entrada_resultado.pack(pady=5)

                self.leyenda_fecha_salida_resultado = tk.Label(self.root, text=f"Fecha de salida: {result[4]}")
                self.leyenda_fecha_salida_resultado.pack(pady=5)

                self.leyenda_falla_resultado = tk.Label(self.root, text=f"Falla: {result[5]}")
                self.leyenda_falla_resultado.pack(pady=5)

                self.leyenda_precio_resultado = tk.Label(self.root, text=f"Precio: {result[6]}")
                self.leyenda_precio_resultado.pack(pady=5)

                self.back_button = tk.Button(self.root, text="Volver", command=self.crear_pantalla_reparacion)
                self.back_button.pack(pady=10)

            else:
                messagebox.showerror("Error", f"No se encontró la reparación con folio {folio}")

        except Exception as e:
            messagebox.showerror("Error", f"Se produjo un error al buscar la reparación: {str(e)}")

        finally:
            self.close_connection()

    def agregar_pieza(self):
        for widget in self.root.winfo_children():
            widget.destroy()
             
        self.leyenda_agregar_pieza = tk.Label(self.root, text="Agregar Pieza", font=("Arial", 16))
        self.leyenda_agregar_pieza.pack(pady=20)

        self.leyenda_descripcion = tk.Label(self.root, text="Descripcion de la pieza:")
        self.leyenda_descripcion.pack(pady=5)
        self.entrada_descripcion = tk.Entry(self.root)
        self.entrada_descripcion.pack(pady=5)

        self.leyenda_cantidad = tk.Label(self.root, text="Cantidad de la pieza:")
        self.leyenda_cantidad.pack(pady=5)
        self.entrada_cantidad = tk.Entry(self.root)
        self.entrada_cantidad.pack(pady=5)

        self.save_button = tk.Button(self.root, text="Guardar", command=self.guardar_pieza)
        self.save_button.pack(pady=20)

        self.back_button = tk.Button(self.root, text="Volver", command=self.crear_pantalla_piezas)
        self.back_button.pack(pady=10)

    def guardar_pieza(self):
        cantidad_pieza = self.entrada_cantidad.get()
        descripcion_pieza = self.entrada_descripcion.get()

        if not descripcion_pieza or not cantidad_pieza:
            messagebox.showerror("Error", "Todos los campos deben ser llenados")
            return

        if not cantidad_pieza.isdigit():
            messagebox.showerror("Error", "La cantidad de piezas debe ser un número")
            return

        self.create_connection()

        if not self.cursor:
            return

        query = "INSERT INTO piezas (descripcion, cantidad) VALUES (%s, %s)"
        self.cursor.execute(query, (descripcion_pieza, cantidad_pieza))
        self.conexion.commit()

        messagebox.showinfo("Éxito", "¡Pieza registrada!")
        self.close_connection()
        self.crear_pantalla_piezas()

    def editar_pieza(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.leyenda_editar_pieza = tk.Label(self.root, text="Editar Pieza", font=("Arial", 16))
        self.leyenda_editar_pieza.pack(pady=20)

        self.leyenda_id_pieza_editar = tk.Label(self.root, text="ID de la pieza a editar")
        self.leyenda_id_pieza_editar.pack(pady=5)
        self.entrada_id_pieza_editar = tk.Entry(self.root)
        self.entrada_id_pieza_editar.pack(pady=5)

        self.find_edit_button = tk.Button(self.root, text="Buscar", command=self.buscar_pieza_a_editar)
        self.find_edit_button.pack(pady=20)

        self.back_button = tk.Button(self.root, text="Volver", command=self.crear_pantalla_piezas)
        self.back_button.pack(pady=10)

    def buscar_pieza_a_editar(self):
        pieza_id = self.entrada_id_pieza_editar.get()

        if not pieza_id.isdigit():
            messagebox.showerror("Error", "El ID del cliente debe ser numérico")
            return

        self.create_connection()

        if not self.cursor:
            return

        query = "SELECT * FROM piezas WHERE id_pieza = %s"
        self.cursor.execute(query, (pieza_id,))
        result = self.cursor.fetchone()

        if result:
            self.name_label = tk.Label(self.root, text="descripcion:")
            self.name_label.pack(pady=5)
            self.name_entry = tk.Entry(self.root)
            self.name_entry.insert(0, result[1])  
            self.name_entry.pack(pady=5)

            self.stock_label = tk.Label(self.root, text="cantidad:")
            self.stock_label.pack(pady=5)
            self.stock_entry = tk.Entry(self.root)
            self.stock_entry.insert(0, result[2])  
            self.stock_entry.pack(pady=5)

            self.save_button = tk.Button(self.root, text="Guardar Cambios", command=self.actualizar_pieza)
            self.save_button.pack(pady=20)
        else:
            messagebox.showerror("Error", f"Pieza con ID {pieza_id} no encontrado")
            self.close_connection()

        self.close_connection()

    def actualizar_pieza(self):
        descripcion = self.name_entry.get()
        cantidad = self.stock_entry.get()

        if not descripcion or not cantidad:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        if not cantidad.isdigit():
            messagebox.showerror("Error", "La cantidad debe ser un número válido")
            return

        cantidad = int(cantidad)
        pieza_id = self.entrada_id_pieza_editar.get()
        self.create_connection()

        if not self.cursor:
            return

        query = "UPDATE piezas SET descripcion = %s, cantidad = %s WHERE id_pieza = %s"
        self.cursor.execute(query, (descripcion, cantidad, pieza_id))
        self.conexion.commit()

        messagebox.showinfo("¡Actualizada!", "Pieza actualizada correctamente")
        self.close_connection()
        self.crear_pantalla_piezas()

    def buscar_pieza(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.leyenda_buscar_pieza = tk.Label(self.root, text="Buscar Pieza", font=("Arial", 16))
        self.leyenda_buscar_pieza.pack(pady=20)

        self.leyenda_id_pieza_buscar = tk.Label(self.root, text="Ingresa el ID a buscar:")
        self.leyenda_id_pieza_buscar.pack(pady=5)
        self.entrada_id_pieza_buscar = tk.Entry(self.root)
        self.entrada_id_pieza_buscar.pack(pady=5)

        self.search_button = tk.Button(self.root, text="Buscar", command=self.encontrar_pieza)
        self.search_button.pack(pady=20)

        self.back_button = tk.Button(self.root, text="Volver", command=self.crear_pantalla_piezas)
        self.back_button.pack(pady=10)

    def encontrar_pieza(self):
        id_pieza = self.entrada_id_pieza_buscar.get()

        self.create_connection()

        if not self.cursor:
            return

        query = "SELECT * FROM piezas WHERE id_pieza = %s"
        self.cursor.execute(query, (id_pieza,))
        result = self.cursor.fetchone()

        if result:
            pieza_info = f"ID de la pieza: {result[0]}\nDescripcion: {result[1]}\nCantidad: {result[2]}"
            messagebox.showinfo("Pieza Encontrada", pieza_info)
        else:
            messagebox.showerror("Error", "Pieza no encontrada")

        self.close_connection()
        self.crear_pantalla_piezas()

    def agregar_vehiculo(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.create_connection()

        query = "SELECT id_cliente, nombre_cliente FROM clientes"
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        self.close_connection()

        self.clientes_dict = {nombre: id_cliente for id_cliente, nombre in result}
        
        self.leyenda_agregar_vehiculo = tk.Label(self.root, text="Agregar Vehiculo", font=("Arial, 16"))
        self.leyenda_agregar_vehiculo.pack(pady=20)

        self.leyenda_matricula = tk.Label(self.root, text="Matricula")
        self.leyenda_matricula.pack(pady=5)
        self.entrada_matricula = tk.Entry(self.root)
        self.entrada_matricula.pack(pady=5)

        self.leyenda_nombre_cliente = tk.Label(self.root, text="Cliente")
        self.leyenda_nombre_cliente.pack(pady=5)
        self.combobox_nombre_cliente = ttk.Combobox(self.root, values=list(self.clientes_dict.keys())) 
        self.combobox_nombre_cliente.pack(pady=5)

        self.leyenda_marca = tk.Label(self.root, text="Marca:")
        self.leyenda_marca.pack(pady=5)
        self.entrada_marca = tk.Entry(self.root)
        self.entrada_marca.pack(pady=5)

        self.leyenda_modelo = tk.Label(self.root, text="Modelo:")
        self.leyenda_modelo.pack(pady=5)
        self.entrada_modelo = tk.Entry(self.root)
        self.entrada_modelo.pack(pady=5)

        self.save_button = tk.Button(self.root, text="Guardar", command=self.guardar_vehiculo)
        self.save_button.pack(pady=20)

        self.back_button = tk.Button(self.root, text="Volver", command=self.crear_pantalla_vehiculos)
        self.back_button.pack(pady=10)

    def guardar_vehiculo(self):
        matricula = self.entrada_matricula.get()
        nombre_cliente = self.combobox_nombre_cliente.get()
        marca = self.entrada_marca.get()
        modelo = self.entrada_modelo.get()

        if not matricula or not nombre_cliente or not marca or not modelo:
            messagebox.showerror("Error", "Todos los campos deben ser llenados")
            return

        id_cliente = self.clientes_dict.get(nombre_cliente)

        if not id_cliente:
            messagebox.showerror("Error", "El cliente seleccionado no es válido")
            return

        self.create_connection()

        if not self.cursor:
            return

        query = "INSERT INTO vehiculos (matricula, id_cliente, marca, modelo) VALUES (%s, %s, %s, %s)"
        try:
            self.cursor.execute(query, (matricula, id_cliente, marca, modelo))
            self.conexion.commit()
            messagebox.showinfo("Éxito", "¡Vehículo agregado exitosamente!")
        except mysql.connector.Error as err:
            if err.errno == 1062:
                messagebox.showerror("Error", "La matrícula ya está registrada. Por favor, ingresa una matrícula única.")
            else:
                messagebox.showerror("Error", f"Error al agregar vehículo: {err}")
        finally:
            self.close_connection()
            self.crear_pantalla_vehiculos()

    def editar_vehiculo(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.leyenda_editar_vehiculo = tk.Label(self.root, text="Editar Vehiculo", font=("Arial", 16))
        self.leyenda_editar_vehiculo.pack(pady=20)

        self.leyenda_matricula_buscar = tk.Label(self.root, text="Matricula:")
        self.leyenda_matricula_buscar.pack(pady=5)
        self.entrada_matricula_buscar = tk.Entry(self.root)
        self.entrada_matricula_buscar.pack(pady=5)

        self.find_edit_button = tk.Button(self.root, text="Buscar", command=self.buscar_vehiculo_a_editar)
        self.find_edit_button.pack(pady=20)

        self.back_button = tk.Button(self.root, text="Volver", command=self.crear_pantalla_vehiculos)
        self.back_button.pack(pady=10)

    def buscar_vehiculo_a_editar(self):
        matricula = self.entrada_matricula_buscar.get()

        if not matricula:
            messagebox.showerror("Error", "La matrícula no puede estar vacía")
            return

        self.create_connection()

        if not self.cursor:
            return

        query = "SELECT * FROM vehiculos WHERE matricula = %s"
        self.cursor.execute(query, (matricula,))
        result = self.cursor.fetchone()

        if result:
            self.marca_label = tk.Label(self.root, text="Marca:")
            self.marca_label.pack(pady=5)
            self.marca_entry = tk.Entry(self.root)
            self.marca_entry.insert(0, result[2])  # Marca del vehículo
            self.marca_entry.pack(pady=5)

            self.modelo_label = tk.Label(self.root, text="Modelo:")
            self.modelo_label.pack(pady=5)
            self.modelo_entry = tk.Entry(self.root)
            self.modelo_entry.insert(0, result[3])  # Modelo del vehículo
            self.modelo_entry.pack(pady=5)

            self.save_button = tk.Button(self.root, text="Guardar Cambios", command=lambda: self.actualizar_vehiculo(matricula))
            self.save_button.pack(pady=20)

        else:
            messagebox.showerror("Error", f"Vehículo con matrícula {matricula} no encontrado")
            self.close_connection()

        self.close_connection()

    def actualizar_vehiculo(self, matricula):
        marca_vehiculo = self.marca_entry.get()
        modelo_vehiculo = self.modelo_entry.get()

        if not marca_vehiculo or not modelo_vehiculo:
            messagebox.showerror("Error", "Todos los campos deben ser llenados")
            return

        self.create_connection()

        if not self.cursor:
            return

        query = "UPDATE vehiculos SET marca = %s, modelo = %s WHERE matricula = %s"
        self.cursor.execute(query, (marca_vehiculo, modelo_vehiculo, matricula))
        self.conexion.commit()

        messagebox.showinfo("Éxito", "¡Vehículo actualizado exitosamente!")
        self.close_connection()
        self.crear_pantalla_vehiculos()

    def buscar_vehiculo(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.leyenda_buscar_vehiculo = tk.Label(self.root, text="Buscar Vehiculo", font=("Arial", 16))
        self.leyenda_buscar_vehiculo.pack(pady=20)

        self.leyenda_matricula_del_vehiculo = tk.Label(self.root, text="Matricula")
        self.leyenda_matricula_del_vehiculo.pack(pady=5)
        self.entrada_matricula_del_vehiculo = tk.Entry(self.root)
        self.entrada_matricula_del_vehiculo.pack(pady=5)

        self.search_button = tk.Button(self.root, text="Buscar", command=self.encontrar_vehiculo)
        self.search_button.pack(pady=20)

        self.back_button = tk.Button(self.root, text="Volver", command=self.crear_pantalla_vehiculos)
        self.back_button.pack(pady=10)

    def encontrar_vehiculo(self):
        matricula_buscar = self.entrada_matricula_del_vehiculo.get()
        self.create_connection()

        if not self.cursor:
            return

        query = "SELECT * FROM vehiculos WHERE matricula = %s"
        self.cursor.execute(query, (matricula_buscar,))
        result = self.cursor.fetchone()

        if result:
            vehiculo_info = f"ID del cliente asociado: {result[1]}\nMarca: {result[2]}\nModelo: {result[3]}"
            messagebox.showinfo("Vehiculo Encontrado", vehiculo_info)
        else:
            messagebox.showerror("Error", "Vehiculo no encontrado")

        self.close_connection()
        self.crear_pantalla_vehiculos()

    def agregar_cliente(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.leyenda_agregar_cliente = tk.Label(self.root, text="Agregar Cliente", font=("Arial", 16))
        self.leyenda_agregar_cliente.pack(pady=20)
        
        self.name_label = tk.Label(self.root, text="Nombre:")
        self.name_label.pack(pady=5)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack(pady=5)

        self.phone_label = tk.Label(self.root, text="Telefono:")
        self.phone_label.pack(pady=5)
        self.phone_entry = tk.Entry(self.root)
        self.phone_entry.pack(pady=5)

        self.id_usuario_label = tk.Label(self.root, text=f"ID del Administrador: {self.admin_id}")
        self.id_usuario_label.pack(pady=5)

        self.name_admin_label = tk.Label(self.root, text=f"Nombre del Administrador: {self.admin_name}")
        self.name_admin_label.pack(pady=5)

        self.save_button = tk.Button(self.root, text="Guardar", command=self.guardar_cliente)
        self.save_button.pack(pady=20)

        self.back_button = tk.Button(self.root, text="Volver", command=self.crear_pantalla_clientes)
        self.back_button.pack(pady=10)

    def guardar_cliente(self):
        nombre_cliente = self.name_entry.get()
        telefono_cliente = self.phone_entry.get()

        if not nombre_cliente or not telefono_cliente:
            messagebox.showerror("Error", "Todos los campos deben ser llenados")
            return

        if not telefono_cliente.isdigit():
            messagebox.showerror("Error", "El teléfono debe contener solo dígitos")
            return

        if len(telefono_cliente) != 10:
            digitos_faltantes = 10 - len(telefono_cliente)
            if digitos_faltantes > 0:
                messagebox.showerror("Error", f"El teléfono debe tener 10 dígitos. Faltan {digitos_faltantes} dígitos.")
            return

        self.create_connection()

        if not self.cursor:
            return

        query = "INSERT INTO clientes (nombre_cliente, telefono, id_usuario) VALUES (%s, %s, %s)"
        self.cursor.execute(query, (nombre_cliente, telefono_cliente, self.admin_id))
        self.conexion.commit()

        messagebox.showinfo("Éxito", "¡Cliente agregado exitosamente!")
        self.close_connection()
        self.crear_pantalla_clientes()

    def editar_cliente(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.leyenda_editar_cliente = tk.Label(self.root, text="Editar Cliente", font=("Arial", 16))
        self.leyenda_editar_cliente.pack(pady=20)

        self.edit_id_label = tk.Label(self.root, text="Id del cliente a editar:")
        self.edit_id_label.pack(pady=5)
        self.edit_id_entry = tk.Entry(self.root)
        self.edit_id_entry.pack(pady=5)

        self.find_edit_button = tk.Button(self.root, text="Buscar", command=self.buscar_cliente_a_editar)
        self.find_edit_button.pack(pady=20)

        self.back_button = tk.Button(self.root, text="Volver", command=self.crear_pantalla_clientes)
        self.back_button.pack(pady=10)

    def buscar_cliente_a_editar(self):
        cliente_id = self.edit_id_entry.get()

        if not cliente_id.isdigit():
            messagebox.showerror("Error", "El ID del cliente debe ser numérico")
            return

        self.create_connection()

        if not self.cursor:
            return

        query = "SELECT * FROM clientes WHERE id_cliente = %s"
        self.cursor.execute(query, (cliente_id,))
        result = self.cursor.fetchone()

        if result:
            self.name_label = tk.Label(self.root, text="Nombre:")
            self.name_label.pack(pady=5)
            self.name_entry = tk.Entry(self.root)
            self.name_entry.insert(0, result[2])  # Nombre del cliente
            self.name_entry.pack(pady=5)

            self.phone_label = tk.Label(self.root, text="Teléfono:")
            self.phone_label.pack(pady=5)
            self.phone_entry = tk.Entry(self.root)
            self.phone_entry.insert(0, result[3])  # Teléfono del cliente
            self.phone_entry.pack(pady=5)

            self.save_button = tk.Button(self.root, text="Guardar Cambios", command=lambda: self.actualizar_cliente(cliente_id))
            self.save_button.pack(pady=20)

            self.back_button = tk.Button(self.root, text="Volver", command=self.crear_pantalla_clientes)
            self.back_button.pack(pady=10)
        else:
            messagebox.showerror("Error", f"Cliente con ID {cliente_id} no encontrado")
            self.close_connection()

        self.close_connection()

    def actualizar_cliente(self, cliente_id):
        nombre_cliente = self.name_entry.get()
        telefono_cliente = self.phone_entry.get()

        if not nombre_cliente or not telefono_cliente:
            messagebox.showerror("Error", "Todos los campos deben ser llenados")
            return

        if not telefono_cliente.isdigit():
            messagebox.showerror("Error", "El teléfono debe contener solo dígitos")
            return

        if len(telefono_cliente) != 10:
            digitos_faltantes = 10 - len(telefono_cliente)
            messagebox.showerror("Error", f"El teléfono debe tener 10 dígitos. Faltan {digitos_faltantes} dígitos.")
            return

        self.create_connection()

        if not self.cursor:
            return

        query = "UPDATE clientes SET nombre_cliente = %s, telefono = %s WHERE id_cliente = %s"
        self.cursor.execute(query, (nombre_cliente, telefono_cliente, cliente_id))
        self.conexion.commit()

        messagebox.showinfo("Éxito", "¡Cliente actualizado exitosamente!")
        self.close_connection()
        self.crear_pantalla_clientes()

    def buscar_cliente(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.search_cliente_label = tk.Label(self.root, text="Buscar Cliente", font=("Arial", 16))
        self.search_cliente_label.pack(pady=20)

        self.search_id_label = tk.Label(self.root, text="ID:")
        self.search_id_label.pack(pady=5)
        self.search_id_entry = tk.Entry(self.root)
        self.search_id_entry.pack(pady=5)

        self.search_button = tk.Button(self.root, text="Buscar", command=self.encontrar_cliente)
        self.search_button.pack(pady=20)

        self.back_button = tk.Button(self.root, text="Volver", command=self.crear_pantalla_clientes)
        self.back_button.pack(pady=10)

    def encontrar_cliente(self):
        id_cliente = self.search_id_entry.get()

        self.create_connection()

        if not self.cursor:
            return

        query = "SELECT * FROM clientes WHERE id_cliente = %s"
        self.cursor.execute(query, (id_cliente,))
        result = self.cursor.fetchone()

        if result:
            user_info = f"ID del cliente: {result[0]}\nId del usuario que lo registro: {result[1]}\nNombre del cliente: {result[2]}\ntelefono: {result[3]}"
            messagebox.showinfo("Cliente Encontrado", user_info)
        else:
            messagebox.showerror("Error", "Cliente no encontrado")

        self.close_connection()
        self.crear_pantalla_clientes()

    def add_user(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.add_user_label = tk.Label(self.root, text="Agregar Usuario", font=("Arial", 16))
        self.add_user_label.pack(pady=20)

        self.email_label = tk.Label(self.root, text="Correo Electrónico:")
        self.email_label.pack(pady=5)
        self.email_entry = tk.Entry(self.root)
        self.email_entry.pack(pady=5)

        self.password_label = tk.Label(self.root, text="Contraseña:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack(pady=5)

        self.name_label = tk.Label(self.root, text="Nombre:")
        self.name_label.pack(pady=5)
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack(pady=5)

        self.role_label = tk.Label(self.root, text="Rol:")
        self.role_label.pack(pady=5)
        self.role_combobox = ttk.Combobox(self.root, values=["admin", "secretaria", "mecanico"])
        self.role_combobox.pack(pady=5)

        self.save_button = tk.Button(self.root, text="Guardar", command=self.save_user)
        self.save_button.pack(pady=20)

        self.back_button = tk.Button(self.root, text="Volver", command=self.create_user_management_screen)
        self.back_button.pack(pady=10)

    def save_user(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        name = self.name_entry.get()
        role = self.role_combobox.get()

        if not email or not password or not name or not role:
            messagebox.showerror("Error", "Todos los campos deben ser llenados")
            return

        self.create_connection()

        if not self.cursor:
            return

        query = "SELECT COUNT(*) FROM usuarios WHERE correo_electronico = %s"
        self.cursor.execute(query, (email,))
        result = self.cursor.fetchone()

        if result[0] > 0:
            messagebox.showerror("Error", "El correo electrónico ya está registrado")
            self.close_connection()
            return

        query = "INSERT INTO usuarios (correo_electronico, contrasena, nombre, rol) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(query, (email, password, name, role))
        self.conexion.commit()

        messagebox.showinfo("Éxito", "¡Usuario agregado exitosamente!")
        self.close_connection()
        self.create_user_management_screen()

    def edit_user(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.edit_user_label = tk.Label(self.root, text="Editar Usuario", font=("Arial", 16))
        self.edit_user_label.pack(pady=20)

        self.edit_email_label = tk.Label(self.root, text="Correo Electrónico a Editar:")
        self.edit_email_label.pack(pady=5)
        self.edit_email_entry = tk.Entry(self.root)
        self.edit_email_entry.pack(pady=5)

        self.find_edit_button = tk.Button(self.root, text="Buscar", command=self.find_user_for_edit)
        self.find_edit_button.pack(pady=20)

        self.back_button = tk.Button(self.root, text="Volver", command=self.create_user_management_screen)
        self.back_button.pack(pady=10)

    def find_user_for_edit(self):
        self.edit_email = self.edit_email_entry.get()  # Guardar el correo original

        self.create_connection()

        if not self.cursor:
            return

        query = "SELECT * FROM usuarios WHERE correo_electronico = %s"
        self.cursor.execute(query, (self.edit_email,))
        result = self.cursor.fetchone()

        if result:
            self.email_entry = tk.Entry(self.root)
            self.email_entry.insert(0, result[1])
            self.email_entry.pack(pady=5)

            self.password_entry = tk.Entry(self.root, show="*")
            self.password_entry.insert(0, result[2])
            self.password_entry.pack(pady=5)

            self.name_entry = tk.Entry(self.root)
            self.name_entry.insert(0, result[3])
            self.name_entry.pack(pady=5)

            self.role_combobox = ttk.Combobox(self.root, values=["admin", "secretaria", "mecanico"])
            self.role_combobox.set(result[4])  # Establecer el rol actual
            self.role_combobox.pack(pady=5)

            self.save_changes_button = tk.Button(self.root, text="Guardar Cambios", command=self.update_user)
            self.save_changes_button.pack(pady=20)
        else:
            messagebox.showerror("Error", "Usuario no encontrado")

        self.close_connection()

    def update_user(self):
        new_email = self.email_entry.get()
        password = self.password_entry.get()
        name = self.name_entry.get()
        role = self.role_combobox.get()

        self.create_connection()

        if not self.cursor:
            return

        query = "SELECT COUNT(*) FROM usuarios WHERE correo_electronico = %s AND correo_electronico != %s"
        self.cursor.execute(query, (new_email, self.edit_email))
        result = self.cursor.fetchone()

        if result[0] > 0:
            messagebox.showerror("Error", "El correo electrónico ya está registrado")
            self.close_connection()
            return

        query = "UPDATE usuarios SET contrasena = %s, nombre = %s, rol = %s WHERE correo_electronico = %s"
        self.cursor.execute(query, (password, name, role, self.edit_email))
        self.conexion.commit()

        messagebox.showinfo("Éxito", "¡Usuario actualizado exitosamente!")
        self.close_connection()
        self.admin_name = name
        self.rol = role
        self.create_menu_screen()

    def search_user(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.search_user_label = tk.Label(self.root, text="Buscar Usuario", font=("Arial", 16))
        self.search_user_label.pack(pady=20)

        self.search_email_label = tk.Label(self.root, text="Correo Electrónico:")
        self.search_email_label.pack(pady=5)
        self.search_email_entry = tk.Entry(self.root)
        self.search_email_entry.pack(pady=5)

        self.search_button = tk.Button(self.root, text="Buscar", command=self.find_user)
        self.search_button.pack(pady=20)

        self.back_button = tk.Button(self.root, text="Volver", command=self.create_user_management_screen)
        self.back_button.pack(pady=10)

    def find_user(self):
        email = self.search_email_entry.get()

        self.create_connection()

        if not self.cursor:
            return

        query = "SELECT * FROM usuarios WHERE correo_electronico = %s"
        self.cursor.execute(query, (email,))
        result = self.cursor.fetchone()

        if result:
            user_info = f"ID: {result[0]}\nCorreo: {result[1]}\nNombre: {result[3]}\nRol: {result[4]}"
            messagebox.showinfo("Usuario Encontrado", user_info)
        else:
            messagebox.showerror("Error", "Usuario no encontrado")

        self.close_connection()

root = tk.Tk()
app = TallerApp(root)
root.mainloop()
