# app/pages/dashboard.py
from sys import modules

from nicegui import ui
from app.services import get_active_modules
from app.services import get_archived_modules
from nicegui import app


@ui.page('/dashboard')
def dashboard_page():

    user_id = app.storage.user.get('user_id')


    if not user_id:
        ui.navigate.to('/')
        return

    modules = get_active_modules(user_id)
    archived_modules = get_archived_modules(user_id)

    # 🔢 total study time berechnen
    total_minutes = 0
    for m in modules:
        for e in m['entries']:
            total_minutes += e['duration_minutes']

    hours = total_minutes // 60
    minutes = total_minutes % 60

    with ui.row().classes('w-full justify-end'):
    
        def logout():
            app.storage.user.clear()
            ui.navigate.to('/')

        ui.button(icon='logout', on_click=logout, color='red')

    # 🎨 Layout
    with ui.row().classes('w-full h-screen justify-center items-start p-10'):

        with ui.column().classes('w-1/2'):

            # 👋 Welcome
            ui.label(f'Welcome {app.storage.user.get("username")}!').classes('text-3xl font-bold')
            



            with ui.column().classes(
                        'fixed right-10 top-1/3 gap-4'
                    ):
                ui.label(f'{hours}h {minutes}min').classes('text-xl mb-6')

                        # 📊 Chart Daten
            chart_data = []

            for m in modules:
                total = sum(e['duration_minutes'] for e in m['entries'])

                if total > 0:
                    chart_data.append({
                        'value': total,
                        'name': m['name'],
                        'itemStyle': {'color': m['color']}
                    })


            # 📊 Chart UI
            ui.echart({
                'tooltip': {'trigger': 'item', 'formatter': '{b}: {c} min'},
                'series': [
                    {
                        'type': 'pie',
                        'radius': ['50%', '70%'],
                        'data': chart_data,

                        
                        'label': {'show': False},
                        'labelLine': {'show': False},

                        'itemStyle': {
                            'borderColor': '#ffffff',
                            'borderWidth': 2
}
                    }
                ]
            }).classes('w-64 h-64')

            # 📚 Module Section
            ui.label('Your Modules').classes('text-xl mb-2')

            # 📦 Module Liste
            if not modules:
                ui.label('No modules yet').classes('text-gray-500')

            def open_module(module_id):
                app.storage.user['selected_module'] = module_id
                ui.navigate.to('/module-detail')

            with ui.row().classes('gap-6 flex-wrap mt-4'):
          
                for m in modules:
                    with ui.card().classes(
                        'w-52 h-28 flex items-center justify-center text-center cursor-pointer rounded-2xl shadow-md'
                    ).style(f'background-color: {m["color"]}; color: white;') \
                    .on('click', lambda e, mid=m['id']: open_module(mid)):

                        ui.label(m['name']).classes('text-sm font-semibold')

               


            with ui.column().classes(
                'fixed right-10 top-1/3 gap-4'
            ):

                ui.button(
                    '+ Add Module',
                    on_click=lambda: ui.navigate.to('/modules')
                ).props('square color=primary')

                is_disabled = len(modules) == 0 

                ui.button(
                    '+ Add Entry',
                    on_click=lambda: ui.navigate.to('/entries')
                ).props(f'square color=primary {"disable" if is_disabled else ""}')

            # 📦 Archived Hinweis
            ui.label('Archived Modules').classes('text-xl mt-6')

            if not archived_modules:
                ui.label('No archived modules').classes('text-gray-500')

            for m in archived_modules:
                    with ui.card().classes(
                        'w-full mb-2 p-4 bg-gray-100 text-gray-500 cursor-pointer'
                    ).on('click', lambda e, mid=m['id']: open_module(mid)):

                        ui.label(m['name'])