import pandas as pd
#import numpy as np
#import csv
from pathlib import Path
#from sys import exit
import os
import seaborn as sns
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

plt.rcParams['figure.dpi'] = 600
plt.rcParams['savefig.dpi'] = 600

sns.set(style = 'darkgrid')

# 'cgtn' or 'chinadaily' or 'globaltimes' or 'xinhuanet'
news = "globaltimes"
paths = sorted(Path("./" + news).iterdir(), key=os.path.getmtime, reverse=True)

China_List = ['China', 'Chinese']
Countries_List = ['EU', 'UK', 'U.S.', 'Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia, Plurinational State of', 'Bonaire, Sint Eustatius and Saba', 'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo', 'Congo, The Democratic Republic of the', 'Cook Islands', 'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 'Holy See (Vatican City State)', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea, Democratic People's Republic of", 'Korea, Republic of', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', 'Macedonia, Republic of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia, Federated States of', 'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territory, Occupied', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Barthélemy', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan, Province of China', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Virgin Islands, British', 'Virgin Islands, U.S.', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']
Nationality_List = ['Afghan', 'Albanian', 'Algerian', 'American', 'Andorran', 'Angolan', 'Antiguans', 'Argentinean', 'Armenian', 'Australian', 'Austrian', 'Azerbaijani', 'Bahamian', 'Bahraini', 'Bangladeshi', 'Barbadian', 'Barbudans', 'Batswana', 'Belarusian', 'Belgian', 'Belizean', 'Beninese', 'Bhutanese', 'Bolivian', 'Bosnian', 'Brazilian', 'British', 'Bruneian', 'Bulgarian', 'Burkinabe', 'Burmese', 'Burundian', 'Cambodian', 'Cameroonian', 'Canadian', 'Cape Verdean', 'Central African', 'Chadian', 'Chilean', 'Colombian', 'Comoran',  'Congolese', 'Costa Rican', 'Croatian', 'Cuban', 'Cypriot', 'Czech', 'Danish', 'Djibouti', 'Dominican', 'Dutch', 'Dutchman', 'Dutchwoman', 'East Timorese', 'Ecuadorean', 'Egyptian', 'Emirian', 'Equatorial Guinean', 'Eritrean', 'Estonian', 'Ethiopian', 'Fijian', 'Filipino', 'Finnish', 'French', 'Gabonese', 'Gambian', 'Georgian', 'German', 'Ghanaian', 'Greek', 'Grenadian', 'Guatemalan', 'Guinea-Bissauan', 'Guinean', 'Guyanese', 'Haitian', 'Herzegovinian', 'Honduran', 'Hungarian', 'I-Kiribati', 'Icelander', 'Indian', 'Indonesian', 'Iranian', 'Iraqi', 'Irish', 'Israeli', 'Italian', 'Ivorian', 'Jamaican', 'Japanese', 'Jordanian', 'Kazakhstani', 'Kenyan', 'Kittian and Nevisian', 'Kuwaiti', 'Kyrgyz', 'Laotian', 'Latvian', 'Lebanese', 'Liberian', 'Libyan', 'Liechtensteiner', 'Lithuanian', 'Luxembourger', 'Macedonian', 'Malagasy', 'Malawian', 'Malaysian', 'Maldivan', 'Malian', 'Maltese', 'Marshallese', 'Mauritanian', 'Mauritian', 'Mexican', 'Micronesian', 'Moldovan', 'Monacan', 'Mongolian', 'Moroccan', 'Mosotho', 'Motswana', 'Mozambican', 'Namibian', 'Nauruan', 'Nepalese', 'Netherlander', 'New Zealander', 'Ni-Vanuatu', 'Nicaraguan', 'Nigerian', 'Nigerien', 'North Korean', 'Northern Irish', 'Norwegian', 'Omani', 'Pakistani', 'Palauan', 'Panamanian', 'Papua New Guinean', 'Paraguayan', 'Peruvian', 'Polish', 'Portuguese', 'Qatari', 'Romanian', 'Russian', 'Rwandan', 'Saint Lucian', 'Salvadoran', 'Samoan', 'San Marinese', 'Sao Tomean', 'Saudi', 'Scottish', 'Senegalese', 'Serbian', 'Seychellois', 'Sierra Leonean', 'Singaporean', 'Slovakian', 'Slovenian', 'Solomon Islander', 'Somali', 'South African', 'South Korean', 'Spanish', 'Sri Lankan', 'Sudanese', 'Surinamer', 'Swazi', 'Swedish', 'Swiss', 'Syrian', 'Taiwanese', 'Tajik', 'Tanzanian', 'Thai', 'Togolese', 'Tongan', 'Trinidadian or Tobagonian', 'Tunisian', 'Turkish', 'Tuvaluan', 'Ugandan', 'Ukrainian', 'Uruguayan', 'Uzbekistani', 'Venezuelan', ' tnamese', 'Welsh', 'Yemenite', 'Zambian', 'Zimbabwean']

data_china = pd.DataFrame()
data_world = pd.DataFrame()

columns = ['CHINA', 'WORLD']

for c in columns:
    data = pd.DataFrame()
    print(c)

    fileList = []
    
    for p in paths:
        temp_str = str(p)
        if temp_str.find(c) != -1:
            fileList.append(str(p))
    
    fileList.reverse()
    for filename in fileList:
        df = pd.read_csv(filename, header = None)
    
        df.columns = ['Time', 'Title']
        
        df = df.drop(columns=['Time'])
    
        df = df.dropna().reset_index(drop=True)
            
        data = pd.concat([data, df], axis = 0)
    
    data = data.drop_duplicates()
    data = data.reset_index(drop=True)
        
    containsCountryName = []
    for i in range(0, len(data)):
        flag = 0
        for c_l in Countries_List:
            r = data['Title'][i].find(c_l)
            if r != -1:
                flag = 1
                break
        if flag == 0:
            for n_l in Nationality_List:
                r = data['Title'][i].find(n_l)
                if r != -1:
                    flag = 1
        for china_l in China_List:
            r = data['Title'][i].find(china_l)
            if r != -1:
                if flag == 0:
                    flag = flag - 1
                    break
                else:
                    flag = flag + 1
                    break
        containsCountryName.append(flag)
    data = pd.concat([data, pd.Series(containsCountryName)], axis=1)

    score = []
    for i in range(0, len(data)):
        title = data['Title'][i]
        vs = analyzer.polarity_scores(title)
        score.append(vs['compound'])
    data = pd.concat([data, pd.Series(score)], axis=1)
    
    #data = data.drop(columns=['Title'])
    
    data.columns = ['Title', 'nation', 'score']
    
    if c == 'CHINA':
        data_china = data
    if c == 'WORLD':
        data_world = data

data_total = pd.concat([data_china, data_world], axis = 0)

data_total = data_total[data_total.nation != 0]

data_total = data_total.reset_index(drop=True)

print(news)

# china only
a = data_total[data_total.nation == -1]
#a = a[a.score != 0.0]
a = a.reset_index(drop=True)
print("domestic: " + str(a['score'].mean()))

# other countries
b = data_total[data_total.nation == 1]
#b = b[b.score != 0.0]
b = b.reset_index(drop=True)
print("foreign: " + str(b['score'].mean()))

# china foreign
c = data_total[data_total.nation == 2]
#c = c[c.score != 0.0]
c = c.reset_index(drop=True)
print("both: " + str(c['score'].mean()))

t1 = pd.DataFrame()
t1 = pd.concat([t1, pd.Series([0.11, -0.14, 0.059])], axis=1)
t1 = pd.concat([t1, pd.Series(['China or Chinese', 'Other Countries', 'Both'])], axis=1)
t1 = pd.concat([t1, pd.Series(['CGTN', 'CGTN', 'CGTN'])], axis=1)

t2 = pd.DataFrame()
t2 = pd.concat([t2, pd.Series([0.086, -0.05718, 0.10038])], axis=1)
t2 = pd.concat([t2, pd.Series(['China or Chinese', 'Other Countries', 'Both'])], axis=1)
t2 = pd.concat([t2, pd.Series(['ChinaDaily', 'ChinaDaily', 'ChinaDaily'])], axis=1)

t3 = pd.DataFrame()
t3 = pd.concat([t3, pd.Series([0.0527, -0.09, -0.042])], axis=1)
t3 = pd.concat([t3, pd.Series(['China or Chinese', 'Other Countries', 'Both'])], axis=1)
t3 = pd.concat([t3, pd.Series(['GlobalTimes', 'GlobalTimes', 'GlobalTimes'])], axis=1)

t4 = pd.DataFrame()
t4 = pd.concat([t4, pd.Series([0.105032, -0.07424, 0.12697])], axis=1)
t4 = pd.concat([t4, pd.Series(['China or Chinese', 'Other Countries', 'Both'])], axis=1)
t4 = pd.concat([t4, pd.Series(['Xinhua', 'Xinhua', 'Xinhua'])], axis=1)

t = pd.DataFrame()
t = pd.concat([t, t1], axis = 0)
t = pd.concat([t, t2], axis = 0)
t = pd.concat([t, t3], axis = 0)
t = pd.concat([t, t4], axis = 0)

t.columns = ['avg', 'Category', 'name']
t = t.reset_index(drop=True)

colors = ["#69b3a2", "#4374B3", "#9569b3"]
sns.set_palette(colors)

plt.figure(figsize=(13, 7))

ax = sns.barplot(
    x="name", 
    y="avg", 
    hue="Category", 
    data=t, 
    ci=None,
    )

ax.set_ylabel("Average Sentiment Score")
ax.set(xlabel=None)
