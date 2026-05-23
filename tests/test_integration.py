from app.services import (
    module_service,
    study_entry_service,
)


# CREATE MODULE AND ADD ENTRY
def test_create_module_and_add_entry():

    # Arrange
    module = module_service.create_module(
        user_id=1,
        name="Maths",
        color="#5898ff"
    )

    # Act
    study_entry_service.create_entry(module.id, 45)
    entries = study_entry_service.get_entries(module.id)

    # Assert
    assert len(entries) == 1
    assert entries[0].duration_minutes == 45


# MULTIPLE ENTRIES UPDATE TOTAL MINUTES
def test_multiple_entries_update_total_minutes():

    # Arrange
    module = module_service.create_module(
        user_id=1,
        name="Maths",
        color="#4CAF50"
    )

    # Act
    study_entry_service.create_entry(module.id, 20)
    study_entry_service.create_entry(module.id, 40)

    total = study_entry_service.get_total_minutes(1)

    # Assert
    assert total >= 60


# ARCHIVE MODULE REMOVES FROM ACTIVE MODULES
def test_archive_module_removes_from_active_modules():

    # Arrange
    module = module_service.create_module(
        user_id=1,
        name="Maths",
        color="#F44336"
    )

    # Act
    module_service.archive_module(module.id)

    active_modules = module_service.get_active_modules(1)

    module_ids = [m["id"] for m in active_modules]

    # Assert
    assert module.id not in module_ids