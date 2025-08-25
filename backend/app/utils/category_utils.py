from datetime import datetime

import click
from sqlalchemy.orm import make_transient

from app.database import session
from app.models import Category
from app.utils import utcnow


class CategoryTreeMapper:
    """
    A set of dictionaries representing category relationships in memory for efficient lookups.
    """

    # Data structure to hold category ID to Category object mappings
    category_map: dict[int, Category] = {}

    # Data structure to hold mapping of category ID to its parent's ID
    category_parent_map: dict[int, int | None] = {}

    # Data structure to map category ID to the list of its children IDs
    category_children_map: dict[int, list[int]] = {}

    # Data structure to map category ID to its level in the hierarchy
    category_level_map: dict[int, int] = {}

    # Cache for category search paths to avoid recomputation
    category_search_path_map: dict[int, str] = {}

    def rebuild_category_map(self):
        """Rebuilds the in-memory maps of categories, their parents, children, and levels."""

        click.secho("Rebuilding category tree maps...")

        # Clear existing maps
        self.category_map = {}
        self.category_parent_map = {}
        self.category_children_map = {}
        self.category_level_map = {}

        # Eager load parent relationships to minimize queries
        categories = session.query(Category).all()

        # Walk through categories to build maps
        for cat in categories:
            make_transient(cat)  # Detach from session to avoid side effects
            self.category_map[cat.id] = cat
            if cat.parent_id is not None:
                self.category_parent_map[cat.id] = cat.parent_id
                if not self.category_children_map.get(cat.parent_id, None):
                    self.category_children_map[cat.parent_id] = []
                self.category_children_map[cat.parent_id].append(cat.id)
            else:
                self.category_parent_map[cat.id] = None

        # Walk through once more to calculate levels and search paths
        for cat_id in self.category_map.keys():
            _level, _search_path = self.calculate_level_and_search_paths(cat_id)
            self.category_level_map[cat_id] = _level
            self.category_search_path_map[cat_id] = _search_path

    def get_category(self, cat_id: int):
        return self.category_map.get(cat_id)

    def calculate_level_and_search_paths(self, cat_id: int) -> tuple[int, str]:
        """Returns the level and search path for a given category. Walks up the tree only once to calculate both."""
        level = 0
        path_parts = []
        current_id = cat_id

        while current_id is not None:
            path_parts.append(str(current_id))
            parent_id = self.category_parent_map.get(current_id, None)
            if parent_id is not None:
                level += 1
            current_id = parent_id

        path_parts.reverse()
        search_path_str = ",".join(path_parts)

        # Cache the search path
        self.category_search_path_map[cat_id] = search_path_str

        return level, search_path_str

    def get_category_level(self, cat_id: int) -> int:
        """
        Returns the hierarchy depth of the given category.


        For instance, if the category hierarchy contained...
            fruits (id: 1) -> level 0
                > apples (id: 18) -> level 1
                    > fuji (id: 59) -> level 2

        ...this function would return 2 for the category ID 59.
        """
        return self.category_level_map.get(cat_id, 0)

    def get_all_search_paths(self, cat_id: int) -> list[str]:
        """
        Returns an array of strings, each containing a comma-delimited sequence of integer IDs
        that should be used to search for this category.

        For instance, if the category hierarchy contained...
            fruits (id: 1) -> level 0
                > apples (id: 18) -> level 1
                    > fuji (id: 59) -> level 2

        ...this function would return: ["1", "1,18", "1,18,59"] for the category ID 59.
        """
        cat = self.category_map.get(cat_id)

        if cat is None:
            return []

        paths = [self.get_search_path(cat_id)]

        parent_id = cat.parent_id

        while parent_id is not None:
            paths.append(self.get_search_path(parent_id))
            parent_id = self.category_parent_map.get(parent_id, None)

        return paths

    def get_search_path(self, cat_id: int) -> str:
        """
        Return a comma-delimited string of category IDs representing the path to the given category.

        For instance, if the category hierarchy contained...
            fruits (id: 1) -> level 0
                > apples (id: 18) -> level 1
                    > fuji (id: 59) -> level 2

        ...this function would return: "1,18,59" for the category ID 59.
        """
        return self.category_search_path_map.get(cat_id, str(cat_id))


class CategoryTreeMapperSingleton:
    """
    Creates a singleton instance of a tree of categories that can be accessed globally.
    A utility class to map and cache category relationships in memory for efficient lookups.
    """

    _instance: CategoryTreeMapper = None
    last_updated: datetime = None

    def __new__(cls) -> CategoryTreeMapper:
        """
        Initializes the singleton instance with the category tree mapper,
        loading all the categories and constructing the relationship dictionaries.

        If an instance already exists, it returns that instance. If the categories table has changed,
        it reinitializes the instance with updated categories.

        Runs BEFORE a CategoryTreeMapperSingleton instance object is created.
        """

        # Find latest last_updated datetime from categories table
        newest_cat = session.query(Category).order_by(Category.last_updated.desc()).first()
        has_been_updated = cls.last_updated != newest_cat.last_updated if newest_cat else True

        if cls._instance is None or has_been_updated:
            cls.last_updated = newest_cat.last_updated if newest_cat else utcnow()
            cls._instance = cls.load_category_tree_mapper()

        return cls._instance

    @classmethod
    def load_category_tree_mapper(cls) -> CategoryTreeMapper:
        """
        Loads the category tree mapper, rebuilding the in-memory maps of categories,
        their parents, children, and levels.

        Returns:
            CategoryTreeMapper: The singleton instance of the category tree mapper.
        """
        click.secho("Loading category tree mapper...")
        mapper = CategoryTreeMapper()
        mapper.rebuild_category_map()
        return mapper


category_tree_mapper = CategoryTreeMapperSingleton()
