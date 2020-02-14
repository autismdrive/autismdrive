import enum


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
    admin = list(Permission)
    test = list(Permission)[:-2]
    researcher = [Permission.user_detail_admin, ]
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


# see migration version 15cfedb47914 for an example of an update to the Role enum
