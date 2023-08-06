import numpy as np
import pandas as pd
import missingno

def show_nulls(input_df):
    if(not isinstance(input_df, pd.DataFrame)):
        print("Can't cleanup an object that is not a dataframe")
        return None
    
    input_df.replace("None", np.nan, inplace = True)
    
    # Matrix that displays data sparsity to see missing/Null values    
    missingno.matrix(input_df,inline=True)
    return missingno.matrix(input_df,inline=False)
