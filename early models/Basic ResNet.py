
# coding: utf-8

# In[1]:


from fastai.vision import *
import zipfile
classes = ['tree','shrub']
path = Path('treeshrub')


# In[2]:


for c in classes:
    myfile = c+'.zip'
    print(myfile)
    with zipfile.ZipFile(path/myfile,"r") as zip_ref:
        zip_ref.extractall(path/c)


# In[3]:


for c in classes:
    print(c)
    verify_images(path/c, delete=True, max_size=500)


# In[4]:


import numpy
np.random.seed(42)
data = ImageDataBunch.from_folder(path, train=".", valid_pct=0.2,
        ds_tfms=get_transforms(), size=224, bs=16, num_workers=4).normalize(imagenet_stats)


# In[5]:


data.show_batch(rows=3, figsize=(7,8))


# In[6]:


data.classes, data.c, len(data.train_ds), len(data.valid_ds)


# In[8]:


learn = cnn_learner(data, models.resnet50, metrics=error_rate)


# In[9]:


learn.fit_one_cycle(4)

