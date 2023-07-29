from fastapi import  APIRouter , Depends
import numpy as np
# # Define the given data as numpy arrays
import pandas as pd
from sklearn.linear_model import LinearRegression
from scipy.interpolate import interp1d
from sqlalchemy.orm import Session
from storage.database import get_db
from cache import cache_set


import warnings
warnings.filterwarnings("ignore")


router = APIRouter()


data = pd.read_csv('./files/excel/trim csv.csv')

@router.get('/api/v1/trim/{imo}')
def index(imo:str , input_speed:float = None  , input_draft:float = None ,db:Session = Depends(get_db)):

    data = cache_set.get_trim_data(db,imo)
    if not data:
         return{'data':[]}
    data = pd.DataFrame(data)
    data['draft'] = data['draft'].astype(float)
    data['speed'] = data['speed'].astype(float)
    data['trim'] = data['trim'].astype(float)
    data['resistance'] = data['resistance'].astype(float)
    data['power'] = data['power'].astype(float)

    draft = np.array(data['draft'])
    speed = np.array(data['speed'])
    trim = np.array(data['trim'])
    resistance = np.array(data['resistance'])
    effective_power = np.array(data['power'])

    # input_trim = 2
    # input_draft = 10.2
    # input_speed = 12.5


    df = pd.DataFrame({'draft': draft, 'speed': speed, 'trim': trim, 'resistance': resistance, 'power': effective_power})

    speed_list = df['speed'].unique()
        
    df_draft = pd.DataFrame(columns = ['draft', 'trim', 'speed', 'resistance'] )

    df2 = pd.DataFrame()

    for i in speed_list:
        row_data = {'speed':i}

        df1 = pd.pivot_table(data[data['speed'] == i], values='resistance', index=['draft'], columns=['trim']).reset_index()

        for j in df1.columns[1:]:
                x = df1['draft'].values
                y = df1[j].values
                
                mymodel = np.poly1d(np.polyfit(x, y, 2))

                row_data[j] = mymodel(input_draft)
        df2 = df2.append(row_data, ignore_index = True)


    speed_list = df2['speed'].unique()


    # exit()
    df3 = pd.DataFrame()

    # for i in speed_list:
    #     row_data = {'speed':i}

    #     dfs = pd.pivot_table(df2[df2['speed'] == i], values='resistance', index=['draft'], columns=['trim']).reset_index()

    #     data_dict = {}
    row_data = {}
    for j in df2.columns[1:]:

        x = df2['speed'].values
        y = df2[j].values
        
        mymodel = np.poly1d(np.polyfit(x, y, 2))

        row_data[j] = mymodel(input_speed)
    df3 = df3.append(row_data, ignore_index = True)

    trim_list = df3.columns.values.tolist()
    values_list = df3.values.tolist()
    print(df3)

    min_value = min(values_list[0])

    idle_trim = df3.idxmin(axis=1).iloc[0]
    
    






    # if input_trim > max(trim):
        
    #     input_trim = max(trim)
        
    # elif input_trim < min(trim):
    #     input_trim = min(trim)

    data_list = []

    def trim_find(input_draft,input_speed,input_trim):

        df = pd.DataFrame({'draft': draft, 'speed': speed, 'trim': trim, 'resistance': resistance, 'power': effective_power})

        speed_list = df['speed'].unique()
            
        df_draft = pd.DataFrame(columns = ['draft', 'trim', 'speed', 'resistance'] )

        df2 = pd.DataFrame()

        for i in speed_list:
            row_data = {'speed':i}

            df1 = pd.pivot_table(data[data['speed'] == i], values='resistance', index=['draft'], columns=['trim']).reset_index()

            for j in df1.columns[1:]:
                    x = df1['draft'].values
                    y = df1[j].values
                    
                    mymodel = np.poly1d(np.polyfit(x, y, 2))

                    row_data[j] = mymodel(input_draft)
            df2 = df2.append(row_data, ignore_index = True)


        speed_list = df2['speed'].unique()


        # exit()
        df3 = pd.DataFrame()

        # for i in speed_list:
        #     row_data = {'speed':i}

        #     dfs = pd.pivot_table(df2[df2['speed'] == i], values='resistance', index=['draft'], columns=['trim']).reset_index()

        #     data_dict = {}
        row_data = {}
        for j in df2.columns[1:]:

            x = df2['speed'].values
            y = df2[j].values
            
            mymodel = np.poly1d(np.polyfit(x, y, 2))

            row_data[j] = mymodel(input_speed)
        df3 = df3.append(row_data, ignore_index = True)

        trim_list = df3.columns.values.tolist()
        values_list = df3.values.tolist()
        min_value = min(values_list[0])
        # print(df3)
        # print(min_value)

        x = trim_list
        y = values_list
        # print(x)
        # print(y)

        y_interp = interp1d(x,y)
        # print(y_interp(input_trim)[0])

        final_result = round((((y_interp(input_trim)[0] - df3[0.00].values)/y_interp(input_trim)[0])*100)[0],2)
        # print("-----------------------------------")
        # print("y_interp(input_trim)[0]:", y_interp(input_trim)[0])
        # print("Oth trim:" , df3[0.00]) 
        # print("input_draft:" , input_draft) 
        # print("input_trim:" , input_trim) 
        # print("input_speed:",input_speed)
        # print("-----------------------------------")
    
        data_dict = {'trim':str(input_trim) ,'draft':str(input_draft) , 'value' : final_result}
        data_list.append(data_dict)

        return final_result
     



    draft_range = [i for i in np.arange(min(draft), max(draft), 0.5)]
    trim_range = [round(i,1) for i in np.arange(min(trim), max(trim), 0.1)]


    for i in draft_range:
        for j in trim_range:
            trim_find(i ,input_speed , j)


    
    return {'data':
            {
            'idle_trim':idle_trim , 
            'data':data_list
            }
        }
