import pandas as pd

class PrepareData(object):
    """
    Prepare a .csv file of bus expected times for later
    charting on ObservableHq.com.
    """

    def __init__(self, filename, busNumber, timeLimit) -> None:
        """
        Read the .csv data, identify the datetime columns and slice by
        the busNumber. Calculate the wait times and then slice further
        by timeLimit. Finally, sort by CurrentTime and forward to the
        .prepare_data() method.

        Args:
            filename: the location of the .csv file
            busNumber: the busNumber data to be collected from the data
            timeLimit: A cutoff to eliminate nighttime waiting when the 
                       buses don't run.
        """
        df = pd.read_csv(filename)
        df['CurrentTime'] = pd.to_datetime(df['CurrentTime'])
        df['ExpectedTime'] = pd.to_datetime(df['ExpectedTime'])
        df = df[df.Bus==str(busNumber)]
        del(df['Bus'])
        df['Time'] = df.ExpectedTime - df.CurrentTime
        df['Time'] = df.Time.apply(lambda x: x.seconds)
        df['Time'] = df.Time / 60
        df = df[df.Time < timeLimit]
        df.sort_values('CurrentTime', inplace=True)

        self.df = self.prepare_data(df)

        
    def prepare_data(self, df):
        """
        The dataframe is grouped by CurrentTime. This group is then iterated
        over, with the minimum ExpectedTime and wait time identified on each
        iteration. These three metric are recorded as a dictionary and appended
        to a list, from which a data frame is created. Day and Hour columns
        are added to the data frame, which is then returned.

        Args:
            df: A pandas data frame.

        Returns:
            df2: A pandas data frame.
        """
        holder = []
        grouper = df.groupby(['CurrentTime'])
        for a, b in grouper:
            holder.append({"CurrentTime": a,
                           "ExpectedTime": b['ExpectedTime'].min(),
                           "Time": b.Time.min()})
            
        df2 = pd.DataFrame(holder)
        df2['Day'] = df2.CurrentTime.apply(lambda x: x.strftime("%A"))
        df2['Hour'] = df2.CurrentTime.apply(lambda x: int(x.strftime("%H")))

        return df2




if __name__ == "__main__":
    x = PrepareData("data/stop_273.csv", 4, 1e3,)
    x.df.to_csv('observable_data/stop_273_route_4.csv', index=False)