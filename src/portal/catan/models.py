from django.db import models

# Create your models here.


class CardSet(models.Model):
    lumber = models.IntegerField(default=0)
    brick = models.IntegerField(default=0)
    wool = models.IntegerField(default=0)
    grain = models.IntegerField(default=0)
    ore = models.IntegerField(default=0)
    dev_knight = models.IntegerField(default=0)
    dev_one_victory_point = models.IntegerField(default=0)
    dev_road_building = models.IntegerField(default=0)
    dev_monopoly = models.IntegerField(default=0)
    dev_year_of_plenty = models.IntegerField(default=0)

    def update_card_set(self, resource_type: str, inc: int):
        if resource_type == 'lumber':
            self.lumber = self.lumber + inc
        elif resource_type == 'brick':
            self.brick = self.brick + inc
        elif resource_type == 'wool':
            self.wool = self.wool + inc
        elif resource_type == 'grain':
            self.grain = self.grain + inc
        elif resource_type == 'ore':
            self.ore = self.ore + inc
        elif resource_type == 'dev_knight':
            self.dev_knight = self.dev_knight + inc
        elif resource_type == 'dev_one_victory_point':
            self.dev_one_victory_point = self.dev_one_victory_point + inc
        elif resource_type == 'dev_road_building':
            self.dev_road_building = self.dev_road_building + inc
        elif resource_type == 'dev_monopoly':
            self.dev_monopoly = self.dev_monopoly + inc
        else:
            self.dev_year_of_plenty = self.dev_year_of_plenty + inc


class Player(models.Model):
    card_set: CardSet = models.OneToOneField(CardSet, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    user_id = models.IntegerField(default=0)
    color = models.CharField(max_length=10)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)

    def save_all(self):
        self.card_set.save()
        self.save()


class Bank(models.Model):
    card_set: CardSet = models.OneToOneField(CardSet, on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)

    def save_all(self):
        self.card_set.save()
        self.save()


class HarborSea(models.Model):
    LUMBER = 'LR'
    BRICK = 'BK'
    WOOL = 'WL'
    GRAIN = 'GN'
    ORE = 'OE'
    ANY3 = 'AY'
    Harbor_TYPE = [
        (LUMBER, 'Lumber'),
        (BRICK, 'Brick'),
        (WOOL, 'Wool'),
        (GRAIN, 'Grain'),
        (ORE, 'Ore'),
        (ANY3, 'Any3'),
    ]

    type = models.CharField(
        max_length=10,
        choices=Harbor_TYPE,
        default=ANY3)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)


class HarborLand(models.Model):
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    z = models.IntegerField(default=0)
    sea = models.ForeignKey(HarborSea, on_delete=models.CASCADE)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)


class Tile(models.Model):
    LUMBER = 'LUMBER'
    BRICK = 'BRICK'
    WOOL = 'WOOL'
    GRAIN = 'GRAIN'
    ORE = 'ORE'
    DESERT = 'DESERT'
    SEA = 'SEA'
    RESOURCE_TYPE = [
        (LUMBER, 'Lumber'),
        (BRICK, 'Brick'),
        (WOOL, 'Wool'),
        (GRAIN, 'Grain'),
        (ORE, 'Ore'),
        (DESERT, 'Desert'),
        (SEA, 'Sea'),
    ]

    type = models.CharField(
        max_length=10,
        choices=RESOURCE_TYPE,
        default=LUMBER)
    number = models.PositiveIntegerField(default=2, null=True)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)

    def save_all(self):
        self.save()


class Construction(models.Model):
    HOUSE = 'HS'
    TOWN = 'TN'
    ROAD = 'RD'
    BUILDING_TYPE = [
        (HOUSE, 'House'),
        (TOWN, 'Town'),
        (ROAD, 'Road'),
    ]

    type = models.CharField(
        max_length=10,
        choices=BUILDING_TYPE,
        default=ROAD)
    owner: Player = models.ForeignKey(Player, on_delete=models.CASCADE)
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    z = models.IntegerField(default=0)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)

    def save_all(self):
        self.owner.save_all()
        self.save()


class DiceHistory(models.Model):
    dice1 = models.PositiveIntegerField(default=1)
    dice2 = models.PositiveIntegerField(default=1)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    turn_id = models.IntegerField(default=0)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)

    def sum(self):
        return self.dice1 + self.dice2

    def save_all(self):
        self.player.save_all()
        self.save()


class RobberHistory(models.Model):
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='current_robber')
    is_knight = models.BooleanField(default=False)
    is_latest = models.BooleanField(default=False)
    victim = models.ForeignKey(Player, on_delete=models.CASCADE)
    turn_id = models.IntegerField(default=0)
    game = models.ForeignKey('Game', on_delete=models.CASCADE)


class Game(models.Model):
    SETTLE = 'ST'
    MAIN = 'MA'
    END = 'ED'
    GAME_STATUS = [
        (SETTLE, 'Settle'),
        (MAIN, 'Main'),
        (END, 'End'),
    ]

    map_name = models.CharField(max_length=200)
    state = models.CharField(max_length=200, default="START")
    turn_id = models.IntegerField(default=0)
    status = models.CharField(
        max_length=2,
        choices=GAME_STATUS,
        default=SETTLE)
    number_of_player = models.PositiveIntegerField(default=2)
    # TODO: rename to current_player_order
    current_player = models.IntegerField(default=0)

    def save_all(self):
        self.save()

    def __str__(self):
        return str({
            'map_name': self.map_name,
            'state': self.state,
            'status': self.status,
            'number_of_player': self.number_of_player,
            'current_player': self.current_player
        })
