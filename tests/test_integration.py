from app.services import (
    create_module,
    create_entry,
    get_entries,
    get_total_minutes,
    archive_module,
    get_active_modules,
)


def test_create_module_and_add_entry():
    module = create_module(
        user_id=1,
        name="Maths",
        color="#5898ff"
    )

    create_entry(module.id, 45)

    entries = get_entries(module.id)

    assert len(entries) == 1
    assert entries[0].duration_minutes == 45


def test_multiple_entries_update_total_minutes():
    module = create_module(
        user_id=1,
        name="Maths",
        color="#4CAF50"
    )

    create_entry(module.id, 20)
    create_entry(module.id, 40)

    total = get_total_minutes(1)

    assert total >= 60


def test_archive_module_removes_from_active_modules():
    module = create_module(
        user_id=1,
        name="Maths",
        color="#F44336"
    )

    archive_module(module.id)

    active_modules = get_active_modules(1)

    module_ids = [m["id"] for m in active_modules]

    assert module.id not in module_ids