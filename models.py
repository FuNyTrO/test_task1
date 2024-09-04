from django.db import models
import pandas


class Player(models.Model):
    player_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        # Добавил __str__ для каждой заданной модели для удобства использования
        return self.player_id


class Level(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Prize(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class PlayerLevel(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    completed = models.DateField()
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)
    prize = models.ForeignKey(
        Prize, null=True, blank=True, on_delete=models.SET_NULL)

    def give_prize(self, prize):
        # Метод присвоения приза. Проверяет пройден ли уровень и, если да
        # то пройден в первый раз или нет, чтобы за один уровень не было несколько призов
        if not self.is_completed:
            raise ValueError("Level not completed")

        if self.prize:
            raise ValueError(
                "The reward for the level has already been claimed")

        self.prize = prize
        self.save()

    def __str__(self):
        return f"{self.player.player_id} - {self.level.title}"


class LevelPrize(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    received = models.DateField()

    def __str__(self):
        return f"{self.prize.title} for {self.level.title}"


def export_to_csv(file_path):
    player_levels = PlayerLevel.objects.values(
        'player__player_id', 'level__title', 'is_completed', 'prize__title'
    )

    # преобразую в dataframe для django pandas
    df = pandas.DataFrame(list(player_levels))

    data = []  # список хранения данных

    for _, row in df.iterrows():
        level_title = row['level__title']

        if row['prize__title']:
            prize_title = row['prize__title']
        else:
            prize_title = 'No Prize'  # проверка наличия приза для уровня

        # возвращаем страку вместо булиевого значения
        completed_status = 'Yes' if row['is_completed'] else 'No'

        data.append({
            'Player ID': row['player__player_id'],
            'Level Title': level_title,
            'Level Completed': completed_status,
            'Prize Title': prize_title
        })  # добавление данных

    final_df = pandas.DataFrame(data)  # создание конечного dataframe

    final_df.to_csv(file_path, index=False)  # сохранение в csv файл

    print("Data successfully exported to", file_path)
