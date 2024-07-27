import subprocess
import os
import pandas as pd


def calculate_rosetta_scores(
    sequence: str, pdb, working_dir: str, python_rosetta_interpreter_path: str
):
    pdb_filepath = "workingpdb.pdb"
    if os.path.exists(working_dir + pdb_filepath):
        os.remove(working_dir + pdb_filepath)
    with open(working_dir + pdb_filepath, "wb") as output_file:
        output_file.write(bytes(pdb[0]))
    return run_rosetta(
        sequence, working_dir + pdb_filepath, python_rosetta_interpreter_path
    )


def run_rosetta(sequence: str, pdb_path: str, python_rosetta_interpreter_path: str):
    out = subprocess.run(
        [
            python_rosetta_interpreter_path,
            "./get_rosetta_scores.py",
            "seq_then_path",
            sequence,
            pdb_path,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        text=True,
    )
    read = pd.read_csv("./cached-extra-seqs/" + sequence + ".csv")
    os.remove("./cached-extra-seqs/" + sequence + ".csv")
    return read.to_numpy()[0].tolist()
