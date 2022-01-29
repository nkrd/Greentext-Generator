import openai, os, discord

client = discord.Client()
openai.api_key = os.environ.get('OPENAI_API_KEY')
ft_model = "curie:ft-personal-2022-01-25-20-15-32"

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.lower().startswith('anon'):
        async with message.channel.typing():
            endloop = False
            while not endloop:
                try:
                    response = openai.Completion.create(model=ft_model, prompt=message.content + " -> ", max_tokens=100, temperature=0.7, stop="END")
                    final = "\n".join(response.choices[0].text.lstrip(" ").split("\n")[:-1]).replace(".", "")
                    if final.count("\n") > 2:
                        endloop = True
                        await message.channel.send(final)
                except Exception as e:
                    await message.channel.send("Error")
                    print(e)

client.run(os.environ.get('DISCORD_TOKEN'))