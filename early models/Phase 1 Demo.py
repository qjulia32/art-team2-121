
# coding: utf-8

# In[1]:


from fastai.vision import *


# In[1]:


import zipfile
with zipfile.ZipFile('small_25_100_data.zip',"r") as zip_ref:
        zip_ref.extractall('small_25_100_data')


# In[2]:


path = Path('phase1_demo_data')
classes = ['Abstract Art', 'Abstract Expressionism', 'Art Informel']
for c in classes:
    print(c)
    verify_images(path/c, delete=True, max_size=500)


# In[3]:


import numpy
np.random.seed(42)
data = ImageDataBunch.from_folder(path, train=".", valid_pct=0.2,
        ds_tfms=get_transforms(), size=224, bs=16, num_workers=0).normalize(imagenet_stats)


# In[4]:


data.show_batch(rows=3, figsize=(7,8))


# In[5]:


data.classes, data.c, len(data.train_ds), len(data.valid_ds)


# In[6]:


learn = cnn_learner(data, models.resnet34, metrics=error_rate)


# In[7]:


learn.fit_one_cycle(4)

