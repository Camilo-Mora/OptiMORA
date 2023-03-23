# OptiMORA
 Python app to optimize TradingView strategies. Designed by Camilo Mora and developed by LightCannon.
 
 WARNING: Tradingview is known for blocking accounts that use automatized precedures within their plataform. A delay is implemented in this app, which make it very slow to run, and prevent being blocked and overloading their servers. Use this at your own risk. It is recomended that you save all your scripts before using this.
 

## Installation

### Get the ChromeDriver
1. Check the version of Chrome you use. Type "Chrome://version" in your Chrome browser. The version is the number in blue. The first numbers are the important ones.

<img src="https://github.com/Camilo-Mora/OptiMORA/blob/main/Images/ChromeVersion.png" width=100% >

While you are in this part...copy the Profile path (Blue selection in image below), and save it somewhere as you will need it later.

<img src="https://github.com/Camilo-Mora/OptiMORA/blob/main/Images/ProfilePath.png" width=40% >

2. Google "chromedriver download" or go [Here](https://chromedriver.chromium.org/downloads) and donwload the latest driver for your chrome version. It is the one with the same first numbers. In the case above, it is the one for version 111.

3. Download the .exe file in this reposotiry and put it inside a folder.

4. Inside that folder place the Unzipped ChromeDriver you downloaded in step 2.



## Instructions
Before runing the app you need to settup Tradinview:

1. Opent TradingView, login and load the strategy you want to optimize. Click "Save" the layaout, 

<img src="https://github.com/Camilo-Mora/OptiMORA/blob/main/Images/Save.png" width=40% >

copy the Chart Path
<img src="https://github.com/Camilo-Mora/OptiMORA/blob/main/Images/ChartPath.png" width=40% >

Close Chrome.

2. Double click on the app. This will open up two windows, in it paste the Chromeprofile Path and the Chart URL you copied above.

<img src="https://github.com/Camilo-Mora/OptiMORA/blob/main/Images/AppGui.png" width=40% >

3. Clicking on "Capture" will collect all the paramters in your stretegy.

4. From the form, you can select the parameters you want to optimize, and run the optimizations in the active ticker, the whole watchlist and in the Deepbacktesting.

The app only changes the values you "Use" in the GUI... you need to be sure to set any default value, before runing the optmization.

