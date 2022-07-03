# -*- coding: utf-8 -*-
"""
<<<<<<< HEAD
Created on Wed Jun 15 17:14:17 2022

@author: leube
Created on Wed Jun 15 15:30:27 2022

@author: matui
>>>>>>> 9e3e1b524221f0a6d71f47353fbac6f42cb887f1
"""

import streamlit as st

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
from scipy import stats
from matplotlib.axis import Axis

from sklearn.preprocessing import LabelEncoder



survival1 = pd.read_csv(r"C:\Users\leube\Ironhack\Ironprojects\Module_2\Project5\clean_surv.csv", sep=",")
################### LAYOUT & INTRO ###################

# st.set_page_config(layout="wide")
st.title('Patient Survival Data')
st.write('Analysis of dead people')
st.sidebar.write('Ferdinand Leube')
st.sidebar.write('Edgar Tomé')
st.sidebar.write('Mathieu Jomain')
st.write('Dataset of ~ 80k rows')
st.text("")
st.text("")

st.write('This data analysis does not serve the purpose of gaining meaningfull real life medical insights. The creator of this project have no medical background what so ever and retrieved this data set for the sole purpose of further practicing data cleaning/processing and getting comfortable with streamlit applications.')

################### Admit source/death - CROSSTAB #######################

#crosstab
st.write('Number of alive/dead people by admission source')
cross1 = pd.crosstab(survival1['icu_admit_source'], survival1['hospital_death'])
cross1 = cross1.rename(columns={0:'Nb alive', 1:'Nb dead'})
st.table(cross1)
cross1
################### gender/death - CROSSTAB #######################

#crosstab
st.write('Number of alive/dead people by gender')
cross2 = pd.crosstab(survival1['gender'], survival1['hospital_death'])
cross2 = cross2.rename(columns={0:'Nb alive', 1:'Nb dead'})
st.table(cross2)

################### ethnicity/death - CROSSTAB #######################

#crosstab
st.write('Number of alive/dead people by ethnicity')
cross3 = pd.crosstab(survival1['ethnicity'], survival1['hospital_death'])
cross3 = cross3.rename(columns={0:'Nb alive', 1:'Nb dead'})
st.table(cross3)

################### STATISTICS #######################
st.write('Statistics for heart rate by gender')
if st.checkbox('Show dataframe'):
        chart_data = (survival1.groupby('gender')['d1_heartrate_max','d1_heartrate_min'].agg(['mean', 'max', 'min']))
        chart_data

st.write('Statistics for glucose rate by gender')
if st.checkbox('Show dataframe',1):
        chart_data2 = (survival1.groupby('gender')['d1_glucose_max','d1_glucose_min'].agg(['mean', 'max', 'min']))
        chart_data2


################### IMAGE #######################
# image = Image.open(r'C:\Users\matui\Downloads\cat.jpg')

data = pd.read_csv(r"C:\Users\leube\Ironhack\Ironprojects\Module_2\Project5\clean_surv.csv")
survival = pd.DataFrame(data)

list_wanted_columns = ['patient_id', 'hospital_id', 'age', 'ethnicity', 'gender', 'height','icu_admit_source','weight','aids','cirrhosis', 'diabetes_mellitus','hepatic_failure', 'immunosuppression', 'leukemia', 'lymphoma','solid_tumor_with_metastasis','hospital_death','d1_heartrate_max', 'd1_heartrate_min','d1_glucose_max', 'd1_glucose_min']
columns = list(survival.columns)
unwanted = [x for x in columns if x not in list_wanted_columns]
for x in unwanted:
    del survival[f'{x}']
    
columns = list(survival.columns)
for x in survival.columns:
    survival.drop(survival[survival[x].isnull()].index, inplace = True)
    
    
conditions = [
    survival['age']<20,
    ((survival['age']>=20)&(survival['age']<30)),
    ((survival['age']>=30)&(survival['age']<40)),
    ((survival['age']>=40)&(survival['age']<50)),
    ((survival['age']>=50)&(survival['age']<60)),
    ((survival['age']>=60)&(survival['age']<70)),
    ((survival['age']>=70)&(survival['age']<80)),
    ((survival['age']>=80)&(survival['age']<90))
]

choices = ['10-20',
           '20-30',
          '30-40',
          '40-50',
          '50-60',
          '60-70',
          '70-80',
          '80-90']

survival['age_bins'] = np.select(conditions, choices, 'huge')

conditions2 = [
    survival['height']<140,
    ((survival['height']>=140)&(survival['height']<150)),
    ((survival['height']>=150)&(survival['height']<160)),
    ((survival['height']>=160)&(survival['height']<170)),
    ((survival['height']>=170)&(survival['height']<180)),
    ((survival['height']>=180)&(survival['height']<190)),
    ((survival['height']>=190)&(survival['height']<200))
]
choices2 = ['130-140',
           '140-150',
           '150-160',
           '160-170',
           '170-180',
           '180-190',
           '190-200']
survival['height_bins'] = np.select(conditions2, choices2, 'huge')


conditions3 = [
    survival['weight']<50,
    ((survival['weight']>=50)&(survival['weight']<70)),
    ((survival['weight']>=70)&(survival['weight']<90)),
    ((survival['weight']>=90)&(survival['weight']<110)),
    ((survival['weight']>=110)&(survival['weight']<130)),
    ((survival['weight']>=130)&(survival['weight']<150)),
    ((survival['weight']>=150)&(survival['weight']<170)),
    ((survival['weight']>=170)&(survival['weight']<190))
]
choices3 = ['30-50',
            '50-70',
            '70-90',
            '90-110',
            '110-130',
            '130-150',
            '150-170',
            '170-190']
survival['weight_bins'] = np.select(conditions3, choices3, 'huge')

survival['gender_encoded'] = LabelEncoder().fit_transform(survival.gender)


def age_pie_chart(sickness):  
    # code to create loop for input of streamlit user input
    chartone = survival[[f'{sickness}','age_bins','patient_id']]
    an = chartone.pivot_table(index=[f'{sickness}'], values=['patient_id'], columns=['age_bins'], aggfunc='count')
    an.reset_index(inplace=True)

    dataforchart = an.loc[an[f'{sickness}']==1].transpose()
    dataforchart.reset_index(inplace=True)
    
    values = dataforchart[1].sum()
    dataforchart.loc[(dataforchart[1]/values < 0.08),'age_bins']='other'
    dataforchart = dataforchart.groupby(by='age_bins').agg({1:'sum'})
    dataforchart.reset_index(inplace=True)
    dataforchart.loc[(dataforchart[1]== np.nan), 1] = 0
    
    #define data
    data = list(dataforchart[1])
    labels = list(dataforchart['age_bins'])
    explode = [0.1 for x in labels]


    #define Seaborn color palette to use
    colors = sns.color_palette('pastel')[0:9]

    #create pie chart
    plt.pie(data,explode = explode, colors = colors, autopct='%.0f%%')
    plt.legend(labels=list(dataforchart['age_bins'].unique()), bbox_to_anchor=(1.2, 1.0), loc='upper left')
    fig.set_size_inches(10, 7)
    return plt.show()

def weight_pie_chart(sickness):  
    # code to create loop for input of streamlit user input
    chartone = survival[[f'{sickness}','weight_bins','patient_id']]
    an = chartone.pivot_table(index=[f'{sickness}'], values=['patient_id'], columns=['weight_bins'], aggfunc='count')
    an.reset_index(inplace=True)

    dataforchart = an.loc[an[f'{sickness}']==1].transpose()
    dataforchart.reset_index(inplace=True)
    
    values = dataforchart[1].sum()
    dataforchart.loc[(dataforchart[1]/values < 0.08),'weight_bins']='other'
    dataforchart = dataforchart.groupby(by='weight_bins').agg({1:'sum'})
    dataforchart.reset_index(inplace=True)
    dataforchart.loc[(dataforchart[1]== np.nan), 1] = 0
    
    #define data
    data = list(dataforchart[1])
    labels = list(dataforchart['weight_bins'])
    explode = [0.1 for x in labels]


    #define Seaborn color palette to use
    colors = sns.color_palette('pastel')[0:9]

    #create pie chart
    plt.pie(data,explode = explode, colors = colors, autopct='%.0f%%')
    plt.legend(labels=list(dataforchart['weight_bins'].unique()),bbox_to_anchor=(1.2, 1.0), loc='upper left')
    fig.set_size_inches(10, 7)
    return plt.show()


def height_pie_chart(sickness):  
    # code to create loop for input of streamlit user input
    chartone = survival[[f'{sickness}','height_bins','patient_id']]
    an = chartone.pivot_table(index=[f'{sickness}'], values=['patient_id'], columns=['height_bins'], aggfunc='count')
    an.reset_index(inplace=True)

    dataforchart = an.loc[an[f'{sickness}']==1].transpose()
    dataforchart.reset_index(inplace=True)
    
    values = dataforchart[1].sum()
    dataforchart.loc[(dataforchart[1]/values <= 0.08),'height_bins']='other'
    dataforchart = dataforchart.groupby(by='height_bins').agg({1:'sum'})
    dataforchart.reset_index(inplace=True)
    dataforchart.loc[(dataforchart[1]== np.nan), 1] = 0
    
    #define data
    data = list(dataforchart[1])
    labels = list(dataforchart['height_bins'])
    explode = [0.1 for x in labels]


    #define Seaborn color palette to use
    colors = sns.color_palette('pastel')[0:9]

    #create pie chart
    plt.pie(data,explode = explode, colors = colors, autopct='%.0f%%')
    plt.legend(labels=list(dataforchart['height_bins'].unique()),bbox_to_anchor=(1.2, 1.0), loc='upper left')
    fig.set_size_inches(10, 7)
    return plt.show()


def gender_sickness(sickness):
    
    charttwo = survival[[f'{sickness}','patient_id','gender_encoded']]

    an = charttwo.pivot_table(index=[f'{sickness}'], values=['patient_id'], columns=['gender_encoded'], aggfunc='count')
    an.reset_index(inplace=True)

    dataforchart = an[an[f'{sickness}']==1]
    dataforchart.rename(columns={0:'female',1:'male'}, inplace=True)

    del dataforchart[f'{sickness}']
    dataforchart=dataforchart.transpose()
    dataforchart.reset_index(inplace=True)

    sns.barplot(x='gender_encoded', y=1, data=dataforchart)
    fig.set_size_inches(10, 7)
    plt.legend()
    return plt.show()


def death_sickness(sickness):
    
    charttwo = survival[[f'{sickness}','patient_id','hospital_death']]

    an = charttwo.pivot_table(index=[f'{sickness}'], values=['patient_id'], columns=['hospital_death'], aggfunc='count')
    an.reset_index(inplace=True)
    dataforchart = an[an[f'{sickness}']==1]
    dataforchart.rename(columns={0:'alive',1:'dead'}, inplace=True)
    
    del dataforchart[f'{sickness}']
    dataforchart=dataforchart.transpose()
    dataforchart.reset_index(inplace=True)

    sns.barplot(x='hospital_death', y=1, data=dataforchart)
    fig.set_size_inches(10, 7)
    plt.legend()
    return plt.show()


option = st.selectbox(
     'What sickness would you like to see analyzed?',
     ('cirrhosis', 'aids', 'diabetes','hepatic_failure','immunosuppression','leukemia','lymphoma','solid_tumor_with_metastasis'))

st.header(option)

diseases = ['cirrhosis', 'aids', 'diabetes','hepatic_failure','immunosuppression','leukemia','lymphoma','solid_tumor_with_metastasis']

for disease in diseases:
    if disease == option:
        st.header('the amount of cases that end in death ')       
        fig, ax = plt.subplots()
        ax = death_sickness(option)
        st.pyplot(fig)
        
        st.header(f'the gender distribution for {option}')       
        fig, ax = plt.subplots()
        ax = gender_sickness(option)
        st.pyplot(fig)
        
        st.header(f'the height(in cm) distribution for {option}')       
        fig, ax = plt.subplots()
        ax = height_pie_chart(option)
        st.pyplot(fig)
        
        st.header(f'the weight(in kg) distribution for {option}')       
        fig, ax = plt.subplots()
        ax = weight_pie_chart(option)
        st.pyplot(fig)

        st.header(f'the age distribution for {option}')       
        fig, ax = plt.subplots()
        ax = age_pie_chart(option)
        st.pyplot(fig)  




## function to show certain statistical info for data of sickness
from scipy.stats import ttest_ind

def stats_info_two_sick_same_survival(sickness1,sickness2):
    datasick1 = survival[survival[sickness1]==1]
    datasick2 = survival[survival[sickness2]==1]
    i = ttest_ind(datasick1['hospital_death'],datasick2['hospital_death'], equal_var=False).pvalue
    
    if i>0.05:
        return 'With a 95% confidence level we can say that patients with either of the two diseases have a similar death rate'
    else:
        return 'The survival rate for the patients with the two diseases are significantly different'


select1 = st.selectbox(
     'What disease would you like to choose?',
     ('cirrhosis', 'aids', 'diabetes','hepatic_failure','immunosuppression','leukemia','lymphoma','solid_tumor_with_metastasis'))

select2 = st.selectbox(
     'What sickness would you like to compare the previous disease to?',
     ('cirrhosis', 'aids', 'diabetes','hepatic_failure','immunosuppression','leukemia','lymphoma','solid_tumor_with_metastasis'))

st.header(select1, select2)


for disease1 in diseases:
    for disease2 in diseases:
        if disease1 == select1 and disease2 == select2:
            a = stats_info_two_sick_same_survival(disease1,disease2)
            st.write(a)
            


numh = survival['hospital_id'].nunique()
nump = survival['patient_id'].nunique()

st.write(f'The data has been collected from over {numh} different hospitals and summarizes data taken from over {nump}.')