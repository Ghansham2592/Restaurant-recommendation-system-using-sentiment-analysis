################
## Background ##
################

This project is based on the dataset which was released by Yelp of it's data challenge. 
Dataset is available at https://www.yelp.com/dataset/download

We used the SQL version to perform operations required in our project since the size of the dataset is huge (7GB).


#########################
## Project Discription ##
########################

We present a system wherein our users can get a list of restaurants by choosing a particular location

They can also choose restaurants based on a particular cuisine. For e.g. Indian food in Phoenix, AZ

Our application will provide them with a list of best restaurants along with their addresses and their open/close status



##################
## Dependencies ##
##################

Bokeh (version: 0.12.10)
pandas (version: 0.20.3)
numpy (version: 1.13.3)
nltk (version: 3.2.4)
sklearn (version: 0.19.1)
json (version: 2.0.9)

pymysql - for MySQL python bridge (One doesn't need to install pymysql since data is exported in txt file)


###########################
## Steps to run the code ##
###########################

1. Open the terminal in the project directory
2. Run the following command: 
    bokeh serve --show main.py
3. Once the bokeh server starts, open the browser window and goto following:
    http://localhost:5006/main
4. Enjoy!


##############################

