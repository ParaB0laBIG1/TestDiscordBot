import json


class CheckPermissions():
    def __init__(self, inter, command: str):
        super().__init__()

        self.author_roles = {role.id for role in inter.author.roles}

        with open("permissions.json", "r", encoding="utf-8") as f:
            self.permissions_data = json.load(f)

        self.permission_roles = self.permissions_data["permissions"].get(command, {})

        self.moderator_role_id = self.permission_roles.get("Модератор")
        self.admin_role_id = self.permission_roles.get("Админ")
        self.main_admin_role_id = self.permission_roles.get("Гл.Админ")
        self.main_role_id = self.permission_roles.get("Главный")

    async def check_permissions(self, member, roles_to_check):
        self.member_roles = {role.id for role in member.roles}

        if any(role_id in self.author_roles for role_id in roles_to_check):
            if self.moderator_role_id in self.author_roles:
                return not any(role_id in self.member_roles for role_id in roles_to_check[1:])
            elif self.admin_role_id in self.author_roles:
                return not any(role_id in self.member_roles for role_id in roles_to_check[1:])
            elif self.main_admin_role_id in self.author_roles:
                return not self.main_role_id in self.member_roles
            elif self.main_role_id in self.author_roles:
                return True

        return False

    async def check_permissions_on_mute(self, member):
        return await self.check_permissions(member, [self.moderator_role_id, self.admin_role_id, self.main_admin_role_id, self.main_role_id])

    async def check_perm_on_slowmode(self):
        return any(role_id in self.author_roles for role_id in [self.moderator_role_id, self.admin_role_id, self.main_admin_role_id, self.main_role_id])

    async def check_perm_on_kick_and_ban(self, member):
        return await self.check_permissions(member, [self.admin_role_id, self.main_admin_role_id, self.main_role_id])