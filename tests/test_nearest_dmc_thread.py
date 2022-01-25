from colour_to_dmc import nearest_dmc_thread


class TestNearestDMCThread:
    def test_loading_threads_csv(self):
        assert len(nearest_dmc_thread.dmc_threads) != 0


