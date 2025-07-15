import sys
import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
from Model import PichuModel
from Automation import PichuAI, play_music, play_specific_song, list_songs, search_google, search_wiki, search_youtube, search_chatgpt

# --- TTS Setup ---
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"==> Master : {query}")
        return query
    except Exception:
        return input("Type your command: ")
# --- Main Query Handler ---
API_KEY = "AIzaSyBvTHlUDojbUvr3V-cuRkFHgyUkrKvgU4E"
pichu_model = PichuModel(api_key=API_KEY)
automation = PichuAI(api_key=API_KEY)

def handle_query(query):
    query = query.lower().strip()
    
   
    # --------- Autiomation Queries ----------
    if "time" in query:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}."
    elif "date" in query:
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        return f"Today's date is {current_date}."
    elif "open google" in query:
        webbrowser.open("https://google.com")
        return "Opening Google."
    elif query.startswith("search for") or query.startswith("google"):
        return automation.search_google(query)
    elif "open youtube" in query or query.startswith("search on youtube") or query.startswith("youtube"):
        return automation.search_youtube(query)
    elif "on chat gpt" in query or "search on chatgpt" in query:
        return automation.search_chatgpt(query)
    elif "wikipedia" in query or "search on wikipedia" in query:
        return automation.search_wiki(query)
    elif "weather" in query:
        city = automation._extract_city(query) or "Bilaspur"
        return automation.get_weather(city)
    
    elif " image" in query or "text from image" in query or "image recognition" in query:
        from image import analyze_image_text_and_faces
        result = model.analyze_image_text_and_faces()
        return result
    
    # ----------- History for gemini response -----------
    elif "give me past conversation" in query or "give me history" in query or "show me past conversation" in query:
        history = automation.get_history()
        if not history:
            return "No conversation history found."
        formatted = []
        for idx, item in enumerate(history, 1):
            role = item.get("role", "user")
            content = item.get("content", "")
            formatted.append(f"{idx}. {role.capitalize()}: {content}")
        return "\n".join(formatted)
    

    # --- Intent matching from Model.py ---
    response = pichu_model.get_intent_response(query)
    if response:
        automation.conversation_history.append({"role": "user", "content": query})
        automation.conversation_history.append({"role": "assistant", "content": response})
        return response

    # --- Fallback: Gemini API ---
    automation.conversation_history.append({"role": "user", "content": query})
    response = pichu_model.handle_ai_query(query)
    automation.conversation_history.append({"role": "assistant", "content": response})
    return response

# --- CLI Entry Point ---
def main_cli():
     while True:
       query = input("You: ")
       if query.lower() in ["quit", "exit"]:
           print("Goodbye!")
           break
       response = handle_query(query)
       print(f"Pichu: {response}")


if __name__ == "__main__":
        main_cli()
