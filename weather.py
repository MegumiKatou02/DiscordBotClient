import discord
import requests
import config

API_KEY = config.API_KEY_OPEN_WEATHER_MAP
BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"

async def weather_command(interaction: discord.Interaction, city_name: str):
    url = f"{BASE_URL}q={city_name}&appid={API_KEY}&units=metric&lang=vi"

    response = requests.get(url)
    data = response.json()
    # print(data)

    if data["cod"] != 200:
        await interaction.response.send_message(f"Không thể lấy thông tin thời tiết cho thành phố: {city_name}.", ephemeral=True)
        return

    main = data['main']
    weather = data['weather'][0]
    wind = data['wind']
    
    city = data['name']
    country = data['sys']['country']
    temperature = main['temp']
    weather_description = weather['description']
    humidity = main['humidity']
    pressure = main['pressure']
    wind_speed = wind['speed']
    
    embed = discord.Embed(
        title=f"Thông tin thời tiết tại {city}, {country}",
        description=f"{weather_description.capitalize()}",
        color=discord.Color.blue()
    )
    embed.add_field(name="Nhiệt độ", value=f"{temperature}°C", inline=False)
    embed.add_field(name="Độ ẩm", value=f"{humidity}%", inline=False)
    embed.add_field(name="Áp suất", value=f"{pressure} hPa", inline=False)
    embed.add_field(name="Tốc độ gió", value=f"{wind_speed} m/s", inline=False)

    await interaction.response.send_message(embed=embed)