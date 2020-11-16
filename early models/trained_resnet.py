
# coding: utf-8

# # ResNet50 Art Style Classifier

# In[2]:


from fastai.vision import *
import zipfile
import numpy
import os
path = Path('data/artData')


# In[15]:


import pickle


# In[2]:


myfile = 'small_25_100_data.zip'
with zipfile.ZipFile(path/myfile,'r') as zip_ref:
    zip_ref.extractall(path)


# In[3]:


path = Path('data/artData/small_25_100_data')
classes = []
for root, dirs, files in os.walk(path, topdown=True):
    for name in dirs:
        classes.append(name)
print(classes)


# In[4]:


for c in classes:
    print(c)
    verify_images(path/c, delete=True, max_size=500)


# In[5]:


np.random.seed(42)
data = ImageDataBunch.from_folder(path, train=".", valid_pct=0.2,
        ds_tfms=get_transforms(), size=224, bs=16, num_workers=4).normalize(imagenet_stats)


# In[6]:


data.show_batch(rows=3, figsize=(7,8))


# In[7]:


data.classes, data.c, len(data.train_ds), len(data.valid_ds)


# In[8]:


learn = cnn_learner(data, models.resnet50, metrics=error_rate)


# In[9]:


learn.fit_one_cycle(4)


# In[10]:


interp = ClassificationInterpretation.from_learner(learn)


# In[11]:


interp.plot_top_losses(9, figsize=(15,11))


# In[12]:


interp.plot_confusion_matrix()


# In[13]:


learn.save('stage-1')


# In[17]:


learn.export('trained_model.pkl')


# In[13]:


# Setting hyperparameters, pretty garbage rn
# learn.lr_find()
# learn.recorder.plot()


# In[14]:


# learn.unfreeze()
# learn.fit_one_cycle(5, max_lr=slice(1e-4,1e-2))


# In[15]:


# learn.save('stage-2')


# In[16]:


# interp = ClassificationInterpretation.from_learner(learn)
# interp.plot_top_losses(9, figsize=(15,11))


# In[17]:


# interp.plot_confusion_matrix()

