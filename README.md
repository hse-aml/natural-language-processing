# Natural Language Processing course resources
This github contains practical assignments for Natural Language Processing course by Higher School of Economics:
https://www.coursera.org/learn/language-processing.
In this course you will learn how to solve common NLP problems using classical and deep learning approaches.

From a practical side, we expect your familiarity with Python, since we will use it for all assignments in the course. Two of the assignments will also involve TensorFlow. You will work with many other libraries, including NLTK, Scikit-learn, and Gensim. You have several options on how to set it up.

## 1. Running on Google Colab
Google has released its own flavour of Jupyter called Colab, which has free GPUs!

Here's how you can use it:
1. Open https://colab.research.google.com, click **Sign in** in the upper right corner, use your Google credentials to sign in.
2. Click **GITHUB** tab, paste https://github.com/hse-aml/natural-language-processing and press Enter
3. Choose the notebook you want to open, e.g. week1/week1-MultilabelClassification.ipynb
4. Click **File -> Save a copy in Drive...** to save your progress in Google Drive
5. _If you need a GPU_, click **Runtime -> Change runtime type** and select **GPU** in Hardware accelerator box
6. **Execute** the following code in the first cell that downloads dependencies (change for your week number):
```python
! wget https://raw.githubusercontent.com/hse-aml/natural-language-processing/master/setup_google_colab.py -O setup_google_colab.py
import setup_google_colab
# please, uncomment the week you're working on
# setup_google_colab.setup_week1()  
# setup_google_colab.setup_week2()
# setup_google_colab.setup_week3()
# setup_google_colab.setup_week4()
# setup_google_colab.setup_project()
# setup_google_colab.setup_honor()
```
7. If you run many notebooks on Colab, they can continue to eat up memory,
you can kill them with `! pkill -9 python3` and check with `! nvidia-smi` that GPU memory is freed.

**Known issues:**
* No support for `ipywidgets`, so we cannot use fancy `tqdm` progress bars.
For now, we use a simplified version of a progress bar suitable for Colab.
* Blinking animation with `IPython.display.clear_output()`.
It's usable, but still looking for a workaround.
* If you see an error "No module named 'common'", make sure you've uncommented the assignment-specific line in step 6, restart your kernel and execute all cells again

## 2. Running locally

Two options here:

1. Use the Docker container of our course. It already has all libraries, that you will need. The setup for you is very simple: install Docker application depending on your OS, download our container image, run everything within the container. Please, see this [detailed Docker tutorial](Docker-tutorial.md).

2. Manually install all the libraries depending on your OS (each task contains a list of needed libraries in the very beginning). If you use Windows/MacOS you might find useful Anaconda distribution which allows to install easily most of the needed libraries. However, some tools, like StarSpace for week 2, are not compatible with Windows, so it's likely that you will have to use Docker anyways, if you go for these tasks.

It might take a significant amount of time and resources to run the assignments code, but we expect that an average laptop is enough to accomplish the tasks. All assignments were tested in the Docker on Mac with 8GB RAM. If you have memory errors, that could be caused by not tested configurations or inefficient code. Consider reporting these cases or double-checking your code.

For the final project, you will need to set up AWS machine - see [AWS tutorial here](AWS-tutorial.md). You are also welcome to try it out earlier during the course.
