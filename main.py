from email import message
from bot_init import Bot
from pyrogram import filters
from pyrogram.types import Message
from os import listdir
from os.path import join
from shutil import rmtree
from Notion import Logs, Usuario
from datetime import datetime
import instaloader


bot = Bot()
app = bot.app

def descargar_reel(url, msg: Message = None):
    try:
        sms = msg.reply("**⬇️ DESCARGANDO VIDEO...**")
        L = instaloader.Instaloader()
        reel_code = url.split("/reel/")[1].split("/")[0]
        post = instaloader.Post.from_shortcode(L.context, reel_code)
        id = post.mediaid
        caption = post.caption
        L.download_post(post, target=id)
        video = join(str(id), [vid for vid in listdir(str(id)) if vid.endswith('mp4')][0])
        thumb = join(str(id), [vid for vid in listdir(str(id)) if vid.endswith('jpg')][0])
        sms.edit_text("**⬆️ SUBIENDO VIDEO...**")
        msg.reply_video(video=video, caption=caption, thumb=thumb, quote=True)
        sms.delete()
        rmtree(str(id))
    except Exception as e:
        msg.reply(f"ERROR: {e}")


def exist_user(id:int):
    data = Usuario().fetch_data()
    if str(id) in data.text:
        return True
    else:
        return False
    
    

@app.on_message(filters.command("start"))
def saludar(app, msg:Message):
    text = f"""**
¡Hola! {msg.from_user.first_name} 🌟 Bienvenido a InstaTG. Aquí puedes descargar reels de Instagram de manera rápida y sencilla. 🎥✨
Solo envía el enlace del reel que deseas descargar y listo 🚀. ¡Que disfrutes tus videos favoritos! 🎉
Si necesitas ayuda, no dudes en preguntar al creador __@MandiCoder__.**"""
    msg.reply(text)
    
    if not exist_user(msg.from_user.id):
        Usuario().send_data(
            id=msg.from_user.id,
            username=msg.from_user.username,
            first_name=msg.from_user.first_name,
        )

@app.on_message(filters.regex("http"))
def download_video(app, msg:Message):
    if not exist_user(msg.from_user.id):
        Usuario().send_data(
            id=msg.from_user.id,
            username=msg.from_user.username,
            first_name=msg.from_user.first_name,
        )
    url = msg.text
    Logs().send_data(username=msg.from_user.username, url=url)
    descargar_reel(url, msg)


# descargar_reel("https://www.instagram.com/reel/DEY0zEnNWnU/?igsh=MXVxOW5renBpb256eg==")
bot.run()