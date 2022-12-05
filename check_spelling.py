from textblob import Word
import string
from langdetect import detect_langs
import json
from website_reading import title


def check_word(string):
    """
    Checks the spelling of the given word. If the word is spelled incorrectly, returns a tuple with two values:
    1) The original word.
    2) Suggested correct word. 
    """
    word = Word(string)
    result = word.spellcheck()
    if word.isalpha() and result[0][1] >= 0.9:
        if result[0][0] != string:
            return (string, result[0][0])

def check_text(text):
    """
    Conditions: text must be in English.
    First, modifies the text into a more readable version by deleting '\n' symbols.
    Then, after checking if the text is in English, returns a list of check_word tuples.
    """
    text_str_unchecked = ' '.join(text.split('\n'))
    langs = detect_langs(text_str_unchecked)
    language = str(langs[0])[:2]
    confidence = float(str(langs[0])[3:])
    if language == 'en' and confidence >= 0.9:
        text_list_unchecked = text_str_unchecked.translate(str.maketrans('', '', string.punctuation)).split()
        text_list_checked = list(map(check_word, text_list_unchecked))
        while True:
            try:
                text_list_checked.remove(None)
            except:
                break
        return text_list_checked
    
async def check_and_notify(text, notify, site_url):
    """
    Using to previous functions:
    1) Returns a dictionary of corrections: {'original: correct word'}.
    2) Notifies with a message containing corrections.
    3) Saves corrections into the file 'Corrections.json'.
    """
    checked = check_text(text)
    corrections = {}
    if checked != None and len(checked) != 0:
        for (original, correct) in checked:
            corrections[original] = correct
        grammarly = ''
        for original in corrections:
            grammarly += f"* not {original}, {corrections[original]}\n"
        corrections_message = f"Oops! There may be mistakes here🤔: {title(site_url)}\n\n{grammarly}\n{site_url}"
        await notify(corrections_message)
        json.dump({site_url: corrections}, open('Corrections.json','w'), indent=4, separators=(', ',' : '))
    return corrections
