#!/usr/bin/env python2

import pylcd
import datetime

PINMAP = {
        'RS': 7,
        'E': 8,
        'D4': 17,
        'D5': 18,
        'D6': 21,
        'D7': 22,
}

class Exam:
    def __init__(self, date, name):
        self.date = datetime.date(date[0], date[1], date[2])
        self.name = name

class ExamLCD:

    def __init_lcd(self):
        self.display = pylcd.hd44780.Display(backend = pylcd.hd44780.GPIOBackend,
                                             pinmap = PINMAP,
                                             lines = 4,
                                             columns = 20,
                                             enable_backlight = False)
        self.display.clear()
        self.display.home()

    def __init__(self):
        self.__init_lcd()
        self.exams = []
        self.date = datetime.date.today()

    @staticmethod
    def days_till(exam):
        timedelta = exam.date - datetime.date.today() 
        return timedelta.days

    def update(self):
        # We will assume that the exams have been added in date order and
        # simply display the first 4 that haven't already occured

        # Clear the LCD display if the day has changed
        if self.date != datetime.date.today():
            self.display.clear()
            self.display.home()
        
        # Update the date we have stored
        self.date = datetime.date.today()

        # The number of exams we've displayed so far
        displayed = 0

        for e in self.exams:
            dt = self.days_till(e)
            if dt < 0:
                # Do next exam
                continue 
            elif displayed < 4:
                self.display.set_cursor_position(line = displayed, column = 0)

                if dt == 0:
                    self.display.write("{0}: today".format(e.name, dt))
                else:
                    self.display.write("{0}: {1} days".format(e.name, dt))

                displayed += 1

    def daemon(self):
        while True:
            self.update()
            # Sleep for 5 seconds
            time.sleep(5)

if __name__ == "__main__":
    el = ExamLCD()
    # Dates are Y, M, D tuples
    el.exams.append(Exam((2014, 05, 20), "TPOP Prac"))
    el.exams.append(Exam((2014, 05, 23), "TPOP Theory"))
    el.exams.append(Exam((2014, 05, 27), "NUMA"))
    el.exams.append(Exam((2014, 05, 30), "MFCS"))
    el.exams.append(Exam((2014, 06, 02), "DACS DCD"))
    el.exams.append(Exam((2014, 06, 02), "DACS CAR"))
    el.exams.append(Exam((2014, 06, 03), "ICAR"))
    el.daemon()
