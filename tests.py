from django.test import TestCase
from .models import Player, Level, Prize, PlayerLevel, LevelPrize, export_to_csv
import os
import pandas


class ExportToCSVTest(TestCase):

    def setUp(self):
        # Создаем тестовые данные
        self.player = Player.objects.create(player_id="player_1")
        self.level = Level.objects.create(title="Level 1", order=1)
        self.prize = Prize.objects.create(title="Prize 1")
        self.player_level = PlayerLevel.objects.create(
            player=self.player, level=self.level, is_completed=True, completed="2024-09-01", prize=self.prize
        )
        LevelPrize.objects.create(
            level=self.level, prize=self.prize, received="2024-09-02")

    def test_export_to_csv(self):
        file_path = 'test_player_levels.csv'
        export_to_csv(file_path)
        self.assertTrue(os.path.exists(file_path))
        df = pandas.read_csv(file_path)

        self.assertEqual(len(df), 1)
        self.assertEqual(df.loc[0, 'Player ID'], 'player_1')
        self.assertEqual(df.loc[0, 'Level Title'], 'Level 1')
        self.assertEqual(df.loc[0, 'Level Completed'], 'Yes')
        self.assertEqual(df.loc[0, 'Prize Title'], 'Prize 1')

        os.remove(file_path)
