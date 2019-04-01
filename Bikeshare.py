#Completed with the help of Stack Overflow and collegues :-)
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
       
    # Gets user input for city (chicago, new york city, washington).
    city = str(input("\nPlease specify the city name either 'chicago', 'new york city' or 'washington':")).lower()
    
    list_of_cities = ['chicago', 'new york city', 'washington']
    
    while city not in list_of_cities:
        print('\nSorry i did not get your input. \n')
        city = str(input("Please specify the city name either 'chicago', 'new york city' or 'washington'):")).lower()
    
    #Get's user input for month (all, january, february, ... , june)
    month = str(input("\nPlease specify the name of the month, from 'january' to 'june' or type 'all' for all months:")).lower()

    list_of_months = ['january','february','march','april','may','june','all']

    while month.lower() not in list_of_months:
        print('\nSorry i did not get your input. \n')
        month = str(input("Please specity the name of the month, from 'january' to 'june' or type 'all' for all months:")).lower()
        
    # Get's user input for day of week (all, monday, tuesday, ... sunday)
    day = str(input("\nPlease specify the day of the week, for example 'monday' or type 'all' for all weekdays:")).lower()

    list_of_days = ['monday','tuesday','wednesday','thursday','friday','all']
    
    while day not in list_of_days:
        print('\nSorry i did not get your input. \n')
        day = str(input("Please specify the day of the week, for example 'monday' or type 'all' for all weekdays:")).lower()
    
    #print('-'*40)
    return city, month, day

def raw_data():
    raw_data_y_n = str(input("Please specify if you want to see 5 lines of raw data ('yes' or 'no'):")).lower()                         
    list_of_answers = ['yes','no']
    
    while raw_data_y_n not in list_of_answers:
        print('\nSorry i did not get your input. \n')
        city = lower(str(input("Please specify if you want to see 5 lines of raw data ('yes' or 'no'):")))
    
    return raw_data_y_n

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
    df = pd.read_csv(CITY_DATA[city])
    
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    
    if month != 'all':
        # uses the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filters by month to create the new dataframe
        df = df[df['month'] == month]

    # filters by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    
    ##print(df.head)
    
    # Displays the most common month
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    if df['month'].nunique() > 1: 
        most_common_month_rank = df['month'].value_counts().index.tolist() 
        print('The most common month is {}.'.format(months[most_common_month_rank[0]-1]))
    #Referenses: #https://stackoverflow.com/questions/45759966/counting-unique-values-in-a-column-in-pandas-dataframe-like-in-qlik
    #https://stackoverflow.com/questions/35523635/extract-values-in-pandas-value-counts

    # Displays the most common day of week
    if df['day_of_week'].nunique() > 1:
        most_common_day_rank = df['day_of_week'].value_counts().index.tolist()
        print('The most common day of the week is {}.'.format(most_common_day_rank[0].lower()))
    
    # Displays the most common start hour
    df['hour'] = df['Start Time'].values.astype('<M8[h]') 
    #Referense: https://stackoverflow.com/questions/42977395/pandas-dt-hour-formatting
    df['hour'] = df['hour'].dt.time
    most_common_hour_rank = df['hour'].value_counts().index.tolist()
    
    from datetime import datetime
    most_common_hour = most_common_hour_rank[0].strftime("%-H %p") 
    #Referenses: https://stackoverflow.com/questions/13855111/how-can-i-convert-24-hour-time-to-12-hour-time
    #http://strftime.org/
    print('The most common start hour is {}.'.format(most_common_hour))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Displays most commonly used start station
    most_common_start_station_rank = df['Start Station'].value_counts().index.tolist()
    print('The most commonly used start station is {}.'.format(most_common_start_station_rank[0]))

    # Displays most commonly used end station
    most_common_end_station_rank = df['End Station'].value_counts().index.tolist()
    print('The most commonly used end station is {}.'.format(most_common_end_station_rank[0]))

    # Displays most frequent combination of start station and end station trip
    #Reference: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.str.cat.html
    df['Start End Station'] = df['Start Station'].str.cat(df['End Station'], sep=' to ') 
    most_common_trip_rank = df['Start End Station'].value_counts().index.tolist()
    print('The most frequent combination of start station and end station trip is {}.'.format(most_common_trip_rank[0]))
                                                          
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Displays total travel time
    #https://stackoverflow.com/questions/22132525/add-column-with-number-of-days-between-dates-in-dataframe-pandas
    total_travel_time = df['Trip Duration'].sum()
    #https://stackoverflow.com/questions/47434724/getting-floor-division-and-remainder-at-same-time-in-2-separate-variables
    minutes, seconds = divmod(total_travel_time,60)
    hours, minutes = divmod(minutes,60)
    #https://stackoverflow.com/questions/493386/how-to-print-without-newline-or-space
    print('The total travel time was:')
    print('\n   {0:.0f} hours, '.format(hours))
    print('\n   {0:.0f} minutes and '.format(minutes))
    print('\n   {0:.2f} seconds.'.format(seconds))
    # Display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    minutes, seconds = divmod(mean_travel_time,60)
    if minutes > 60:
        hours, minutes = divmod(minutes,60)
        print('\nThe mean travel time was:')
        print('\n   {0:.0f} hours, '.format(hours))
        print('\n   {0:.0f} minutes and '.format(minutes))
        #https://stackoverflow.com/questions/455612/limiting-floats-to-two-decimal-points
        print('\n   {0:.2f} seconds.'.format(seconds))
 
    else:
        print('\nThe mean travel time was:')
        print('\n   {0:.0f} minutes and '.format(minutes))
        print('\n   {0:.2f} seconds.'.format(seconds))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Creates a rank table based on Pandas method value_counts()    
def create_rank_table(df, column_name):
    counts_of_user_types_index = df[column_name].value_counts().index.tolist()
    counts_of_user_types_values = df[column_name].value_counts().values.tolist()
    items = {'Count': pd.Series(counts_of_user_types_values, index=counts_of_user_types_index)}
    type_counts = pd.DataFrame(items)
    return type_counts
    
def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displays counts of user types
    print('The counts of user types was:\n')
    print(create_rank_table(df,'User Type'))
    
    # Displays earliest, most recent, and most common year of birth
    
    if city == 'chicago' or city == 'new york city':
        earliest_year_of_birth = int(df['Birth Year'].min())
        most_recent_year_of_birth = int(df['Birth Year'].max())
        most_common_year_of_birth = int(df['Birth Year'].value_counts().index.tolist()[0])
        print("\nThe earliest year of birth was {}".format(earliest_year_of_birth))
        print("The most recent year of birth was {}".format(most_recent_year_of_birth))
        print("The most common year of birth was {}".format(most_common_year_of_birth))
        # Displays the the counts of gender
        print('\nThe counts of gender was:\n')
        print(create_rank_table(df,'Gender'))        
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

# Displays raw data to the user, in increments of 5 rows, upon request   
def display_raw_data(df):
    raw_data = str(input("\nPlease specify if you want to see the raw data ('yes' or 'no')")).lower()
    start_row = 0
    end_row = 5
    while True:
        if raw_data == 'yes':
            #https://www.shanelynn.ie/select-pandas-dataframe-rows-and-columns-using-iloc-loc-and-ix/
            print(df[df.columns[0:-1]].iloc[start_row:end_row])
            start_row += 5
            end_row += 5
            while True:
                raw_data = str(input("Please specify if you want to see more raw data ('yes' or 'no')")).lower()
                if raw_data == 'yes':
                    print(df[df.columns[0:-1]].iloc[start_row:end_row])
                    start_row += 5
                    end_row += 5
                elif raw_data == 'no':
                    break
                else: 
                    print('\nSorry i did not get your input. \n')
        elif raw_data == 'no':
            break
        else:
            print('\nSorry i did not get your input. \n')
            raw_data = str(input("Please specify if you want to see the raw data ('yes' or 'no')")).lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
           
            
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        display_raw_data(df)
        
        restart = input("\nWould you like to restart? Enter 'yes' or 'no':\n")
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()