# This file converts from the old naming standard to the new one.
# variables should not start with a type letter
# pointer asterisks will generally be attached to variables

import re

def GetFileText( fileName ):
  file = open(fileName, "r")
  fileText = file.read()
  file.close()
  return fileText

def FixVariableNames( text ):
# any "uVar" -> "var" for u, i, s, c, e, b
#     only for variables ie. preceded by " ", ">", ".", "=", "(", "[", "{", ",", "!", "/", "*", "+", "-", "%", "|", "&", "<"
#     basically any non-letter or number
  lettersToReplace = ["u", "i", "s", "c", "e", "b", "z"]
  for letter in lettersToReplace:
    oldNames = re.findall(r'[\W]' + letter + '[A-Z]', text)
    for name in oldNames:
      newName = name[0] + name[2].lower()
      text = text.replace(name, newName)
  return text

def FixPointers( text ):
# any " * const" -> "* const"
# any " * pVar" -> " *pVar"
  oldPointers = re.findall(r' ?\* ?(?!\w*const\w*)(?!\w*p[A-Z]\w*)[a-z]\w*\b', text)
  for pointer in oldPointers:
    newPointer = re.sub(r' ?\* ?', '', pointer)
    newPointer = ' *p' + newPointer[0].upper() + newPointer[1:]
    text = text.replace(pointer, newPointer)

  text = text.replace(' * const', '* const')
  text = re.sub(r' ?\* ?p', ' *p', text)
  return text

def FixSpacingByParentheses( text ):
# standardizes the spacing in function definitions
  text = re.sub(r'\( (?=\S)', '(', text)
  text = re.sub(r'(?<=\S) \)', ')', text)
  return text

def replace_bool_with_BOOL(text):
  return re.sub(r'\bbool\b', 'BOOL', text)

def replace_uint_with_UINT(text):
  text = re.sub(r'\buint_(\d+)_t\b', r'UINT\1', text)
  text = re.sub(r'\buint_(\d+)\b', r'UINT\1', text)
  text = re.sub(r'\buint(\d+)_t\b', r'UINT\1', text)
  return re.sub(r'\buint(\d+)\b', r'UINT\1', text)
    
def FixTypeNames( text ):
# any bool, uint[0-9] must be capitalized
  text = replace_bool_with_BOOL(text)
  return replace_uint_with_UINT(text)

def WriteToFile( fileName, text ):
  file = open(fileName, "w")
  file.write( text ) #overwrites whole file
  file.close()
  return 




fileName = input('file (path) to convert: ')
fileText = GetFileText( fileName )

fileText = FixVariableNames( fileText )
fileText = FixPointers( fileText )
fileText = FixSpacingByParentheses( fileText )
fileText = FixTypeNames( fileText )

WriteToFile( fileName, fileText )