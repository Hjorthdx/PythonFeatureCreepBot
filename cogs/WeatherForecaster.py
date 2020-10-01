import discord, requests
from discord.ext import commands

# To do
    # Weather by:
        # City name
        # Geographic coordinates
        # zip code

    # Specify time:
        # .weather aalborg should return the 5 days with an icon of the day avg I guess? Then Highest and lowest temp? Idk google how they normally do these things.
        # .weather aalborg now, the weather now with more info.
        # .weather aalborg 3 pm, the weather at 15
        # .weather tomorrow, can you somehow squeeze in all the information of one day? Small inline slices with all the different times? Idk figure it out.
            # Perhabs only do 3 days cause its easier to fit? Idk time will tell.
    
    # Some smart way of determining what time the user specified without having to type exact date and time with correct seperators.
        # I.e. .weather Aalborg 2020-09-29 00:00:00 should be avoided at almost all cause
            # Perhabs an enum with the different times and a name for them. I.e. Noon = 12:00:00, midnight = 00:00:00 etc.
            # The same for the date = today = this date, tomorrow = today + 8 time intervals etc.

class WeatherForecaster(commands.Cog):
    # Some documentation

    def __init__(self, bot):
        self.bot = bot
        self.apikey = "9ca0f27430d11f09efb68e4083ccc13e"
        self.baseUrl = "http://api.openweathermap.org/data/2.5/forecast?" # Full url example api.openweathermap.org/data/2.5/forecast?q={city name}&appid={API key}

    @commands.Cog.listener()
    async def on_ready(self):
        print("WeatherForecaster cog is loaded")

    @commands.command()
    async def weather(self, ctx, *, city:str):
        UnitOfMeasurement = "metric" # standard = kelvin, metric = celsius, imperial = Fahrenheit
        url = f"{self.baseUrl}q={city}&units={UnitOfMeasurement}&appid={self.apikey}"
        r = requests.get(url).json()
        e = r['list']
        time = e[0]['dt_txt']
        x = e[0]['main']
        temp = x['temp']
        feelsLike = x['feels_like']
        y = e[0]['clouds']
        clouds = y['all']
        z = e[0]['wind']
        windSpeed = z['speed']
        a = e[0]['weather']
        description = a[0]['description']
        x = 1
        
        embed = discord.Embed(title=f"Weather in {city}", inline=False)
        embed.add_field(name="Description", value=f"{description}", inline=False)
        embed.add_field(name="Temperature(C)", value=f"{temp}", inline=False)
        embed.add_field(name="Feels like", value=f"{feelsLike}", inline=False)
        embed.add_field(name="Wind speed", value=f"{windSpeed}", inline=False)
        embed.add_field(name="Clouds", value=f"{clouds}", inline=False)
        embed.add_field(name="Time", value=f"{time}", inline=False)
        await ctx.send(embed=embed, delete_after=30)
        await ctx.message.delete()
            


def setup(bot):
    bot.add_cog(WeatherForecaster(bot))

