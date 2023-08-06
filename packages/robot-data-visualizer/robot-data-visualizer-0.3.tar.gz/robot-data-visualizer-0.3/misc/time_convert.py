"""Convert epoch time to datetime format and remove subseconds."""
import datetime

def epoch_to_date_time(time):
    """Convert epoch time to datetime format."""
    #convert to string
    time = str(time)
    #remove subseconds
    time = int(time[:10])
    #convert to datetime
    time = datetime.datetime.fromtimestamp(time).strftime('%c')

    return time
