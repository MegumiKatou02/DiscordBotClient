# music.py
import yt_dlp
import discord

async def play_music(ctx, url):
    # Kiểm tra xem bot đã vào kênh voice chưa, nếu chưa thì vào
    if not ctx.voice_client:
        await ctx.invoke(join)

    # Cấu hình yt-dlp để tải âm thanh từ YouTube
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegAudioConvertor',  # Sửa lại ở đây
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'ffmpeg_location': 'D:\\py\\ffmpeg-master-latest-win64-gpl\\bin\\ffmpeg.exe',  # Đảm bảo đường dẫn đúng
        'outtmpl': 'downloads/%(id)s.%(ext)s',
    }


    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['formats'][0]['url']
        voice = ctx.voice_client
        voice.play(discord.FFmpegPCMAudio(url2), after=lambda e: print('done', e))

async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You need to join a voice channel first!")

async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

async def pause(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.pause()

async def resume(ctx):
    if ctx.voice_client.is_paused():
        ctx.voice_client.resume()

async def stop(ctx):
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()