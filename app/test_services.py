from services import save_study_entry

save_study_entry(1, 60)

print("It worked!")

from services import save_study_entry, get_all_entries

save_study_entry(1, 60)

entries = get_all_entries()

for entry in entries:
    print(entry.id, entry.module_id, entry.duration_minutes)

print("It worked!")