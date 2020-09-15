import os
import cv2
import numpy as np
import albumentations as A

def read_image(path, color_format='rgb'):
    image = cv2.imread(path)
    if color_format.lower() == 'rgb':
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image.astype(np.float32)/255.
    
    return image

def transformation(image):
    transform = A.Compose([A.HorizontalFlip(p=0.5), 
                           A.RandomScale(p=0.5, interpolation=1, scale_limit=(-0.1, 0.1)),
                           A.ShiftScaleRotate(p=0.5, rotate_limit=(-2, 2)),
                           A.Resize(always_apply=False, height=128, width=64)])
    augmented_img = transform(image=image)["image"]
    return augmented_img
    
class DataLoader:
    def __init__(self, dir_path='Market-1501/gt_bbox',
                 image_reader=None, batch_size=16):
        self.dir_path = dir_path
        self.image_reader = image_reader
        self.batch_size = batch_size
        
        self._load()
        
    def _get_image(self, path):
        return self.image_reader(path)
    
    def _load(self):
        paths = os.listdir(self.dir_path)
        self.path_ids = {}
        for path in paths:
            if path != 'Thumbs.db':
                id_ = int(path.split('_')[0])
                if id_ in self.path_ids.keys():
                    self.path_ids[id_].append(os.path.join(self.dir_path, path))
                else:
                    self.path_ids[id_] = [os.path.join(self.dir_path, path)]
                
    def generator(self):
        while True:
            input_1 = []
            input_2 = []
            batch_y = []
            
            for _ in range(self.batch_size):
                if np.random.choice([0, 1]):
                    id_ = np.random.choice(np.arange(1, 1501+1))
                    image_1 = self._get_image(np.random.choice(self.path_ids[id_]))
                    image_1 = transformation(image_1)
                    input_1.append(image_1)
                                        
                    image_2 = self._get_image(np.random.choice(self.path_ids[id_]))
                    image_1 = transformation(image_1)
                    input_2.append(image_2)
                    
                    batch_y.append([1])
                else:
                    id_ = np.random.choice(np.arange(1, 1501+1))
                    image_1 = self._get_image(np.random.choice(self.path_ids[id_]))
                    image_1 = transformation(image_1)
                    input_1.append(image_1)
                    
                    id_ = np.random.choice(np.arange(1, 1501+1))
                    image_2 = self._get_image(np.random.choice(self.path_ids[id_]))
                    image_2 = transformation(image_2)
                    input_2.append(image_2)
                    
                    batch_y.append([0])
                   
            input_1 = np.array(input_1)
            input_2 = np.array(input_2)
            
            yield [input_1, input_2], np.array(batch_y)
