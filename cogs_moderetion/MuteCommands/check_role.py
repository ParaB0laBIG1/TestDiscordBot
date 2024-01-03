import disnake
from disnake.ext import commands
from config import MODER_ROLE_ID, ADMIN_ROLE_ID, ID_ROLE_MAIN


async def has_admin_or_main_role(inter, member):
    """
        checking top role
    """
    author_top_role = inter.author.top_role
    member_top_role = member.top_role

    if author_top_role > member_top_role:
        return True
    else:
        return False

async def has_moder_role(inter):
    user_roles = inter.author.roles
    print(user_roles)

    return any(role.id in {MODER_ROLE_ID, ADMIN_ROLE_ID, ID_ROLE_MAIN} for role in user_roles)

