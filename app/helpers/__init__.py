from datetime import datetime as dt

# get current date_time
def current_dt():
    return dt.now().strftime("%d/%m/%Y %H:%M:%S")


# remove _id of database
def serialize(response):
    del response["_id"]
    return response
