from carRent import CUSTOMER, RentalShop, Car, VIP
import datetime
import random



""" 
This file is the main code in the part 1 of coursework.

This car rental program initialize ten cars in three categories. 
Customers can see the car rental or return options after input their customer type (ordinary customer or VIP customer). 
When all ten cars are lent, the system will randomly ask the customer if they need to return the car. 
If current customer needs to return the car, enter 2 to return the car, 
if current customer don’t need to return, enter 1 then the systom will ask next random customer. 
When the customer chooses to return the car, the rental car shop will give the customer a bill. 
New customers can borrow cars when there are free cars.""" 




def make_select(customer: 'CUSTOMER'):
     # Define the function for customers to choose to rent or return the car.
    select='1'
    while True:
        select=input(
            f'Dear {customer.__class__.__name__.lower()} {customer.ID}: what you want to do:' + '\n' +
            f'1: rent a car' + '\n' +
            f'2: return a car' + '\n' +
            f'please enter 1 or 2: ').strip()

        if select not in ['1', '2']:
            print('Please input current optional 1 or 2. Enter again!')
            continue
        break
    return select

def selectAction(select, customer: 'CUSTOMER'):
    # Define the function that the customer has rented the car. Then only needs to ask whether to return the car.
    if select=='1':
        if customer.check_have_rent_car():
            print(
                'Sorry you ready rent a car!!Please rent other car after'
                'you return the car you rent first!')
            return -1
        else:
            customer.inquire(carShop)
            carShop.requests(customer)
            return 1
    else:
        if customer.check_have_rent_car():
            carShop.getSingleCarBack(customer.rented[0])
            return 1
        else:
            print('You have not rent a car.Please entry again')
            return -1


if __name__=='__main__':
    #  Initialize rental shop
    carShop=RentalShop()
    current_customer=CUSTOMER(0)
    # Initialize the customer list. Customers choose whether they are VIP or ordinary customers
    customer_id=0
    customer_type='normal'
    while True:
        # It shows that there are still vehicles that can be borrowed.
        if len(carShop.rental)!=10:
            while True:
                customer_type=input(f'Please select the customer type for '
                                      f'customer{customer_id}[normal/vip]: ').strip().lower()
                if customer_type not in ['normal', 'vip']:
                    print('please input right customer type!')
                    continue
                if customer_type=='normal':
                    current_customer=CUSTOMER(customer_id)
                else:
                    current_customer=VIP(customer_id)
                break
            customer_id+=1

            # Car loan and return operation.
            while True:
                select=make_select(current_customer)
                res=selectAction(select, current_customer)
                if res==1:
                    break
        else:
            rent_number=0
            # Randomly select a customer to return a car.
            if random.random()<0.5:
                rent_number=1
            # Randomly select customers to return two cars.
            else:
                rent_number=2
            i=0

            while i<rent_number:
                print('------------- require a customer who rent a car -----------')
                return_car=random.choice(carShop.rental)
                owner=return_car.owner
                select=make_select(owner)
                res=selectAction(select, owner)
                if res==1:
                    i += 1