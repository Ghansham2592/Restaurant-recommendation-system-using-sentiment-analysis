######################################################################################################################
##                                                                                                                  ##  
## This file is used to score businesses. A business_data.txt file is exported which has all the necessary data     ##
## This is only for REFERENCE, one should not run this file to build the project. The above file has been exported  ##
##                                                                                                                  ##
######################################################################################################################


"""
import pymysql
from sentiment_analysis import sentiment_analysis

# Open database connection
db = pymysql.connect("localhost","root","akash123","yelp_db" )

# prepare a cursor object using cursor() method
cursor = db.cursor()
# Create an object of sentiment analysis class
senti = sentiment_analysis()

business_list = []
reviews_dict = {}
update_query = []
count = 1

def get_all_reviews():
    # Fetch all the reviews from database
    query = "SELECT r.business_id, text FROM yelp_db.review r, yelp_db.business_data b WHERE b.id = r.business_id;"
    cursor.execute(query)
    data = list(cursor.fetchall())
    for i in range(cursor.rowcount):
        if (reviews_dict.get(data[i][0]) == None):
            reviews_dict[data[i][0]] = []
        reviews_dict[data[i][0]].append(data[i][1])
    
    
def get_business():
    # Get business ids to assign the score
    query = "SELECT id FROM yelp_db.business_data;"
    cursor.execute(query)
    data = list(cursor.fetchall())
    for i in range(cursor.rowcount):
        get_reviews(data[i][0])

def get_reviews(id):
    # Invoke score calculation function for business
    reviews = reviews_dict[id]
    get_scores(id, reviews)

def get_confidence_score(num_reviews):
    # Return the confidence level of the business based on number of reviews it has
    if (num_reviews > 0 and num_reviews < 5):
        return 1
    elif (num_reviews >= 5 and num_reviews < 10):
        return 1.1
    elif (num_reviews >= 10 and num_reviews < 18):
        return 1.15
    elif (num_reviews >= 18 and num_reviews < 35):
        return 1.2
    elif (num_reviews >= 35 and num_reviews < 70):
        return 1.3
    elif (num_reviews >= 70 and num_reviews < 190):
        return 1.4
    else:
        return 1.5

def get_scores(id, review_list):
    # Calculate score of the business by checking sentiment of the user reviews
    num_reviews = len(review_list)
    num_pos = 0
    num_neg = 0
    num_neutral = 0
    sum = 0
    for i in range(num_reviews):
        tempScore = senti.check_sentiment(review_list[i])
        if (tempScore == 0):
            num_neg += 1
        if (tempScore == 1):
            num_neutral += 1
        if (tempScore == 2):
            num_pos += 1
        if (tempScore == 2 or tempScore == 1):
            sum += tempScore / 2

    confidence_score = get_confidence_score(num_reviews)
    print(sum, num_reviews, confidence_score, num_pos, num_neg, num_neutral, id)
    score = format(( sum / num_reviews ) * confidence_score * 3.33, '.3f')
    business_list.append((id, score))
    update_score(id, score, num_pos, num_neg, num_neutral)

def update_score(id, score, num_pos, num_neg, num_neutral):
    # Update the score of the business in database
    global count, update_query
    count += 1
    query = (score, str(num_pos), str(num_neg), str(num_neutral), id)
    update_query.append(query)

def update():
    # Update query to update score, and sentiment counts in database
    query = "UPDATE yelp_db.business_data SET `score` = %s, `pos_count` = %s, `neg_count` = %s, `neutral_count` = %s  WHERE `id` = %s ; "
    cursor.executemany(query, update_query)
    db.commit()
    

get_all_reviews()
get_business()
# To update the database
update()

# disconnect from server
db.close()
"""