#!/usr/bin/env python
# coding: utf-8

# # Analysis of Movie data across various streaming platforms

# # Project overview:

# Our dataset consists of movies across various streaming platforms like Netflix, Hulu, Prime Video and Disney plus. This dataset contains columns like movie name, release year, movie ratings, genres, etc. We have focused on few attributes in this analysis which include (but are not limited to): genre, age group, release year, country of production etc.
# 
# Following are some of the key questions which we have tried to answer from our analysis:
# - Analyzing the genre-platform relationship e.g. movies of which genre are streamed more on which platform? <br>
# - Identifying the target age group for each platform <br>
# - Analyze the release year attribute to find which platform has most of the new movies.<br>
# - Study the country wise production for each platform.
# 
# In addition to this, we have also tried to elaborate on any common trends, exceptions observed in the pattern and what could be the cause for it.
# 
# <!-- We have performed analysis to find answers to the questions like movies of which genre are streamed mostly on which platform? or which countries have the largest movie production on which platform? or Relation between age group and streaming platforms or are new movies or old movies mostly streamed online -->

# # ReadMe
# To run our project the following libraries are needed: pandas, numpy, matplotlib, plotly, pycountry <br>
# These libraries can be installed using the command
# >pip install library-name

# In[1]:


#Path for the dataset
path = ''
file = path + 'MoviesOnStreamingPlatforms_updated.csv'


# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import pycountry


# In[3]:


#Read csv
movie_data = pd.read_csv(file)
movie_data.head()


# In[4]:


#check datatypes
movie_data.dtypes


# # I. Data cleaning and pre-processing

# From the above data, we can see the first column has just the row ids and it does not give any other information apart from the row number.
# Also, the Type column has all the values set to 0
# Since both these columns do not hold any information that will impact our analysis, we can drop the columns from our data frame.

# In[5]:


#Dropping columns which contain no value for our analysis
movie_data = movie_data.drop(columns = ['Unnamed: 0', 'Type'])
movie_data


# Check if the dataset contains any missing values

# In[6]:


missing_data = movie_data.isna().sum()
missing_data


# We can observe that 8/15 columns have missing values. These missing values can be replaced by an empty string or 0 for number columns

# In[48]:


#replace null values with empty string
movie_data.fillna('',inplace = True)


# In[8]:


#converting string to float for numeric columns
movie_data['IMDb'] = movie_data['IMDb'].str[:3].replace('',0).astype(float)
movie_data['Rotten Tomatoes'] = movie_data['Rotten Tomatoes'].str[:2].replace('',0).astype(float)
movie_data['Runtime'] = movie_data['Runtime'].replace('',0).astype(float)
movie_data


# In[9]:


missing_data = movie_data.isna().sum()
missing_data


# Thus all the missing data is handled

# In[10]:


#copy of dataframe
df = movie_data
df.shape


# In our dataset,the columns Genres, Directors, Languages and Country have multiple values in one cell. Thus if we perform one hot encoding and create a separate column for every value then it would be easier for us to perform further analysis

# In[49]:


#One hot encoding
df = pd.concat([df,df['Genres'].str.get_dummies(sep = ","),df['Directors'].str.get_dummies(sep = ","),
              df['Country'].str.get_dummies(sep = ","),df['Language'].str.get_dummies(sep = ",")], axis = 1)
df


# The data is now cleaned and encoded and ready for us to perform our exploratory analysis

# # II. Exploratory Analysis

# # Finding the relation between different movie genres and streaming platforms

# In[12]:


#Making a list of different genres of movies in our dataset
list_all = df['Genres'].str.split(',').to_numpy()
list_unique = np.unique(sum(list_all, []))
print(list_unique)


# In[13]:


#creating a separate dataframe for each streaming platform
netflix_data = df[(df['Netflix'] == 1)]
hulu_data = df[(df['Hulu'] == 1)]
prime_data = df[(df['Prime Video'] == 1)]
disney_data = df[(df['Disney+'] == 1)]


# In[14]:


#Genre count for each platform
category=[]
netflix_count=[]
disney_count=[]
hulu_count=[]
prime_count=[]
for i in df.columns:
    if i in list_unique:
        category.append(i)
        if i in netflix_data:
            netflix_count.append(netflix_data[i].sum())
        if i in hulu_data:
            hulu_count.append(hulu_data[i].sum())
        if i in prime_data:
            prime_count.append(prime_data[i].sum())
        if i in disney_data:
            disney_count.append(disney_data[i].sum())
genre_data=pd.DataFrame({'Genre':category, 'Netflix Count':netflix_count,'Hulu Count':hulu_count,
                      'Prime Count':prime_count,'Disney Count':disney_count})
genre_data


# We have created a dataframe with the count of movies of a specific genre on different streaming platforms. We will also calculate total number of movies on a platform

# In[15]:


#Calculating total number of movies on a platform
netflix_total=genre_data['Netflix Count'].sum()
prime_total=genre_data['Prime Count'].sum()
hulu_total=genre_data['Hulu Count'].sum()
disney_total=genre_data['Disney Count'].sum()
total_count=netflix_total+prime_total+hulu_total+disney_total


# In[16]:


streaming_platform=['Netflix','Prime Video','Hulu','Disney Plus']
x=[netflix_total,prime_total,hulu_total,disney_total]
pie, ax = plt.subplots(figsize=[10,5])
plt.pie(x, autopct="%.1f%%", explode=[0.06]*4, labels=streaming_platform, shadow=True)
plt.title("Movie count by Streaming Platform")
plt.tight_layout()
plt.show()


# From the above plot we can see that Prime video has the most content of all the platforms. We can further plot these results according to genre

# # Plot

# In[17]:


x=[]
x=genre_data.iloc[:,0].tolist()
net=genre_data.iloc[:,1].tolist()
hulu=genre_data.iloc[:,2].tolist()
prime=genre_data.iloc[:,3].tolist()
disney=genre_data.iloc[:,4].tolist()
# genre_data.plot.bar()


# In[18]:


barWidth = 0.2
fig = plt.subplots(figsize =(20, 10))

br1 = np.arange(len(net))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
br4 = [x + barWidth for x in br3]

plt.bar(br1, net, width = barWidth,
        edgecolor ='grey', label ='Netflix')
plt.bar(br2, hulu,  width = barWidth,
        edgecolor ='grey', label ='Hulu')
plt.bar(br3, prime, width = barWidth,
        edgecolor ='grey', label ='Prime Video')
plt.bar(br4, disney, width = barWidth,
        edgecolor='grey', label ='Disney Plus', linewidth=1)

plt.xlabel('Genre', fontweight ='bold', fontsize = 12)
plt.ylabel('No. of movies', fontweight ='bold', fontsize = 12)
plt.xticks([r + barWidth for r in range(len(net))],
        x, rotation=90)
plt.title('No. of Movies on a platform',fontweight ='bold', fontsize = 12)
plt.legend()
plt.show()


# Conclusions from above graph:
# - Most of the comedy, drama, action, romance, thriller, documentaries, mystery movies are on Netflix and 
# Prime
# - Disney has mostly animated, family and short films
# - Hulu has all type of movies in a mid range. <br>
# Since the genre distribution is different across platforms it would be interesting to see if the audience age group also has some pattern to it.

# # Relation between age group and streaming platforms

# In[19]:


#check different age groups
list_age = df['Age'].str.split(',').to_numpy()
unique_age = np.unique(sum(list_age, []))
print(unique_age)


# In[20]:


#platform wise age criteria
netflix_age_grp = netflix_data['Age'].value_counts().rename_axis('Age').reset_index(name='Netflix Count')

hulu_age_grp = hulu_data['Age'].value_counts().rename_axis('Age').reset_index(name='Hulu Count')

prime_age_grp = prime_data['Age'].value_counts().rename_axis('Age').reset_index(name='Prime Count')

disney_age_grp = disney_data['Age'].value_counts().rename_axis('Age').reset_index(name='Disney Count')

age_data=pd.merge(netflix_age_grp,hulu_age_grp, on='Age')
age_data=pd.merge(age_data,prime_age_grp, on='Age')
age_data=pd.merge(age_data,disney_age_grp, on='Age')
age_data=age_data.iloc[1:]
age_data


# we have created a dataframe according to the age criteria for movies on different platforms

# # Plot

# In[21]:


y=[]
y=age_data.iloc[:,0].tolist()
age_net=age_data.iloc[:,1].tolist()
age_hulu=age_data.iloc[:,2].tolist()
age_prime=age_data.iloc[:,3].tolist()
age_disney=age_data.iloc[:,4].tolist()


# In[22]:


barWidth = 0.2
fig = plt.subplots(figsize =(20, 10))

br1 = np.arange(len(age_net))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
br4 = [x + barWidth for x in br3]

plt.bar(br1, age_net, width = barWidth,
        edgecolor ='grey', label ='Netflix')
plt.bar(br2, age_hulu,  width = barWidth,
        edgecolor ='grey', label ='Hulu')
plt.bar(br3, age_prime, width = barWidth,
        edgecolor ='grey', label ='Prime Video')
plt.bar(br4, age_disney, width = barWidth,
        edgecolor='grey', label ='Disney Plus', linewidth=1)

plt.xlabel('Age', fontweight ='bold', fontsize = 12)
plt.ylabel('No. of movies', fontweight ='bold', fontsize = 12)
plt.xticks([r + barWidth for r in range(len(age_net))],
        y, rotation=90)
plt.title('No. of Movies on a platform according to age',fontweight ='bold', fontsize = 12)
plt.legend()
plt.show()


# - As we can see, most of the movies that are available on these platforms are targetting 18+ audience (since that is the age group which has highest number of movies)
# - Netflix, Prime videos, and Hulu target the 18+ audience. 
# - Disney Plus targets kids in age 7+ and 'all' age group ('all' would include children under age 7)
# - Also, if we  notice carefully, the age group 16+ does have movies from different platforms but it is the lowest when compared to other age groups. It seems that no streaming platform specifically targets this age group audience. 

# # Release year
# (Analyzing the newness of the content of each platform)

# In[46]:


#platform wise release year
netflix_year = netflix_data['Year'].value_counts().rename_axis('Year').reset_index(name = 'Netflix Count')

hulu_year = hulu_data['Year'].value_counts().rename_axis('Year').reset_index(name = 'Hulu Count')

prime_year = prime_data['Year'].value_counts().rename_axis('Year').reset_index(name = 'Prime Count')

disney_year = disney_data['Year'].value_counts().rename_axis('Year').reset_index(name = 'Disney Count')

year_data = pd.merge(netflix_year,hulu_year, on = 'Year')
year_data = pd.merge(year_data,prime_year, on = 'Year')
year_data = pd.merge(year_data,disney_year, on ='Year')

year_data = year_data.sort_values(['Year'])
year_data


# We have created a dataframe according to release year of movies and sorted it in ascending order for year. We have movies from 1960-2021 in our dataset.

# # Plot

# In[54]:


z = []
z = year_data.iloc[:,0].tolist()
year_net = year_data.iloc[:,1].tolist()
year_hulu = year_data.iloc[:,2].tolist()
year_prime = year_data.iloc[:,3].tolist()
year_disney = year_data.iloc[:,4].tolist()


# In[25]:


barWidth = 0.2
fig = plt.subplots(figsize =(20, 10))

br1 = np.arange(len(year_net))
br2 = [x + barWidth for x in br1]
br3 = [x + barWidth for x in br2]
br4 = [x + barWidth for x in br3]

plt.bar(br1, year_net, width = barWidth,
        edgecolor ='grey', label ='Netflix')
plt.bar(br2, year_hulu,  width = barWidth,
        edgecolor ='grey', label ='Hulu')
plt.bar(br3,year_prime, width = barWidth,
        edgecolor ='grey', label ='Prime Video')
plt.bar(br4, year_disney, width = barWidth,
        edgecolor='grey', label ='Disney Plus', linewidth=1)

plt.xlabel('Year', fontweight ='bold', fontsize = 12)
plt.ylabel('No. of movies', fontweight ='bold', fontsize = 12)
plt.xticks([r + barWidth for r in range(len(year_net))],
        z, rotation=90)
plt.title('No. of Movies on a platform according to year', fontweight ='bold', fontsize = 12)
plt.legend()
plt.show()


# As we can see from the plot above, in the 90s although movies were being released on all the platforms, the count was pretty low. However, from 2004 the number of movies released on the platforms has shown an upward trend. For most of the years (until 2014), Prime was the platform which hosted most of the new movie content but in 2016 Netflix showed a drastic increase (roughly 80%) and it's leading then. 
# 
# One interesting pattern that we can see is that there was a decrease in the number of new movies on each platform in the year 2020 compared to 2019 (although the trend was continuously growing until then). One potential reason can be the decrease in production of movies due COVID-19 break out. This fact holds true for all the platforms except Disney. Although, when compared to other platforms, Disney had lower count of new movies. However, it showed a steady increase in the count in the year 2020.
# 
# (Please note, the data set does not have all the movies for year 2021 but we have still included it in the plotting)
# 

# # Country of Production
# 
# # Which countries have the largest movie production and on which platform

# In[26]:


#check countries list
list_all = df['Country'].str.split(',').to_numpy()
list_country = np.unique(sum(list_all, []))
print(list_country)


# In[27]:


#Overall country wise movie production
cntry=[]
count=[]
for i in df.columns:
    if i in list_country:
        cntry.append(i)
        count.append(df[i].sum())
        
c_data=pd.DataFrame({'Country':cntry, 'Count':count})
c_data=c_data.sort_values(['Count'],ascending=False)
c_data


# Plotting country wise movie production

# In[45]:


barWidth = 0.2
fig = plt.subplots(figsize =(20, 10))

plt.bar(c_data['Country'], c_data['Count'])
plt.xticks(rotation=90)
plt.show()


# We can see from the above plot that most of the movies are originating from United States but we dont get much insights from this plot. So lets break this data according to streaming platforms

# In[29]:


#Country wise movie count for each platform
country=[]
netflix_country_count=[]
disney_country_count=[]
hulu_country_count=[]
prime_country_count=[]
for i in df.columns:
    if i in list_country:
        country.append(i)
        if i in netflix_data:
            netflix_country_count.append(netflix_data[i].sum())
        if i in hulu_data:
            hulu_country_count.append(hulu_data[i].sum())
        if i in prime_data:
            prime_country_count.append(prime_data[i].sum())
        if i in disney_data:
            disney_country_count.append(disney_data[i].sum())
country_data=pd.DataFrame({'Country':country, 'Netflix Count':netflix_country_count,'Hulu Count':hulu_country_count,
                      'Prime Count':prime_country_count,'Disney Count':disney_country_count})
country_data


# # Plot

# We have data for 130 countries in our dataset. From the above plot we can see that it is difficult to form conclusions based on bar graphs for 130 countries. As the data that is to be shown is world wide data, we have used choropleth maps.

# Each country has a ISO code. Thus a code column is made in the dataframe so that it becomes easier to map data on choropleth maps.

# In[30]:


import pycountry 
def alpha3code(column):
    CODE=[]
    for country in column:
        try:
            code=pycountry.countries.get(name=country).alpha_3
            CODE.append(code)
        except:
            CODE.append('None')
    return CODE
# create a column for code 
country_data['CODE']=alpha3code(country_data.Country)
country_data


# There are some countries whose ISO codes are missing. If an ISO code is missing then the data for that country won't be shown on our map plot.
# Below we have identified such countries which don't have any ISO code. These columns are renamed manually so that ISO code is assigned to them.
# 

# In[31]:


print(country_data['Country'].where(country_data['CODE']=='None').to_list())


# In[32]:


country_data = country_data.replace({'Country':{'Bolivia':'Bolivia (Plurinational State of)', 
                  'Congo - Brazzaville':'Congo',
                  'Congo - Kinshasa':'Congo',                                    
                  'Palestinian Territories':'Palestine, State of',
                  'Bosnia & Herzegovina':'Bosnia and Herzegovina',
                  'Serbia and Montenegro':'Serbia',
                  'Hong Kong SAR China':'Hong Kong',                                  
                  'Soviet Union':'Russian Federation',
                   'Russia':'Russian Federation',                             
                  'South Korea':'Korea, Republic of',
                  'Korea':'Korea, Republic of',
                  'Republic of North Macedonia':'North Macedonia',
                  "Côte d’Ivoire":"Côte d'Ivoire",
                  'Federal Republic of Yugoslavia':'Serbia',
                  'Yugoslavia':'Serbia',
                  'Vietnam':'Viet Nam',
                  'Trinidad & Tobago':'Trinidad and Tobago',
                  'West Germany':'Germany',
                  'East Germany':'Germany'
                 }})


# In[33]:


#alpha3code function is called again
country_data['CODE']=alpha3code(country_data.Country)
country_data


# # Plot

# As world wide data is depicted below, different maps are plotted for different platforms.
# Also our dataset does not contain data for all countries. Thus these missing countries are shown as blanks in the map.

# In[34]:


#NETFLIX
fig = px.choropleth(country_data, locations="CODE",
                    color="Netflix Count", 
                    hover_name="Country", 
                    color_continuous_scale="Viridis"
                   )
fig.update_layout(title_text = 'Countrywise distributed Netflix Movies'
                 )
fig.show()


# We can observe from the above plot that most of the netflix content is produced in United States, followed by India.

# In[35]:


#HULU
fig2 = px.choropleth(country_data, locations="CODE",
                    color="Hulu Count", 
                    hover_name="Country", 
                    color_continuous_scale="Viridis"
                   )
fig2.update_layout(title_text = 'Countrywise distributed Hulu Movies'
                 )
fig2.show()


# From the above plot we can see that most of the Hulu content is USA based followed by Canada.

# In[36]:


#PRIME VIDEO
fig3 = px.choropleth(country_data, locations="CODE",
                    color="Prime Count", 
                    hover_name="Country",
                    color_continuous_scale="Viridis"
                   )
fig3.update_layout(title_text = 'Countrywise distributed Prime Video Movies'
                 )
fig3.show()


# From the above plot we can see that most of the Prime video content is from USA followed by Canada and India.

# In[37]:


#DISNEY PLUS
fig3 = px.choropleth(country_data, locations="CODE",
                    color="Disney Count", 
                    hover_name="Country",
                    color_continuous_scale="Viridis"
                   )
fig3.update_layout(title_text = 'Countrywise distributed Disney Plus Movies'
                 )
fig3.show()


# From the above plot we can see that most of the Disney Plus content is USA based followed by Canada.

# Thus we have gained various insights regarding streaming platforms and how the movies that are streamed here are affected by genre, year produced, countries or age group.
