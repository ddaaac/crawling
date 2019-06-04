from PIL import Image
import os


def join_path(path):
    _path = ""
    for idx, p in enumerate(path):
        if idx != len(path) - 1:
            _path = _path + p + "\\"
        else:
            _path = _path + p
    return _path


root_path = "C:\\Users\\skybl\\Downloads\\Assignment6"
cat_path = join_path([root_path, "cat"])
dog_path = join_path([root_path, "dog"])
cat_dirs = os.listdir(cat_path)
dog_dirs = os.listdir(dog_path)


def resize(path, dirs, animal):
    for idx, item in enumerate(dirs):
        im = Image.open(path+"\\"+item).convert(mode='LA')
        imResize = im.resize((28, 28))
        imResize.save(join_path([root_path, "train", animal, animal])+str(idx)+".png")


resize(dog_path, dog_dirs, "dog")


