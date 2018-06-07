##################################################################################################################
##                                                                                                              ##  
## This file is used to enter data into a temporary business table which has additional columns for our purpose ##
## This is only for REFERENCE, one should not run this file to build the project                                ##
##                                                                                                              ##
##################################################################################################################


"""
import pymysql
import json

# Open database connection
db = pymysql.connect("localhost","username","password","yelp_db" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

categories_dict = {}
business_list = []

def get_category_data():    
    # Get category data
    query_categories = "SELECT business_id, category FROM yelp_db.category;"
    cursor.execute(query_categories)
    
    data = list(cursor.fetchall())
    
    for i in range(cursor.rowcount):
        if (categories_dict.get(data[i][0]) == None):
            categories_dict[data[i][0]] = []
        categories_dict[data[i][0]].append(data[i][1])

def build_business_data():
    # Build Bussiness data
    query = "SELECT b.* FROM yelp_db.business b, yelp_db.category c WHERE b.id = c.business_id AND c.category = 'Restaurants' AND b.review_count > 0;"
    cursor.execute(query)
    
    data = list(cursor.fetchall())
    
    num_rows = cursor.rowcount
    for i in range(num_rows):
        business_list.append(list(data[i]))
        business_list[i].extend((json.dumps(categories_dict[business_list[i][0]]), 0, 0, 0, 0))
    # Last 4 parameters are for storing score, pos_count, neg_count, neutral_count in the table
        
def insert_business_data():
    for i in range(len(business_list)):
        insert(tuple(business_list[i]))
        

def insert(data):
    # Insert query to insert data into business_data
    query = "INSERT INTO business_data(id, name, neighborhood, address, city, state, postal_code, latitude, longitude, stars, review_count, is_open, categories, score, pos_count, neg_count, neutral_count) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ;"
    cursor.execute(query, data)
    db.commit()

get_category_data()
build_business_data()
insert_business_data()

# disconnect from server
db.close()
"""
