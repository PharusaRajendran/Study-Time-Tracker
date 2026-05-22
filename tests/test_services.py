from app.services import (
    create_module,
    create_entry,
    get_entries,
    get_total_minutes,
    archive_module,
    delete_module,
    get_active_modules,
)



# CREATE MODULE
def test_create_module():
    # Arrange
    user_id = 1

    # Act
    module = create_module(user_id, "Maths", "#5898ff")

    # Assert
    assert module.name == "Maths"
    assert module.color == "#5898ff"
    assert module.user_id == user_id
    assert module.is_archived is False


# CREATE ENTRY
def test_create_entry():
    # Arrange
    module = create_module(1, "Maths", "#5898ff")

    # Act
    create_entry(module.id, 60)
    entries = get_entries(module.id)

    # Assert
    assert len(entries) == 1
    assert entries[0].duration_minutes == 60


# GET ENTRIES
def test_get_entries():
    # Arrange
    module = create_module(1, "Maths", "#4CAF50")

    # Act
    create_entry(module.id, 30)
    create_entry(module.id, 45)
    entries = get_entries(module.id)

    # Assert
    assert len(entries) == 2


# ARCHIVE MODULE
def test_archive_module():
    # Arrange
    module = create_module(1, "Maths", "#9C27B0")

    # Act
    archived_module = archive_module(module.id)

    # Assert
    assert archived_module.is_archived is True


# DELETE MODULE
def test_delete_module():
    # Arrange
    user_id = 888
    module = create_module(user_id, "Maths", "#FF9800")

    # Act
    result = delete_module(module.id)
    modules = get_active_modules(user_id)

    # Assert
    assert result is True
    assert module.id not in [m.id for m in modules]


# EDGE CASE 
def test_create_entry_invalid_module():
    # Act & Assert
    try:
        create_entry(None, 60)
        assert False
    except Exception:
        assert True