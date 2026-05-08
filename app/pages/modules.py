from nicegui import ui
from app.services import create_module


@ui.page('/modules')
def modules_page():

    ui.label("Create New Module").classes("text-2xl font-bold")

    module_name = ui.input(label="Name")

    color_options = {
        "Blue": "#5898ff",
        "Green": "#4CAF50",
        "Red": "#F44336",
        "Purple": "#9C27B0",
        "Orange": "#FF9800",
        "Teal": "#009688",
    }

    module_color = ui.select(
        options=list(color_options.keys()),
        label="Color",
        value="Blue"
    )

    def save_module():
        if not module_name.value:
            ui.notify("Enter module name")
            return

        create_module(
            user_id=1,
            name=module_name.value,
            color=color_options[module_color.value]
        )

        ui.notify("Module created!")

        module_name.value = ""
        module_color.value = "Blue"

    ui.button("Create Module", on_click=save_module)