import csv
import os
import shutil
import subprocess

from plcg.structure_prediction.fasta.fasta import save_fasta_file


def run_colabfold(input_filepath: str, output_dir: str):
    subprocess.call(
        [
            "colabfold_batch",
            input_filepath,
            output_dir,
            "--stop-at-score",
            "88.0",
            "--num-recycle",
            "4",
        ]
    )


def run_colabfold_and_get_filepath(seq: str, working_dir: str):
    if os.path.exists(working_dir):
        shutil.rmtree(working_dir)
    os.mkdir(working_dir)
    with open(working_dir + "working.csv", "w") as f:
        write = csv.writer(f)
        write.writerows([["id", "sequence"], ["sequence", seq]])
    files = os.listdir(working_dir)
    flag = 0
    while flag == 0:
        pdb_filepath = [result for result in files if "unrelaxed_rank_001" in result]
        if len(pdb_filepath) > 0:
            pdb_filepath = pdb_filepath[0]
            flag = 1
        else:
            pdb_filepath = [result for result in files if "unrelaxed_" in result]
            if len(pdb_filepath) > 0:
                pdb_filepath = pdb_filepath[0]
                flag = 1
            else:
                run_colabfold(working_dir + "working.csv", working_dir)
                files = os.listdir(working_dir)
    return pdb_filepath


def colabfold_batch(fasta_filepath: str, output_dir: str):
    subprocess.call(
        [
            "colabfold_batch",
            fasta_filepath,
            output_dir,
            "--stop-at-score",
            "88.0",
            "--num-recycle",
            "4",
        ]
    )


def run_colabfold_batch_and_return_filepaths(sequences: list[str], working_dir: str):
    if os.path.exists(working_dir):
        shutil.rmtree(working_dir)
    os.mkdir(working_dir)
    fasta_file_path = "output.fasta"
    save_fasta_file(sequences, working_dir + fasta_file_path)
    colabfold_batch(working_dir + fasta_file_path, working_dir)
    sequences_to_pdb_filepaths = {}
    files = os.listdir(working_dir)
    for i, sequence in enumerate(sequences):
        results = [result for result in files if "Sequence_" + str(i) in result]
        result = [result for result in results if "unrelaxed_rank_001" in result]
        if len(result) > 0:
            result = result[0]
            sequences_to_pdb_filepaths[i] = working_dir + result
    return sequences_to_pdb_filepaths
