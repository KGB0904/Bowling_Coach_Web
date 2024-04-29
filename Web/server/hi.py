class 자동차:
    def __init__(self,speed,gear):
        self.speed = 0
        self.gear = 1
        self.max_speed = 100
        self.min_speed = 0
        self.max_gear = 10
        self.min_gear = 1

    def go(self):
        self.speed = self.speed + 1
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        print("고고!")
    def stop(self):
        self.speed = self.speed - 1
        if self.speed < self.min_speed:
            self.speed = self.min_speed
        print("스탑!")

    def gear_up(self):
        self.gear = self.gear + 1
        if self.gear > self.max_gear:
            self.gear = self.max_gear
        print("기어 업!")

    def gear_down(self):
        self.gear = self.gear - 1
        if self.gear < self.min_gear:
            self.gear = self.min_gear
        print("기어 다운!")


car1=자동차(0,1)

car1.go()
print(car1.speed)

car1.gear_up()
print(car1.speed)