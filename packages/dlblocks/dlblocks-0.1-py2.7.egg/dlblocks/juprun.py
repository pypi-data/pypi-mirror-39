#!/usr/bin/python


# coding: utf-8

# In[19]:

"""

commands 

cp juprun.py /usr/bin/juprun
chmod +x /usr/bin/juprun
touch /usr/bin/juprun2
echo "jupyter nbconvert --to notebook --execute \"\$1\" --output \"\$2\"" > /usr/bin/juprun2
chmod +x /usr/bin/juprun2
"""

import random
from shutil import copyfile
import os
import sys


# In[2]:


source_notebook = sys.argv[1]
destination_notebook = sys.argv[2]


print "source_notebook" , source_notebook
print "destination_notebook" , destination_notebook

port_no = 9200 + random.randint(0 , 600 )
# In[3]:


from subprocess import Popen
import subprocess
import time
commands = [ 'jupyter' , 'notebook' , "--NotebookApp.token=''" , '--NotebookApp.port=%d'%port_no  , '--ip=127.0.0.1' , '--allow-root' ] 
# p = Popen( commands ,stdout=subprocess.PIPE ,  universal_newlines=True ) # something long running
# ... do other stuff while subprocess is running


# In[4]:


tmp_name = "." + str(random.randint(999999, 99999999))+".ipynb"
copyfile( source_notebook , tmp_name )


# In[5]:


p = subprocess.Popen( commands )#  , stderr=subprocess.PIPE, universal_newlines=True)


import atexit

def exit_handler():
    p.terminate()


atexit.register(exit_handler)


# for l in iter(p.stderr.readline, ""):
#     print l
#     if "The Jupyter Notebook is runnin" in l:
#         break

time.sleep(5)
print "The notebook server is ready"



# In[6]:


from selenium import webdriver
d = webdriver.PhantomJS()


# In[7]:


d.get("http://localhost:%d"%port_no)
d.find_element_by_css_selector("[name=password]").send_keys("letmein2")
d.find_element_by_css_selector("[type=submit]").click()
d.find_element_by_css_selector("body").text


# In[8]:


d.get("http://localhost:%d/notebooks/%s"%(port_no,tmp_name) )
d.find_element_by_css_selector("body").text


# In[9]:


time.sleep( 7 )


# In[10]:


d.execute_script("IPython.notebook.execute_all_cells();")


# In[11]:


copyfile( tmp_name , destination_notebook )
i = 0
while True:
    i += 1
    time.sleep( 5 )
    if i%2 == 0:
        d.execute_script("IPython.notebook.save_checkpoint();")
        copyfile( tmp_name , destination_notebook )
        os.system( "jupyter nbconvert --to html %s"% destination_notebook )
        print "saving"
        if not d.execute_script("return  IPython.notebook.kernel_busy;") :
            break
            
d.execute_script("IPython.notebook.save_checkpoint();")
time.sleep( 5 )


# In[12]:


# d.save_screenshot('out.png');


# In[13]:


print "Execution complete"


# In[21]:





# In[18]:


copyfile( tmp_name , destination_notebook )
os.system( "jupyter nbconvert --to html %s"% destination_notebook )


# In[15]:


# IPython.notebook.save_notebook_success


# In[16]:


# c = d.execute_script("IPython.notebook.toJSON();")


# In[20]:


os.remove( tmp_name )


# In[17]:


p.terminate()


# In[23]:


try:
    os.remove("ghostdriver.log")
except:
    pass
