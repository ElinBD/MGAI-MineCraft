# Generating a beautiful settlement in Minecraft using PCG
### Koen Bouwman, Elin Dijkstra, Sem Kluiver, Jerry Schonenberg, Tim Schwarz
##### Modern Game AI Algorithms | 20-05-2021

This repository contains the code to generate a beautiful settlement in Minecraft using the MCEdit framework. The generation of the settlement is inspired by dutch towns. It contains multiple filters which can be executed by MCEdit. This is an attempt at solving the [Generative Design in Minecraft competition (GDMC)](https://gendesignmc.engineering.nyu.edu/).

## Contents

* [Requirements](#requirements)
* [Usage](#usage)

## Requirements <div id="requirements"></div>
* python==2.7
* numpy
* pygame==1.9.4
* pyyaml
* pillow
* ftputil==3.4
* PyOpenGL
* PyOpenGL-accelerate
* xlib

## Usage <div id="usage"></div>
All filters of this repository should all be copied to the directory `./GDMC/stock-filters/`. Then, simply run the MCEdit framework with:
```
python mcedit.py
```
Once the startup is completed, open/generate a world and start moving around. Use the following buttons to navigate:
* move around using W/S/A/D
* turn using I/J/K/L
* go up and down using SPACE and SHIFT, respectively

Then, use the left-most button on the toolbar to select a box in which the settlement should be generated. NOTE: our filters only work if the size of the box is large enough, otherwise an error occurs. Also make sure that all trees and hills are inside the box.

Once the box is selected, select the fifth button from the left and select the `Beautiful_settlement` filter. Press the filter button and then a beautiful settlement is generated (this may take a couple of minutes). The filter will print status-updates to the terminal during the generation. Once the terminal contains the message `Generation Completed!`, it is finished.

Moreover, the characteristics of the settlement can be altered in `Beautiful_settings.py`. However, note that the current settings are finetuned for nice looking settlements. Drastically changing one of the settings may result in drastic changes.