from nicegui import ui
from app.services import get_user

current_user = {"id": None}


@ui.page('/')
def login_page():
    with ui.row().classes('w-full h-screen justify-center items-center'):

        with ui.column().classes('items-center'):

            ui.label('Study Tracker Login').classes('text-2xl font-bold mb-4')

            username = ui.input(label='Username').classes('w-64')
            password = ui.input(label='Password', password=True).classes('w-64')

            def handle_login():
                user = get_user(username.value, password.value)

                if user:
                    current_user["id"] = user.id
                    ui.notify("Login successful!", color="green")
                    ui.navigate.to('/entries')
                else:
                    ui.notify("Invalid username or password", color="red")

            ui.button('Go to Register', on_click=lambda: ui.navigate.to('/register')).props('flat')
            ui.button('Login', on_click=handle_login).classes('w-64 mt-2')