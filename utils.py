from scipy import stats
from statsmodels.nonparametric.smoothers_lowess import lowess
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal

def setUp(path, startOffset, endOffset):
    df = pd.read_csv(path, sep = ', ', engine = 'python')

    #After grabing start and end time, drop nan data
    start = df['SamplingTime'].iloc[0]
    end = df['SamplingTime'].iloc[-1]
    df.dropna(axis = 0, inplace = True)

    #Drop data
    start += startOffset
    end -= endOffset
    df.drop(df[df['SamplingTime'] < start].index, inplace = True)
    df.drop(df[df['SamplingTime'] > end].index, inplace = True)

    #Find acceleration
    df['Acceleration'] = ((df['AccelerationX']**2+
                          df['AccelerationY']**2+
                          df['AccelerationZ']**2)**(1/2))
    # df['Acceleration'] -= 9.81

    #SamplingTime to datetime
    df['Date'] = pd.to_datetime(df['SamplingTime'], unit='s')

    #Time duration
    df['Time'] = df['SamplingTime']-start

    #butter
    b, a = signal.butter(3, 0.10, btype='lowpass', analog=False)
    df['Filtered'] = signal.filtfilt(b, a, df['Acceleration'])
    return df;

def outputAccelWithButter(df, name):
    plt.plot(df['Time'], df['Acceleration'])
    plt.plot(df['Time'], df['Filtered'])
    plt.title(name + ' acceleration data')
    plt.xlabel('Time (Second)')
    plt.ylabel('Acceleration (Meter/Second^2)')
    plt.legend(['Collected Data', 'Butter Filter'])
    plt.savefig('output/' + name + '.svg')
    plt.close()

def outputSpeed(df):
    #Approximate speed using acceleration(after filter) * time
    df['PreviousTime'] = df['Time'].shift(1)
    df = df.fillna(0.0)
    df['Speed'] = df['Filtered'] * (df['Time'] - df['PreviousTime'])
    plt.plot(df['Time'], df['Speed'])

    #Lowess line
    filtered = lowess(df['Speed'], df['Time'], frac=0.15)
    plt.plot(filtered[:, 0], filtered[:, 1])

    plt.title('Speed')
    plt.xlabel('Time (Second)')
    plt.ylabel('Speed (Meter/Second)')
    plt.legend(['Collected Data', 'Lowess'])
    plt.savefig('output/ankle_speed.svg')
    plt.close()

def outputFB(forward, backward):
    #graph comparison
    plt.plot(forward['Time'], forward['Filtered'])
    plt.plot(backward['Time'], backward['Filtered'])
    plt.title('Forward vs Backward Acceleration comparison')
    plt.xlabel('Time (Second)')
    plt.ylabel('Acceleration (Meter/Second^2)')
    plt.legend(['Forward', 'Backward'])
    plt.savefig('output/forward_backward_accel.svg')
    plt.close()
    
    #Speed comparison forward and backward
    #Approximate speed for both
    #forward
    forward['PreviousTime'] = forward['Time'].shift(1)
    forward = forward.fillna(0.0)
    forward['Speed'] = forward['Filtered'] * (forward['Time'] - forward['PreviousTime'])

    #backward
    backward['PreviousTime'] = backward['Time'].shift(1)
    backward = backward.fillna(0.0)
    backward['Speed'] = backward['Filtered'] * (backward['Time'] - backward['PreviousTime'])

    #Forward lowess line
    filtered = lowess(forward['Speed'], forward['Time'], frac=0.15)
    plt.plot(filtered[:, 0], filtered[:, 1])
    #Backward lowess line
    filtered = lowess(backward['Speed'], backward['Time'], frac=0.15)
    plt.plot(filtered[:, 0], filtered[:, 1])
    plt.title('Forward vs Backward speed')
    plt.legend(['Forward', 'Backward'])
    plt.xlabel('Time (Second)')
    plt.ylabel('Speed (Meter/Second)')
    plt.savefig('output/forward_backward_speed.svg')
    plt.close()

def outputGender(male, forward, female):
    #plot compare speed between 2 male and 1 female
    #male S
    male['PreviousTime'] = male['Time'].shift(1)
    male = male.fillna(0.0)
    male['Speed'] = male['Filtered'] * (male['Time'] - male['PreviousTime'])
    filtered = lowess(male['Speed'], male['Time'], frac=0.15)
    plt.plot(filtered[:, 0], filtered[:, 1], 'blue')

    #male C
    forward['PreviousTime'] = forward['Time'].shift(1)
    forward = forward.fillna(0.0)
    forward['Speed'] = forward['Filtered'] * (forward['Time'] - forward['PreviousTime'])
    filtered = lowess(forward['Speed'], forward['Time'], frac=0.15)
    plt.plot(filtered[:, 0], filtered[:, 1], 'cornflowerblue')

    #female D
    female['PreviousTime'] = female['Time'].shift(1)
    female = female.fillna(0.0)
    female['Speed'] = female['Filtered'] * (female['Time'] - female['PreviousTime'])
    filtered = lowess(female['Speed'], female['Time'], frac=0.15)
    plt.plot(filtered[:, 0], filtered[:, 1], 'pink')

    plt.title('Male vs Female Speed')
    plt.xlabel('Time (Second)')
    plt.ylabel('Speed (Meter/Second)')
    plt.legend(['Male 1', 'Male 2','Female'])
    plt.savefig('output/gender_speed.svg')
    plt.close()
    
