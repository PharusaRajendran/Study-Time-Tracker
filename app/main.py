from nicegui import ui

from app.init_db import init_db

# import pages → dadurch werden sie registriert
import app.pages.login
import app.pages.register

init_db()

ui.run()