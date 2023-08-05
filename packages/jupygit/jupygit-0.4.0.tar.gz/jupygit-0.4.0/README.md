
# jupygit

[![CircleCI](https://circleci.com/gh/fferegrino/jupygit.svg?style=svg)](https://circleci.com/gh/fferegrino/jupygit) [![PyPI](https://img.shields.io/pypi/v/jupygit.svg)](https://pypi.org/project/jupygit/)

Integrating Jupyter Notebooks to a git workflow.
  
### Installation.  
(I highly recommend installing this into a conda environment) To install the extension and enable it just run the following commands:  

```
pip install jupygit
jupyter serverextension enable --py jupygit --sys-prefix
jupyter nbextension install --py jupygit --sys-prefix
jupyter nbextension enable --py jupygit --sys-prefix
```

### Why?  
I've been working with Jupyter Notebooks for a while, and I always felt something dying inside me everytime I pushed a massive file to GitHub, only to have it overwritten by my next **huge** commit causing me to have unreadable diffs. I decided to create this extension that, as I previously stated, is a hack.

### How?  (and usage)
Let's say you are working on a file called `Awesome.ipynb`. What this extension will do once you press shiny new **git** button on your Notebook is:  

 0. Shows a nice modal with an encouraging message.  
 1. Renames your current file to `Awesome-jupygit___.ipynb` using Jupyter's API so that your kernel stays alive and you do not lose any work, we'll call this the *"dirty"* file.
 2. Adds the pattern `*-jupygit___.ipynb` to your .gitignore file, so that your *"dirty"* file does not show up as a new file in your git repository.
 3. Creates a copy of `Awesome-jupygit___.ipynb` but with the original name `Awesome.ipynb`, this copy is clean, no outputs and no `execution_counts`, we'll call this the *"clean"* file.
 4. Now is your turn to commit `Awesome.ipynb`, the *"clean"* file to source control!

Are you done pushing things to Git? Now close the dialog and this will happen:  

 1. Delete the file `Awesome.ipynb` (do not worry! your kernel and work is safe in the *"dirty"* file).  
 2. Rename `Awesome-jupygit___.ipynb` to `Awesome.ipynb` so that you can resume your work where you left it before being a good human and using source control.