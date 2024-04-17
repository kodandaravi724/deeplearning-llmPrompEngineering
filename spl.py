s =" BEEF PATTY, HAMBURGER ROLL, MUSHROOMS, SWISS CHEESE, LETTUCE, TOMATO , MAYONNAISE, VEGETABLE OIL BLEND, GARLIC CONCENTRATE, EXTRA VIRGIN OLIVE OIL, LEMON JUICE, DIJON MUSTARD, ROSEMARY, SALT, SALT, BLACK PEPPER"

l = list(map(lambda x:x.strip().lower(),s.split(',')))
l = list(map(lambda x: "\""+x+"\"", l))
print(','.join(l))
#
#
#
# l = []
# ans = []
# i =0
# st = 0
# while i < len(s):
#     k = s[i]
#     if(k == '('):
#         l.append(k)
#     if(k==')'):
#         l.pop()
#     if(k == ','):
#         if(len(l) == 0):
#             ans.append(s[st:i])
#             st = i+1
#     i=i+1
# if(len(l)==0):
#     ans.append(s[st:i].lower())
# print(ans)
#
# l = list(map(lambda x:x.strip().lower(),ans))
# l = list(map(lambda x: "\""+x+"\"", l))
# print(','.join(l))

# Python program to read
# json file

# import json
#
# # Opening JSON file
# f = open('input_hub.json')
#
# # returns JSON object as
# # a dictionary
# data = json.load(f)
#
# # Iterating through the json
# # list
# print(data[0]['menu'][0]['dish'])
#
# # Closing file
# f.close()
