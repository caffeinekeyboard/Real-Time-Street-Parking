import settings
from datetime import datetime

# import math
# Dynamic Pricing
# Parking price is a function of the equivalent car space needed, weekend or weekday, current time, location of the
# street, number of parking slots available when the user wants to book a slot, walking distance
# parking charges will increase every hour by 100%
# peak hours = 8 am to 12 pm and 5 pm to 9 pm

'''
r1 = 60  # %age rise in vehicle registrations in a financial year
r2 = 8.15  # max. %age rise in ready reckoner rate
base_charge = 60  # rs/hour

revised_charge = base_charge + (0.61 * r1 + 0.4 * r2) * base_charge
base_charge = revised_charge
'''


class Price:

    def __init__(self, zone, weekend, time_booked):

        self.zone = zone
        self.weekend = weekend

        self.time_booked = time_booked
        self.hours = 0
        self.total_price = 0

        self.illegal = False

        if self.zone == 'A':
            self.base_price = 60
        elif self.zone == 'B':
            self.base_price = 40
        else:
            self.base_price = 20

    @staticmethod
    def get_slots():
        available_slots = 10  # value is hard-coded here temporarily
        return available_slots

    def get_duration(self, now):
        time = datetime(int(self.time_booked[0:4]), int(self.time_booked[5:7]), int(self.time_booked[8:10]),
                        int(self.time_booked[11:13]), int(self.time_booked[14:16]))
        hours = ((now - time).total_seconds()) / 3600  # duration of parking in hours
        return hours

    def check_legal(self, now):
        # if the user parks for more than 24 hours a fine will be levied
        if self.get_duration(now) > 24:
            self.illegal = True

    def get_price(self):

        now = datetime.now()
        time = datetime(int(self.time_booked[0:4]), int(self.time_booked[5:7]), int(self.time_booked[8:10]),
                        int(self.time_booked[11:13]), int(self.time_booked[14:16]))

        hour = time.hour

        if self.weekend:
            self.base_price = self.base_price * settings.WEEKEND_RATE

        if time.day == now.day:
            while hour < now.hour:
                if settings.EVEN_PEAK_TIME_START <= hour <= settings.EVEN_PEAK_TIME_END:
                    self.total_price += self.base_price * settings.EVEN_PEAK_RATE
                elif settings.MORN_PEAK_TIME_START <= hour <= settings.MORN_PEAK_TIME_END:
                    self.total_price += self.base_price * settings.MORN_PEAK_RATE
                else:
                    self.total_price += self.base_price
                hour += 1
            if time.minute < now.minute:
                if settings.EVEN_PEAK_TIME_START <= hour <= settings.EVEN_PEAK_TIME_END:
                    self.total_price += self.base_price * settings.EVEN_PEAK_RATE
                elif settings.MORN_PEAK_TIME_START <= hour <= settings.MORN_PEAK_TIME_END:
                    self.total_price += self.base_price * settings.MORN_PEAK_RATE
                else:
                    self.total_price += self.base_price
        elif time.day + 1 == now.day:  # check for corner cases

            while hour < 24:
                if settings.EVEN_PEAK_TIME_START <= hour <= settings.EVEN_PEAK_TIME_END:
                    self.total_price += self.base_price * settings.EVEN_PEAK_RATE
                elif settings.MORN_PEAK_TIME_START <= hour <= settings.MORN_PEAK_TIME_END:
                    self.total_price += self.base_price * settings.MORN_PEAK_RATE
                else:
                    self.total_price += self.base_price
                hour += 1

            hour = 0
            if hour == now.hour:
                if time.minute < now.minute:
                    self.total_price += (self.base_price * 2)
                else:
                    self.total_price += self.base_price
                self.check_legal(now)
                if not self.illegal:
                    return self.total_price
                else:
                    # if the user parks for more than 24 hours a fine will be levied
                    return f'You parked for: {self.get_duration(now)} hours. A fine will be levied.'

            while hour < now.hour:
                if settings.EVEN_PEAK_TIME_START <= hour <= settings.EVEN_PEAK_TIME_END:
                    self.total_price += self.base_price * settings.EVEN_PEAK_RATE
                elif settings.MORN_PEAK_TIME_START <= hour <= settings.MORN_PEAK_TIME_END:
                    self.total_price += self.base_price * settings.MORN_PEAK_RATE
                else:
                    self.total_price += self.base_price
                hour += 1
            if time.min < now.min:
                if settings.EVEN_PEAK_TIME_START <= hour <= settings.EVEN_PEAK_TIME_END:
                    self.total_price += self.base_price * settings.EVEN_PEAK_RATE
                elif settings.MORN_PEAK_TIME_START <= hour <= settings.MORN_PEAK_TIME_END:
                    self.total_price += self.base_price * settings.MORN_PEAK_RATE
                else:
                    self.total_price += self.base_price

        self.check_legal(now)
        if not self.illegal:
            return self.total_price
        else:
            # if the user parks for more than 24 hours a fine will be levied
            return f'You parked for: {self.get_duration(now)} hours. A fine will be levied.'


car_1 = Price('A', True, settings.BOOKING_TIME)
print(car_1.get_price())
