from app.services import (
    module_service,
    study_entry_service,
    ServiceError,
)


# CREATE MODULE
def test_create_module():
    # Arrange
    user_id = 1

    # Act
    module = module_service.create_module(
        user_id,
        "Maths",
        "#5898ff"
    )

    # Assert
    assert module.name == "Maths"
    assert module.color == "#5898ff"
    assert module.user_id == user_id
    assert module.is_archived is False


# CREATE ENTRY
def test_create_entry():
    # Arrange
    module = module_service.create_module(
        1,
        "Maths",
        "#5898ff"
    )

    # Act
    study_entry_service.create_entry(module.id, 60)
    entries = study_entry_service.get_entries(module.id)

    # Assert
    assert len(entries) == 1
    assert entries[0].duration_minutes == 60


# GET ENTRIES
def test_get_entries():
    # Arrange
    module = module_service.create_module(
        1,
        "Maths",
        "#4CAF50"
    )

    # Act
    study_entry_service.create_entry(module.id, 30)
    study_entry_service.create_entry(module.id, 45)
    entries = study_entry_service.get_entries(module.id)

    # Assert
    assert len(entries) == 2


# ARCHIVE MODULE
def test_archive_module():
    # Arrange
    module = module_service.create_module(
        1,
        "Maths",
        "#9C27B0"
    )

    # Act
    archived_module = module_service.archive_module(module.id)

    # Assert
    assert archived_module.is_archived is True


# DELETE MODULE
def test_delete_module():
    # Arrange
    user_id = 888

    module = module_service.create_module(
        user_id,
        "Maths",
        "#FF9800"
    )

    # Act
    result = module_service.delete_module(module.id)
    modules = module_service.get_active_modules(user_id)

    # Assert
    assert result is True
    assert module.id not in [m["id"] for m in modules]


# EDGE CASE: INVALID DURATION
def test_create_entry_invalid_duration():
    # Act & Assert
    try:
        study_entry_service.create_entry(1, 0)
        assert False

    except ServiceError:
        assert True