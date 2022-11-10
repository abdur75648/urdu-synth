import random
with open("en.txt","r") as f:
    lines = f.readlines()

# Select 2000 random lines
lines = random.sample(lines, 2000)

# write the lines to a new file
with open("en_random.txt","w") as f:
    for line in lines:
        if len(line)>1:
            f.write(line)