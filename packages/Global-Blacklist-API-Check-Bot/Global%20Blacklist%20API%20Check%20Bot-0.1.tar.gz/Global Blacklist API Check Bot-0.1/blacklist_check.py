import os
import urllib.request
from discord.ext.commands import Bot

bot = Bot(description='Blacklist Checker', command_prefix='?')

@bot.command()
async def blacklist_check(user):
    """Queries blacklist status of user using @themarkymark's Blacklist API."""
    contents = urllib.request.urlopen("http://blacklist.usesteem.com/user/"+user).read()
    bl = (str(contents).split('"blacklisted":[')[1]).split(']')[0]
    if bl == '':
        await bot.say('@'+user+' is not on any blacklist tracked via the API')
        return
    else:
        blacklists = []
        bl = bl.split(',')
        for b in bl:
            blacklists.append(b.replace('"',''))
        await bot.say('@'+user+' is on the following blacklists: ')
        for b in blacklists:
            await bot.say(b)

def main():
    bot.run(os.getenv('TOKEN'))

if __name__ == '__main__':
    main()