"""
__author__ = Hagai Hargil
"""
import unittest
from pysight.ascii_list_file_parser.file_io import ReadMeta
import pathlib


class TestMetaTools(unittest.TestCase):
    """ Tests for new multiscaler readout functions """

    list_of_file_names = [
        str(next(pathlib.Path("tests/").rglob("*1.lst")).absolute()),
        str(next(pathlib.Path("tests/").rglob("*2.lst")).absolute()),
    ]
    file_io_objects = []
    for file in list_of_file_names:
        cur_obj = ReadMeta(
            file,
            debug=False,
            input_start="Frames",
            input_stop1="PMT1",
            input_stop2="Lines",
        )
        cur_obj.run()
        file_io_objects.append(cur_obj)

    def test_determine_binary(self):
        list_of_file_binary_formats = [False, False]
        list_of_returned_binaries = []
        for oname in self.file_io_objects:
            list_of_returned_binaries.append(oname.is_binary)

        self.assertEqual(list_of_file_binary_formats, list_of_returned_binaries)

    def test_check_range_extraction(self):
        list_of_real_range = [80_000_000, 8064]
        list_of_returned_range = []
        for oname in self.file_io_objects:
            list_of_returned_range.append(oname.data_range)

        self.assertEqual(list_of_real_range, list_of_returned_range)

    def test_check_time_patch_extraction(self):
        list_of_real_time_patch = ["32", "5b"]
        list_of_returned_time_patch = []
        for oname in self.file_io_objects:
            metadata = oname._ReadMeta__get_metadata()
            list_of_returned_time_patch.append(oname.timepatch)

        self.assertEqual(list_of_real_time_patch, list_of_returned_time_patch)

    def test_check_start_of_data_value(self):
        list_of_real_start_loc = [1749, 1567]
        list_of_returned_locs = []
        for oname in self.file_io_objects:
            list_of_returned_locs.append(oname.start_of_data_pos)

        self.assertEqual(list_of_real_start_loc, list_of_returned_locs)

    def test_find_active_channels(self):
        real_list_of_active_channels = [
            [True, True, True, False, False, False],
            [True, True, True, False, False, False],
        ]
        returned_list_of_active_channels = []
        for oname in self.file_io_objects:
            metadata = oname._ReadMeta__get_metadata()
            returned_list_of_active_channels.append(
                oname.list_of_recorded_data_channels
            )

        self.assertEqual(returned_list_of_active_channels, real_list_of_active_channels)

    def test_create_inputs_dict(self):
        real_list_of_real_inputs_dict = [
            {"Frames": "110", "PMT1": "001", "Lines": "010"},
            {"Frames": "110", "PMT1": "001", "Lines": "010"},
        ]
        list_of_returned_inputs_dict = []
        for oname in self.file_io_objects:
            list_of_returned_inputs_dict.append(oname.dict_of_input_channels)

        self.assertEqual(list_of_returned_inputs_dict, real_list_of_real_inputs_dict)

    def test_fstchan(self):
        real_fstchan = [0, 54 * 8]
        returned_fstchan = []
        for oname in self.file_io_objects:
            returned_fstchan.append(oname.acq_delay)

        self.assertEqual(real_fstchan, returned_fstchan)

    def test_time_after_sweep(self):
        real_time_after = [120, 120]
        returned_time_after = []
        for oname in self.file_io_objects:
            returned_time_after.append(oname.time_after)

        self.assertEqual(real_time_after, returned_time_after)
