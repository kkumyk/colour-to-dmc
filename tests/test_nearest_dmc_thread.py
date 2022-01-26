from colour_to_dmc import nearest_dmc_thread


class TestNearestDMCThread:
    def test_loading_threads_csv(self):
        assert len(nearest_dmc_thread.dmc_threads) != 0

    def test_find_nearest_thread(self):
        # try an exact color
        black = nearest_dmc_thread.rgb_to_dmc(0, 0, 0)
        assert black["thread"] == "#310"

        # # try a near color
        # not_quite_light_salmon = nearest_dmc_thread.rgb_to_dmc(254, 200, 201)
        # self.assertEqual(not_quite_light_salmon["floss"], "#761")
