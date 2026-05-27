# JESUS CABRERA AVILA
# CRUD GAMER CON FLET Y SQLITE

import flet as ft
import sqlite3
import sys

def main(page: ft.Page):

    # =====================================================
    # CONFIGURACIÓN
    # =====================================================
    page.title = "CRUD GAMER"
    page.window_width = 1000
    page.window_height = 750
    page.bgcolor = "#0f172a"
    page.theme_mode = "dark"

    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    # =====================================================
    # BASE DE DATOS
    # =====================================================
    conn = sqlite3.connect("gamer.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            correo TEXT,
            edad INTEGER
        )
    """)

    conn.commit()

    # =====================================================
    # INPUTS
    # =====================================================
    id_usuario = ft.TextField(
        label="ID",
        width=320,
        read_only=True,
        bgcolor="#1e293b",
        color="white"
    )

    nombre = ft.TextField(
        label="Nombre del jugador",
        width=320,
        bgcolor="#1e293b",
        color="white"
    )

    correo = ft.TextField(
        label="Correo",
        width=320,
        bgcolor="#1e293b",
        color="white"
    )

    edad = ft.TextField(
        label="Edad",
        width=320,
        bgcolor="#1e293b",
        color="white"
    )

    resultado = ft.Text(size=16)

    # =====================================================
    # LISTA
    # =====================================================
    lista = ft.Column(scroll="auto")

    contenedor_lista = ft.Container(
        content=lista,
        width=420,
        height=250,
        bgcolor="#111827",
        padding=10,
        border_radius=15
    )

    # =====================================================
    # LIMPIAR
    # =====================================================
    def limpiar(e):

        id_usuario.value = ""
        nombre.value = ""
        correo.value = ""
        edad.value = ""

        resultado.value = ""

        page.update()

    # =====================================================
    # CONSULTAR
    # =====================================================
    def consultar(e):

        lista.controls.clear()

        cursor.execute("SELECT * FROM usuarios")

        registros = cursor.fetchall()

        for id_, nom, cor, ed in registros:

            def seleccionar(e, id_=id_, nom=nom, cor=cor, ed=ed):

                id_usuario.value = str(id_)
                nombre.value = nom
                correo.value = cor
                edad.value = str(ed)

                resultado.value = "Jugador seleccionado"

                page.update()

            tarjeta = ft.Container(

                content=ft.ListTile(
                    title=ft.Text(
                        f"{nom}",
                        color="white"
                    ),

                    subtitle=ft.Text(
                        f"{cor} | Edad: {ed}",
                        color="#cbd5e1"
                    ),

                    on_click=seleccionar
                ),

                bgcolor="#1e293b",
                border_radius=10,
                padding=5
            )

            lista.controls.append(tarjeta)

        page.update()

    # =====================================================
    # GUARDAR
    # =====================================================
    def guardar(e):

        if nombre.value == "" or correo.value == "" or edad.value == "":

            resultado.value = "Completa todos los campos"
            resultado.color = "red"

        elif not edad.value.isdigit():

            resultado.value = "Edad inválida"
            resultado.color = "orange"

        else:

            cursor.execute(
                """
                INSERT INTO usuarios(nombre, correo, edad)
                VALUES (?, ?, ?)
                """,
                (
                    nombre.value,
                    correo.value,
                    edad.value
                )
            )

            conn.commit()

            resultado.value = "Registro guardado"
            resultado.color = "#00ff88"

            limpiar(None)
            consultar(None)

        page.update()

    # =====================================================
    # ACTUALIZAR
    # =====================================================
    def actualizar(e):

        if id_usuario.value == "":

            resultado.value = "Selecciona un registro"
            resultado.color = "orange"

        else:

            cursor.execute(
                """
                UPDATE usuarios
                SET nombre=?, correo=?, edad=?
                WHERE id=?
                """,
                (
                    nombre.value,
                    correo.value,
                    edad.value,
                    id_usuario.value
                )
            )

            conn.commit()

            resultado.value = "Registro actualizado"
            resultado.color = "#00ffff"

            consultar(None)

        page.update()

    # =====================================================
    # ELIMINAR
    # =====================================================
    def eliminar(e):

        if id_usuario.value == "":

            resultado.value = "Selecciona un registro"
            resultado.color = "red"

        else:

            cursor.execute(
                "DELETE FROM usuarios WHERE id=?",
                (id_usuario.value,)
            )

            conn.commit()

            resultado.value = "Registro eliminado"
            resultado.color = "#ff4d6d"

            limpiar(None)
            consultar(None)

        page.update()

    # =====================================================
    # SALIR
    # =====================================================
    def salir(e):

        conn.close()
        sys.exit()

    # =====================================================
    # BOTONES
    # =====================================================
    btn_guardar = ft.FilledButton(
        "Guardar",
        on_click=guardar
    )

    btn_consultar = ft.FilledButton(
        "Consultar",
        on_click=consultar
    )

    btn_actualizar = ft.FilledButton(
        "Actualizar",
        on_click=actualizar
    )

    btn_eliminar = ft.FilledButton(
        "Eliminar",
        on_click=eliminar
    )

    btn_limpiar = ft.FilledButton(
        "Limpiar",
        on_click=limpiar
    )

    btn_salir = ft.FilledButton(
        "Salir",
        bgcolor="red",
        on_click=salir
    )

    fila1 = ft.Row(
        [
            btn_guardar,
            btn_consultar,
            btn_actualizar
        ],
        alignment="center"
    )

    fila2 = ft.Row(
        [
            btn_eliminar,
            btn_limpiar,
            btn_salir
        ],
        alignment="center"
    )

    # =====================================================
    # CONTENEDOR PRINCIPAL
    # =====================================================
    interfaz = ft.Container(

        content=ft.Column(

            [
                ft.Text(
                    "CRUD GAMER",
                    size=35,
                    weight="bold",
                    color="#00ffff"
                ),

                ft.Text(
                    "Sistema de jugadores",
                    color="white"
                ),

                id_usuario,
                nombre,
                correo,
                edad,

                fila1,
                fila2,

                resultado,

                ft.Text(
                    "LISTA DE JUGADORES",
                    size=18,
                    weight="bold",
                    color="#00ffff"
                ),

                contenedor_lista
            ],

            horizontal_alignment="center",
            spacing=15
        ),

        width=500,
        bgcolor="#111827",
        padding=25,
        border_radius=20
    )

    page.add(interfaz)

    consultar(None)

# =====================================================
# EJECUTAR APP
# =====================================================
ft.app(target=main)