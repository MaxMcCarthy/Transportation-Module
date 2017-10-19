# Transportation-Module

Project was designed for University of Illinois Rowing Team to coordinate transportation to practice.
The team currently takes 10-15 private vehicles to Clinton Lake each day at 5:00AM. To maximize efficiency, 
this module uses a K-Means Clustering algorithm with the Cars as centroids and the athletes as points. The algorithm
clusters students into cars and directs them to a pickup location that minimizes the walking distance for each athlete. The
driver is then to meet all the athletes at that location. The program calculates the minimum number of drivers needed to get
the necessary athletes to the lake and recommends which driver(s) be taking out of the driver pool to save gas for a particular
trip.

The module is currently being used by the captain of the Illinois Men's Rowing team to administer car assignments. The module
is in an early release that the captain downloaded.

The current plan is to add database support for the athletes instead of reading from a CSV. A team could instead save a number
of athlete profiles and simply log in to make the car assignments.

After database support is added, a workout tracker will be added to increase accountability during winter training.
