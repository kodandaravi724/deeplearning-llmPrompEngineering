import os
import PIL
import google.generativeai as genai
import google.ai.generativelanguage as glm
import time

# do not reveal your api key when submitting the assignment
GOOGLE_API_KEY = "AIzaSyAP5sFy5JlqbNR-MqQ2hiMk2CaDS4UjWks"
genai.configure(api_key=GOOGLE_API_KEY)


def list_genai_models():
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)


def read_file_as_string(filename):
    with open(filename, "r") as f:
        content = f.read()
    return content


def detect_object(model, filepath):
    img = PIL.Image.open(filepath)
    prompt = "list objects in the image in this way: 1. ing 2. ing 3. ing etc"
    response = model.generate_content([prompt, img])
    print(response.text)


def sendInstructions(data, prompt):
    l = []
    for i in range(len(data)):
        k = data[i]['menu']
        for j in range(len(k)):
            msg = ""
            dish_name = k[j]['dish']
            ingredients = k[j]['ingredients']
            tree = []
            msg = msg + f'Dish Name:- {dish_name}\n'
            msg = msg + f'Ingredients:- {ingredients}\n'
            print(msg)
            model = genai.GenerativeModel(model_name='gemini-1.0-pro-latest')
            chat = model.start_chat(history=[])
            instructions = chat.send_message(prompt+"\n"+msg)
            print(instructions)
            temp = instructions.text.split("\n")
            for jj in temp:
              if(len(jj)>0):
                 l.append(jj)
    l = list(map(lambda x:x.lower(), l))
    l = list(set(l))

    with open('kitchen.txt', 'w') as f:
      for elem in l:
        f.write(elem+"\n")



if __name__ == "__main__":
    prompt = read_file_as_string("prompt.txt")
    prompt = prompt + "\n"
    import json
    f = open('inputhub.json')
    data = json.load(f)
    sendInstructions(data, prompt)

    f.close()