from nicegui import ui
from nicegui import app
from datetime import datetime, timedelta
import time

from app.database import SessionLocal
from app.models import Module

from app.services import module_service, study_entry_service


@ui.page('/module-detail')
def module_detail_page():

    user_id = app.storage.user.get('user_id')
    module_id = app.storage.user.get('selected_module')

    if not user_id or not module_id:
        ui.navigate.to('/dashboard')
        return
    
    ui.button(
    icon='arrow_back',
    on_click=lambda: ui.navigate.to('/dashboard')
    ).props('flat round') \
    .classes('mb-4')

    modules = module_service.get_active_modules(user_id) + module_service.get_archived_modules(user_id)

    module = next((m for m in modules if m['id'] == module_id), None)

    if not module:
        ui.label("Module not found")
        return

    # Calculate total study time
    total_minutes = sum(e['duration_minutes'] for e in module['entries'])

    with SessionLocal() as session:
        m = session.get(Module, module['id'])
        goal = m.goal_minutes


    hours = total_minutes // 60
    minutes = total_minutes % 60

    

    with ui.row().classes('w-full h-screen justify-center items-start p-10'):

        with ui.card().classes('w-1/2 p-6 rounded-2xl shadow-lg'):

            ui.label(module['name']).classes('text-3xl font-bold mb-1')

            ui.label(f'Total Study Time: {hours}h {minutes}min') \
                .classes('text-lg text-black-1000 mb-4')

            # Timer functionality
            def start_timer():
                start_time["value"] = time.time()


            def stop_timer():
                if not start_time["value"]:
                    return

                duration_seconds = int(time.time() - start_time["value"])
                duration_minutes = max(1, duration_seconds // 60)

                study_entry_service.create_entry(module['id'], duration_minutes)

                ui.notify(f"{duration_minutes} min saved!", color="green")
                start_time["value"] = None
                ui.navigate.to('/module-detail')

                show_entries()  

            def update_timer():
                if start_time["value"]:
                    seconds = int(time.time() - start_time["value"])
                    minutes = seconds // 60
                    secs = seconds % 60
                    timer_label.set_text(f"{minutes:02}:{secs:02}")

            ui.timer(1, update_timer)

            with ui.row().classes('items-center gap-4 mb-6'):

                timer_label = ui.label("00:00") \
                    .classes('text-3xl')

                if not module['is_archived']:
                    ui.button("Start", on_click=start_timer, color='green') \
                        .classes('rounded-xl')
                    ui.button("Stop", on_click=stop_timer, color='red') \
                        .classes('rounded-xl')
                else:
                    ui.button("Start", color='grey').props('disable')
                    ui.button("Stop", color='grey').props('disable')


                start_time = {"value": None}

            # Goal progress section
            if goal:
                progress = min(100, int((total_minutes / goal) * 100))


                with ui.column():

                    ui.label(f"🎯 Your goal is {goal // 60}h") \
                        .classes('text-md font-semibold')

                    ui.label(f"You’ve completed {progress}%") \
                        .classes('text-sm text-black-600')


                    with ui.row().classes('w-full h-3 bg-gray-300 rounded-full mt-2'):
                        ui.row().style(f'width: {progress}%;') \
                            .classes('h-3 bg-blue-500 rounded-full')

                    if progress >= 100:
                        message = "Goal reached 🎉"
                    else:
                        message = "Keep going 💪"

                    ui.label(message).classes('text-xs text-gray-500 mt-1')

            def open_goal_dialog():
                with ui.dialog() as dialog, ui.card():
                    goal_input = ui.input(
                        label="Goal (hours)",
                    )

                    def save_goal():
                        if not goal_input.value.isdigit() or int(goal_input.value) <= 0:
                            ui.notify("Only positive whole numbers are allowed", color="red")
                            return
                        
                        minutes = int(goal_input.value) * 60

                        with SessionLocal() as session:
                            m = session.query(Module).get(module['id'])
                            m.goal_minutes = minutes
                            session.commit()

                        ui.notify("Goal saved!", color="green")
                        dialog.close()
                        ui.navigate.to('/module-detail')

                    ui.button("Save", on_click=save_goal)

                dialog.open()

            button = ui.button(
                "Set Goal", on_click=open_goal_dialog
            ).props('outline') \
            .classes('mb-6 rounded-xl')

            if module['is_archived']:
                button.props('disable')


            ui.label('All Entries').classes('text-xl mb-2')
            filter_select = ui.select(
                ['All', 'Today', 'This week', 'This month'],
                value='All'
            ).classes('w-40 mb-6')
            entries_container = ui.column()


            # Filter study entries
            def show_entries():
                entries_container.clear()

                selected = filter_select.value
                now = datetime.now()

                entries = module['entries']


                if selected == 'Today':
                    entries = [e for e in entries if e['studied_at'].date() == now.date()]

                elif selected == 'This week':
                    start = now - timedelta(days=now.weekday())
                    entries = [e for e in entries if e['studied_at'] >= start]

                elif selected == 'This month':
                    entries = [
                        e for e in entries
                        if e['studied_at'].month == now.month
                        and e['studied_at'].year == now.year
                    ]


                with entries_container:
                    if not entries:
                        ui.label("No entries").classes('text-gray-500')

                    for e in entries:

                        with ui.row().classes('justify-between items-center'):

                            with ui.column():
                                ui.label(str(e['studied_at']).split(' ')[0]) \
                                    .classes('text-sm')

                            ui.label(f"{e['duration_minutes']} min") \
                                .classes('text-lg font-bold text-blue-600')


            def handle_delete():
                module_service.delete_module(module['id'])
                ui.notify("Module deleted", color="red")
                ui.navigate.to('/dashboard')


            def handle_toggle():
                if module['is_archived']:
                    module_service.unarchive_module(module['id'])
                    ui.notify("Module unarchived", color="green")
                else:
                    module_service.archive_module(module['id'])
                    ui.notify("Module archived", color="orange")

                ui.navigate.to('/dashboard')

            with ui.row().classes('gap-2 mt-6'):

                ui.button("Delete", on_click=handle_delete, color='red') \
                    .classes('rounded-xl')

                ui.button(
                    "Unarchive" if module['is_archived'] else "Archive",
                    on_click=handle_toggle
                ).classes('rounded-xl bg-orange-500 text-white')

                button = ui.button(
                    '+ Add Entry',
                    on_click=lambda: ui.navigate.to('/entries') 
                ).classes('rounded-xl bg-black text-white')

                if module['is_archived']:
                    button.props('disable')

            filter_select.on('update:model-value', lambda e: show_entries()) 
            show_entries()