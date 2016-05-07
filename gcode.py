
from parse import compile
mycode = "G01 X1.0000 Y3.0000"
p = compile("G{code} X{x} Y{y}")
command = p.parse(mycode)
print command


#Does not do what I want
'''
mycode = "G04"
command = p.parse(mycode)
print command
'''



f= open("output_001.gcode")
for line in f:
    print line
    if line[0:3] == "G01":
        command = p.parse(line)
        draw_line
    elif line[0:3] == "G03":
        raisepen()
    elif line[0:3] == "G05":
        lowerpen()
