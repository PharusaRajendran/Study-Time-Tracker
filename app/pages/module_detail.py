# app/pages/module_detail.py
from nicegui import ui
from app.services import get_active_modules, archive_module, delete_module, get_archived_modules, unarchive_module
from nicegui import app
from datetime import datetime, timedelta
from app.services import create_entry 
import time 
from app.database import SessionLocal
from app.models import Module


@ui.page('/module-detail')
def module_detail_page():

    user_id = app.storage.user.get('user_id')
    module_id = app.storage.user.get('selected_module')

    if not user_id or not module_id:
        ui.navigate.to('/dashboard')
        return

    modules = get_active_modules(user_id) + get_archived_modules(user_id)

    start_time = None

    # 🔍 finde aktuelles Modul
    module = next((m for m in modules if m['id'] == module_id), None)

    if not module:
        ui.label("Module not found")
        return

    # 🔢 total time
    total_minutes = sum(e['duration_minutes'] for e in module['entries'])

    with SessionLocal() as session:
        m = session.get(Module, module['id'])
        goal = m.goal_minutes


    hours = total_minutes // 60
    minutes = total_minutes % 60

    

    with ui.row().classes('w-full h-screen justify-center items-start p-10'):

        with ui.column().classes('w-1/2'):

            # 📚 Titel
            ui.label(module['name']).classes('text-3xl font-bold')

            # ⏱ Total Time
            ui.label(f'{hours}h {minutes}min').classes('text-xl mb-4')

            if goal:
                progress = int((total_minutes / goal) * 100)

                ui.label(f"🎯 Goal: {goal // 60}h").classes('text-lg')
                ui.linear_progress(progress / 100).classes('w-full')
                ui.label(f"{progress}% completed")

            def start_timer():
                start_time["value"] = time.time()


            def stop_timer():
                if not start_time["value"]:
                    return

                duration_seconds = int(time.time() - start_time["value"])
                duration_minutes = max(1, duration_seconds // 60)

                create_entry(module['id'], duration_minutes)

                ui.notify(f"{duration_minutes} min saved!", color="green")

                start_time["value"] = None

                show_entries()  

            def update_timer():
                if start_time["value"]:
                    seconds = int(time.time() - start_time["value"])
                    minutes = seconds // 60
                    secs = seconds % 60
                    timer_label.set_text(f"{minutes:02}:{secs:02}")

            ui.timer(1, update_timer)

            with ui.row().classes('items-center gap-3 mb-4'):

                timer_label = ui.label("00:00").classes('text-2xl font-bold')

                if not module['is_archived']:
                    ui.button("Start", on_click=start_timer, color='green')
                    ui.button("Stop", on_click=stop_timer, color='red')
                else:
                    ui.button("Start", color='grey').props('disable')
                    ui.button("Stop", color='grey').props('disable')


                start_time = {"value": None} 

            def open_goal_dialog():
                with ui.dialog() as dialog, ui.card():
                    goal_input = ui.number(label="Goal (hours)", min=1)

                    def save_goal():
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

            ui.button("Set Goal", on_click=open_goal_dialog)



            # 📊 Timeline Filter (placeholder)
            filter_select = ui.select(
                ['All', 'Today', 'This week', 'This month'],
                value='All'
            ).classes('w-40 mb-6')

            # 📋 Entries
            ui.label('All Entries').classes('text-xl mb-2')
            entries_container = ui.column()

            if not module['entries']:
                ui.label('No entries yet').classes('text-gray-500')


            def show_entries():
                entries_container.clear()

                selected = filter_select.value
                now = datetime.now()

                entries = module['entries']

                # 🔥 Filter direkt hier
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

                # 🔥 Anzeige
                with entries_container:
                    if not entries:
                        ui.label("No entries").classes('text-gray-500')

                    for e in entries:
                        with ui.row().classes('justify-between w-full mb-1'):
                            ui.label(str(e['studied_at']).split(' ')[0])
                            ui.label(f"{e['duration_minutes']} min")
    
            # 🗑 Delete Button
            def handle_delete():
                delete_module(module['id'])
                ui.notify("Module deleted", color="red")
                ui.navigate.to('/dashboard')

            ui.button("Delete Module", on_click=handle_delete, color='red').classes('mt-4')

            def handle_toggle():
                if module['is_archived']:
                    unarchive_module(module['id'])
                    ui.notify("Module unarchived", color="green")
                else:
                    archive_module(module['id'])
                    ui.notify("Module archived", color="orange")

                ui.navigate.to('/dashboard')

            ui.button(
                "Unarchive Module" if module['is_archived'] else "Archive Module",
                on_click=handle_toggle
            ).classes('mt-2')

            filter_select.on('update:model-value', lambda e: show_entries()) 
            show_entries()