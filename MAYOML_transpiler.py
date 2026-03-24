import sys

ld = "{"    # delimiters
rd = "}"
ldLit = "!@#$(" # literals of the delimter characters are temporarily 
rdLit = "!@#$)" # stored as this, to later be turned back into the literal characters
esc = "\\"  # escape "\"
nl = "\n" # newline


def parse(text:str):
    # replace escaped delimiters that intend to use the literal
    # "\{" intends "{" replace with "!@#$("
    working = text.replace(esc+ld,ldLit).replace(esc+rd,rdLit)

    # check for number of delimiters 
    if count(working,ld) != count(working,rd):
        print("ERROR: Uneven Delimiters!!!")
        pass

    # call parse helper
    working = parse_helper(working)

    # replace literals
    working = working.replace(ldLit,ld).replace(rdLit,rd)
    
    # fix newlines
    working = working.replace(nl,nl+"<br>")

    return working

# recursively akflasjdf;aslkd
# pass in text without the external braces
def parse_helper(text:str) -> str:
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
def hat(text:str) -> str:
    ans=""
    for i in range(len(text)):
        ans+=text[i]+"&#770;"
    return ans


symbols = {
    "perp": "⟂",
    "+-": "±",
    "tri": "△",
    "alpha": "α",
    "Alpha": "Α",
    "beta": "β",
    "Beta": "Β",
    "gamma": "γ",
    "Gamma": "Γ",
    "delta": "δ",
    "Delta": "Δ",
    "epsilon": "ε",
    "Epsilon": "Ε",
    "zeta": "ζ",
    "Zeta": "Ζ",
    "eta": "η",
    "Eta": "Η",
    "theta": "θ",
    "Theta": "Θ",
    "iota": "ι",
    "Iota": "Ι",
    "kappa": "κ",
    "Kappa": "Κ",
    "lambda": "λ",
    "Lambda": "Λ",
    "mu": "μ",
    "Mu": "Μ",
    "nu": "ν",
    "Nu": "Ν",
    "xi": "ξ",
    "Xi": "Ξ",
    "omicron": "ο",
    "Omicron": "Ο",
    "pi": "π",
    "Pi": "Π",
    "rho": "ρ",
    "Rho": "Ρ",
    "sigma": "σ",
    "Sigma": "Σ",
    "tau": "τ",
    "Tau": "Τ",
    "upsilon": "υ",
    "Upsilon": "Υ",
    "phi": "ϕ",
    "Phi": "Φ",
    "chi": "χ",
    "Chi": "Χ",
    "psi": "ψ",
    "Psi": "Ψ",
    "omega": "ω",
    "Omega": "Ω",
    "ele": "∈",
    "and": "∧",
    "or": "∨",
    "eqv": "≡",
    "C": bold("ℂ"),
    "H": bold("ℍ"),
    "N": bold("ℕ"),
    "P": bold("ℙ"),
    "Q": bold("ℚ"),
    "R": bold("ℝ"),
    "Z": bold("ℤ")
}

modifications = {
    "sub": subscript,
    "sup": superscript,
    "und": underline,
    "bold": bold,
    "ital": italicize,
    "bar": bar,
    "hat": hat
}

def main():
    if len(sys.argv) <= 1:
        print("Usage: MAYOML_transpiler.py <input_file> [output_file]")
        exit()

    in_file_name = sys.argv[1]
    in_file = open(in_file_name, "r")
    mayoml = in_file.read()
    html = parse(mayoml)

    out_file_name = None
    if len(sys.argv) > 2:
        out_file_name = sys.argv[2]
    else:
        a = in_file_name.split(".")
        a[-1] = "html"
        out_file_name = ".".join(a)

    #print(out_file_name)

    out_file = open(out_file_name, "w", encoding="utf-8")
    out_file.write(html)
    out_file.close()


main()