from .runner import Runner
from .visualizer import visualize
import pandas as pd


class SnackRace:
    def __init__(self, runners: list[Runner]):
        self.runners = runners

        self.df = None

    def show(self):
        visualize(self.df)

    def get_summary_df(self) -> pd.DataFrame:
        data = [
            {'name': runner.name,
             'place': place,
             'goaled_in': runner.goaled_time}
            for place, runner in enumerate(sorted(self.runners), start=1)
        ]
        return pd.DataFrame(data)

    def run(self) -> pd.DataFrame:
        runners = self.runners
        [runner.reset() for runner in runners]
        while any(not runner.is_finished for runner in runners):
            [runner.step() for runner in runners]

        data = [{'name': runner.name,
                 'time': time,
                 'pos': pos}
                for runner in runners
                for time, pos in enumerate(runner.history)]
        df = pd.DataFrame(data)
        df = df.sort_values(by='time', ignore_index=True)
        df["rank"] = df.groupby("time")["pos"].rank(method="first", ascending=False).astype(int)
        self.df = df

    def manipulate(self):
        raise NotImplementedError
