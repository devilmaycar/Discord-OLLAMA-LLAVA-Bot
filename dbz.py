import discord
import os
import Discord

TOKEN = 'MTI4MTU4MzU2MjAyNTU5OTEwOA.GEUX8h.8UpdsKO0X5aX3KoxoZQ_GB2E4H0sRuZAVyV10Q'
SAVE_DIRECTORY = r'C:\Users\Administrator\Desktop\Hackathon Project\DiscordImages'
warning_message = 'Please don\'t send pictures like that'

class MyClient(discord.Client):
    def __init__(self, **options):
        intents = discord.Intents.default()
        intents.messages = True
        intents.message_content = True
        intents.reactions = True  # Enable reactions to track replies
        super().__init__(intents=intents, **options)
        self.conversations = {}

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return

        # Initialize conversation history for the user if not already present
        user_name = message.author.name
        if user_name not in self.conversations:
            self.conversations[user_name] = [
                {'role': 'system', 'content': 'You are Dio Brando from Jojo’s Bizarre Adventures, and you keep talking like him always.'}
            ]

        # Handle mentions
        if self.user.mentioned_in(message):
            user_message = {'role': 'user', 'content': message.content}
            self.conversations[user_name].append(user_message)

            # Retrieve conversation history
            conversation_history = self.conversations[user_name]
            response = Discord.describe_text(conversation_history)

            # Append AI response
            ai_response = {'role': 'assistant', 'content': response}
            self.conversations[user_name].append(ai_response)

            await message.channel.send(response)

        # Handle image attachments
        elif message.channel.name == 'general' and message.attachments:
            for attachment in message.attachments:
                file_path = os.path.join(SAVE_DIRECTORY, attachment.filename)
                await attachment.save(file_path)
                print(f'Saved image: {file_path}')

                # Describe image 
                ai_response = Discord.describe_image(file_path)

                # Delete the message if it contains specific keywords
                if any(keyword in ai_response.lower() for keyword in ["dog", "puppy", "dogs", "puppies"]):
                    await message.delete()
                    await message.channel.send(warning_message)
                    print(f'Deleted message with image: {file_path}')
                else:
                    await message.channel.send(ai_response)

                    # Update conversation history with the image description
                    user_message = {'role': 'user', 'content': 'Give a short description', 'images': [file_path]}
                    ai_response = {'role': 'assistant', 'content': ai_response}
                    self.conversations[user_name].append(user_message)
                    self.conversations[user_name].append(ai_response)

client = MyClient()
client.run(TOKEN)

2m1KAxKX4Ia3j2Ar61MFVMEfAZg_57CG2SuxGu5PZquLx2nLK