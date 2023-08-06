"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = Hagai Har-Gil
"""

from typing import Union, Tuple
import matplotlib

matplotlib.rcParams["backend"] = "TkAgg"
import json
import pandas as pd
import warnings
import colorama
import numpy as np
import pickle
import matplotlib.pyplot as plt

from pysight.ascii_list_file_parser.file_io import ReadMeta
from pysight.ascii_list_file_parser.tabulation import Tabulate
from pysight.nd_hist_generator.allocation import Allocate
from pysight.nd_hist_generator.movie import Movie
from pysight.ascii_list_file_parser import timepatch_switch
from pysight.nd_hist_generator.outputs import OutputParser
from pysight.nd_hist_generator.gating import GatedDetection
from pysight.nd_hist_generator.photon_df import PhotonDF
from pysight.nd_hist_generator.tag_bits import ParseTAGBits
from pysight.ascii_list_file_parser.distribute_data import DistributeData
from pysight.nd_hist_generator.line_signal_validators.validation_tools import (
    SignalValidator,
)
from pysight.tkinter_gui_multiscaler import GuiAppLst
from pysight.tkinter_gui_multiscaler import verify_gui_input
from pysight.nd_hist_generator.volume_gen import VolumeGenerator
from pysight.binary_list_file_parser.binary_parser import BinaryDataParser
from pysight.read_lst import ReadData

colorama.init()


def main_data_readout(gui):
    """
    Main function that reads the lst file and processes its data.
    Should not be run independently - only from other "run_X" functions.
    """
    # Read the .lst file
    if gui.filename.endswith(".lst"):
        cur_file = ReadMeta(
            filename=gui.filename,
            input_start=gui.input_start,
            input_stop1=gui.input_stop1,
            input_stop2=gui.input_stop2,
            binwidth=gui.binwidth,
            use_sweeps=gui.sweeps_as_lines,
            mirror_phase=gui.phase,
        )
        cur_file.run()

        raw_data_obj = ReadData(
            filename=gui.filename,
            start_of_data_pos=cur_file.start_of_data_pos,
            timepatch=cur_file.timepatch,
            is_binary=cur_file.is_binary,
            debug=gui.debug,
        )
        raw_data = raw_data_obj.read_lst()

        if cur_file.is_binary:
            binary_parser = BinaryDataParser(
                data=raw_data,
                data_range=cur_file.data_range,
                timepatch=cur_file.timepatch,
                use_tag_bits=gui.tag_bits,
                dict_of_inputs=cur_file.dict_of_input_channels,
            )
            binary_parser.run()
        else:
            # Create input structures and create a DataFrame
            dict_of_slices_hex = timepatch_switch.ChoiceManagerHex().process(
                cur_file.timepatch
            )
            tabulated_data = Tabulate(
                data_range=cur_file.data_range,
                data=raw_data,
                dict_of_inputs=cur_file.dict_of_input_channels,
                use_tag_bits=gui.tag_bits,
                dict_of_slices_hex=dict_of_slices_hex,
                time_after_sweep=cur_file.time_after,
                acq_delay=cur_file.acq_delay,
                num_of_channels=cur_file.num_of_channels,
            )
            tabulated_data.run()

            separated_data = DistributeData(
                df=tabulated_data.df_after_timepatch,
                dict_of_inputs=tabulated_data.dict_of_inputs,
                use_tag_bits=gui.tag_bits,
            )
            separated_data.run()

    ####### START OF "PUBLIC API" ##########
    try:
        if cur_file.is_binary:
            relevant_columns = binary_parser.data_to_grab
            dict_of_data = binary_parser.dict_of_data
        else:
            relevant_columns = separated_data.data_to_grab
            dict_of_data = separated_data.dict_of_data
        lst_metadata = cur_file.lst_metadata
        fill_frac = gui.fill_frac \
        if cur_file.fill_fraction == -1 \
        else cur_file.fill_fraction
    except NameError:  # dealing with a pickle file
        print(f"Reading file {gui.filename}...")
        with open(gui.filename, "rb") as f:
            dict_of_data = pickle.load(f)
        lst_metadata = dict()
        relevant_columns = ["abs_time"]
        fill_frac = gui.fill_frac

    validated_data = SignalValidator(
        dict_of_data=dict_of_data,
        num_of_frames=gui.num_of_frames,
        binwidth=float(gui.binwidth),
        use_sweeps=gui.sweeps_as_lines,
        delay_between_frames=float(gui.frame_delay),
        data_to_grab=relevant_columns,
        line_freq=gui.line_freq,
        num_of_lines=gui.x_pixels,
        bidir=gui.bidir,
        bidir_phase=gui.phase,
        image_soft=gui.imaging_software,
    )

    validated_data.run()

    photon_df = PhotonDF(dict_of_data=validated_data.dict_of_data)
    tag_bit_parser = ParseTAGBits(
        dict_of_data=validated_data.dict_of_data,
        photons=photon_df.gen_df(),
        use_tag_bits=gui.tag_bits,
        bits_dict=gui.tag_bits_dict,
    )

    analyzed_struct = Allocate(
        bidir=gui.bidir,
        tag_offset=gui.tag_offset,
        laser_freq=float(gui.reprate),
        binwidth=float(gui.binwidth),
        tag_pulses=int(gui.tag_pulses),
        phase=gui.phase,
        keep_unidir=gui.keep_unidir,
        flim=gui.flim,
        censor=gui.censor,
        dict_of_data=validated_data.dict_of_data,
        df_photons=tag_bit_parser.gen_df(),
        tag_freq=float(gui.tag_freq),
        tag_to_phase=True,
    )
    analyzed_struct.run()

    # Determine type and shape of wanted outputs, and open the file pointers there
    outputs = OutputParser(
        num_of_frames=len(validated_data.dict_of_data["Frames"]),
        output_dict=gui.outputs,
        filename=gui.filename,
        x_pixels=gui.x_pixels,
        y_pixels=gui.y_pixels,
        z_pixels=gui.z_pixels if analyzed_struct.tag_interp_ok else 1,
        num_of_channels=analyzed_struct.num_of_channels,
        flim=gui.flim,
        binwidth=gui.binwidth,
        reprate=gui.reprate,
        lst_metadata=lst_metadata,
        debug=gui.debug,
    )
    outputs.run()

    if gui.gating:
        gated = GatedDetection(
            raw=analyzed_struct.df_photons, reprate=gui.reprate, binwidth=gui.binwidth
        )
        gated.run()

    data_for_movie = gated.data if gui.gating else analyzed_struct.df_photons

    # Create a movie object
    volume_chunks = VolumeGenerator(
        frames=analyzed_struct.dict_of_data["Frames"], data_shape=outputs.data_shape
    )
    frame_slices = volume_chunks.create_frame_slices()

    final_movie = Movie(
        data=data_for_movie,
        frames=analyzed_struct.dict_of_data["Frames"],
        frame_slices=frame_slices,
        num_of_frame_chunks=volume_chunks.num_of_chunks,
        reprate=float(gui.reprate),
        name=gui.filename,
        data_shape=outputs.data_shape,
        binwidth=float(gui.binwidth),
        bidir=gui.bidir,
        fill_frac=fill_frac,
        outputs=outputs.outputs,
        censor=gui.censor,
        mirror_phase=gui.phase,
        lines=analyzed_struct.dict_of_data["Lines"],
        num_of_channels=analyzed_struct.num_of_channels,
        flim=gui.flim,
        lst_metadata=lst_metadata,
        exp_params=analyzed_struct.exp_params,
        line_delta=int(validated_data.line_delta),
        use_sweeps=gui.sweeps_as_lines,
        tag_as_phase=True,
        tag_freq=float(gui.tag_freq),
        image_soft=gui.imaging_software,
        frames_per_chunk=volume_chunks.frames_per_chunk,
    )

    final_movie.run()

    return analyzed_struct.df_photons, final_movie


class GUIClass:
    """ Helper class to create intermediate representation of the GUI's content """

    def __init__(self, **entries):
        self.__dict__.update(entries)
        self.tag_bits_dict = dict(
            bits_grp_1_label=entries["bits_grp_1_label"],
            bits_grp_2_label=entries["bits_grp_2_label"],
            bits_grp_3_label=entries["bits_grp_3_label"],
        )

    @property
    def outputs(self):
        """ Create a dictionary with the wanted user outputs. """
        output = {}

        if self.summed is True:
            output["summed"] = True
        if self.memory is True:
            output["memory"] = True
        if self.stack is True:
            output["stack"] = True

        if "stack" in output:
            if not "summed" in output and not "memory" in output:
                warnings.warn(
                    "Performance Warning: Writing data to file might take a long time when the required"
                    " output is only 'Full Stack'."
                )
        return output


def tkinter_to_object(gui: Union[GuiAppLst, dict]) -> GUIClass:
    """ Convert a tkinter instance into a pickable dictionary """
    if isinstance(gui, dict):
        gui["tuple_of_data_sources"] = (
            "PMT1",
            "PMT2",
            "Lines",
            "Frames",
            "Laser",
            "TAG Lens",
            "Empty",
        )
        return GUIClass(**gui)
    else:
        dic = {
            key: val.get() for key, val in gui.__dict__.items() if "Var" in repr(val)
        }
        dic["tuple_of_data_sources"] = gui.tuple_of_data_sources
        return GUIClass(**dic)


def convert_json_to_input_dict(cfg_fname):
    """ Convert a config file to a usable dictionary """
    if not isinstance(cfg_fname, str):
        raise TypeError

    try:
        with open(cfg_fname) as f:
            gui = json.load(f)
        gui = {key: val[1] for key, val in gui.items()}
        return gui
    except:
        raise TypeError


def run(cfg_file: str = None) -> Tuple[pd.DataFrame, Movie]:
    """ Run PySight.

    :param str cfg_file: Optionally supply an existing configuration filename. Otherwise a GUI will open.

    :return (pd.DataFrame, Movie): DataFrame with all the data, and a ``Movie`` object.
    """
    from pysight.tkinter_gui_multiscaler import GuiAppLst
    from pysight.tkinter_gui_multiscaler import verify_gui_input

    if cfg_file:
        gui = convert_json_to_input_dict(cfg_file)
    else:
        gui = GuiAppLst()
        gui.root.mainloop()
    gui_as_object = tkinter_to_object(gui)
    verify_gui_input(gui_as_object)
    return main_data_readout(gui_as_object)


def run_batch_lst(
    foldername: str,
    glob_str: str = "*.lst",
    recursive: bool = False,
    cfg_file: str = "",
) -> pd.DataFrame:
    """
    Run PySight on all list files in the folder

    :param str foldername: - Main folder to run the analysis on.
    :param str glob_str: String for the `glob` function to filter list files
    :param bool recursive: Whether the search should be recursive.
    :param str cfg_file: Name of config file to use
    :return pd.DataFrame: Record of analyzed data
    """

    import pathlib
    from pysight.tkinter_gui_multiscaler import GuiAppLst
    from pysight.tkinter_gui_multiscaler import verify_gui_input
    import numpy as np

    path = pathlib.Path(foldername)
    num_of_files = 0
    if not path.exists():
        raise UserWarning(f"Folder {foldername} doesn't exist.")
    if recursive:
        all_lst_files = path.rglob(glob_str)
        print(f"Running PySight on the following files:")
        for file in list(all_lst_files):
            print(str(file))
            num_of_files += 1
        all_lst_files = path.rglob(glob_str)
    else:
        all_lst_files = path.glob(glob_str)
        print(f"Running PySight on the following files:")
        for file in list(all_lst_files):
            print(str(file))
            num_of_files += 1
        all_lst_files = path.glob(glob_str)

    data_columns = ["fname", "done", "error"]
    data_record = pd.DataFrame(
        np.zeros((num_of_files, 3)), columns=data_columns
    )  # store result of PySight
    try:
        cfg_dict = convert_json_to_input_dict(cfg_file)
        named_gui = tkinter_to_object(cfg_dict)
    except TypeError:
        gui = GuiAppLst()
        gui.root.mainloop()
        gui.filename.set(".lst")  # no need to choose a list file
        named_gui = tkinter_to_object(gui)
    verify_gui_input(named_gui)

    try:
        for idx, lst_file in enumerate(all_lst_files):
            named_gui.filename = str(lst_file)
            data_record.loc[idx, "fname"] = str(lst_file)
            try:
                main_data_readout(named_gui)
            except BaseException as e:
                print(f"File {str(lst_file)} returned an error. Moving onwards.")
                data_record.loc[idx, "done"] = False
                data_record.loc[idx, "error"] = repr(e)
            else:
                data_record.loc[idx, "done"] = True
                data_record.loc[idx, "error"] = None
    except TypeError as e:
        print(repr(e))

    print(f"Summary of batch processing:\n{data_record}")
    return data_record


def mp_batch(
    foldername, glob_str="*.lst", recursive=False, n_proc=None, cfg_file: str=""
):
    """
    Run several instances of PySight using the multiprocessing module.

    :param str foldername: Folder to scan
    :param str glob_str: Glob string to filter files
    :param bool recursive: Whether to scan subdirectories as well
    :param int n_proc: Number of processes to use (None means all)
    :param str cfg_file: Configuration file name
    """
    import pathlib
    import multiprocessing as mp

    path = pathlib.Path(foldername)
    if not path.exists():
        raise UserWarning(f"Folder {foldername} doesn't exist.")
    if recursive:
        all_lst_files = path.rglob(glob_str)
    else:
        all_lst_files = path.glob(glob_str)
    print(f"Running PySight on the following files:")
    for file in list(all_lst_files):
        print(str(file))

    all_lst_files = path.rglob(glob_str) if recursive else path.glob(glob_str)
    try:
        gui = convert_json_to_input_dict(cfg_file)
    except TypeError:
        gui = GuiAppLst()
        gui.root.mainloop()
        gui.filename.set(".lst")  # no need to choose a list file
    g = tkinter_to_object(gui)
    verify_gui_input(g)
    all_guis = []
    for file in all_lst_files:
        g.filename = str(file)
        all_guis.append(g)
    pool = mp.Pool(n_proc)
    pool.map(main_data_readout, all_guis)


if __name__ == "__main__":
    df, movie = run()
