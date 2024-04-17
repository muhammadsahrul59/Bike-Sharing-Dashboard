# <div align="center">🚲 Bike Sharing Dashboard ✨</div>

Streamlit Cloud: <a href='https://bike-sharing-dashboard-project-sahrul.streamlit.app/' target='_blank' title='Bike Sharing Dashboard | Streamlit'>Bike Sharing Dashboard</a>

## Preview

![demo_gif](https://github.com/muhammadsahrul59/Bike-Sharing-Dashboard/assets/101655285/2b0ce4fd-e043-4ada-bb96-96ac6ead232e)


## Description

This project is part of the bike sharing data analysis project to analyze the <a href='https://drive.google.com/drive/folders/1Jfqu10ea7MCZK6pImhz1jfipNZ94jTeS?usp=sharing' target='_blank' title='Bike-sharing-dataset.zip'>Bike Sharing Dataset</a>. The results of the analysis are then made into the form of data visualization into an interactive dashboard.

## Directory

- `/image`: stores image and video assets used in this project
- `/dashboard`: contains the file `cleaned_bikeshare` which is for the dashboard, and file 'dashboard.py' to run the dashboard
- `/data`: stores data used in the data analysis project
- `README.md`: file that provides information about this GitHub project
- `dashboard.py`: main file to run the dashboard
- `notebook.ipynb`: interactive jupyter notebook files to analyze data
- `requirements.txt`: file that stores information about the libraries used in this project

## Setup environment
```
conda create --name main-ds python=3.9
conda activate main-ds
pip install numpy pandas plotly scipy matplotlib seaborn streamlit
```

## Run streamlit app
```
streamlit run dashboard.py
```
or
```
python -m streamlit run dashboard.py
```
## Run the notebook on Google Colab
```
- Download the file above
- open https://colab.research.google.com/
- Upload the file notebook.ipynb
```

or you can open it with this Google Colab Link below :

<a href="https://colab.research.google.com/drive/13Dq69DRVNNtTMNqRz27WtqMuL_qFwC6W?usp=sharing" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>
