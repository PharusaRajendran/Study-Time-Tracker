from nicegui import app, ui
from app.services import create_entry
from app.database import SessionLocal
from app.models import Module, StudyEntry


@ui.page('/entries')
def entries_page():

    ui.button(
    icon='arrow_back',
    on_click=lambda: ui.navigate.to('/dashboard')
    ).props('flat round') \
    .classes('mb-4')

    def load_modules():
            user_id = app.storage.user.get('user_id')

            with SessionLocal() as session:
                modules = (
                    session.query(Module)
                    .filter(Module.user_id == user_id)  
                    .filter(Module.is_archived == False)  
                    .all()
                )

            return {module.name: module.id for module in modules}
    
    module_options = load_modules()

    ui.label("Add Study Entry").classes("text-2xl font-bold")

    module_dropdown = ui.select(
        options=list(module_options.keys()),
        label="Choose module"
    )

    minutes_input = ui.number(label="Minutes studied", min=1)

    entries_container = ui.column()

    def get_entries(module_id: int, user_id: int):
        with SessionLocal() as session:
            return (
                session.query(StudyEntry)
                .join(Module)
                .filter(StudyEntry.module_id == module_id)
                .filter(Module.user_id == user_id)
                .all()
            )

    def save_entry():
        if not module_dropdown.value or not minutes_input.value:
            ui.notify("Fill everything")
            return

        module_id = module_options[module_dropdown.value]
        create_entry(module_id, int(minutes_input.value))

        ui.notify("Saved!")
        minutes_input.value = None
 

        ui.navigate.to('/dashboard')

    ui.button("Save Entry", on_click=save_entry)