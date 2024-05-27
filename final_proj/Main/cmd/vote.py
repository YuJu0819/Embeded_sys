import pandas as pd
def vote_count():
    # read the test data
    df = pd.read_csv('data/test.csv')
    # convert the last column to a list
    vote = df.iloc[:,-1].values.tolist()
    # build a dictionary to store the vote count
    result = {}
    for v in vote:
        if v in result:
            result[v] += 1
        else:
            result[v] = 1
    return result