# Natural Language Processing course resources
https://www.coursera.org/learn/language-processing

## Running on Google Colab
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

## Running elsewhere

[AWS](AWS-tutorial.md)

[Docker](Docker-tutorial.md)
