from os import listdir


async def setup(bot):
    
    for command in filter(lambda x: not x.startswith("__"), listdir(__path__[0])):
        await bot.load_extension("commands." + command.replace(".py", ""))
