from nicegui import ui
from app.services import user_service
import hashlib


@ui.page('/register')
def register_page():
 with ui.row().classes('w-full h-screen justify-center items-center'):

        with ui.column().classes('items-center'):

            ui.label('Register').classes('text-2xl mb-4')

            username = ui.input('Username')
            password = ui.input('Password', password=True)

            def handle_register():
                if not username.value or not password.value:
                    ui.notify('Please fill all fields', color='red')
                    return

                password_hash = hashlib.sha256(password.value.encode()).hexdigest()

                user_service.create_user(username.value, password_hash)

                ui.notify('User created!', color='green')
                ui.navigate.to('/') 

            ui.button('Register', on_click=handle_register)