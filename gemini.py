import os
import PIL
import google.generativeai as genai
import google.ai.generativelanguage as glm

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


def sendInstructions(model, data):
    t = ""
    k = data[i]['menu']
    for j in range(len(k)):
        dish_name = k[j]['dish']
        ingredients = k[j]['ingredients']
        t = t + f'Dish Name:- {dish_name}\n'
        # print(f'Dish Name:- {dish_name}\n')
        t = t + f'Ingredients:- {ingredients}\n'
        # print(f'Ingredients:- {ingredients}\n')
        t = t + 'Prepare the above dish using given ingredients. Give me steps on how to prepare\n'
        t = t + "Give me only instructions as ouput. I need to parse the instructions and send to other program.\n"
        t = t + "give me only instructions not heading and all."
        t = t + "Give each instruction seperated by new line."
        chat = model.start_chat(history=[])
        ins = chat.send_message(t)
        print(ins.text)
        msg = "Using the intructions generated in previous message give me the task tree to prepare the dish in the format I will train you below."
        response = chat.send_message(msg)
        response = chat.send_message(prompt)
        response = chat.send_message(
            "After trainign with the above mesage I will give you instruction by instreuction give me tasl tree in json format as above.")
        l = ins.text.split('\n')
        print(ins.text)
        d = []
        s = ""
        for instr in range(len(l)):
            if (len(l[instr]) != 0):
                if (instr == len(l) - 1):
                    s = "last: " + "dish: " + dish_name + " " + l[instr]
                    r1 = chat.send_message(s)
                else:
                    s = l[instr]
                r1 = chat.send_message(s)
                res = r1.text
                print(res)
                if '```json' in res:
                    index = res.find('```json')
                    endIndex = res.find('```', index + 8)
                    final = res[index + 8:endIndex]
                    while ((final.strip('\n')[-1] != ']')):
                        print('response is not full. Resensding the request')
                        request_msg = 'I didnt got the full response for this in previous request. Make sure the generated json is valid and give me shorter response if possible.\n' \
                                      'Give me structure of json in format ```json message ```. Follow this strictly. and only generate task tree do give instruction in response. only task tree.'
                        s = s + '\n' + request_msg
                        r1 = chat.send_message(s)
                        res = r1.text
                        index = res.find('```json')
                        endIndex = res.find('```', index + 8)
                        final = res[index + 8:endIndex]
                    if (len(d) == 0):
                        d = json.loads(final)
                    else:
                        print(final)
                        d.append(json.loads(final))
                    print(len(d), endIndex)
                else:
                    print('Except:--')
                    print(res)
        k1 = dish_name.replace(' ', '_')
        file_path = f'{k1}1.json'
        with open(file_path, 'w') as f:
            json.dump(d, f, indent=4)


if __name__ == "__main__":
    # list_genai_models()
    objectNode = glm.Schema(
        type=glm.Type.OBJECT,
        properties={
            'label': glm.Schema(type=glm.Type.STRING),
            'states': glm.Schema(type=glm.Type.ARRAY, items=glm.Schema(type=glm.Type.STRING)),
            'ingredients': glm.Schema(type=glm.Type.ARRAY, items=glm.Schema(type=glm.Type.STRING)),
            'container': glm.Schema(type=glm.Type.STRING)
        },
        required=['label', 'states', 'ingredients', 'container']
    )

    foon = glm.Schema(
        type=glm.Type.OBJECT,
        properties={
            'input_nodes': glm.Schema(type=glm.Type.ARRAY, items=objectNode),
            'motion_node': glm.Schema(type=glm.Type.STRING),
            'output_nodes': glm.Schema(type=glm.Type.ARRAY, items=objectNode)
        },
        required=['input_nodes', 'motion_node', 'output_nodes']
    )

    taskTree = glm.Schema(
        type=glm.Type.OBJECT,
        properties={
            'task_tree': glm.Schema(type=glm.Type.ARRAY, items=foon)
        },
        required=['task_tree']
    )
    finalTaskTree = glm.FunctionDeclaration(
        name="add_to_database",
        description="Builds the task tree for dish",
        parameters= glm.Schema(type=glm.Type.ARRAY, items=foon)
    )
    prompt = read_file_as_string("prompt.txt")
    prompt = prompt + "\n"
    import json
    # Opening JSON file
    f = open('input_hub.json')
    # returns JSON object as
    # a dictionary
    data = json.load(f)

    for i in range(len(data)):
        k = data[i]['menu']
        for j in range(len(k)):
            r = ""
            t = prompt
            model = genai.GenerativeModel(model_name='gemini-1.0-pro-latest')
            dish_name = k[j]['dish']
            ingredients = k[j]['ingredients']
            r = r + f'Dish Name:- {dish_name}\n'
            print(f'Dish Name:- {dish_name}\n')
            r = r + f'Ingredients:- {ingredients}\n'
            t = t+r
            print(ingredients)
            t += "First generate instructions to prepare dish and then prepare final task tree to prepare dish based on instructions."
            k1 = dish_name.replace(' ', '_')
            file_path = f'{k1}1.json'
            response = model.generate_content(t)
            print(response.text)

    f.close()
