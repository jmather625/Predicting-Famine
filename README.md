# Predicting Famine
The purpose of this repository is to predict three different measurements of food insecurity (rCSI, HDDS, and FCS) using satellite imagery. All scripts are put in Jupyter Notebook (.ipynb) files to encourage exploration and modification of the work. I only work with data from Malawi.

# Results
<p align="center">
  <img src="figures/malawi_2016/Malawi_rCSI_results.png" width="400">
  <img src="figures/malawi_2016/Malawi_FCS_results.png" width="400">
  <img src="figures/malawi_2016/Malawi_HDDS_results.png" width="400">
</p>

# Setup
I recommend creating a virtual environment for this project. I prefer using Anaconda.

First run:
```
git clone https://github.com/jmather625/predicting-famine
conda create -n predicting-famine python=3.7 pip gdal
conda activate predicting-famine
conda install pytorch torchvision -c pytorch
pip install -r requirements.txt
```
The libraries that are most likely to fail are gdal and geoio. If a requirement fails to install, first make sure you follow this install procedure exactly. Using `pip` to install GDAL did not work for me, and the only way I got it to install was by including it when I first make the conda environment (hence `pip gdal`). Also, there are several Stack Overflow posts on these issues, so hopefully one will work on your machine.

If you want to run Jupyter Notebooks in an environment, run the following inside the environment:
```
pip install --user ipykernel
python -m ipykernel install --user --name=predicting-famine
```

Then, set the kernel for all the Jupyter files to predicting-famine is.

To allow tqdm (the progress bar library) to run in a Jupyter Notebook, also run:
```
conda install -c conda-forge ipywidgets
```

To get the data, you need to do three things:
1) get the LSMS survey data from the world bank. Download the 2016-2017 Malawi survey data from https://microdata.worldbank.org/index.php/catalog/lsms. The World Bank wants to know how people use their data, so you will have to sign in and explain why you want their data. Make sure to download the CSV version. Unzip the downloaded data into `countries/malawi_2016/LSMS/`. Country name should be `malawi_2016`.
2) get an api key from either Planet or Google's Static Maps API service. Both of these should be free, but Planet may take some time to approve and require you to list a research project to be eligible for the free tier. Google's service should be free if you download under 25k images a day. Save the api keys to `planet_api_key.txt` or `google_api_key.txt` in the root directory. I used Planet's API because then I could download images from 2015 and 2016, whereas Google's service only offers recent images over the last year. The code will show how to get the images.

# Scripts
Run the Jupyter files in the following order:
```
scripts/process_survey_data.ipynb
scripts/download_images.ipynb
scripts/train_cnn.ipynb
scripts/feature_extract.ipynb
scripts/predict_famine_metrics.ipynb
```

In the code itself you should see some comments and lines explaining ever step. Couple points:
- the image download step will take the longest amount of time (several thousand per hour)
- if you are working on a VM like Google's Deep Learning VM, connections can close after extended periods of time. This doesn't stop the script itself from running, but there's no way to see the progress bar in the notebook.
- training the CNN on CPU is something you should try to avoid. Training the CNN took just a few hours on a single GPU, and a forward pass to extract features took just a few minutes. On CPU, those runtimes are at least an order of magnitude higher.

Besides training the CNN from scratch, you can also do one of the following:



# Contact
You can reach me via email at jatinm2@illinois.edu



