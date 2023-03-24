import openai
from flask import Flask, render_template, request, Markup


app = Flask(__name__)
openai.api_key = "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"


@app.route("/", methods=("GET", "POST"))
def get_story():
    if request.method == "POST":
        prompt = request.form["prompt"]
        genre = request.form["genre"]
        title, story = generate_story(prompt, genre)
        return render_template("index.html", title=title, story=story)
    else:
        return render_template("index.html", title=None, story=None)
        

def generate_story(prompt, genre):
    
    # Set up the parameters for generating the story
    model = "text-davinci-003"
    
    # Add genre to the prompt
    prompt_with_genre = f"Generate an exciting story with a title and proper English grammar and punctuations on the topic of {prompt} and based on the genre of {genre},"
    
    
    # Generate the title
    title_response = openai.Completion.create(
        engine=model,
        prompt=prompt_with_genre,
        temperature=0.5,
        max_tokens=8,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    
    # Get the generated title
    title = title_response.choices[0].text.strip()
    
    # Add title to the prompt
    prompt_with_title = f"{prompt_with_genre} {title}."
    
    # Generate the story
    story_response = openai.Completion.create(
        engine=model,
        prompt=prompt_with_title,
        temperature=0.5,
        max_tokens=2500,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )

    # Get the generated story
    initial_story = story_response.choices[0].text.strip()
    
    
    # Add appropriate paragraphs
    paragraph_length = 5  # Average sentence length for a paragraph
    sentences = initial_story.split('.')
    num_sentences = len(sentences)
    num_paragraphs = int(num_sentences / paragraph_length)
    paragraphs = []
    story = ''
    for i in range(num_paragraphs):
        start_idx = i * paragraph_length
        end_idx = min((i+1) * paragraph_length, num_sentences)
        paragraph = ".".join(sentences[start_idx:end_idx]) + "."
        paragraphs.append(paragraph)

    
   
    story = Markup("<br>".join(paragraphs))

    return  title, story
