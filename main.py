import requests
from bs4 import BeautifulSoup
import os
from discord.ext import commands
import asyncio
from keep_alive import keep_alive

bot = commands.Bot(command_prefix='.')

BC = "British Columbia"
AB = "Alberta"

urls=['https://www.memoryexpress.com/Products/MX00118106', 'https://www.memoryexpress.com/Products/MX00117777', 'https://www.memoryexpress.com/Products/MX00117359', 'https://www.memoryexpress.com/Products/MX00118106', 'https://www.memoryexpress.com/Products/MX00118106', 'https://www.memoryexpress.com/Products/MX00118618','https://www.memoryexpress.com/Products/MX00119055','https://www.memoryexpress.com/Products/MX00118518', 'https://www.memoryexpress.com/Products/MX00118130', 'https://www.memoryexpress.com/Products/MX00118076', 'https://www.memoryexpress.com/Products/MX00119891', 'https://www.memoryexpress.com/Products/MX00119892', 'https://www.memoryexpress.com/Products/MX00118036', 'https://www.memoryexpress.com/Products/MX00118345', 'https://www.memoryexpress.com/Products/MX00118341', 'https://www.memoryexpress.com/Products/MX00117360', 'https://www.memoryexpress.com/Products/MX00118542']

#scrape and format the results
def get_stock(region):
  results = ''
  for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    results += (url + ' ')
    li = soup.find('li', attrs={"data-region-name":region}).select('div.c-capr-inventory-store')
    for store in li:
        str = store.get_text(" ",strip=True)
        results +=str
    results+="\n"
  results = results.replace('( Store Info )', '').replace('Out of Stock' , 'OOS')
  if (region == "Alberta"):
      results = results.replace('Calgary', 'yyz').replace('Edmonton', 'yeg')
  return results

@bot.event
async def on_ready():
  print('logged in as {0.user}'.format(bot))


@bot.command()
async def memex(ctx, *arg1):
  if "ab" in arg1:
    prov = AB
  else: prov = BC
  await ctx.send('Checking stock for ' + prov + "...")
  #pretend the bot is typing
  async with ctx.typing():
    body = get_stock(prov)
    await asyncio.sleep(10)
  await ctx.send(body)
  
keep_alive()
bot.run(os.environ['DISCORD_API_KEY'])


