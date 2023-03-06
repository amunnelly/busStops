# Scraping Dublin Bus Real Time Passenger Information (RTPI) Data

Dublin Bus RTPI data is available here: https://www.dublinbus.ie/en/RTPI/

Information from the website is scrapped by `bus_stop.py`, and that data is then prepared for plotting on ObserableHQ by `prepare_data.py`. The data is collected by initiating `bus_stop.py` with a bus stop number, and then running a `crontab` job every minute for a week to collect data.

The data for Bus Stop #273, O'Connell Bridge southbound for Bus Number 4, from Harriston to Monkstown Ave, is plotted and discussed here: https://observablehq.com/@anthony-munnelly/waiting-for-a-bus-on-oconnell-bridge-dublin. The dates in question are Monday, February 27th, 2023 to Friday, March 3rd, 2023 inclusive.