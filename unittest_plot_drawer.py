import unittest
from unittest.mock import patch
from plot_drawer import PlotDrawer

class TestPlotDrawer(unittest.TestCase):
    def setUp(self):
        self.plot_drawer = PlotDrawer()

    @patch('os.path.exists')
    @patch('os.makedirs')
    def test_directories_created(self, mock_makedirs, mock_exists):
        mock_exists.return_value = False
        self.plot_drawer.__init__()
        self.assertTrue(mock_makedirs.called)

    @patch('requests.get')
    def test_data_loading(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = '''{
            "mean": [3.956313, 23.019122, 1.013833],
            "max": [8.562939, 52.605437, 1.950322],
            "min": [0.274574, 0.724299, 0.301673],
            "floor_mean": [3.987864, 1.253103, 0.659138],
            "floor_max": [8.562939, 1.897612, 1.318714],
            "floor_min": [0.274574, 0.724299, 0.301673],
            "ceiling_mean": [3.924762, 44.785141, 1.368528],
            "ceiling_max": [8.501885, 52.605437, 1.950322],
            "ceiling_min": [0.331494, 36.880814, 0.878106]
        }'''
        plot_paths = self.plot_drawer.draw_plots()
        self.assertNotEqual(plot_paths, [])

    @patch('matplotlib.pyplot.savefig')
    def test_plots_saved(self, mock_savefig):
        with patch('requests.get') as mock_get:
            mock_get.return_value.status_code = 200
            mock_get.return_value.text = '''{
            "mean": [3.956313, 23.019122, 1.013833],
            "max": [8.562939, 52.605437, 1.950322],
            "min": [0.274574, 0.724299, 0.301673],
            "floor_mean": [3.987864, 1.253103, 0.659138],
            "floor_max": [8.562939, 1.897612, 1.318714],
            "floor_min": [0.274574, 0.724299, 0.301673],
            "ceiling_mean": [3.924762, 44.785141, 1.368528],
            "ceiling_max": [8.501885, 52.605437, 1.950322],
            "ceiling_min": [0.331494, 36.880814, 0.878106]
        }'''
            plot_paths = self.plot_drawer.draw_plots()
            self.assertTrue(mock_savefig.called)

if __name__ == '__main__':
    unittest.main()
