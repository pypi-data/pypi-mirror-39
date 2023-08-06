
import os

def getProjectRoot():
    p = os.getcwd()
    for _ in range(10):
        if os.path.exists( os.path.join( p , ".project_root") ):
            return os.path.abspath(p)
        p = os.path.join(p , '..')
    raise ValueError('Project Root not found')
    
    
    
def isnotebook():
    try:
        shell = get_ipython().__class__.__name__
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter
    

def get_tqdm():
    from tqdm import tqdm_notebook , tqdm
    if isnotebook():
        return tqdm # tqdm_notebook
    else:
        return tqdm