def rot13(s):
    alph = "abcdefghijklmnopqrstuvwxyz"
    result = ''
    for ch in s:
        if ch.lower() in alph:
            p = alph.find(ch.lower())
            if p >= 13:
                p = -13
            else:
                p = 13
            result += chr(ord(ch)+p)
        else:
            result += ch
    return result

def escape_html(s):
    for(i,o) in (('&',"&amp;"),('>',"&gt;"),('<',"&lt;"),('"',"&quot;")):
        s = s.replace(i,o)
    return s



