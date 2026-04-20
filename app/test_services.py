from services import create_entry, get_entries, get_total_minutes

#Create test entries
create_entry(1, 60)
create_entry(1, 30)


# Get entries for module 1
entries = get_entries(1)
print("Entries for module 1:")
for entry in entries:
    print(entry.id, entry.module_id, entry.duration_minutes)

# Get total minutes for user 1
total = get_total_minutes(1)
print("Total minutes:", total)

print("Test completed successfully!")