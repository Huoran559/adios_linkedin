import re

'''
All of the fields must be in lower cases.
Enter your required fields here.
required1 is the field that exactly matches what the user is searching for.
required2 is the filed that may be what user is searching for: if required2 provides extra info it searches required1 in that extra info..if it 
          does not find it then required2 is skipped. If required2 does not provide extra info, then it is stored.
required3: unlike required2 it must need a extra info and it searches for required1 in that extra info, if not provided with it, it is skipped.
'''

required1 = r'\bjava\b|\bjee\b|\bj2ee\b|\bspring framework\b|\bhibernate\b'
required2 = r'\bsoftware engineer\b|\bsolution architect\b'
required3 = r'\bfreelanc(e|er|ing)\b|\bfounder\b|\bpresident\b|\bcto\b'

'''
required is for use in middleware, it generally is combination of required1, required2, required3. 
location is for use in middleware to check if the current profile is of required location or not.
'''
required = r'\bjava\b|\bjee\b|\bj2ee\b|\bspring framework\b|\bhibernate\b|\bsoftware engineer\b|\bsolution architect\b|\bfreelanc(e|er|ing)\b|\bfounder\b|\bpresident\b|\bcto\b'
location= r'nepal' 
