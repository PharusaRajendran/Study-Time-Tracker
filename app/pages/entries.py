from nicegui import ui
from app.services import create_entry, get_entries
from app.database import SessionLocal
from app.models import Module


@ui.page('/entries')
def entries_page():

    def load_modules():
        with SessionLocal() as session:
            modules = session.query(Module).all()
            return {module.name: module.id for module in modules}

    module_options = load_modules()

    ui.label("Add Study Entry").classes("text-2xl font-bold")

    module_dropdown = ui.select(
        options=list(module_options.keys()),
        label="Choose module"
    )

    minutes_input = ui.number(label="Minutes studied", min=1)

    entries_container = ui.column()

    def show_entries():
        entries_container.clear()

        if not module_dropdown.value:
            return

        module_id = module_options[module_dropdown.value]
        entries = get_entries(module_id)

        with entries_container:
            ui.label("Entries:")
            for entry in entries:
                ui.label(f"{entry.duration_minutes} minutes")

    def save_entry():
        if not module_dropdown.value or not minutes_input.value:
            ui.notify("Fill everything")
            return

        module_id = module_options[module_dropdown.value]
        create_entry(module_id, int(minutes_input.value))

        ui.notify("Saved!")
        minutes_input.value = None
        show_entries()

    ui.button("Save Entry", on_click=save_entry)