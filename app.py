import os
import re
import gc
import io
import numpy as np
import pandas as pd
import scipy.io
import matplotlib.pyplot as plt
plt.switch_backend('agg')
from flask import Flask, render_template, url_for, send_file

app = Flask(__name__)

# Load the meta.csv and other globals once at startup
data = pd.read_csv('meta.csv')
labels = ['I','II','III','aVR','aVL','aVF','V1','V2','V3','V4','V5','V6']
times = np.arange(500)/50
xticks = [i * 0.2 for i in range(51)]


def clear_images():
    for file in os.listdir('static'):
        if '.png' in file:
            os.remove(f'static/{file}') 

def gen_im(name):
    raw_im = np.load(f'static/{name}.npy')
    fig, ax = plt.subplots(12, 1, figsize=(30, 30))
    for ix, lead in enumerate(raw_im):
        ax[ix].plot(times, lead)
        ax[ix].set_ylabel(labels[ix])
        ax[ix].set_xticks(xticks)
        ax[ix].set_yticks([])
        ax[ix].grid(True)

    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    return img


@app.route('/')
@app.route('/<int:index>')
def home(index=0):
    # Set index
    if index >= len(data):
        index = 0  # Restart from the first image if out of bounds
    elif index < 0:
        index = len(data) - 1  # Go to the last image if negative index
    next_index = (index + 1) % len(data)
    previous_index = (index - 1) % len(data)

    # Get name and description
    name, description = data.iloc[index]['name'], data.iloc[index]['Dx']
    
    # Pass the index to the template
    return render_template('main.html', index=index, description=description, next_index=next_index, previous_index=previous_index)

@app.route('/plot_image/<int:index>')
def plot_image(index):
    name = data.iloc[index]['name']
    img = gen_im(name)
    return send_file(img, mimetype='image/png')


if __name__ == '__main__':
    app.run(debug=True)




#Thing to Fix
#make a temp file in static for the images
#allow it to produce several images in advance
