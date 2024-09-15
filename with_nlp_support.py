import discord
import os
import whisper
import warnings
import Discord

# Suppress specific warnings
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

# Load the Whisper model
model = whisper.load_model("tiny")

TOKEN = 'token here'
SAVE_DIRECTORY = r'C:\Users\Administrator\Desktop\Hackathon Project\DiscordImages'
warning_message = 'Please don\'t send audio files.'

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
                {'role': 'system', 'content': 'You are a Discord Bot called ContentCop and you were created by a group of people called hacksaw.'}
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
                
                # Handle image attachment
                if attachment.filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
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
                        user_name = message.author.name
                        user_message = {'role': 'user', 'content': 'Give a short description', 'images': [file_path]}
                        ai_response = {'role': 'assistant', 'content': ai_response}
                        self.conversations[user_name].append(user_message)
                        self.conversations[user_name].append(ai_response)

                # Handle audio attachment
                elif attachment.filename.endswith('.ogg' or '.mp3'):
                    await attachment.save(file_path)
                    print(f'Saved audio: {file_path}')

                    #convert audio to text
                    result = model.transcribe(file_path)
                    print(result['text'])
                    audio_text = result['text']

                    
                    user_message = {'role': 'user', 'content': audio_text}
                    self.conversations[user_name].append(user_message) 

                    # Retrieve conversation history
                    conversation_history = self.conversations[user_name]
                    response = Discord.describe_text(conversation_history)

                    # Append AI response
                    ai_response = {'role': 'assistant', 'content': response}
                    self.conversations[user_name].append(ai_response)

                    await message.channel.send(response)
                

client = MyClient()
client.run(TOKEN)
