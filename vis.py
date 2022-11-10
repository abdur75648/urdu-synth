import os,shutil,random
data_dir = '3M_simplebg'
images = os.listdir(data_dir)

# pick 100 random images
random.shuffle(images)
images = images[:100]

# make a directory for them
if not os.path.exists('vis'):
    os.mkdir('vis')
# copy them to the directory
for image in images:
    shutil.copy('3M_simplebg/' + image, 'vis/' + image)