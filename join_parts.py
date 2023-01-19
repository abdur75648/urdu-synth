# Put in the same folder as the images and labels.txt
import os,shutil,random
from PIL import Image
from tqdm import tqdm

os.makedirs("out",exist_ok=True)

# Function to horizontally concatenate 2 images
def get_concat_h(im1, im2):
    dst = Image.new('RGB', (im1.width + im2.width, im1.height))
    dst.paste(im2, (0, 0))
    dst.paste(im1, (im2.width, 0))
    return dst

# images = os.listdir(".")
with open("labels.txt","r") as f:
    lines = f.readlines()

for i in tqdm(range(100)):
    indices_selected = []
    for j in range (random.randint(2,5)):
        index = random.randint(0,len(lines)-1)
        while index in indices_selected:
            index = random.randint(0,len(lines)-1)
        indices_selected.append(index)
    
    
    the_line = lines[indices_selected[0]]
    img = the_line.split(" ")[0]
    gt = (" ".join(the_line.split(" ")[1:])).strip("\n")
    image = Image.open(img)
    
    for index in indices_selected[1:]:
        the_line = lines[index]
        img = the_line.split(" ")[0]
        this_gt = (" ".join(the_line.split(" ")[1:])).strip("\n")
        
        # choose factor as 0 or 1 with 25% probability
        factor = random.random() < 0.25
        if factor:
            flip = random.randint(0,1)
        if factor:
            bracket_number = random.randint(0,9)
            bracket_img = "ra_brackets/" + str(bracket_number)+"_bracket_resized.png"
            if flip:
                pil_img = Image.open(bracket_img).transpose(Image.FLIP_LEFT_RIGHT)
                # Resize the pil_image to have height 128
                image = get_concat_h(image, pil_img)
                gt += " " + ")"
            else:
                pil_img = Image.open(bracket_img)
                image = get_concat_h(pil_img, image)
                gt += " " + "("
        image = get_concat_h(image, Image.open(img))
        gt += " "+ this_gt
    image.save("out/"+str(i)+".jpg")
    # write gt to file
    with open("out/labels.txt","a") as f:
        f.write(str(i)+".jpg "+gt+"\n")