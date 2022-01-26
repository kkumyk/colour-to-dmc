from colour_to_dmc import nearest_dmc_thread


class TestNearestDMCThread:
    def test_loading_threads_csv(self):
        assert len(nearest_dmc_thread.dmc_threads) != 0

    def test_find_nearest_thread(self):
        # try thread with the exact RGB colour combination
        black = nearest_dmc_thread.rgb_to_dmc(0, 0, 0)
        assert black["thread"] == "#310"

        # try thread with the near RGB colour combination
        not_quite_dark_lavender = nearest_dmc_thread.rgb_to_dmc(165, 125, 161)
        assert not_quite_dark_lavender["thread"] == "#209"
