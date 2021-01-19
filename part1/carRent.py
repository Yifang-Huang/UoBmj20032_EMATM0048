import datetime
import copy
from typing import List

# Global variables: basic information of the vehicle.
CAR={
    'hatchback': {
        'short_period': 30,
        'long_period': 25,
        'vip': 20,
    },
    'sedan': {
        'short_period': 50,
        'long_period': 40,
        'vip': 35,
    },
    'suv': {
        'short_period': 100,
        'long_period': 90,
        'vip': 80,
    }
}


class Car:
    """ Define the class of the car. Because the program involves the rental and borrowing of different cars, a separate class is defined for the car to facilitate management. """

    def __init__(self, ID):
        # The ID of the cars.
        self.ID=ID
        # Determine whether the vehicle can be rented. If True means rentable, False means it has been rented.
        self.available=True
        # Time to start renting the car.
        self.rent_start=None
        # Time to return the car.
        self.rent_back=None
        # Reantal Duration
        self.days=0
        #  When the vehicle is rented out, record its employer.
        self.owner: 'CUSTOMER'=None

    def start(self, date: datetime.datetime):
        """ Set the start time of renting the car."""
        self.rent_start=date

    def set_days(self, days: int):
        """  Set the number of days for renting a car."""
        self.days=days
        self._back(days)

    def _back(self, days: int):
        """Set the time of returning the car."""
        self.rent_back=self.rent_start + datetime.timedelta(days=days)

    def rented(self, name: 'CUSTOMER', start: datetime.datetime, days):
        """ Call this  when function when the vehicle is rented."""
        self.owner=name
        self.available=False
        self.start(start)
        self.set_days(days)

    def return_car(self):
        """Define the function to update the car status in the store and return the cutomer bill when changing cars."""
        self.available=True
        price=self._rent_price()
        return price

    def _rent_price(self):
        """ The function to calculate the bill."""
        customer=self.owner
        if customer.__class__.__name__=='VIP':
            return CAR[self.__class__.__name__.lower()]['vip'] * self.days
        if self.days / 7<=1:
            return CAR[self.__class__.__name__.lower()][
                       'short_period'] * self.days
        else:
            return CAR[self.__class__.__name__.lower()][
                       'long_period'] * self.days

    def __eq__(self, other):
        """ The definition function determines whether the current vehicle and other vehicles are the same vehicle."""
        return self.__class__.__name__==other.__class__.__name__ and self.ID == other.ID

    def __str__(self):
        """ Print the information of cars."""
        if self.rent_start is None:
            return f"{self.__class__.__name__}{self.ID}: Available"

        return f"{self.__class__.__name__}{self.ID}: {self.rent_start.strftime('%Y-%m-%d %H:%m')} - " \
               f"{self.rent_back.strftime('%Y-%m-%d %H:%m')}"


class Hatchback(Car):
    """ Hatchback cars inherit the car class."""

    def __init__(self, ID):
        super().__init__(ID)


class Sedan(Car):
    """ Sedan cars inherit the car class."""

    def __init__(self, ID):
        super().__init__(ID)


class SUV(Car):
    """ SUV cars inherit the car class."""

    def __init__(self, ID):
        super().__init__(ID)


class RentalShop:
    """ Define the class of the car rental shop. """

    def __init__(self):
        # The kind of cars.
        self.car_type=['hatchback', 'sedan', 'suv']
        # Save the number of vehicles with dict to make the category and number correspond.
        self.cars_counts=dict(zip(self.car_type, [4, 3, 3]))
        #  list of cars
        self.cars=[Hatchback(i) for i in range(4)] + \
                    [Sedan(i) for i in range(3)] + \
                    [SUV(i) for i in range(3)]
        # manage the cars which are rented
        self.rental=[]
        # current time
        self.date=datetime.datetime.now()

    def display(self):
        """  Defind the function to display the basic information.  """
        content='Note: price1: the price for rent a car less than a week' + '\n' + \
                'price2: the price for a rent a car more than a week' + '\n' + \
                'price3: the price for vip customer' + '\n' + \
                  self.date.strftime('%Y-%m-%d %H:%M') + '\n'

        content+='{:^10}|{:^12}|{:^8}|{:^8}|{:^8}'.format('type',
                                                            'available',
                                                            'price1',
                                                            'price2',
                                                            'price3') + '\n'

        for car in self.car_type:
            content+='{:^10}|{:^12}|{:^8}|{:^8}|' \
                       '{:^8}'.format(car,
                                      self.cars_counts[car],
                                      CAR[car]['short_period'],
                                      CAR[car]['long_period'],
                                      CAR[car]['vip'])
            content+='\n'
        print(content)

    def requests(self, customer: 'CUSTOMER'):
        """ Defind request function. When customers request a car run this function. """
        # greet customers
        customer_type=customer.__class__.__name__.lower()
        if customer_type=='customer':
            print('Dear normal customer: ')
        else:
            print('Dear VIP customer: ')
        try:

            car_type=input(
                'please input car type you want to rent: ').lower().strip()
            if car_type not in self.car_type:
                print('Please enter right type!!')
                return self.requests(customer)

            if self.cars_counts[car_type]==0:
                print(
                    'Sorry this car type is rent out!!Please choose other car!')
                return self.requests(customer)

            while True:
                # input the number of days that customer needs the car.
                days=input(
                    'Please input the number of days you want to rent: ').lower().strip()
                try:
                    days=int(days)
                except ValueError:
                    print('Please input right number')
                    continue
                if days<=0:
                    print('Rent days can not be zero or negative!')
                    continue
                break


        except Exception as e:
            print('------------------------------------------')
            print('------------ please enter again ----------')
            print('------------------------------------------')
            return self.requests(customer)
        # check available or not

        days = int(days)
        if customer.__class__.__name__=='VIP':
            print(
                f'You have rented a {car_type} car for {days} days.You will be'
                f'charged {CAR[car_type]["vip"]} per days, We hope '
                f'that you enjoy our service.')
        else:
            if days / 7<=1:
                print(
                    f'You have rented a {car_type} car for {days} days.You will be'
                    f'charged {CAR[car_type]["short_period"]} per days, We hope'
                    f'that you enjoy our service.')
            else:
                print(
                    f'You have rented a {car_type} car for {days} days.You will be'
                    f'charged {CAR[car_type]["long_period"]} per days, We hope'
                    f'that you enjoy our service.')
       # Once the vehicle is successfully rented, the information in the store should be updated, corresponding to the number of available vehicles-1 
       # Call the rent method of rented out vehicles to record relevant information, 
       # Save the rented vehicle in the rental
        self.cars_counts[car_type]=self.cars_counts[car_type] - 1
        for car in self.cars:
            if car.__class__.__name__.lower()==car_type:
                # customer get car
                if car.available:
                    car.rented(name=customer, start=copy.deepcopy(self.date),
                               days=days)
                    customer.rent_process(car)
                    # rent back info
                    self.rental.append(car)
                    break

        # Display the stock after each transaction
        print()
        print('----------- Update stock -----------')
        self.display()

    def getSingleCarBack(self, car: CAR):
        """ Defind a function to get single car back. """
        owner=car.owner
        # prompt the bill
        print('************************* Bill *******************************')
        if owner.__class__.__name__.lower()=='customer':
            print(
                f'Dear {owner.ID}: The bill for {car.__class__.__name__}: {car.return_car()} for {car.days} days')
        else:
            print(
                f'Dear VIP {owner.ID}: The bill for {car.__class__.__name__}: {car.return_car()} for {car.days} days')
        print('*********************Bill Finish ******************************')
        print()
        owner.car_return(car)

        self.cars_counts[car.__class__.__name__.lower()] += 1
        temp = []
        for _car in self.rental:
            if _car != car:
                temp.append(_car)
        self.rental = temp
        return

    def update(self):
        """ Defind a funtion to update time"""
        self.date = self.date + datetime.timedelta(days=1)


class CUSTOMER:
    """ Class of customer. """

    def __init__(self, ID):
        self.ID = ID
        # Used to save the vehicle information rented by customers
        self.rented = []

    def check_have_rent_car(self):
        """Check if current customer have rented a car."""
        return len(self.rented) == 1

    @staticmethod
    def inquire(rental_shop: 'RentalShop'):
        rental_shop.display()

    def rent(self, rental_shop: 'RentalShop'):
        """  Call this function when renting a car."""
        rental_shop.requests(self)

    def rent_process(self, car):
        """ After successfully renting a car, save the rented car in the list."""
        self.rented.append(car)

    def car_return(self, car):
        """ Call this function when the vehicle returns, and delete the returned vehicle from the list."""
        self.rented = []


class VIP(CUSTOMER):
    """ Defind the class of VIP customer. It is inherit from the general class. """

    def __init__(self, ID):
        super(VIP, self).__init__(ID)
