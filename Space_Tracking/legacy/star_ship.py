from player import player

HEIGHT = 10
WIDTH = 10


class Engine:
    def __init__(self, power: int, weight: int):
        self.power = power
        self.weight = weight


class Tank:
    def __init__(self, capacity: int, weight: int):
        self.capacity = capacity
        self.fuel = 0
        self.weight = weight


class StarShip:
    def __init__(self, name: str, capacity: int, location, engine, tank):
        self.name = name
        self.location = location
        self.engine = engine
        self.tank = tank
        self.capacity = capacity
        self.cargo = {'minerals': 0,
                      'medicines': 0,
                      'food': 0,
                      'materials': 0,
                      'appliances': 0,
                      'technic': 0,
                      'luxuries': 0
                      }

    @property
    def current_capacity(self) -> int:
        return sum(self.cargo.values())

    def get_distance(self, planet) -> int:
        distance = round(((planet.coord[0] - self.location.coord[0]) ** 2 + (
                planet.coord[1] - self.location.coord[1]) ** 2) ** 0.5)
        return distance

    def move_to_planet(self, planet):
        if planet != self.location:
            distance = self.get_distance(planet)
            if distance * self.engine.power > self.tank.fuel:
                print('Вы не можете полететь на эту планету, так как у вас не хватает топлива.')
            elif distance * self.engine.power <= self.tank.fuel:
                self.location = planet
                self.tank.fuel -= distance * self.engine.power
                print(f'Вы прибыли на планету {planet.name}')
        else:
            print('Вы уже находитесь на этой планете.')

    @staticmethod
    def is_valid_fuel(fuel: int) -> bool:
        if type(fuel) is int and fuel > 0:
            return True
        else:
            print('Введите числовое положительное значение.')
        return False

    def is_possible_refuel(self, fuel: int) -> bool:
        if fuel * self.location.stock.products['fuel'][1] <= player.money:
            if fuel <= self.location.stock.products['fuel'][0]:
                return True
            else:
                print(
                    f"{fuel} топлива нет на складе. На складе {self.location.stock.products['Fuel'][0]} "
                    f"топлива."
                )
        else:
            print(f'У вас не хватает денег, чтобы заправить {fuel} топлива.')
        return False

    def refuel(self, fuel: int):
        if self.is_valid_fuel(fuel) and self.is_possible_refuel(fuel):
            if fuel + self.tank.fuel > self.tank.capacity:
                player.money -= (self.tank.capacity - self.tank.fuel) * self.location.stock.products['fuel'][1]
                self.location.stock.products['fuel'][0] -= self.tank.capacity - self.tank.fuel
                self.tank.fuel += self.tank.capacity - self.tank.fuel
            else:
                player.money -= self.location.stock.products['fuel'][1] * fuel
                self.location.stock.products['fuel'][0] -= fuel
                self.tank.fuel += fuel

    def is_valid_product_b(self, product: str, amount: int) -> bool:
        if product in self.cargo:
            if type(amount) is int and amount > 0:
                return True
            else:
                print('Введите числовое положительное значение.')
        else:
            print('Такого продукта нет.')
        return False

    def is_possible_buy(self, product: str, amount: int) -> bool:
        if self.location.stock.products[product][0] >= amount:
            if player.money >= self.location.stock.products[product][1] * amount:
                return True
            else:
                print(f'У вас не хватает денег, чтобы купить {amount} {product.lower()}.')
        else:
            print(f'{amount} {product.lower()} нет на складе. На складе '
                  f'{self.location.stock.products[product][0]} {product.lower()}')
        return False

    def buy(self, product: str, amount: int):
        if self.is_valid_product_b(product, amount) and self.is_possible_buy(product, amount):
            if self.current_capacity + amount > self.capacity:
                player.money -= (self.capacity - self.current_capacity) * self.location.stock.products[product][1]
                self.location.stock.products[product][0] -= self.capacity - self.current_capacity
                self.cargo += self.capacity - self.current_capacity
            else:
                player.money -= self.location.stock.products[product][1] * amount
                self.location.stock.products[product][0] -= amount
                self.cargo[product] += amount

    def is_valid_product_s(self, product: str, amount: int) -> bool:
        if product in self.cargo:
            if type(amount) is int and amount > 0:
                return True
            else:
                print('Введите числовое положительное значение.')
        else:
            print('Такого продукта нет.')
        return False

    def sale(self, product: str, amount: int):
        if self.is_valid_product_s(product, amount):
            if self.cargo[product] >= amount:
                self.cargo[product] -= amount
                self.location.stock.products[product][0] += amount
                player.money += self.location.stock.products[product][1] * amount
            else:
                print(f'У вас есть только {self.cargo[product]} {product.lower()}')