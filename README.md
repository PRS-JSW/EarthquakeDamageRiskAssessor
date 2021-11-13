## SECTION 1 : PROJECT TITLE
### Earthquake Damage Risk Assessor
<img src="misc/logo.png" style="float: left; margin-right: 0px;" />

## SECTION 2 : EXECUTIVE SUMMARY
On Saturday, 25 April 2015, a 7.6 magnitude earthquake struck Gorkha Nepal. The devastating earthquake was followed by more than 300 aftershocks that has magnitude more than 4.0. These deadly impacts had caused widespread destruction across Nepal’s social and economic infrastructure, roads, residential houses, schools, government building, power plant and even century old heritage monuments. 
Post disaster assessment that was conducted by the government has highlighted that the over half a million houses were destroyed, and the damage was more critical as 58 percent of buildings were made of low strength masonry stone or brick masonry with mud mortar, lacking in seismic-resistant features and some were not built according to the building regulation. 
The government of Nepal has come out with the post disaster support programme. The transitional phase (2015-2018) of the programme has provided temporarily shelters for those who lost their houses. The approach of the long-term recovery activities is owner driven reconstruction and thus, focus on beneficiary identification, which is reviewed based on the survey data collected by the Kathmandu Living Labs and the Central Bureau of Statistics of Nepal. Identified beneficiaries will receive financial, technical and social assistance which will accelerate own recovery effort once their reconstructed building complies to the safe construction standards (Reference: Post Disaster Needs Assessment). According to the National Reconstruction Authority (NRA), 93 percent of beneficiaries has been identified and received the government grant for reconstruction. (Reference: NRA has made 93 percent progress in private housing reconstruction)
However, as the grant for the government were not sufficient for the reconstruction, more than half of households that completed reconstruction built just one- or two-room houses. As the houses they have reconstructed are too small for the whole family, many are often still using either damaged or improvised repair houses for living.
Our group sees that the allocation and distribution of grant can be improved in terms of speed and accuracy. With the use of the dataset that was collected by the Nepal government, our group like to implement the Earthquake Damage Risk Assessor (EDRA) application to assist the government officials of NRA for the faster and more accurate beneficiary identification. 
Our system is designed to provide the users with the predicted damage grade of the building before and after the reconstruction, and thus able to help the user to easily determine whether the building that applied for the reconstruction grant meets the requirements. On the other hand, our system can potentially benefit the grant applicants by helping them with the selection of building style or materials for their reconstruction.  
In summary, we hope that our system can improve the grant selection process for the Nepal’s reconstruction plan and eventually contribute to the speedy recovery of the Nepal from the deadly earthquake.

## SECTION 3 : PROJECT OBJECTIVE
The earthquake that struck Nepal on April 25, 2015, has caused tremendous damage and loss. According to the Nepal Disaster Report 2015, more than 600,000 houses were completed destroyed and caused 649,815 families to be displaced from their house. To identify beneficiaries eligible for housing reconstruction, the government of Nepal has carried out massive household surveys which contained valuable information to assess the building damage in the earthquake affected district. (Reference: Nepal Disaster Report 2015)
The building damage report indicates that structure design and building materials of most of the damaged buildings were unreinforced stone masonry whereas buildings that performed well against the impact were made of reinforced concrete with seismic detailing. This indicates that use of modern civil engineered structural design is the key to minimize the post-earthquake risk in earthquake prone Nepal. (Building typologies and failure modes observed in the 2015 Gorkha (Nepal) earthquake)
With the lesson learnt from the various report and studies, we would like to utilise the building damage data to assess the possible damage risk on the buildings in the earthquake prone region. The damage risk can be used by the government officials to remind the building owners whose buildings are identified as weak to reinforce the structural integrity or plan for a reconstruction.

## SECTION 4 : TEAM MEMBERS

| Full Name | Student ID | Email |
|-----------|------------|-------|
|Toh Kah Khek|A0229968E|E0687376@u.nus.edu|
|Jeon Sungmin|A0133374J|E0689806@u.nus.edu|
|Yee Wei Liang|A0045422R|E0258287@u.nus.edu|

## SECTION 5 : VIDEO PRESENTATION

[![](http://img.youtube.com/vi/OBeyQfCPETg/0.jpg)](http://www.youtube.com/watch?v=OBeyQfCPETg "Video Presentation")


## SECTION 6 : SYSTEM ARCHITECTURE


## SECTION 7 : INSTALLATION AND USER GUIDE
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
