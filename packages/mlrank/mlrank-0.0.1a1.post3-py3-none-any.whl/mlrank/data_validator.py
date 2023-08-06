import pickle
import pandas as pd


def type_cast(val):
    try:
        return float(val)
    except (ValueError, TypeError):
        return val.strip().lower()


class Litmus:

    def __init__(self, dataframe=None):
        self.df = dataframe
        self._tc = self._load_tc()
        self._eda = self._load_eda()

    def __call__(self, file, eda):
        score = 0
        try:
            dataframe = pd.read_csv(file)
            self.df = dataframe
            score += self._test()
            dataframe = pd.read_csv(eda)
            self.df = dataframe
            score += self._test_eda()
        except Exception as ex:
            pass
        print(int(round(score, 0)))

    @staticmethod
    def _load_tc():
        import os
        directory, filename = os.path.split(__file__)
        return pickle.load(open(os.path.join(directory, 'tc.dat'), 'rb'))

    @staticmethod
    def _load_eda():
        import os
        directory, filename = os.path.split(__file__)
        return pickle.load(open(os.path.join(directory, 'eda.dat'), 'rb'))

    def _test_cn(self):
        error_score = 0
        cn = self._tc.get('cn')
        for col in cn:
            if col not in self.df.columns:
                error_score += 20
        return error_score

    def _test_rc(self):
        error_score = 0
        rc = self._tc.get('rc')
        rec_cnt = self.df.shape[0]
        if rec_cnt != rc[0]:
            error_score += (abs(rec_cnt - rc[0]) / rc[0]) * 100
        non_na_rec_cnt = self.df.dropna().shape[0]
        if non_na_rec_cnt != rc[1]:
            error_score += (abs(non_na_rec_cnt - rc[1]) / rc[1]) * 100
        return error_score

    def _test_col(self):
        error_score = 0
        cols = self._tc.get('col')
        for col in cols:
            name, has_null, non_na_cnt, unique = col
            if name in self.df.columns:
                if has_null != bool(self.df[name].isnull().sum()):
                    error_score += 1
                if non_na_cnt != self.df[name].dropna().shape[0]:
                    error_score += 1
                if unique != self.df[name].unique().shape[0]:
                    error_score += 1
            else:
                error_score += 5
        return error_score

    def _test(self):
        max_error = 450
        error_score = 0
        error_score += self._test_cn()
        error_score += self._test_rc()
        error_score += self._test_col()
        error_score = int(round(error_score))
        score = max_error - error_score
        return (score/max_error) * 30

    def _test_eda(self):
        max_score = 11
        error = 0
        lst = list()
        for item in self.df.ans.tolist():
            lst.append(type_cast(item))
        for x, y in zip(self._eda, lst):
            if x != y:
                error += 1
        return ((max_score-error)/max_score) * 70


litmus = Litmus()
