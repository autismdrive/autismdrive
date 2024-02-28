def cat_has_parent(cat=None) -> bool:
    """Returns true if the given category has a parent category."""
    from app.models import Category

    return cat and isinstance(cat, Category) and cat.parent and cat.parent.id is not None


def calculate_level(cat_id: int) -> int:
    """
    Returns the hierarchy depth of the given category.


    For instance, if the category hierarchy contained...
        fruits (id: 1) -> level 0
            > apples (id: 18) -> level 1
                > fuji (id: 59) -> level 2

    ...this function would return 2 for the category ID 59.
    """
    from app.resources.CategoryEndpoint import get_category_by_id

    db_cat = get_category_by_id(cat_id, with_joins=True)
    level = 0
    cat = db_cat

    if cat is None:
        return 0

    while cat_has_parent(cat):
        level = level + 1
        cat = cat.parent

    return level


def all_search_paths(cat_id: int) -> list[str]:
    """
    Returns an array of strings, each containing a comma-delimited sequence of integer IDs
    that should be used to search for this category.

    For instance, if the category hierarchy contained...
        fruits (id: 1) -> level 0
            > apples (id: 18) -> level 1
                > fuji (id: 59) -> level 2

    ...this function would return: ["1", "1,18", "1,18,59"] for the category ID 59.
    """
    from app.resources.CategoryEndpoint import get_category_by_id

    db_cat = get_category_by_id(cat_id, with_joins=True)
    cat = db_cat

    if cat is None:
        return []

    paths = [search_path(cat_id)]

    while cat_has_parent(cat):
        cat = cat.parent
        paths.append(search_path(cat.id))

    return paths


def search_path(cat_id: int) -> str:
    """
    Return a comma-delimited string of category IDs representing the path to the given category.

    For instance, if the category hierarchy contained...
        fruits (id: 1) -> level 0
            > apples (id: 18) -> level 1
                > fuji (id: 59) -> level 2

    ...this function would return: "1,18,59" for the category ID 59.
    """
    from app.resources.CategoryEndpoint import get_category_by_id

    db_cat = get_category_by_id(cat_id, with_joins=True)
    cat = db_cat

    if cat is None:
        return ""

    path = str(cat.id)
    while cat_has_parent(cat):
        cat = cat.parent
        path = str(cat.id) + "," + path

    return path
