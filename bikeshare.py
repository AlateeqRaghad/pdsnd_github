import time
import pandas as pd

#Array to help data loading
CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }
Valid_days=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday' , 'All']

Valid_months=['January','February','March','April','May','June', 'All']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('Hello! Let\'s explore some US bikeshare data!')

    while(True):
        # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city=input(print('Would you like to see data for Chicago , New York , Washington ?')).title()

        # TO DO: get user input for month (all, january, february, ... , june)
        month=input(print('Which month ? January , February , Martch , April , May , or June ? or All if no specific month ')).title()

        # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        day=input(print('Which day ? (e.g. Sunday)  or All if no specific day ?')).title()

        if (day not in Valid_days and month not in Valid_months and city not in CITY_DATA):
            print('Please enter valid city , month , and day')
            continue

        print('-'*40)


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


    # extract month and day of week from Start Time to create new columns
    df['month'] =  df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable to create new dataframe
    if month != 'All':
        df = df[df['month'] == month]

    # filter by day of week if applicable to create new dataframe
    if day != 'All':
        df = df[df['day_of_week'] == day]

    df['hour'] = (df['Start Time'].dt.hour)



    return df


def time_stats(df, month , day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # If no month and day filter
    if (day=='All' and month =='All') :
        print('Most common Month: {}, Day: {}, Hour: {}'.format(df['month'].mode()[0],df['day_of_week'].mode()[0] , df['hour'].mode()[0]))

    # If specific month and no day filter
    elif(day=='All' and month != 'All'):
        print('Most common Day: {}, Hour: {}'.format(df['day_of_week'].mode()[0] , df['hour'].mode()[0]))

    # If specific day and no month filter
    elif(day!='All' and month =='All'):
        print('Most common Month: {}, Hour: {}'.format(df['month'].mode()[0] , df['hour'].mode()[0]))

    else :
        # If specific month and day
        print('Most common Hour: {}'.format(df['hour'].mode()[0]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print('Most popular start station is: {} , with count {}\n'.format( df['Start Station'].mode()[0], df['Start Station'].value_counts().max() ))

    # TO DO: display most commonly used end station
    print('Most popular end station is: {} , with count {}\n'.format( df['End Station'].mode()[0], df['End Station'].value_counts().max() ))


    # TO DO: display most frequent trip
    print('Most popular trip is: {} , with count {}\n'.format((df['Start Station'] +' - '+ df['End Station']).mode()[0],
                                                            (df['Start Station'] +' - '+ df['End Station']).value_counts().max() ) )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Calculate total trips
    Total_trips= len(df)

    #To calculate each trip duration
    #Convert End time to date , Start time has converted
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Duration']= df['End Time']-df['Start Time']

    #Calculate total duration in minutes
    Total_duration=df['Duration'].sum().total_seconds()/60

    #Calculate mean
    Avg= Total_duration/Total_trips
    print('Total trips : {},\nTotal duration : {} minutes ,\nAverage duration : {} minutes'.format(Total_trips,Total_duration,Avg))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print('User types:\n{}\n'.format(df['User Type'].value_counts()))

    #Washimgton has no birth year and gender data
    if 'Gender' in df :

        #TO DO: Display counts of gender
        print('Gender:\n{}\n'.format(df['Gender'].value_counts()))

        # TO DO: Display earliest, most recent, and most common year of birth
        print('Users birth year:\nEarlist birth year is: {}\nMost resent birth year is: {}\nMost common birth year is: {}\n'
              .format(df['Birth Year'].min(),df['Birth Year'].max(),df['Birth Year'].mode()[0]))
    else :
        print('No Gender and birth year data to share')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():

    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, month , day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        counter = 0
        indivisual_trip_data = input('\nWould you like to see indivisual trip data? Enter yes or no.\n')
        while (indivisual_trip_data.lower() == 'yes'):
            print(df[counter:counter + 5])
            indivisual_trip_data = input('\nWould you like to see indivisual trip data? Enter yes or no.\n')
            counter +=5

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
	main()
