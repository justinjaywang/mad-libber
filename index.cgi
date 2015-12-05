#!/usr/bin/env python

import cgitb, string, math, random, cgi
cgitb.enable()

header = 'Content-Type: text/html\n\n'

htmlHeader = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>Python-powered Mad Libber</title>
    <meta name="description" content="Python-powered Mad Libber by Justin Wang">
    <meta name="viewport" content="user-scalable=no, initial-scale=1.0, maximum-scale=1.0, width=device-width">
    <link rel="stylesheet" href="css/style.css">
  </head>
  <body>
    <h1>Python-powered Mad Libber <small>by Justin Jay Wang</small></h1>
    <p class="divider"></p>"""

htmlFooter = """  </body>
</html>"""

# templates
templates = {}
templates[1] = ['Absence makes the %s grow %s.', 'NOUN', 'COMP-ADJ', ['NOUN', 'COMP-ADJ']]
templates[2] = ['Better to have %s and %s, than to have never %s at all.', 'PAST-PARTICIPLE', 'PAST-VERB', 'PAST-PARTICIPLE', ['PAST-PARTICIPLE', 'PAST-VERB']]
templates[3] = ['If a %s is worth %s it is worth %s %s.', 'NOUN', 'GERUND', 'GERUND', 'ADVERB', ['NOUN', 'GERUND', 'ADVERB']]
templates[4] = ["It's not the size of the %s in the %s, it's the size of the %s in the %s.", 'NOUN1', 'NOUN2', 'NOUN2', 'NOUN1', ['NOUN1', 'NOUN2']]
templates[5] = ['You are what you %s.', 'VERB', ['VERB']]

# prompts
prompts = {}
prompts['NOUN'] = 'Noun'
prompts['NOUN1'] = 'Noun'
prompts['NOUN2'] = 'Noun'
prompts['COMP-ADJ'] = "Comparative adjective, like <em>bigger</em>"
prompts['PAST-PARTICIPLE'] = "Past participle, such as <em>eaten</em>"
prompts['PAST-VERB'] = 'Verb in the past tense'
prompts['GERUND'] = "Verb ending in <em>-ing</em>"
prompts['ADVERB'] = 'Adverb'
prompts['VERB'] = 'Verb'

def main():
  """
  Determine which page to print, according to number of inputs, and print HTML
  """
  form = cgi.FieldStorage()
  print header + htmlHeader
  if not form.keys(): # if form.keys() is empty, or 0 inputs
    htmlBody = makeForm()
    print htmlBody
  else: # form inputs exist
    if makeSent(form): # if user filled out all text fields
      htmlSent = makeSent(form)
      htmlBody = htmlSent + '<form action="index.cgi"><input type="submit" value="Try another one" class="submit"></form>'
    else: # form error occurred
      htmlBody = makeForm()
    print htmlBody
  print htmlFooter

def makeForm():
  """
  Returns altered HTML form
  """
  # generate random template number
  randNum = random.random() * len(templates)
  f = math.ceil(randNum) # float
  n = int(f) # int
  # create form
  formStart = '<form action="index.cgi">'
  formMiddle = ''
  promptList = templates[n][-1][:]
  for i in range(len(promptList)): # create text fields
    promptRaw = promptList[i]
    prompt = prompts[promptRaw]
    if i == 0: # first time, for autofocus
      focus = ' autofocus="autofocus" '
    else:
      focus = ''
    formMiddle = formMiddle + '<p class="prompt">' + prompt + '</p><input type="text" name="' + promptRaw + '" class="text"' + focus + '><br>'
  formEnd = '<input type="hidden" name="template" value="' + str(n) + '"><input type="submit" value="Submit" class="submit"></form>'
  formTotal = formStart + formMiddle + formEnd
  return formTotal
  
def makeSent(form):
  """
  Returns correctly filled in sentence, or False if user input did not fill one or more text fields
  """
  # get template value
  n = int(form['template'].value)
  tempSent = templates[n][0]
  placeholderList = templates[n][1:-1]
  userValueList = []
  formError = False
  for i in range(len(placeholderList)): # iterate through placeholders and replace with user input
    placeholder = placeholderList[i]
    try:
      userValue = form[placeholder].value.replace('<','&lt;') # replace left angle bracket
      userValueItalic = '<em>' + userValue + '</em>'
      userValueList.append(userValueItalic)
    except KeyError:
      formError = True
  if not formError:
    # replace format sequence in template lists with user values
    userValueTuple = tuple(userValueList)
    newSent = tempSent % userValueTuple
    newSentHTML = '<p class="sentence">' + newSent + '</p>'
  else:
    newSentHTML = False
  return newSentHTML
              
if __name__ == '__main__':
  main()