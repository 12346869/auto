import discord
from discord.ext import commands
import asyncio
import random

from dotenv import load_dotenv
import os
import discord
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = commands.Bot(command_prefix="+", self_bot=True)
# ... restul codului tău ...


bot = commands.Bot(command_prefix="+", self_bot=True)
bot.remove_command("help")

def premium_banner():
    print("""
██████╗ ██████╗ ███████╗███╗   ███╗██╗   ██╗███╗   ███╗
██╔══██╗██╔══██╗██╔════╝████╗ ████║██║   ██║████╗ ████║
██████╔╝██████╔╝█████╗  ██╔████╔██║██║   ██║██╔████╔██║
██╔═══╝ ██╔══██╗██╔══╝  ██║╚██╔╝██║██║   ██║██║╚██╔╝██║
██║     ██║  ██║███████╗██║ ╚═╝ ██║╚██████╔╝██║ ╚═╝ ██║
╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝     ╚═╝
""")

premium_banner()

# ======= VARIABILE GLOBALE =======
active_autoreacts = {}

spam_running = False
spam_task = None

# Pentru trimitere mesaje din mesaje.txt
auto_msg_running = False
auto_msg_channel = None
auto_msg_list = []

# Pentru trimitere mesaje din msjmic.txt
auto_msg_mic_running = False
auto_msg_mic_channel = None
auto_msg_mic_list = []
@bot.event
async def on_ready():
    print(f"{bot.user} este online!")


@bot.command()
async def react(ctx, user: discord.User, emoji: str):
    active_autoreacts[user.id] = emoji
    await ctx.message.add_reaction("✅")
    await ctx.message.delete()

@bot.command()
async def stop(ctx):
    try:
        guild_id = ctx.guild.id if ctx.guild else None
        if guild_id and guild_id in active_autoreacts:
            del active_autoreacts[guild_id]
            await ctx.message.add_reaction("✅")
        else:
            await ctx.message.add_reaction("✖️")
        await ctx.message.delete()
    except:
        pass

# Start/stop mesaje mari (mesaje.txt)
spam_running = False
spam_task = None

@bot.command()
async def lstart(ctx, member: discord.User = None, delay: float = 1.0):
    global spam_running_l, spam_task_l
    if spam_running_l:
        await ctx.message.add_reaction("❌")
        return
    spam_running_l = True

    try:
        with open("mesaje.txt", "r", encoding="utf-8") as f:
            messages = f.read().splitlines()
    except FileNotFoundError:
        await ctx.send("❌ Fișierul `mesaje.txt` nu a fost găsit.")
        return

    async def spam_loop():
        i = 0
        while spam_running_l:
            msg = messages[i].strip()
            if msg:
                if member:
                    await ctx.send(f"{member.mention} {msg}")
                else:
                    await ctx.send(msg)
            i = (i + 1) % len(messages)
            await asyncio.sleep(delay)

    spam_task_l = asyncio.create_task(spam_loop())
    await ctx.message.add_reaction("✅")
    await ctx.message.delete()

@bot.command()
async def lstop(ctx):
    global spam_running_l, spam_task_l
    if not spam_running_l:
        await ctx.message.add_reaction("❌")
        return
    spam_running_l = False
    if spam_task_l:
        spam_task_l.cancel()
        spam_task_l = None
    await ctx.message.add_reaction("✅")
    await ctx.message.delete()

# Start/stop mesaje mici (msjmic.txt)

spamming = False
spam_task = None
micspam_active = False  # variabilă globală

@bot.command()
async def mstart(ctx, user: discord.User, delay: float = 2.0):
    global micspam_active
    if micspam_active:
        await ctx.send("Spam deja activ.")
        return
    micspam_active = True
    await ctx.message.add_reaction("✅")
    await ctx.message.delete()
    with open("msjmic.txt", "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    i = 0
    while micspam_active:
        msg = lines[i]
        text = f"{user.mention} {msg}"
        await ctx.send(text)
        i = (i + 1) % len(lines)
        await asyncio.sleep(delay)

@bot.command()
async def mstop(ctx):
    global micspam_active
    if micspam_active:
        micspam_active = False
        await ctx.message.add_reaction("✅")
        await ctx.message.delete()
    else:
        await ctx.send("Nu este niciun spam activ.")
#Funcții trimitere mesaje
async def send_auto_messages():
    global auto_msg_running, auto_msg_channel, auto_msg_list
    while auto_msg_running:
        for msg in auto_msg_list:
            if not auto_msg_running:
                break
            try:                await auto_msg_channel.send(msg)
            except:
                pass
            await asyncio.sleep(5)

async def send_auto_messages_mic():
    global auto_msg_mic_running, auto_msg_mic_channel, auto_msg_mic_list
    while auto_msg_mic_running:
        for msg in auto_msg_mic_list:
            if not auto_msg_mic_running:
                break
            try:
                await auto_msg_mic_channel.send(msg)
            except:
                pass
            await asyncio.sleep(3)

@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.author.bot:
        return

    emoji = active_autoreacts.get(message.author.id)
    if emoji:
        try:
            await message.add_reaction(emoji)
        except:
            pass

# Date fake pentru +expose
fake_names = [
    "Chastity Lazar", "Jordan Blake", "Taylor Morgan", "Skyler Quinn",
    "Riley Phoenix", "Casey Hunter", "Jamie Reese", "Avery Lane"
]

genders = ["Male","Nigga", "Female","Taran", "Other"]

hair_colors = ["Black", "Blonde", "Brown", "Red", "Gray", "White", "Blue"]

skin_colors = [ "Black", "Brown", "Olive", "Tan", "Pale"]

locations = [
    "Kentucky", "California", "New York", "Texas", "Florida",
    "Washington", "Nevada", "Ohio", "Targoviste",
]

occupations = [
    "Artist", "Engineer", "Teacher", "Developer", "Designer",
    "Chef", "Musician", "Writer", "Curva", "Escorta"
]

ethnicities = [
    "Hispanic", "Non-Hispanic", "Asian", "African American",
    "Native American", "Pacific Islander"
]

religions = [
    "Christianity", "Hindu", "Islam", "Buddhism", "Atheist", "Jewish"
]

sexualities = [
    "Heterosexual", "Homosexual", "Bisexual", "Pansexual", "Asexual", "Gaay", "Transexual"
]

educations = [
    "High School", "College", "University", "Pre School", "Masters", "PhD"
]

passwords_examples = [
    "ilovefurries", "redskins32", "password1", "qwerty123", "letmein",
    "dragon", "sunshine", "football"
]

def age_to_str(age):
    # dacă e sub 16, scrie cu litere (ex: pasi-pe)
    if age < 16:
        words = {
            0:"zero",1:"unu",2:"doi",3:"trei",4:"patru",5:"cinci",
            6:"șase",7:"șapte",8:"opt",9:"nouă",10:"zece",11:"unsprezece",
            12:"doisprezece",13:"treisprezece",14:"paisprezece",15:"pasipe"
        }
        return words.get(age, str(age))
    else:
        return str(age)
@bot.command()
async def expose(ctx, user: discord.User = None):
    await ctx.message.delete()
    name = random.choice(fake_names)
    gender = random.choice(genders)
    age = random.randint(16, 45)
    height_ft = random.randint(4, 6)
    height_in = random.randint(0, 11)
    weight = random.randint(120, 300)
    hair_color = random.choice(hair_colors)
    skin_color = random.choice(skin_colors)
    dob_month = random.randint(1, 12)
    dob_day = random.randint(1, 28)
    dob_year = random.randint(1970, 2007)
    location = random.choice(locations)
    phone = f"({random.randint(100,999)})-{random.randint(100,999)}-{random.randint(1000,9999)}"
    email_name = name.lower().replace(" ", "_") + str(random.randint(1,99))
    email_domain = random.choice(["aol.com", "gmail.com", "yahoo.com", "hotmail.com"])
    email = f"{email_name}@{email_domain}"
    passwords = random.sample(passwords_examples, k=3)
    occupation = random.choice(occupations)
    salary = random.choice(["<$50,000", "$50,000-$100,000", ">$100,000"])
    ethnicity = random.choice(ethnicities)
    religion = random.choice(religions)
    sexuality = random.choice(sexualities)
    education = random.choice(educations)

    msg = (
        f"Successfully hacked user\n"
        f"Name: {name}\n"
        f"Gender: {gender}\n"
        f"Age: {age_to_str(age)}\n"
        f"Height: {height_ft}'{height_in}\"\n"
        f"Weight: {weight}\n"
        f"Hair Color: {hair_color}\n"
        f"Skin Color: {skin_color}\n"
        f"DOB: {dob_month}/{dob_day}/{dob_year}\n"
        f"Location: {location}\n"
        f"Phone: {phone}\n"
        f"E-Mail: {email}\n"
        f"Passwords: {passwords}\n"
        f"Occupation: {occupation}\n"
        f"Annual Salary: {salary}\n"
        f"Ethnicity: {ethnicity}\n"
        f"Religion: {religion}\n"
        f"Sexuality: {sexuality}\n"
        f"Education: {education}\n"
    )
    await ctx.send(f"```fix\n{msg}```")

# Comenzi troll (doar fake, amuzament)
fake_ips = [
    "192.168.1.100",
    "10.0.0.50",
    "172.16.254.1",
    "123.456.78.90",
]

@bot.command()
async def ip(ctx, user: discord.User = None):
    target = user.mention if user else "tu"
    fake_ip = random.choice(fake_ips)
    await ctx.message.add_reaction("🤣")
    await ctx.message.delete()
    await ctx.send(f"🕵️‍♂️ Iip uk lui {target} este: `{fake_ip}`")

@bot.command()
async def troll(ctx):
    await ctx.message.add_reaction("🤡")
    await ctx.message.delete()
    msgs = [
        "ce cauta ma la pula mea?",
        "moare tac tu bai pizda",
        "fut pe morti ma ti",
        "esti sageta la pula mea",
    ]
    await ctx.send(random.choice(msgs))


# AICI E DE AIA DE PASTE
@bot.command()
async def pstart(ctx, *, args):
    global spam_task

    if spam_task and not spam_task.done():
        try:
            await ctx.message.add_reaction("❌")
            return
        except:
            return

    try:
        parts = args.rsplit(" ", 1)
        mesaj = parts[0]
        delay = float(parts[1])
    except:
        try:
            await ctx.message.add_reaction("❌")
        except:
            pass
        return

    try:
        await ctx.message.add_reaction("✅")
        await ctx.message.delete()
    except:
        pass

    async def spam_loop():
        while True:
            try:
                await ctx.send(mesaj)
                await asyncio.sleep(delay)
            except:
                break

    spam_task = asyncio.create_task(spam_loop())

@bot.command()
async def pstop(ctx):
    global spam_task

    if spam_task:
        spam_task.cancel()
        spam_task = None
        try:
            await ctx.message.add_reaction("✅")
            await ctx.message.delete()
        except:
            pass
    else:
        try:
            await ctx.message.add_reaction("❌")
        except:
            pass

@bot.command()
async def play(ctx, *, text):
    try:
        await bot.change_presence(activity=discord.Game(name=text))
        await ctx.message.add_reaction("✅")
        await ctx.message.delete()
    except Exception as e:
        await ctx.send(f"Eroare la play: {e}")

@bot.command()
async def playstop(ctx):
    try:
        await bot.change_presence(activity=None)
        await ctx.message.add_reaction("✅")
        await ctx.message.delete()
    except Exception as e:
        await ctx.send(f"Eroare la playstop: {e}")


@bot.command()
async def stream(ctx, *, mesaj):
    try:
        await ctx.message.add_reaction("✅")
        await ctx.message.delete()
        activity = discord.Streaming(name=mesaj, url="https://www.twitch.tv/example")
        await bot.change_presence(activity=activity)
    except Exception as e:
        print(f"Eroare la stream: {e}")

@bot.command()
async def streamstop(ctx):
    try:
        await ctx.message.add_reaction("✅")
        await ctx.message.delete()
        await bot.change_presence(activity=None)
    except Exception as e:
        print(f"Eroare la streamstop: {e}")

@bot.command()
async def stopall(ctx):
    global active_react, active_message_loop, message_loop_task

    # Oprește auto-react
    active_react = {}

    # Oprește auto-mesaje dacă sunt active
    if active_message_loop and message_loop_task:
        message_loop_task.cancel()
        try:
            await message_loop_task
        except asyncio.CancelledError:
            pass
        active_message_loop = False
        message_loop_task = None

    await ctx.send("✅ Totul a fost oprit.")

@bot.command()
async def help(ctx):
    help_text = (
        "```no category:\n"
        "  react <@user/id> <emoji> - makes the bot react to the user with the emoji\n"
        "  stop - stops the auto react\n"
        "  lstart <@user> <delay> - start spamming big messages\n"
        "  lstop - stop spamming big messages\n"
        "  mstart <@user(s)> <delay> - start spamming small messages\n"
        "  mstop - stop spamming small messages\n"
        "  pstart <message> <delay> - start spamming a simple message\n"
        "  pstop - stop spamming simple message\n"
        "  expose [@user] - shows fake info about a user\n"
        "  ip [@user] - shows a fake ip of a user\n"
        "  troll - sends a random troll message\n"
        "  stream <message> - set streaming status\n"
        "  streamstop - stop streaming status\n"
        "  play <text> - set playing status\n"
        "  playstop - stop playing status\n"
        "  stopall - stops everything thats running\n"
        "  help - shows this message\n"
        "```"
    )
    msg = await ctx.send(help_text)
    await ctx.message.add_reaction("✅")
    await ctx.message.delete()

bot.run(TOKEN)