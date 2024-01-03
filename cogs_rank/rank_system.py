import disnake
import sqlite3
from disnake.ext import commands

conn = sqlite3.connect('database\\rank.db')
c = conn.cursor()

class RankSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.ranks = [
            1188484736851656825, # Прошел начальный курс лечения
            1188484736851656826, # Получеловек
            1188484736851656826, # Рецензент
            1188484736881000539, # Здравомыслящий
            1188484736881000540, # Возвышенный
            1188484736881000541, # Почетный
        ]

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        member_id = message.author.id

        if await self.member_exists_in_db(member_id):
            await self.process_existing_member(message, member_id)
        else:
            await self.process_new_member(message, member_id)

    async def process_existing_member(self, message, member_id):
        exp_value = await self.get_exp_member(member_id, column="now_exp")

        if exp_value is not None:
            new_now_exp_value = exp_value + 10
            new_all_exp_value = new_now_exp_value
            new_exp_for_advancement_value = new_all_exp_value * 2

            new_rank = self.ranks[0] + 1

            if exp_value > 100:
                await self.update_rank_member(new_rank=new_rank, member_id=member_id)
                await self.update_exp_member(new_exp_value=0, member_id=member_id, column="now_exp")
                await self.update_exp_member(new_exp_value=new_all_exp_value, member_id=member_id, column="all_exp")
                await self.update_exp_member(new_exp_value=new_exp_for_advancement_value, member_id=member_id, column="exp_for_advancement")
                
                await self.send_rank_update_message(message)
            else:
                await self.update_exp_member(new_exp_value=new_now_exp_value, member_id=member_id, column="now_exp")
                await self.send_exp_update_message(message, member_id)
        else:
            print(f"Участник с ID {member_id} не найден в базе данных.")

    async def process_new_member(self, message, member_id):
        await message.reply(f"Ваш текущий опыт: {await self.get_exp_member(member_id=member_id, column='now_exp')}")
        print(f"{message.author.name} был добавлен в базу данных")
        await self.save_member_in_db(
            member_name=message.author.mention,
            member_id=member_id,
            rank=self.ranks[0],
            now_exp=0,
            all_exp=0,
            exp_for_advancement=0,
            boost=None
        )

    async def send_rank_update_message(self, message):
        await message.reply(f"Участник {message.author.mention} получил новый ранг")

    async def send_exp_update_message(self, message, member_id):
        await message.reply(f"Ваш текущий опыт: {await self.get_exp_member(member_id=member_id, column='now_exp')}")

    async def update_exp_member(self, column ,new_exp_value, member_id):
        if column == "now_exp":
            c.execute('UPDATE user_rank SET now_exp = ? WHERE member_id = ?', (new_exp_value, member_id))
            conn.commit()
            
        elif column == "all_exp":
            c.execute('UPDATE user_rank SET all_exp = ? WHERE member_id = ?', (new_exp_value, member_id))
            conn.commit()

        elif column == "exp_for_advancement":
            c.execute('UPDATE user_rank SET exp_for_advancement = ? WHERE member_id = ?', (new_exp_value, member_id))
            conn.commit()
        else:
            print("ERROR: the column from the database is not clear")


    async def save_member_in_db(self, member_name, member_id, rank, now_exp, all_exp, exp_for_advancement, boost):
        c.execute("INSERT INTO user_rank VALUES (?, ?, ?, ?, ?, ?, ?)", 
                (member_name, member_id, rank, 
                now_exp, all_exp, exp_for_advancement, boost))
        conn.commit()

    async def member_exists_in_db(self, member_id):
        c.execute('SELECT * FROM user_rank WHERE member_id = ?', (member_id,))
        return bool(c.fetchone())

    async def get_exp_member(self, member_id, column):
            
        if column == "now_exp":
            c.execute('SELECT now_exp FROM user_rank WHERE member_id = ?', (member_id,))
            result = c.fetchone()
            if result:
                return result[0]
            else:
                return None
            
        elif column == "all_exp":
            c.execute('SELECT all_exp FROM user_rank WHERE member_id = ?', (member_id,))
            result = c.fetchone()
            if result:
                return result[0]
        elif column == "exp_for_advancement":
            c.execute('SELECT exp_for_advancement FROM user_rank WHERE member_id = ?', (member_id,))
            result = c.fetchone()
            if result:
                return result[0]
        else:
            print("ERROR: the column from the database is not clear")


    async def update_rank_member(self, new_rank ,member_id):
        c.execute('UPDATE user_rank SET rank = ? WHERE member_id = ?', (new_rank, member_id,))
        conn.commit()

def setup(bot: commands.Bot):
    bot.add_cog(RankSystem(bot))

