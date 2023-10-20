from __future__ import annotations

import enum


class ChainPromptLevel(enum.Enum):
    """
    1. No Prompt (Independent)
    2. Shadow Prompt (approximately one inch)
    3. Partial Physical Prompt (thumb and index finger)
    4. Full Physical Prompt (hand-over-hand)
    """

    none = 1
    shadow = 2
    partial_physical = 3
    full_physical = 4

    @classmethod
    def has_name(cls, name):
        return any(name == item.name for item in cls)

    @classmethod
    def options(cls):
        return [item.name for item in cls]


class Relationship(enum.Enum):
    self_participant = 1
    self_guardian = 2
    dependent = 3
    self_professional = 4
    self_interested = 5

    @classmethod
    def has_name(cls, name):
        return any(name == item.name for item in cls)

    @classmethod
    def is_self(cls, name):
        if isinstance(name, str):
            return name != "dependent"
        if isinstance(name, cls):
            return name != cls.dependent

    @classmethod
    def options(cls):
        return [item.name for item in cls]


class Status(enum.Enum):
    currently_enrolling = "Currently enrolling"
    study_in_progress = "Study in progress"
    results_being_analyzed = "Results being analyzed"
    study_results_published = "Study results published"

    @classmethod
    def has_name(cls, name):
        return any(name == item.name for item in cls)

    @classmethod
    def options(cls):
        return [item.name for item in cls]


class Permission(enum.Enum):
    create_resource = "Create Resources"
    edit_resource = "Edit Resources"
    delete_resource = "Delete Resources"
    publish_resource = "Publish Resources"
    create_study = "Create Studies"
    edit_study = "Edit Studies"
    delete_study = "Delete Studies"
    user_admin = "Visit User Admin"
    participant_admin = "Visit Participant Admin"
    data_admin = "Visit Data Admin"
    user_detail_admin = "User Admin Data Details"
    export_status = "View Export Status"
    taxonomy_admin = "Visit Taxonomy Admin"

    # keep user_roles and delete_user last to keep off of test user permissions
    delete_user = "Delete User"
    user_roles = "Manage User Roles"


class Role(enum.Enum):
    # see migration version 15cfedb47914 for an example of an update to the Role enum

    admin = list(Permission)
    test = list(Permission)[:-2]
    researcher = [
        Permission.user_detail_admin,
    ]
    editor = [Permission.create_resource, Permission.edit_resource, Permission.delete_resource]
    user = []

    def permissions(self):
        return self.value

    @classmethod
    def has_name(cls, name):
        return any(name == item.name for item in cls)

    @classmethod
    def options(cls):
        return [item.name for item in cls]


class StudyUserStatus(enum.Enum):
    inquiry_sent = 1
    enrolled = 2
