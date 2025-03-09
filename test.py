import google.generativeai as genai

genai.configure(api_key="AIzaSyC10gnIogn1voJf0TqVInQzfKnYJdON76A")

models = genai.list_models()
for model in models:
    print(model.name)