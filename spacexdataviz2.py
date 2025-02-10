import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/dataset_part_2.csv")

# TASK 1: Visualize the relationship between Flight Number and Launch Site
sns.catplot(x="FlightNumber", y="LaunchSite", hue="Class", data=df, aspect=5)
plt.xlabel("Flight Number", fontsize=20)
plt.ylabel("Launch Site", fontsize=20)
plt.show()

# TASK 2: Visualize the relationship between Payload and Launch Site
sns.catplot(x="PayloadMass", y="LaunchSite", hue="Class", data=df, aspect=5)
plt.xlabel("Pay Load Mass (kg)", fontsize=20)
plt.ylabel("Launch Site", fontsize=20)
plt.show()

# TASK 3: Visualize the relationship between success rate of each orbit type
success_rate = df.groupby('Orbit')['Class'].mean()
success_rate.plot(kind='bar')
plt.xlabel("Orbit", fontsize=20)
plt.ylabel("Success Rate", fontsize=20)
plt.show()

# TASK 4: Visualize the relationship between FlightNumber and Orbit type
sns.catplot(x="FlightNumber", y="Orbit", hue="Class", data=df, aspect=5)
plt.xlabel("Flight Number", fontsize=20)
plt.ylabel("Orbit", fontsize=20)
plt.show()

# TASK 5: Visualize the relationship between Payload and Orbit type
sns.catplot(x="PayloadMass", y="Orbit", hue="Class", data=df, aspect=5)
plt.xlabel("Payload Mass (kg)", fontsize=20)
plt.ylabel("Orbit", fontsize=20)
plt.show()

# TASK 6: Visualize the launch success yearly trend
# A function to Extract years from the date 
def Extract_year(date):
    return date.split("-")[0]

df['Year'] = df['Date'].apply(Extract_year)
yearly_success = df.groupby('Year')['Class'].mean()
yearly_success.plot(kind='line')
plt.xlabel("Year", fontsize=20)
plt.ylabel("Success Rate", fontsize=20)
plt.show()

# Feature selection
features = df[['FlightNumber', 'PayloadMass', 'Orbit', 'LaunchSite', 'Flights', 
               'GridFins', 'Reused', 'Legs', 'LandingPad', 'Block', 'ReusedCount', 'Serial']]

# TASK 7: Create dummy variables for categorical columns
categorical_columns = ['Orbit', 'LaunchSite', 'LandingPad', 'Serial']
features_one_hot = pd.get_dummies(features, columns=categorical_columns)

# TASK 8: Cast all numeric columns to float64
features_one_hot = features_one_hot.astype('float64')

# Export to CSV
features_one_hot.to_csv('dataset_part_3.csv', index=False)