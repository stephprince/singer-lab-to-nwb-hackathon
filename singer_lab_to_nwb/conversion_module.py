# authors: Luiz Tauffer and Ben Dichter
# written for Jaeger Lab
# ------------------------------------------------------------------------------
from pynwb import NWBHDF5IO
from ecephys.intan import Intan2NWB
import yaml
import os


def conversion_function(source_paths, f_nwb, metadata, add_rhd=False, **kwargs): #todo: finish this function
    """
    Convert data from a diversity of experiment types to nwb.

    Parameters
    ----------
    source_paths : dict
        Dictionary with paths to source files/directories. e.g.:
        {
        'dir_ecepys_rhd': {'type': 'dir', 'path': ''},
        'file_electrodes': {'type': 'file', 'path': ''},
        }
    f_nwb : str
        Path to output NWB file, e.g. 'my_file.nwb'.
    metadata : dict
        Metadata dictionary
    **kwargs : key, value pairs
        Extra keyword arguments
    """

    # Source files and directories
    dir_ecephys_rhd = None #todo: add extrafilenames
    file_electrodes = None
    for k, v in source_paths.items():
        if v['path'] != '':
            if k == 'dir_ecephys_rhd':
                dir_ecephys_rhd = v['path']
            if k == 'file_electrodes':
                file_electrodes = v['path']

    nwbfile = None

    # Adding ecephys
    if add_rhd:
        nwbfile = add_ecephys_rhd(
            nwbfile=nwbfile,
            metadata=metadata,
            source_dir=dir_ecephys_rhd,
            electrodes_file=file_electrodes,
        )

    # Saves to NWB file
    with NWBHDF5IO(f_nwb, mode='w') as io:
        io.write(nwbfile)
    print('NWB file saved with size: ', os.stat(f_nwb).st_size / 1e6, ' mb')


def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description='convert .mat file to NWB',
    )

    # Positional arguments
    parser.add_argument(
        "output_file",
        help="Output file to be created."
    )
    parser.add_argument(
        "metafile",
        help="The path to the metadata YAML file."
    )

    # Source dir/file arguments
    parser.add_argument(
        "--dir_ecephys_rhd",
        default=None,
        help="The path to the directory containing rhd files."
    )
    parser.add_argument(
        "--file_electrodes",
        default=None,
        help="The path to the electrodes info file."
    )

    # Boolean arguments
    parser.add_argument(
        "--add_rhd",
        action="store_true",
        default=False,
        help="Whether to add the ecephys data to the NWB file or not",
    )

    if not sys.argv[1:]:
        args = parser.parse_args(["--help"])
    else:
        args = parser.parse_args()

    # Setting conversion function args and kwargs
    source_paths = {
        'dir_ecephys_rhd': {'type': 'dir', 'path': args.dir_ecephys_rhd},
        'file_electrodes': {'type': 'file', 'path': args.file_electrodes},
    }

    f_nwb = args.output_file

    # Load metadata from YAML file
    metafile = args.metafile
    with open(metafile) as f:
        metadata = yaml.safe_load(f)

    # Lab-specific kwargs
    kwargs_fields = {
        'add_rhd': args.add_rhd,
    }

    conversion_function(
        source_paths=source_paths,
        f_nwb=f_nwb,
        metadata=metadata,
        **kwargs_fields
    )


# If called directly fom terminal
if __name__ == '__main__':
    main()
