import tkinter as tk
import openai
import re
import webbrowser

# Set up the OpenAI API client
openai.api_key = "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"

# Define the search engine model ID
model_id = "text-davinci-002"

# Set the maximum token length for the prompt
max_prompt_length = 2000

# Set the maximum token length for the completion
max_completion_length = 50

def search_engine():
    # Get the user's query input and clean it by removing special characters and excess whitespace
    query = prompt_entry.get()
    cleaned_query = re.sub('[^a-zA-Z0-9 \n\.]', '', query).strip()

    # Split the query into chunks of max_prompt_length tokens or less
    chunks = [cleaned_query[i:i+max_prompt_length] for i in range(0, len(cleaned_query), max_prompt_length)]

    # Define an empty list to store the results
    results = []

    # Loop through each chunk of the query and generate a completion
    for chunk in chunks:
        prompt = f"Search the web for information on the following topic:\n{chunk}\n\nResults:\n"
        response = openai.Completion.create(
            engine=model_id,
            prompt=prompt,
            max_tokens=max_completion_length,
            n=1,
            stop=None,
            temperature=0.5,
        )

        # Extract the text of the completion from the API response
        completion_text = response.choices[0].text.strip()

        # Add the completion text to the results list
        results.append(completion_text)

    # Concatenate the results into a single string and display it in the label
    results_label.config(text="\n".join(results), wraplength=500)

    # Make links clickable
    results_label.bind("<Button-1>", lambda event: webbrowser.open_new(event.widget.cget("text")))

# Create the GUI
root = tk.Tk()
root.title("Search Engine")
root.config(bg="#2c2c2c")

# Set the GUI to start in full-screen mode
root.attributes('-fullscreen', True)

# Set the GUI zoom level to 150%
root.tk.call('tk', 'scaling', 1.5)

# Create the prompt entry widget
prompt_entry = tk.Entry(root, width=50, bg="#444444")
prompt_entry.pack(padx=10, pady=10)

# Create the search button widget
search_button = tk.Button(root, text="Search", command=search_engine, bg="#3f3f3f", fg="#ffffff", activebackground="#4f4f4f", activeforeground="#ffffff")
search_button.pack(padx=10, pady=5)

# Create the quit button widget
quit_button = tk.Button(root, text="Quit", command=root.quit, bg="#3f3f3f", fg="#ffffff", activebackground="#4f4f4f", activeforeground="#ffffff")
quit_button.pack(padx=10, pady=5)

# Create the results label widget
results_label = tk.Label(root, wraplength=500, bg="#2c2c2c", fg="#ffffff", cursor="hand2")
results_label.pack(padx=10, pady=10)

# Start the GUI
root.mainloop()

