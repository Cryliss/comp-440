def check_payload(text):
    # Does the first or last character in our string contain
    # any of the following symbols?
    if text[0] == ';' or text[-1] == ';':
        # Yes - someone's trying to do SQL injection, return true
         return True
    elif text[0] == "'" or text[-1] == "'":
        # Yes - someone's trying to do SQL injection, return true
        return True
    elif text[0] == '<' or text[-1] == '>':
        # Yes - someone's trying to do an XSS attack, return true
        return True
    elif text[0] == '-':
        # Yes - someone's trying to do SQL injection, return true
        return True
    else:
        # None of the other conditions matched, we're probably ok?
        return False

def check_blogpost(text):
    if "'DROP TABLE" in text:
        return True
    if "'SELECT * FROM " in text:
        return True;
    return False
