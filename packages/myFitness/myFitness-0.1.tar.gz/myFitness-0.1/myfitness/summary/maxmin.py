
# coding: utf-8

# In[ ]:


def getMax(data):
    """ Find the maximum number of steps in the data and the date it was achieved.
        Parameters:
            data: Pandas DataFrame containing Apple Health data imported from a
                  .csv file.
        Return:
            The row of values for when the maximum number of steps were achieved:
            Start date, Finish date, Distance(mi), Steps (count)"""

    # ensure pandas has been imported

    import pandas as pd

    # Verify datatype in Steps is correct datatype, then find the
    # row containing the maximum steps and return that row.

    try:
        maximum = data.loc[data['Steps (count)'].idxmax()]
        return maximum
    except:
        data['Steps (count)'] = data['Steps (count)'].astype(int)
        maximum = data.loc[data['Steps (count)'].idxmax()]
        return maximum


def getMin(data):
    """ Find the maximum number of steps in the data and the date it was achieved.
        Parameters:
            data: Pandas DataFrame containing Apple Health data imported from a
                  .csv file.
        Return:
            The row of values for when the maximum number of steps were achieved:
            Start date, Finish date, Distance(mi), Steps (count)"""

    #ensure pandas has been imported

    import pandas as pd

    # Verify datatype in Steps is correct datatype, then find the
    # row containing the minimum steps and return that row.

    try:
        minimum = data.loc[data['Steps (count)'].idxmin()]
        return minimum
    except:
        data['Steps (count)'] = data['Steps (count)'].astype(int)
        minimum = data.loc[data['Steps (count)'].idxmin()]
        return minimum
