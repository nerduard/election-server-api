import unittest
import json
import os
from server import app, controller


class TestScoreboard(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.server = app.test_client(self)
        file_dir: str = os.path.dirname(os.path.realpath(__file__))
        self.RESULT_SAMPLE_PATH: str = f"{file_dir}/resources/sample-election-results"

    def load_and_post_result_file(self, num: str) -> dict:
        file_number: str = str(num).zfill(3)
        with open(f"{self.RESULT_SAMPLE_PATH}/result{file_number}.json", "r") as file:
            result = file.read()
        return self.server.post("/result", json=json.loads(result))

    def load_results(self, quantity: int) -> list[dict]:
        results = []
        for i in range(quantity):
            results.append(self.load_and_post_result_file(i + 1))
        return results

    def fetch_scoreboard(self) -> list[dict]:
        response = self.server.get("/scoreboard")
        return [] if response.data == b'{}\n' else json.loads(response.data.decode("utf-8"))

    def setUp(self) -> None:
        controller.reset()

    def test_first_5(self) -> None:
        self.load_results(5)
        scoreboard: list = self.fetch_scoreboard()
        self.assertNotEqual(len(scoreboard), 0)
        assert scoreboard['parties']['LD']['seats'] == 1
        assert scoreboard['parties']['LAB']['seats'] == 4
        assert scoreboard['winner'] == None

    def test_first_100(self) -> None:
        self.load_results(100)
        scoreboard: list = self.fetch_scoreboard()
        self.assertNotEqual(len(scoreboard), 0)
        assert scoreboard['parties']['LD']['seats'] == 12
        assert scoreboard['parties']['LAB']['seats'] == 56
        assert scoreboard['parties']['CON']['seats'] == 31
        assert scoreboard['winner'] == None

    def test_first_554(self) -> None:
        self.load_results(554)
        scoreboard: list = self.fetch_scoreboard()
        self.assertNotEqual(len(scoreboard), 0)
        assert scoreboard['parties']['LD']['seats'] == 52
        assert scoreboard['parties']['LAB']['seats'] == 325
        assert scoreboard['parties']['CON']['seats'] == 167
        assert scoreboard['winner'] == 'LAB'

    def test_all_results(self) -> None:
        self.load_results(650)
        scoreboard: list = self.fetch_scoreboard()
        # print(scoreboard)
        self.assertNotEqual(len(scoreboard), 0)
        assert scoreboard['parties']['LD']['seats'] == 62
        assert scoreboard['parties']['LAB']['seats'] == 349
        assert scoreboard['parties']['CON']['seats'] == 210
        assert scoreboard['winner'] == 'LAB'
        sum = 0
        for party in scoreboard['parties']:
            sum += scoreboard['parties'][party]['seats']
        assert sum == 650


if __name__ == "__main__":
    unittest.main()
