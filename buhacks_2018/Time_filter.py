
# coding: utf-8

# In[ ]:


data = pd.read_csv("Messages.csv")
data = data.dropna(axis=0)
data = data.reset_index(drop=True)
data['group']=[-1]*len(data)
data['Date_Received'] = pd.to_datetime(data['Date_Received'])
data = data[data['Date_Received'] >= time_15] 
data = data[data['Date_Received'] <= current_time]
data

