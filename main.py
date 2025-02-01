from bot_init import Bot
from pyrogram import filters
from pyrogram.types import Message
from os import listdir
from os.path import join
from shutil import rmtree
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



@app.on_message(filters.command("start"))
def saludar(app, msg:Message):
    msg.reply(f"**Hola {msg.from_user.first_name} 😊**\n\n__Este bot ha sido creado por @MandiCoder__")
    

@app.on_message(filters.regex("http"))
def download_video(app, msg:Message):
    url = msg.text
    descargar_reel(url, msg)


# descargar_reel("https://www.instagram.com/reel/DEY0zEnNWnU/?igsh=MXVxOW5renBpb256eg==")
bot.run()