## SECTION 1 : PROJECT TITLE
### Earthquake Damage Risk Assessor
<img src="misc/logo.png" style="float: left; margin-right: 0px;" />

## SECTION 2 : EXECUTIVE SUMMARY

## SECTION 3 : TEAM MEMBERS

| Full Name | Student ID | Email |
|-----------|------------|-------|
|Toh Kah Khek|A0229968E|E0687376@u.nus.edu|
|Jeon Sungmin|A0133374J|E0689806@u.nus.edu|
|Yee Wei Liang|A0045422R|E0258287@u.nus.edu|

## SECTION 4 : VIDEO PRESENTATION

[![](http://img.youtube.com/vi/OBeyQfCPETg/0.jpg)](http://www.youtube.com/watch?v=OBeyQfCPETg "Video Presentation")


## SECTION 5 : SYSTEM ARCHITECTURE


## SECTION 5 : INSTALLATION AND USER GUIDE
**Installation guide for Ubuntu 20.04**

1. Navigate to folder of your choice and download the github repository

   command: git clone https://github.com/IRS-JSSW/HDBResalePriceRecommender

   <img src="Miscellaneous/Install Guide/Step1-1.png" style="float: left; margin-right: 0px;" />
   <img src="Miscellaneous/Install Guide/Step1-2.png" style="float: left; margin-right: 0px;" />

2. Install pip3 package

   command 1: sudo apt-get update
   
   command 2: sudo apt-get install python3-pip

   <img src="Miscellaneous/Install Guide/Step2-1.png" style="float: left; margin-right: 0px;" />
   <img src="Miscellaneous/Install Guide/Step2-2.png" style="float: left; margin-right: 0px;" />

3. Install virtualenv package

   command: sudo pip3 install virtualenv

   <img src="Miscellaneous/Install Guide/Step3.png" style="float: left; margin-right: 0px;" />

4. Navigate to HDBResalePriceRecommender and create virtualenv

   command: virtualenv -p python3 venv

   <img src="Miscellaneous/Install Guide/Step4-1.png" style="float: left; margin-right: 0px;" />
   <img src="Miscellaneous/Install Guide/Step4-2.png" style="float: left; margin-right: 0px;" />

5. Activate virtualenv

   command: source venv/bin/activate (Note: Ensure that you are seeing (venv) in the terminal)

   <img src="Miscellaneous/Install Guide/Step5.png" style="float: left; margin-right: 0px;" />

6. Install project dependencies from requirements.txt

   command: pip install -r requirements.txt

   | **No** | **Package** | **Version** |
   |----|---------|---------|
   | 1 | flask | 1.1.2 |
   | 2 | flask-wtf | 0.14.3 |
   | 3 | haversine | 2.3.0 |
   | 4 | requests | 2.25.1 |
   | 5 | selenium | 3.141.0 |
   | 6 | sklearn |---------|
   | 7 | sqlalchemy | 1.3.23 |

   <img src="Miscellaneous/Install Guide/Step6.png" style="float: left; margin-right: 0px;" />

**User guide**
**Part 1 - To start the app**
1. Navigate to HDBResalePriceRecommender and activate virtualenv
   
   command: source venv/bin/activate (Note: Ensure that you are seeing (venv) in the terminal) 
   
   <img src="Miscellaneous/User Guide/Step1-1.png" style="float: left; margin-right: 0px;" />
   <img src="Miscellaneous/User Guide/Step1-2.png" style="float: left; margin-right: 0px;" />

2. Start the flask application on local machine

   command: project run.py

   <img src="Miscellaneous/User Guide/Step2.png" style="float: left; margin-right: 0px;" />

3. Open browser (Firefox or Google Chrome) and navigate to URL http://127.0.0.1:5000/home

   <img src="Miscellaneous/User Guide/Step3.png" style="float: left; margin-right: 0px;" />

**Part 2 - To get predicted price of HDB Resale Flats**
1. Input valid Propertyguru Resale HDB listing in textbox and click on the Search button

   <img src="Miscellaneous/User Guide/Step4.png" style="float: left; margin-right: 0px;" />

2. Results of predicted price and other recommended Propertyguru listings will be generated

   <img src="Miscellaneous/Images/Poster.png" style="float: left; margin-right: 0px;" />

**Part 3 - To update HDB Resale Transactions Records from Data.gov**

1. Click on “Update” on the navigation bar and click on “Update Data Gov Table”

   <img src="Miscellaneous/User Guide/Step6.png" style="float: left; margin-right: 0px;" />

2. Next, select “Yes” in the dropdown menu and click on “Update” button. Selecting “No” will not update the database and redirects back to the homepage

   <img src="Miscellaneous/User Guide/Step7.png" style="float: left; margin-right: 0px;" />

**Part 4 - To update Propertyguru listings**

1. Click on “Update” on the navigation bar and click on “Update Propertyguru Table”

   <img src="Miscellaneous/User Guide/Step6.png" style="float: left; margin-right: 0px;" />

2. Next, select “Yes” in the dropdown menu and click on “Update” button. Selecting “No” will not update the database and redirects back to the homepage

   <img src="Miscellaneous/User Guide/Step8.png" style="float: left; margin-right: 0px;" />

**Part 5 - To update Amenities Table**

1. Click on “Update” on the navigation bar and click on “Update Amenities Tables”

   <img src="Miscellaneous/User Guide/Step6.png" style="float: left; margin-right: 0px;" />

2. Next, select “Yes” in the dropdown menu and click on “Update” button. Selecting “No” will not update the database and redirects back to the homepage

   <img src="Miscellaneous/User Guide/Step9.png" style="float: left; margin-right: 0px;" />

**Part 6 - To train Regression Model**

1. Click on “Update” on the navigation bar and click on “Update Training Model”

   <img src="Miscellaneous/User Guide/Step6.png" style="float: left; margin-right: 0px;" />

2. Next, select “Yes” in the dropdown menu and click on “Train” button. Selecting “No” will not update the regression model and redirects back to the homepage

   <img src="Miscellaneous/User Guide/Step10.png" style="float: left; margin-right: 0px;" />