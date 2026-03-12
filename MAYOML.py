ld = "{"    # delimiters
rd = "}"
ldLit = "!@#$(" # literals of the delimter characters are temporarily 
rdLit = "!@#$)" # stored as this, to later be turned back into the literal characters
esc = "\\"  # escape "\"


def parse(text:str):
    # replace escaped delimiters that intend to use the literal
    # "\{" intends "{" replace with "!@#$("
    working = text.replace(esc+ld,ldLit).replace(esc+rd,rdLit)

    # check for number of delimiters 
    if count(working,ld) != count(working,rd):
        print("ERROR: Uneven Delimiters!!!")

    # call parse helper
    working = parse_helper(working)


    


    return working

# recursively akflasjdf;aslkd
# pass in text without the external braces
def parse_helper(text:str) ->str:
    if ld not in text:      # Base case, no more braces {}
        if esc in text:     # modifications
            op = text.split(esc,1)
            oprnd = op[0]
            oprtn = op[1]
            if oprtn in modifications:
                return modifications[oprtn](oprnd) # 2\sub -> <sub>2</sub>
            else:
                return text # no-op
        else:
            if text in symbols:   # insert symbols ele -> ∈
                return symbols[text]
            else:
                return text     # no-op
    
    # recursing
    while (ld in text and rd in text):
        left_i:int  # indices of start and end of {section} (indeces of braces)
        right_i:int

        # find start of {section}
        for i in range(len(text)):
            if text[i]==ld:
                left_i = i
                break
        
        # find end of {section}

        depth:int = 1
        for i in range(left_i+1,len(text)):
            if text[i]==ld:
                depth+=1
            elif text[i]==rd:
                depth-=1
            if depth==0:
                right_i = i
                break
        
        # replaces {section} with result by recursing
        #print("from: "+text)
        #print("left: "+str(left_i))
        #print("right: "+str(right_i))
        text = text[:left_i]+parse_helper(text[left_i+1:right_i])+text[right_i+1:]
        #print("to: "+text)
    return parse_helper(text)

        

def count(text:str,target:str) -> int:
    if len(text)==0 or len(target)==0:
        return 0
    count = 0
    n = len(text)
    d = len(target)
    for i in range(0,n-d+1):
        if text[i:i+d] == target:
            count+=1
    
    return count

def superscript(text:str) -> str:
    return "<sup>"+text+"</sup>"
def subscript(text:str) -> str:
    return "<sub>"+text+"</sub>"
def underline(text:str) -> str:
    return "<u>"+text+"</u>"
def bold(text:str) -> str:
    return "<b>"+text+"</b>"
def italicize(text:str) -> str:
    return "<i>"+text+"</i>"
def bar(text:str) -> str:
    ans=""
    for i in range(len(text)):
        ans+=text[i]+"&#x0305;"
    return ans

symbols = {
    "perp": "⟂",
    "ele": "∈",
    "and": "∧",
    "or": "∨",
    "eqv": "≡",
}

modifications = {
    "sub": subscript,
    "sup": superscript,
    "und": underline,
    "bold": bold,
    "ital": italicize,
    "bar": bar
}





asdf = "{x\bar} and {asdf\bar}"
asdf = input("type here: ")
print(asdf)
print(parse(asdf))