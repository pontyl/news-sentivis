import pandas as pd
#import numpy as np
#import csv
from pathlib import Path
#from sys import exit
import os
#import seaborn as sns
import itertools
#import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from pyvis.network import Network
import networkx as nx

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from afinn import Afinn
afinn = Afinn()

stop_words = set(stopwords.words('english'))

analyzer = SentimentIntensityAnalyzer()

#news = "bbc"
# 'cgtn' or 'chinadaily' or 'globaltimes' or 'xinhuanet'
news = "globaltimes"
paths = sorted(Path("./" + news).iterdir(), key=os.path.getmtime, reverse=True)

China_List = ['China', 'Chinese']
Countries_List = ['EU', 'UK', 'U.S.', 'US', 'Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia, Plurinational State of', 'Bonaire, Sint Eustatius and Saba', 'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo', 'Congo, The Democratic Republic of the', 'Cook Islands', 'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 'Holy See (Vatican City State)', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea, Democratic People's Republic of", 'Korea, Republic of', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', 'Macedonia, Republic of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia, Federated States of', 'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territory, Occupied', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Barthélemy', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan, Province of China', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Virgin Islands, British', 'Virgin Islands, U.S.', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']
Nationality_List = ['Afghan', 'Albanian', 'Algerian', 'American', 'Andorran', 'Angolan', 'Antiguans', 'Argentinean', 'Armenian', 'Australian', 'Austrian', 'Azerbaijani', 'Bahamian', 'Bahraini', 'Bangladeshi', 'Barbadian', 'Barbudans', 'Batswana', 'Belarusian', 'Belgian', 'Belizean', 'Beninese', 'Bhutanese', 'Bolivian', 'Bosnian', 'Brazilian', 'British', 'Bruneian', 'Bulgarian', 'Burkinabe', 'Burmese', 'Burundian', 'Cambodian', 'Cameroonian', 'Canadian', 'Cape Verdean', 'Central African', 'Chadian', 'Chilean', 'Colombian', 'Comoran',  'Congolese', 'Costa Rican', 'Croatian', 'Cuban', 'Cypriot', 'Czech', 'Danish', 'Djibouti', 'Dominican', 'Dutch', 'Dutchman', 'Dutchwoman', 'East Timorese', 'Ecuadorean', 'Egyptian', 'Emirian', 'Equatorial Guinean', 'Eritrean', 'Estonian', 'Ethiopian', 'Fijian', 'Filipino', 'Finnish', 'French', 'Gabonese', 'Gambian', 'Georgian', 'German', 'Ghanaian', 'Greek', 'Grenadian', 'Guatemalan', 'Guinea-Bissauan', 'Guinean', 'Guyanese', 'Haitian', 'Herzegovinian', 'Honduran', 'Hungarian', 'I-Kiribati', 'Icelander', 'Indian', 'Indonesian', 'Iranian', 'Iraqi', 'Irish', 'Israeli', 'Italian', 'Ivorian', 'Jamaican', 'Japanese', 'Jordanian', 'Kazakhstani', 'Kenyan', 'Kittian and Nevisian', 'Kuwaiti', 'Kyrgyz', 'Laotian', 'Latvian', 'Lebanese', 'Liberian', 'Libyan', 'Liechtensteiner', 'Lithuanian', 'Luxembourger', 'Macedonian', 'Malagasy', 'Malawian', 'Malaysian', 'Maldivan', 'Malian', 'Maltese', 'Marshallese', 'Mauritanian', 'Mauritian', 'Mexican', 'Micronesian', 'Moldovan', 'Monacan', 'Mongolian', 'Moroccan', 'Mosotho', 'Motswana', 'Mozambican', 'Namibian', 'Nauruan', 'Nepalese', 'Netherlander', 'New Zealander', 'Ni-Vanuatu', 'Nicaraguan', 'Nigerian', 'Nigerien', 'North Korean', 'Northern Irish', 'Norwegian', 'Omani', 'Pakistani', 'Palauan', 'Panamanian', 'Papua New Guinean', 'Paraguayan', 'Peruvian', 'Polish', 'Portuguese', 'Qatari', 'Romanian', 'Russian', 'Rwandan', 'Saint Lucian', 'Salvadoran', 'Samoan', 'San Marinese', 'Sao Tomean', 'Saudi', 'Scottish', 'Senegalese', 'Serbian', 'Seychellois', 'Sierra Leonean', 'Singaporean', 'Slovakian', 'Slovenian', 'Solomon Islander', 'Somali', 'South African', 'South Korean', 'Spanish', 'Sri Lankan', 'Sudanese', 'Surinamer', 'Swazi', 'Swedish', 'Swiss', 'Syrian', 'Taiwanese', 'Tajik', 'Tanzanian', 'Thai', 'Togolese', 'Tongan', 'Trinidadian or Tobagonian', 'Tunisian', 'Turkish', 'Tuvaluan', 'Ugandan', 'Ukrainian', 'Uruguayan', 'Uzbekistani', 'Venezuelan', ' tnamese', 'Welsh', 'Yemenite', 'Zambian', 'Zimbabwean']

#China_List = ['UK', 'British', 'Scottish', 'Welsh', 'English', 'England', 'Scotland', 'Wales', 'Northern Ireland', 'Northern Irish']
#Countries_List = ['China', 'US', 'U.S.', 'Afghanistan', 'Aland Islands', 'Albania', 'Algeria', 'American Samoa', 'Andorra', 'Angola', 'Anguilla', 'Antarctica', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba', 'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus', 'Belgium', 'Belize', 'Benin', 'Bermuda', 'Bhutan', 'Bolivia, Plurinational State of', 'Bonaire, Sint Eustatius and Saba', 'Bosnia and Herzegovina', 'Botswana', 'Bouvet Island', 'Brazil', 'British Indian Ocean Territory', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 'Burundi', 'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Cayman Islands', 'Central African Republic', 'Chad', 'Chile', 'Christmas Island', 'Cocos (Keeling) Islands', 'Colombia', 'Comoros', 'Congo', 'Congo, The Democratic Republic of the', 'Cook Islands', 'Costa Rica', "Côte d'Ivoire", 'Croatia', 'Cuba', 'Curaçao', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti', 'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 'Equatorial Guinea', 'Eritrea', 'Estonia', 'Ethiopia', 'Falkland Islands (Malvinas)', 'Faroe Islands', 'Fiji', 'Finland', 'France', 'French Guiana', 'French Polynesia', 'French Southern Territories', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana', 'Gibraltar', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe', 'Guam', 'Guatemala', 'Guernsey', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti', 'Heard Island and McDonald Islands', 'Holy See (Vatican City State)', 'Honduras', 'Hong Kong', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran, Islamic Republic of', 'Iraq', 'Ireland', 'Isle of Man', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jersey', 'Jordan', 'Kazakhstan', 'Kenya', 'Kiribati', "Korea, Democratic People's Republic of", 'Korea, Republic of', 'Kuwait', 'Kyrgyzstan', "Lao People's Democratic Republic", 'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania', 'Luxembourg', 'Macao', 'Macedonia, Republic of', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali', 'Malta', 'Marshall Islands', 'Martinique', 'Mauritania', 'Mauritius', 'Mayotte', 'Mexico', 'Micronesia, Federated States of', 'Moldova, Republic of', 'Monaco', 'Mongolia', 'Montenegro', 'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands', 'New Caledonia', 'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Niue', 'Norfolk Island', 'Northern Mariana Islands', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestinian Territory, Occupied', 'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Pitcairn', 'Poland', 'Portugal', 'Puerto Rico', 'Qatar', 'Réunion', 'Romania', 'Russian Federation', 'Rwanda', 'Saint Barthélemy', 'Saint Helena, Ascension and Tristan da Cunha', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Martin (French part)', 'Saint Pierre and Miquelon', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino', 'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 'Singapore', 'Sint Maarten (Dutch part)', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 'South Georgia and the South Sandwich Islands', 'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'South Sudan', 'Svalbard and Jan Mayen', 'Swaziland', 'Sweden', 'Switzerland', 'Syrian Arab Republic', 'Taiwan, Province of China', 'Tajikistan', 'Tanzania, United Republic of', 'Thailand', 'Timor-Leste', 'Togo', 'Tokelau', 'Tonga', 'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Turks and Caicos Islands', 'Tuvalu', 'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom', 'United States', 'United States Minor Outlying Islands', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela, Bolivarian Republic of', 'Viet Nam', 'Virgin Islands, British', 'Virgin Islands, U.S.', 'Wallis and Futuna', 'Yemen', 'Zambia', 'Zimbabwe']
#Nationality_List = ['Chinese', 'Afghan', 'Albanian', 'Algerian', 'American', 'Andorran', 'Angolan', 'Antiguans', 'Argentinean', 'Armenian', 'Australian', 'Austrian', 'Azerbaijani', 'Bahamian', 'Bahraini', 'Bangladeshi', 'Barbadian', 'Barbudans', 'Batswana', 'Belarusian', 'Belgian', 'Belizean', 'Beninese', 'Bhutanese', 'Bolivian', 'Bosnian', 'Brazilian', 'Bruneian', 'Bulgarian', 'Burkinabe', 'Burmese', 'Burundian', 'Cambodian', 'Cameroonian', 'Canadian', 'Cape Verdean', 'Central African', 'Chadian', 'Chilean', 'Colombian', 'Comoran',  'Congolese', 'Costa Rican', 'Croatian', 'Cuban', 'Cypriot', 'Czech', 'Danish', 'Djibouti', 'Dominican', 'Dutch', 'Dutchman', 'Dutchwoman', 'East Timorese', 'Ecuadorean', 'Egyptian', 'Emirian', 'Equatorial Guinean', 'Eritrean', 'Estonian', 'Ethiopian', 'Fijian', 'Filipino', 'Finnish', 'French', 'Gabonese', 'Gambian', 'Georgian', 'German', 'Ghanaian', 'Greek', 'Grenadian', 'Guatemalan', 'Guinea-Bissauan', 'Guinean', 'Guyanese', 'Haitian', 'Herzegovinian', 'Honduran', 'Hungarian', 'I-Kiribati', 'Icelander', 'Indian', 'Indonesian', 'Iranian', 'Iraqi', 'Irish', 'Israeli', 'Italian', 'Ivorian', 'Jamaican', 'Japanese', 'Jordanian', 'Kazakhstani', 'Kenyan', 'Kittian and Nevisian', 'Kuwaiti', 'Kyrgyz', 'Laotian', 'Latvian', 'Lebanese', 'Liberian', 'Libyan', 'Liechtensteiner', 'Lithuanian', 'Luxembourger', 'Macedonian', 'Malagasy', 'Malawian', 'Malaysian', 'Maldivan', 'Malian', 'Maltese', 'Marshallese', 'Mauritanian', 'Mauritian', 'Mexican', 'Micronesian', 'Moldovan', 'Monacan', 'Mongolian', 'Moroccan', 'Mosotho', 'Motswana', 'Mozambican', 'Namibian', 'Nauruan', 'Nepalese', 'Netherlander', 'New Zealander', 'Ni-Vanuatu', 'Nicaraguan', 'Nigerian', 'Nigerien', 'North Korean', 'Norwegian', 'Omani', 'Pakistani', 'Palauan', 'Panamanian', 'Papua New Guinean', 'Paraguayan', 'Peruvian', 'Polish', 'Portuguese', 'Qatari', 'Romanian', 'Russian', 'Rwandan', 'Saint Lucian', 'Salvadoran', 'Samoan', 'San Marinese', 'Sao Tomean', 'Saudi', 'Senegalese', 'Serbian', 'Seychellois', 'Sierra Leonean', 'Singaporean', 'Slovakian', 'Slovenian', 'Solomon Islander', 'Somali', 'South African', 'South Korean', 'Spanish', 'Sri Lankan', 'Sudanese', 'Surinamer', 'Swazi', 'Swedish', 'Swiss', 'Syrian', 'Taiwanese', 'Tajik', 'Tanzanian', 'Thai', 'Togolese', 'Tongan', 'Trinidadian or Tobagonian', 'Tunisian', 'Turkish', 'Tuvaluan', 'Ugandan', 'Ukrainian', 'Uruguayan', 'Uzbekistani', 'Venezuelan', ' tnamese', 'Yemenite', 'Zambian', 'Zimbabwean']


data_china = pd.DataFrame()
data_world = pd.DataFrame()

columns = ['CHINA', 'WORLD']
#columns = ['UK', 'WORLD']

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
        
    flags = []
    flag_detail = []
    for i in range(0, len(data)):
        flag = 0
        flag_to_be_appended = '-'
        for c_l in Countries_List:
            r = data['Title'][i].find(c_l)
            if r != -1:
                flag = 1
                flag_to_be_appended = c_l
                break
        if flag == 0:
            for n_l in Nationality_List:
                r = data['Title'][i].find(n_l)
                if r != -1:
                    flag = 1
                    flag_to_be_appended = n_l
        for china_l in China_List:
            r = data['Title'][i].find(china_l)
            if r != -1:
                if flag == 0:
                    flag = flag - 1
                    flag_to_be_appended = china_l
                    break
                else:
                    flag = flag + 1
                    break
        flags.append(flag)
        flag_detail.append(flag_to_be_appended)
    data = pd.concat([data, pd.Series(flags)], axis=1)
    data = pd.concat([data, pd.Series(flag_detail)], axis=1)
    
    data.columns = ['Title', 'Nation', 'Country']
    data = data[data.Nation != 2]
    data = data[data.Nation != 0]
    
    if c == 'CHINA':
    #if c == 'UK':
        data_china = data
    if c == 'WORLD':
        data_world = data

data_total = pd.concat([data_china, data_world], axis = 0)

#data_total = data_total[data_total.nation != 0]

data_total = data_total.reset_index(drop=True)


# -------------------------------------------------------------------------------------
# draw negative and positive network
'''
pairs = []

for i in range(0, len(data_total)):
    #i = 343
    word_tokens = word_tokenize(data_total["Title"][i])
    word_tokens_without_sw = [word for word in word_tokens if not word.lower() in stop_words]
    word_tokens_without_len1 = [word for word in word_tokens_without_sw if len(word) > 1]
    word_tokens_without_notalpha = [word for word in word_tokens_without_len1 if word.isalpha()]
    word_tokens_negative = [word for word in word_tokens_without_notalpha if afinn.score(word) > 0]
    word_pairs = list(itertools.product([data_total["Country"][i]], word_tokens_negative))
    for pair in word_pairs:
        pair += (afinn.score(pair[1]), )
        pairs.append(pair)


nt1 = Network(height='750px', width='100%', bgcolor='#080808', font_color='white')

for p in pairs:
    src = p[0]
    dst = p[1]
    sie = 1 #p[2] * 10

    #if src == "Chinese" or src == "China":
    if src == "UK" or src == "British" or src == "Scottish" or src == "Welsh" or src == "English" or src == "England" or src == "Scotland" or src == "Wales":
        #nt1.add_node(src, src, size=5, title=src, group=1)
        nt1.add_node(src, src, size=5, title=src, color='#fa0a10')
    else:
        #nt1.add_node(src, src, size=5, title=src, group=2)
        nt1.add_node(src, src, size=5, title=src, color='#2b7ce9')
    nt1.add_node(dst, dst, size=abs(sie), title=dst, group=3)
    nt1.add_edge(src, dst)
nt1.show_buttons()
nt1.show('z-' + news + '-positive.html')

# -------------------

pairs = []

for i in range(0, len(data_total)):
    #i = 343
    word_tokens = word_tokenize(data_total["Title"][i])
    word_tokens_without_sw = [word for word in word_tokens if not word.lower() in stop_words]
    word_tokens_without_len1 = [word for word in word_tokens_without_sw if len(word) > 1]
    word_tokens_without_notalpha = [word for word in word_tokens_without_len1 if word.isalpha()]
    word_tokens_negative = [word for word in word_tokens_without_notalpha if afinn.score(word) < 0]
    word_pairs = list(itertools.product([data_total["Country"][i]], word_tokens_negative))
    for pair in word_pairs:
        pair += (afinn.score(pair[1]), )
        pairs.append(pair)

nt2 = Network(height='750px', width='100%', bgcolor='#080808', font_color='white')

for p in pairs:
    src = p[0]
    dst = p[1]
    sie = 1 #p[2] * 10

    #if src == "Chinese" or src == "China":
    if src == "UK" or src == "British" or src == "Scottish" or src == "Welsh" or src == "English" or src == "England" or src == "Scotland" or src == "Wales":
        #nt2.add_node(src, src, size=5, title=src, group=1)
        nt2.add_node(src, src, size=5, title=src, color='#fa0a10')
    else:
        #nt2.add_node(src, src, size=5, title=src, group=2)
        nt2.add_node(src, src, size=5, title=src, color='#2b7ce9')
    nt2.add_node(dst, dst, size=abs(sie), title=dst, group=3)
    nt2.add_edge(src, dst)
nt2.show_buttons()
nt2.show('z-' + news + '-negative.html')
'''

# draw complete network
pairs = []

for i in range(0, len(data_total)):
    word_tokens = word_tokenize(data_total["Title"][i])
    word_tokens_without_sw = [word for word in word_tokens if not word.lower() in stop_words]
    word_tokens_without_len1 = [word for word in word_tokens_without_sw if len(word) > 1]
    word_tokens_without_notalpha = [word for word in word_tokens_without_len1 if word.isalpha()]
    word_tokens_negative = [word for word in word_tokens_without_notalpha if afinn.score(word) < 0]
    word_pairs = list(itertools.product([data_total["Country"][i]], word_tokens_negative))
    for pair in word_pairs:
        pair += (afinn.score(pair[1]), )
        pairs.append(pair)
for i in range(0, len(data_total)):
    word_tokens = word_tokenize(data_total["Title"][i])
    word_tokens_without_sw = [word for word in word_tokens if not word.lower() in stop_words]
    word_tokens_without_len1 = [word for word in word_tokens_without_sw if len(word) > 1]
    word_tokens_without_notalpha = [word for word in word_tokens_without_len1 if word.isalpha()]
    word_tokens_negative = [word for word in word_tokens_without_notalpha if afinn.score(word) > 0]
    word_pairs = list(itertools.product([data_total["Country"][i]], word_tokens_negative))
    for pair in word_pairs:
        pair += (afinn.score(pair[1]), )
        pairs.append(pair)

nt2 = Network(height='750px', width='100%', bgcolor='#080808', font_color='white')

for p in pairs:
    src = p[0]
    dst = p[1]
    sie = p[2] * 13

    if src == "Chinese" or src == "China":
    #if src == "UK" or src == "British" or src == "Scottish" or src == "Welsh" or src == "English" or src == "England" or src == "Scotland" or src == "Wales" or src == 'Northern Ireland' or src == 'Northern Irish':
        #nt2.add_node(src, src, size=12, title=src, group=1)
        nt2.add_node(src, src, size=12, title=src, color='#fa0a10') # red
    else:
        #nt2.add_node(src, src, size=12, title=src, group=2)
        nt2.add_node(src, src, size=12, title=src, color='#2b7ce9') # blue
        
    if sie < 0:
        #nt2.add_node(dst, dst, size=abs(sie), title=dst, group=3)
        nt2.add_node(dst, dst, size=abs(sie), title=dst, color='#ffff00') # yellow
    else:
        #nt2.add_node(dst, dst, size=abs(sie), title=dst, group=4)
        nt2.add_node(dst, dst, size=abs(sie), title=dst, color='#7be141') # green
    
    nt2.add_edge(src, dst)

nt2.show_buttons()
nt2.show('z-' + news + '.html')
