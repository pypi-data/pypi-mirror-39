
# coding: utf-8

# In[ ]:


def summary_data(data):
    """ Function to summarize the average number of steps taken per month
    Parameters:
        data: Apple Health .csv file imported as a Pandas DataFrame
    Return:
        A Pandas dataframe, summarizing the average number of steps taken by month,
        indicated by the last date of the month."""

    import pandas as pd   # to ensure pandas has been imported

    # format the DataFrame
    data['Start'] = pd.to_datetime(data['Start'])
    data =data.drop(['Finish'], axis =1)
    data.columns = ['date', 'distance', 'steps']

    # group data by month and calculate average number of steps per month
    try:
        table = data.groupby(pd.Grouper(key='date',freq='M')).agg({'steps':'mean'})
        table.sort_values(['date'], ascending = True)
        return table
    except:
        data.steps = data.steps.astype(int)
        table = data.groupby(pd.Grouper(key='date',freq='M')).agg({'steps':'mean'})
        table.sort_values(['date'], ascending = True)
        return table
