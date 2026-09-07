import pyttsx3

# Create Text-to-Speech engine
engine = pyttsx3.init()

# Set speech speed and volume
engine.setProperty("rate", 150)
engine.setProperty("volume", 1.0)

# Display project title
print("=" * 50)
print("       TEXT-TO-SPEECH CONVERTER")
print("             USING PYTHON")
print("=" * 50)

# Main program loop
while True:

    # Take text input from the user
    text = input("\nEnter text to convert into speech: ")

    # Check if the user entered empty text
    if text.strip() == "":
        print("Please enter some text.")
        continue

    # Convert text into speech
    engine.say(text)
    engine.runAndWait()

    print("Speech conversion completed successfully!")

    # Ask user whether to continue
    choice = input("\nDo you want to convert another text? (y/n): ")

    if choice.lower() != "y":
        print("\nThank you for using Text-to-Speech Converter!")
        break
