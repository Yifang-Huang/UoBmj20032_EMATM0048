import unittest
from carRent import CUSTOMER, RentalShop, Car, Hatchback, Sedan, SUV
import datetime


class RentalTest(unittest.TestCase):

    def testCar(self):
        car = Car(ID=0)
        assert car.days is 0
        assert car.owner is None
        customer = CUSTOMER(0)
        days = 8
        date = datetime.datetime(year=2021, month=1, day=10, hour=12, minute=30)
        car.rented(customer, date, days)
        assert car.rent_back.strftime('%Y-%m-%d %H:%M') == '2021-01-18 12:30'
        assert car.days == 8



if __name__ == '__main__':
    unittest.main()
