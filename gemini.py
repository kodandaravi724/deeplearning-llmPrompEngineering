import os
import PIL
import google.generativeai as genai
import google.ai.generativelanguage as glm
import time

# do not reveal your api key when submitting the assignment
GOOGLE_API_KEY = "AIzaSyDSrs_QCfYIwV_JpJE0duppfCOALai96Sw"
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
    for i in range(len(data)):
        k = data[i]['menu']
        for j in range(len(k)):
            msg = ""
            dish_name = k[j]['dish']
            ingredients = k[j]['ingredients']
            msg = msg + f'Dish Name:- {dish_name}\n'
            msg = msg + f'Ingredients:- {ingredients}\n'
            print(msg)
            model = genai.GenerativeModel(model_name='gemini-1.0-pro-latest')
            chat = model.start_chat(history=[])
            instructions = chat.send_message(prompt+"\n"+msg)
            instructions_list = instructions.text.split('\n')
            print(instructions.text)
            chat.send_message("From now I will pas each instruction. Generate the task tree following the JSON format I specified. Strictly send task tree as response. No other information.")
            counter = 0
            for instruction_index in range(len(instructions_list)):
                if(counter%10==0): #call sleep on current thread to not make it a bottleneck for API calls.
                    time.sleep(5)
                if (len(instructions_list[instruction_index]) != 0):
                    if (instruction_index == len(instructions_list) - 1):
                        instruction = "lastInstruction: " + "dish: " + dish_name + " " + instructions_list[instruction_index]
                    else:
                        instruction = "Instruction: "+instructions_list[instruction_index]
                    response = chat.send_message(instruction)
                    counter+=1
                    print(response.text)

if __name__ == "__main__":
    prompt = read_file_as_string("prompt.txt")
    prompt = prompt + "\n"
    import json
    f = open('input_hub.json')
    data = json.load(f)
    sendInstructions(data, prompt)
    # for i in range(len(data)):
    #     k = data[i]['menu']
    #     for j in range(len(k)):
    #         r = ""
    #         t = prompt
    #         model = genai.GenerativeModel(model_name='gemini-1.0-pro-latest')
    #         dish_name = k[j]['dish']
    #         ingredients = k[j]['ingredients']
    #         r = r + f'Dish Name:- {dish_name}\n'
    #         print(f'Dish Name:- {dish_name}\n')
    #         r = r + f'Ingredients:- {ingredients}\n'
    #         t = t+r
    #         print(ingredients)
    #         t += "First generate instructions to prepare dish and then prepare final task tree to prepare dish based on instructions."
    #         k1 = dish_name.replace(' ', '_')
    #         file_path = f'{k1}1.json'
    #         response = model.generate_content(t)
    #         print(response.text)


    f.close()
