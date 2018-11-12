import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city_name - name of the city to analyze
        (str) filter_option - type of selected filter option. Can be 'Month','Day','Both','None'.
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print("It's time to explore some US bikeshare data!\n")
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    valid_input_check = False; 
    while (valid_input_check == False):
        city_name = input('From which city you want to analyze data? (Chicago, New York City or Washington) \n ---> ').title()
        if city_name in ['Chicago','New York City','Washington']:
            print('OK! You selected ' + city_name)
            valid_input_check = True
        elif (city_name.isalpha()):
            print('You entered a string, but not a correct one! Try again!\n')                
        elif (city_name.isalpha() ==  False):
            print('Please read the question again on what to enter!\n')
    
    if city_name == "New York City":
        city_name = "new_york_city"
    
    
    # get user input for filter option
    valid_input_check = False;
    while (valid_input_check == False):
        filter_option = input("\nWould you like to filter the data by month, day, both or not at all? Type 'none' for no filter. \n --> ").title()
        if filter_option in ['Month','Day','Both','None']:
            print('OK! You selected ' + filter_option)
            valid_input_check = True
            
        elif (filter_option.isalpha()):
            print('You entered a string, but not a correct one! Try again!\n')                
        elif (filter_option.isalpha() ==  False):
            print('Please read the question again on what to enter! \n')
    
    # get user input for month (all, january, february, ... , june)
    valid_input_check = False;
    while (valid_input_check == False) and ((filter_option == 'Month') or (filter_option == 'Both')):
        month = input("\nWhich month you want analyze? (Only the first half of the year can be chosen) \n --> ").title()
        if month in ['January','February','March','April','May','June','All']:
            print('OK! You selected ' + month)
            valid_input_check = True
        elif (month.isalpha()):
            print('You entered a string, but not a correct one! Try again!\n')                
        elif (month.isalpha() ==  False):
            print('Please read the question again on what to enter! \n')
            

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_input_check = False;
    while (valid_input_check == False) and ((filter_option == 'Day') or (filter_option == 'Both')):
        day = input("\nWhich day you want to analyze? \n --> ").title()
        if day in ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','All']:
            print('OK! You selected ' + day)
            valid_input_check = True
        elif (day.isalpha()):
            print('You entered a string, but not a correct one! Try again!\n')                
        elif (day.isalpha() ==  False):
            print('Please read the question again on what to enter! \n')
    
    if filter_option == "None":
        month="None"
        day="None"

    if filter_option == "Day":
        month="None"
        
    if filter_option == "Month":
        day="None"   
    

    print('-'*40)
    return city_name, filter_option, month, day


def load_data(city_name, filter_option, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city_name - name of the city to analyze
        (str) filter_option - type of selected filter option. Can be 'Month','Day','Both','None'.
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    
    df = pd.read_csv('./'+city_name+'.csv')

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
   
    # filter by month if applicable
    if filter_option == 'Both':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    if filter_option == 'Month':
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    if filter_option == 'Day':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel based on previous filtering...')
    start_time = time.time()

    # display the most common month
    print("\nMost common month (in decimal / descending list format):")
    print("--------------------------------------------------------")
    print(df["month"].value_counts().max)
       
    
    # display the most common day of week
    print("\nMost common day of week (desc. list):")
    print("-------------------------------------")
    print(df["day_of_week"].value_counts().max)


    # display the most common start hour
    df['start_hour'] = df['Start Time'].dt.hour
    print("\nMost common start hour (desc. list):")
    print("------------------------------------")
    print(df["start_hour"].value_counts().max)
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip based on previous filtering..."""

    print('\nCalculating The Most Popular Stations and Trip based on previous filtering...\n')
    start_time = time.time()

    # display most commonly used start station
    print("\nMost commonly used start station in descending list format:")
    print("----------------------------------------------------------")
    print(df["Start Station"].value_counts().max)

    # display most commonly used end station
    print("\nMost commonly used end station in descending list format:")
    print("---------------------------------------------------------")
    print(df["End Station"].value_counts().max)

    # display most frequent combination of start station and end station trip    
    print("\nMost frequent combination of start station and end station trip in descending list format:")
    print("-----------------------------------------------------------------------------------------")
    df["Start_End_Combination"]=df['Start Station']+'  --->  '+df['End Station']
    print(df["Start_End_Combination"].value_counts().max)
             
                 
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration based on previous filtering...\n')
    start_time = time.time()

    # display total travel time
    print("\nTotal travel time: " + str(df['Trip Duration'].sum()) +'s / '+ str(df['Trip Duration'].sum()/3600)+'h')

    # display mean travel time
    print("Mean  travel time: " + str(df['Trip Duration'].mean()) +'s / '+ str(df['Trip Duration'].mean()/3600)+'h')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city_name):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats based on previous filtering...\n')
    start_time = time.time()

    # Display counts of user types
    print("\nCounts of user types:")
    print("---------------------")
    print(df['User Type'].value_counts())

    # Display counts of gender
    if city_name != "Washington":
        print("\nCounts of gender:")
        print('-'*17)
        print(df['Gender'].value_counts())
        print("\nYear of birth data:")
        print('-'*19)
        print("Earliest: " + str(df["Birth Year"].min()) + ", Most Recent: " + str(df["Birth Year"].max()))
        print("\nMost common years in descending list format:")
        print('-'*43)
        print(df["Birth Year"].value_counts().max)
        
        
    if city_name == "Washington":
        print("\n\n--> There is no gender data available for Washington!")
        print("--> There is no year of birth information available for Washington!")
    # Display earliest, most recent, and most common year of birth
    
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:

        city_name, filter_option, month, day = get_filters()
        df = load_data(city_name, filter_option, month, day)

		# Function-calls in given order. First some time-based statistics, then station and trip statistics, finally certain user statistics.	
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city_name)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            print("\nProgram quit.\n")
            break


if __name__ == "__main__":
	main()
