from nicegui import app, ui

from app.services import module_service, study_entry_service, ServiceError


@ui.page('/entries')
def entries_page():

    ui.button(
        icon='arrow_back',
        on_click=lambda: ui.navigate.to('/dashboard')
    ).props('flat round').classes('mb-4')

    user_id = app.storage.user.get('user_id')

    if not user_id:
        ui.navigate.to('/')
        return

    def load_modules():
        modules = module_service.get_active_modules(user_id)
        return {module["name"]: module["id"] for module in modules}

    module_options = load_modules()

    ui.label("Add Study Entry").classes("text-2xl font-bold")

    module_dropdown = ui.select(
        options=list(module_options.keys()),
        label="Choose module"
    )

    minutes_input = ui.number(label="Minutes studied", min=1)

    def save_entry():
        if not module_dropdown.value or not minutes_input.value:
            ui.notify("Fill everything", color="red")
            return

        module_id = module_options[module_dropdown.value]

        try:
            study_entry_service.create_entry(
                module_id,
                int(minutes_input.value)
            )

            ui.notify("Saved!", color="green")
            minutes_input.value = None
            ui.navigate.to('/dashboard')

        except ServiceError as error:
            ui.notify(str(error), color="red")

    ui.button("Save Entry", on_click=save_entry)