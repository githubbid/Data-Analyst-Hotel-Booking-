#!/usr/bin/env python
# coding: utf-8

# # Importing Libraries

# In[2]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


# # Loading the dataset

# In[3]:


df = pd.read_csv('hotel_bookings 2.csv')


#  # Exploratory Data Analysis and Data cleaning

# In[4]:


df.head() #return first 5 values


# In[7]:


df.tail()  #return last 5 values from table (5 is defalut )


# In[9]:


df.shape # returns how many no of rows and cloums present in table


# In[10]:


df.columns #returns columns (0 represents booking not cancelled and 1 represent booking cancelled)


# In[13]:


df.info()  #returns the data type of columns


# In[12]:


df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])  #convert a data type 


# In[14]:


df.describe(include = 'object') #returing a data of object columns


# In[15]:


for col in df.describe(include = 'object').columns:
    print(col)
    print(df[col].unique())
    print('-'*50)


# In[16]:


df.isnull().sum()  #returns column names and total valus which are missing 


# In[21]:


df.describe() 


# In[22]:


df = df[df['adr']<5000]


# # Data Analysis and Visualizations

# In[31]:


#we will see that in data set how much amount of data is there which is cancelled and which was not cancelled we will see % and count
cancelled_perc = df['is_canceled'].value_counts(normalize = True)
cancelled_perc #0 not canclled , 1 cancelled


# In[28]:


plt.figure(figsize = (5,4))  #1 vistualization
plt.title('Reservation status count')
plt.bar(['Not Canceled','Canceled'],df['is_canceled'].value_counts(), edgecolor = 'k', width = 0.7)
plt.show()


# In[36]:


#depending on hotels which hotel rates has high cancellation and which hotels has less cancellation rate we use count plot
plt.figure(figsize = (8,4))# set the plotes
ax1= sns.countplot(x = 'hotel', hue = 'is_canceled', data = df, palette = 'Blues' ) # we are using seaborn libraries countplot, on the basis of
# is_cancelled we are counting and data come from df.

# for data beutyfy lower details 
legend_labels,_ = ax1. get_legend_handles_labels()
ax1.legend (bbox_to_anchor=(1,1))
plt.title('Reservation status in different hotels', size = 20)
plt.xlabel('hotel')
plt.ylabel('number of reservations')
plt.legend(['not canceled', 'canceled'])
plt.show()


# In[37]:


resort_hotel = df[df['hotel'] == 'Resort Hotel']
resort_hotel['is_canceled'].value_counts(normalize = True) #in resort hotel 72 % is  not getting cancelled and 27 is cancelled


# In[38]:


city_hotel = df[df['hotel'] == 'City Hotel']
city_hotel['is_canceled'].value_counts(normalize = True)


# In[39]:


resort_hotel = resort_hotel.groupby('reservation_status_date')[['adr']].mean()
city_hotel = city_hotel.groupby('reservation_status_date')[['adr']].mean()


# In[41]:


plt.figure(figsize = (20,8)) 
plt.title('Average Daily Rate in City and Resort Hotel', fontsize = 30)
plt.plot(resort_hotel.index, resort_hotel['adr'], label = 'Resort Hotel')
plt.plot(resort_hotel.index, resort_hotel['adr'], label = 'City Hotel')
plt.legend(fontsize = 20)
plt.show()


# In[43]:


#on which months reservations are higher and lower 
df['month'] = df['reservation_status_date'].dt.month  #reservation status per month
plt.figure(figsize = (16,8))
ax1 = sns.countplot(x = 'month', hue = 'is_canceled', data = df, palette = 'bright')
legend_labels,_ = ax1. get_legend_handles_labels()
ax1.legend(bbox_to_anchor=(1,1))
plt.title('Reservation status per month', size = 20)
plt.xlabel('month')
plt.ylabel('number of reservations')
plt.legend(['not canceled', 'canceled '])
plt.show()


# In[46]:


#we will perform visualization on cancellation only we we want to find the affect of cancellation rate on which month
plt.figure(figsize = (15,8))
plt.title('ADR per month', fontsize = 30)
sns.barplot('month', 'adr', data = df[df['is_canceled'] == 1].groupby('month')[['adr']].sum().reset_index())
plt.legend(fontsize = 20)
plt.show() #on august the cancellation rate is low and in jan highest cancellation rate 


# In[49]:


cancelled_data = df[df['is_canceled']==1]
top_10_country = cancelled_data['country'].value_counts()[:10]
plt.figure(figsize = (8,8))
plt.title('Top 10 coutries with reservation cancelled')
plt.pie(top_10_country, autopct = '%.2f', labels = top_10_country.index)
plt.show()


# In[ ]:


#company should work on these as they should do advertisment, do camps and provide good services to increse the reservation
#should lower some prize of room to increase customers and can provide so much facilty at the same pacakage 


# In[50]:


#from which sources all customers are comming for reservation
df['market_segment'].value_counts()


# In[51]:


#percentage of people coming from different sources for reservation
df['market_segment'].value_counts(normalize = True)


# In[52]:


#people from which sources are canclling more
cancelled_data['market_segment'].value_counts(normalize = True)


# In[53]:


cancelled_df_adr = cancelled_data.groupby('reservation_status_date')[['adr']].mean()
cancelled_df_adr.reset_index(inplace = True)
cancelled_df_adr.sort_values('reservation_status_date', inplace = True)

not_cancelled_data = df[df['is_canceled'] == 0]
not_cancelled_df_adr = not_cancelled_data.groupby('reservation_status_date')[['adr']].mean()
not_cancelled_df_adr.reset_index(inplace = True)
not_cancelled_df_adr.sort_values('reservation_status_date', inplace = True)

plt.figure(figsize = (20,6))
plt.title('Average Daily Rate')
plt.plot(not_cancelled_df_adr['reservation_status_date'],not_cancelled_df_adr['adr'], label = 'not cancelled')
plt.plot(cancelled_df_adr['reservation_status_date'],cancelled_df_adr['adr'], label = 'cancelled')
plt.legend()


# In[55]:


cancelled_df_adr = cancelled_df_adr[(cancelled_df_adr['reservation_status_date']>'2016') & (cancelled_df_adr['reservation_status_date']<'2017-09')]
not_cancelled_df_adr = not_cancelled_df_adr[(not_cancelled_df_adr['reservation_status_date']>'2016') & (not_cancelled_df_adr['reservation_status_date']<'2017-09')]


# In[60]:


plt.figure(figsize = (20,6))
plt.title('Average Daily rate', fontsize = 30)
plt.plot(not_cancelled_df_adr['reservation_status_date'],not_cancelled_df_adr['adr'],label = 'not cancelled')
plt.plot(cancelled_df_adr['reservation_status_date'],cancelled_df_adr['adr'], label = 'cancelled')
plt.legend(fontsize = 20)
plt.show()
#this plot will provide us more information as compare to earlier graph


# In[ ]:




