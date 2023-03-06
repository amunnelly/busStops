import datetime
import requests
from bs4 import BeautifulSoup

class BusStop(object):
    """
    Scrape the Dublin Bus website for Real Time Passenger Information and
    download that information to .csv
    """

    def __init__(self, stopNumber):
        """
        Args:
            stopNumber: The bus stop from which the RTPI data is to be
            recorded.
        """

        self.url = f"https://www.dublinbus.ie/RTPI/Sources-of-Real-Time-Information/?searchtype=view&searchquery={stopNumber}"
        self.make_request()
        
    def make_request(self):
        """
        Calls .get() on the requests module with self.url as the parameter.
        If the status code returned is 200, calls the .cook_soup() method
        with the data requests object as its parameter.
        If the status code returned is not 200, the csv is appended with the
        current time and the rest of the cells blank.
        If the get call fails, the time of the failure is appended to the 
        data/duds.csv file.
        """

        try:
            data = requests.get(self.url)
            if data.status_code == 200:
                self.cook_soup(data)
            else:
                with open("data/record.csv", "a") as f:
                    time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    line = ",".join([time_now, "", ""])
                    f.write(line+"\n")

        except:
            with open('data/duds.csv', 'a') as f:
                time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(time_now+"\n")

    def cook_soup(self, data):
        """
        A BeautifulSoup object is created from the data.text property.
        The table variable is found by identifying the table with id 
        `rtpi-results`. All the table rows in this table are iterated over.
        Those that have table data cells are sent to the self.record() method
        to be written to .csv.

        Args: data
            A requests object.
        """

        soup = BeautifulSoup(data.text, features='lxml')
        table = soup.find("table", id="rtpi-results")
        rows = table.findAll("tr")
        for row in rows:
            cells = row.findAll("td")
            if len(cells) == 0:
                continue
            else:
                self.record(cells)


    def record(self, cells):
        """
        The cells ResultSet is parsed and the Expected Arrival times associated
        with the appropriate buses. The data is then appended to data/record.csv
        
        Args: cells
            A bs4.element.ResultSet object
        """

        today = datetime.datetime.now().strftime("%Y-%m-%d")
        time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        due = cells[2].text.strip()
        if due == "Due":
            due_time = today + " " + time_now[10:16] + ":00"
        else:
            due_time = today + " " + due + ":00"

        bus = cells[0].text.strip()
        record = ",".join([time_now, due_time, bus])
        with open("data/record.csv", "a") as f:
            f.write(record+"\n")



if __name__ == "__main__":
    # 273: O'Connell Bridge southbound 4, 7, 7A, 40
    # 792: Dawson Street northbound 40, 46A, 150, 155 
    x = BusStop(273)
