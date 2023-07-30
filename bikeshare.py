from tabulate import tabulate
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington)
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington?\n").lower()
        if city in CITY_DATA:
            break
        else:
            print("Invalid city. Please enter either Chicago, New York City, or Washington.")
            
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("We have data from January to June, which month would you like to see? Please type the month name or 'all' to see all months.\n").lower()  
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:    
            break    
        else:
            print("Invalid month. Please enter either January, February, March, April, May, June, or all.")
             
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Would you like to filter the data by day of week? Please type the day name. Otherwise type 'all' to see all days of the week.\n").lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break   
        else:
            print("Invalid day. Please enter either Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all.")           

    print('-'*100)
    
    # print city, month, day
    print("Here is information about bike share use in {} for month: {}, and day of week: {}.".format(city, month, day))
        
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
                 
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def display_raw_data(df):
    """
    Asks user if they would like to see 5 lines of raw data at a time
    
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day 5 rows at a time until user says 'no' or no more raw data to display
    """          
    
    # get user input if they want to see 5 lines of raw data
    while True:
        raw_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n').lower()  
        if raw_data in ('yes','no'):   
            break    
        else:
            print("Invalid answer. Please enter either yes or no.")
    
    # get user input if they want to see the next 5 lines of raw data. Only show raw data if user answers 'yes', otherwise break the loop.
    # continue iterating these prompts and displaying the next 5 lines of raw data at each iteration.
    i = 0
    more_raw_data = True
       
    while more_raw_data:          
        if raw_data == 'yes':                        
            print(df.iloc[i:i+5])                       
            i += 5            
            raw_data = input('\nWould you like to see the next 5 lines of raw data? Enter yes or no.\n').lower()
            if raw_data.lower() != 'yes':
                break  
            else:
                print("Invalid answer. Please enter either yes or no.")              
                if raw_data == 'no' or i >= len(df):                
                    more_raw_data = False
                       
    
def time_stats(df):
    """Displays statistics on the most frequent times of travel
    
    Returns:
        Table containing the popular month, day of week, and start hour
    """
    print('\n1. Popular Times of Travel\n')
    
    # map month integers to month names
    month_dict = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
                    7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'}

    # display the most common month
    month_mode = df['month'].mode().item()
    popular_month = month_dict.get(month_mode, 'Invalid')
 
    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    
    # display the most common start hour
    popular_hour = df['hour'].mode()[0]
    
    # convert hour to 12 hour format, add PM as suffix if hour greater than 12 otherwise add AM as suffix
    if popular_hour > 12:
        popular_hour = popular_hour - 12
        popular_hour = str(popular_hour) + 'PM'
    else:
        popular_hour = str(popular_hour) + 'AM'        
    
    # create table with time data
    time_data = [["Month", popular_month], 
                ["Day of week", popular_day], 
                ["Start hour", popular_hour]]
           
    # define header names
    columns = [" ", "Most Frequent Travel Time"]
  
    # display table
    print(tabulate(time_data, headers = columns, tablefmt="fancy_grid"))


def station_stats(df):
    """Displays statistics on the most popular stations and trip
    
        Returns:
        Table containing the popular stations and trip
    """
    print('\n2. Most Popular Stations and Trip\n')

    # display most commonly used start station, remove dtype in output
    popular_start_station = df['Start Station'].mode().values[0]
 
    # display most commonly used end station, remove dtype in output    
    popular_end_station = df['End Station'].mode().values[0]
      
    # display most frequent combination of start station and end station trip. 
    popular_trip = df.groupby(['Start Station', 'End Station']).size().idxmax()
    
    # create table with station data
    station_data = [["Start station", popular_start_station], 
                    ["End station", popular_end_station], 
                    ["Start and end station", popular_trip]]
           
    # define header names
    columns = ["Most popular station", "Station name"]
  
    # display table
    print(tabulate(station_data, headers = columns, tablefmt="fancy_grid"))


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration
    
        Returns:
        Table containing the total and average trip duration
    """
    print('\n3. Trip Duration\n')
    
    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    
    # convert total travel time to either the nearest years, months, days, minutes, or seconds based on the following conditions  
    if  total_travel_time >= 2.80872e8:
        total_travel_time = total_travel_time / 2.80872e8
        total_travel_time = int(total_travel_time)
        total_travel_time = str(total_travel_time) + ' years'
      
    elif total_travel_time >= 2.628e+6:
        total_travel_time = total_travel_time / 2.628e+6
        total_travel_time = int(total_travel_time)
        total_travel_time = str(total_travel_time) + ' months'
    
    elif total_travel_time >= 86400:
        total_travel_time = total_travel_time / 86400
        total_travel_time = int(total_travel_time)
        total_travel_time = str(total_travel_time) + ' days'
        
    elif total_travel_time >= 3600:
        total_travel_time = total_travel_time / 3600
        total_travel_time = int(total_travel_time)
        total_travel_time = str(total_travel_time) + ' hours'
        
    elif total_travel_time >= 60:
        total_travel_time = total_travel_time / 60
        total_travel_time = int(total_travel_time)
        total_travel_time = str(total_travel_time) + ' minutes'
        
    else:
        total_travel_time = int(total_travel_time)
        total_travel_time = str(total_travel_time) + ' seconds'
                     
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    
    # convert mean travel time to either the nearest years, months, days, minutes, or seconds based on the following conditions    
    if  mean_travel_time >= 2.80872e8:
        mean_travel_time = mean_travel_time / 2.80872e8
        mean_travel_time = int(mean_travel_time)
        mean_travel_time = str(mean_travel_time) + ' years'
      
    elif mean_travel_time >= 2.628e+6:
        mean_travel_time = mean_travel_time / 2.628e+6
        mean_travel_time = int(mean_travel_time)
        mean_travel_time = str(mean_travel_time) + ' months'
    
    elif mean_travel_time >= 86400:
        mean_travel_time = mean_travel_time / 86400
        mean_travel_time = int(mean_travel_time)
        mean_travel_time = str(mean_travel_time) + ' days'
        
    elif mean_travel_time >= 3600:
        mean_travel_time = mean_travel_time / 3600
        mean_travel_time = int(mean_travel_time)
        mean_travel_time = str(mean_travel_time) + ' hours'
        
    elif mean_travel_time >= 60:
        mean_travel_time = mean_travel_time / 60
        mean_travel_time = int(mean_travel_time)
        mean_travel_time = str(mean_travel_time) + ' minutes'
        
    else:
        mean_travel_time = int(mean_travel_time)
        mean_travel_time = str(mean_travel_time) + ' seconds'
    
    # create table with duration data
    duration_data = [["Total Travel Time", total_travel_time], 
                    ["Mean Travel Time", mean_travel_time]] 
                               
    # define header names
    columns = [" ", "Trip Duration"]
  
    # display table
    print(tabulate(duration_data, headers = columns, tablefmt="fancy_grid"))


def user_stats(df):
    """Displays statistics on bikeshare users
    
        Returns:
        Table 1 - breakdown of user types (subscriber, customer, dependent)
        Table 2 - breakdown of gender types (male, female)
        Table 3 - breakdown of birth years
    """
    print('\n4. User Information\n')

    # display counts of user types
    print('\ni. Types of Bikeshare Users\n')
    
    user_types = df['User Type'].value_counts()
        
    user_types = user_types.reset_index() 

    user_types.columns = ['User Type', 'Number of users']
    print(tabulate(user_types, headers = "keys", tablefmt="fancy_grid"))
    
    # display counts of gender in table format, no index column
    print('\n(ii) Gender Breakdown\n')
    
    if 'Gender' in df:    
        gender_types = df['Gender'].value_counts()
        gender_types = gender_types.reset_index()
        gender_types.columns = ['Gender', 'Number of users']
        print(tabulate(gender_types, headers = "keys", tablefmt="fancy_grid"))
    else:
        print("No gender type data available.")
        
    # display breakdown of birth years
    print('\n(iii) Birth Year Breakdown\n')
    if 'Birth Year' in df:
        earliest_birth_year = df['Birth Year'].min()
                
        most_recent_birth_year = df['Birth Year'].max()
                
        most_common_birth_year = df['Birth Year'].mode()[0]
        birth_data = [["Earliest", earliest_birth_year], 
                    ["Most recent", most_recent_birth_year],
                    ["Most common", most_common_birth_year]] 
        columns = [" ", "Birth Year"]
        print(tabulate(birth_data, headers = columns, tablefmt="fancy_grid"))
    else:
        print("No birth year data available.")
                 
                       
def main():
    """
    Asks user if they want to start the program again or exit. """

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        display_raw_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart this program? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
