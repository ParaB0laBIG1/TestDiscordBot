import json
import disnake
from disnake import guild
from config import ADMIN_ROLE_ID, MAIN_ADMIN_ROLE_ID


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
    
    async def remove_admin_roles(self, member):
        self.member_roles = {role.id for role in member.roles}

        admin_role = disnake.utils.get(member.guild.roles, id=self.admin_role_id)
        main_admin_role = disnake.utils.get(member.guild.roles, id=self.main_admin_role_id)

        if any(role_id in self.member_roles for role_id in [self.admin_role_id, self.main_admin_role_id]):
            if self.admin_role_id in self.member_roles:
                await member.remove_roles(admin_role)
            elif self.main_admin_role_id in self.member_roles:
                await member.remove_roles(main_admin_role)
            
            return False
        return False
