CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
            "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
CYR = list(CYRILLIC_SYMBOLS)
TRANS = {}

for c, l in zip(CYR, TRANSLATION):    
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()    
   
    
def normalize(file_name:str) -> str:
    output = ""
        
    for ch in file_name:
        if ch.lower() in CYR:
            output += ch.translate(TRANS)
        elif  ch.isnumeric() or ch.isalpha() or ch == "." or ch == " ":
            output += ch
        else:
            output += "_"
            
    return output