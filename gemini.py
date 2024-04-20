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
    with open("kitchen.txt", "r") as file:
        lines = file.readlines()

    kitchen_list = [line.strip() for line in lines]

    for i in range(len(data)):
        k = data[i]['menu']
        for j in range(len(k)):
            time.sleep(60)
            msg = ""
            dish_name = k[j]['dish']
            ingredients = k[j]['ingredients']
            tree = []
            msg = msg + f'Dish Name:- {dish_name}\n'
            msg = msg + f'Ingredients:- {ingredients}\n'
            print(msg)
            model = genai.GenerativeModel(model_name='gemini-1.0-pro-latest')
            chat = model.start_chat(history=[])
            while(True):
                try:
                    errMsg = f"kitchen_items: {','.join(kitchen_list)}. Use these items when generating instructions and task tree. If it is not possible to prepare dish with avaialable items in kitchen then give response Dish can\'t be prepared with available items."
                    instructions = chat.send_message(prompt+"\n"+msg+"\n Strictly Give only instructions as response each seperated in new line.\n"+errMsg)
                    print(instructions.text)
                    instructions_list = instructions.text.split('\n')
                    print(instructions.text)
                    chat.send_message("From now I will pas each instruction. Generate the task tree following the JSON format I specified. Strictly send only task tree as json response. No other information.")
                    break
                except Exception as e:
                    print("Got an exception. Retrying the request.")
                    time.sleep(60)
                    pass
            counter = 0
            for instruction_index in range(len(instructions_list)):
                if(counter%10==0): #call sleep on current thread to not make it a bottleneck for API calls.
                    time.sleep(60)
                if (len(instructions_list[instruction_index]) != 0):
                    if (instruction_index == len(instructions_list) - 1):
                        instruction = "lastInstruction: " + "dish: " + dish_name + " " + instructions_list[instruction_index]
                    else:
                        instruction = "Instruction: "+instructions_list[instruction_index]
                    print(instruction+" <-- instruction")
                    retry_count = 0
                    while(retry_count<10):
                        try:
                            response = chat.send_message(instruction)
                            break
                        except Exception as e:
                            print("exception retyring!!")
                            print(e)
                            retry_count+=1
                            time.sleep(60)
                            print(retry_count)
                    counter+=1
                    data1 = response.text
                    try:
                        sIndex = data1.index('[')
                        pIndex = data1.index('{')
                        jsonData = ""
                        if(sIndex!=-1 and (sIndex<pIndex)):
                            jsonData = data1[sIndex: data1.rfind(']')+1]
                        else:
                            jsonData = data1[data1.index('{'): data1.rfind('}')+1]
                        print(type(json.loads(jsonData)))
                        if isinstance(json.loads(jsonData), dict):
                            tree.append(json.loads(jsonData))
                        else:
                            tree.extend(json.loads(jsonData))
                    except Exception as e:
                        print(e)
                        print(jsonData)
                        print(data1)
            file_path = f"{dish_name.replace(' ', '_')}.json"

            # Write JSON list to a JSON file
            with open("tasktree/"+file_path, "w") as json_file:
                json.dump(tree, json_file, indent=4)

if __name__ == "__main__":
    prompt = read_file_as_string("prompt.txt")
    prompt = prompt + "\n"
    import json
    f = open('inputhub.json')
    data = json.load(f)
    sendInstructions(data, prompt)
    f.close()
