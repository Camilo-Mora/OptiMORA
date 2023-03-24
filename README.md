# OptiMORA
 Python app to optimize TradingView strategies. Designed by Camilo Mora and developed by LightCannon.
 
 WARNING: Tradingview is known for blocking accounts that use automatized precedures within their plataform. A delay is implemented in this app, which make it very slow to run, and prevent being blocked and overloading their servers. Use this at your own risk. It is recomended that you save all your scripts before using this.
 

## Installation

### Get the ChromeDriver
1. Check the version of Chrome you use. Type "Chrome://version" in your Chrome browser. The version is the number in blue. The first numbers are the important ones.


<img src="https://github.com/Camilo-Mora/OptiMORA/blob/main/Images/ChromeVersion.png" width=60% >


While you are in this part...copy the Profile path (Blue selection in image below), and save it somewhere as you will need it later.


<img src="https://github.com/Camilo-Mora/OptiMORA/blob/main/Images/ProfilePath.png" width=60% >


2. Google "chromedriver download" or go [Here](https://chromedriver.chromium.org/downloads) and donwload the latest driver for your chrome version. It is the one with the same first numbers. In the case above, it is the one for version 111.

3. Download the OptiMORA.exe file in this reposotiry and put it inside a folder.

4. Inside that folder place the Unzipped ChromeDriver you downloaded in step 2.

5. Create an empty folder inside this folder and name it "run", this is where all files will be downloaded to.

6. Set the download folder path in Chrome. Click on the Menu bottom in Chrome (sandwidtch buton on the upper rihgt corner), then click on "Settings"

<img src="https://github.com/Camilo-Mora/OptiMORA/blob/main/Images/Settings.png" width=60% >

The click on "Dowloads", then click on "Change" and direct to the "run" folder you created in step 5.

<img src="https://github.com/Camilo-Mora/OptiMORA/blob/main/Images/SetDownloadFolder.png" width=60% >


## Instructions
Before runing the app you need to settup Tradinview:

1. Opent TradingView, login and load the strategy you want to optimize. Click "Save" the layaout, 


<img src="https://github.com/Camilo-Mora/OptiMORA/blob/main/Images/Save.png" width=60% >


copy the Chart Path

<img src="https://github.com/Camilo-Mora/OptiMORA/blob/main/Images/ChartPath.png" width=60% >


Close Chrome.

2. Double click on the app (Be sure that Chrome is closed). This will open up two windows, in it paste the Chromeprofile Path and the Chart URL you copied above.


<img src="https://github.com/Camilo-Mora/OptiMORA/blob/main/Images/AppGui.png" width=60% >


3. Clicking on "Capture" will collect all the paramters in your stretegy (Be sure that Chrome is closed). All parameters should now appear in the GUI...You may have to expand it, with the buton shown below.

<img src="https://github.com/Camilo-Mora/OptiMORA/blob/main/Images/Expand.png" width=60% >


4. From that GUI, you net to tickmark the parameters you want to optmize, and select any values you want. After you have set the values you want to optimzie, the can be tested on the active ticker, the whole watchlist and in the Deepbacktesting, by clicking on the respective buttons.

The OptiMORA only optmizes values you "Use" in the GUI... you need to be sure to set any default value, before runing the optmization; those default values will not be touched by OptiMora.

