from ollama import Client

client = Client(host='https://94f8-34-16-210-209.ngrok-free.app/')

def describe_text(conversation_history):
    try:
        response = client.chat(
            model='llava',
            messages=conversation_history
        )
        return response['message']['content']
    except Exception as e:
        print(f"Error describing text: {e}")
        return None

def describe_image(image_path):
    try:
        response = client.chat(
            model='llava',
            messages=[
                {'role': 'user', 'content': 'Give a short description', 'images': [image_path]}
            ]
        )
        description = response['message']['content']
        return description
    except Exception as e:
        print(f"Error describing image: {e}")
        return None
