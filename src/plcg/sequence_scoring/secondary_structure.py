import subprocess
import os
from typing import NamedTuple, cast

from plcg.structure_prediction.fasta.fasta import save_fasta_file


class SecondaryStructure(NamedTuple):
    pred: str
    filtered_pred: str
    threshold: int | float
    n_helix: int
    n_sheet: int
    n_coil: int
    f_helix: float
    f_sheet: float
    f_coil: float


def get_secondary_structure_from_seq(
    seq: str | list[str],
    s4_python_program_path: str,
    working_dir_path: str,
    threshold: float = 5,
) -> list[SecondaryStructure]:
    if seq is None:
        raise ValueError("No sequence provided")

    fasta_path = working_dir_path + "fasta"
    if isinstance(seq, str):
        seq = [seq]
    save_fasta_file(seq, fasta_path)
    temp_fasta_path: str = cast(str, fasta_path)

    secondary_structure = calculate_secondary_structure(
        temp_fasta_path, s4_python_program_path, threshold
    )
    os.remove(fasta_path)
    return secondary_structure


def get_secondary_structure_from_fasta(
    input_fasta_path: str, s4_python_program_path: str, threshold: float = 5
) -> list[SecondaryStructure]:
    fasta_path = cast(str, input_fasta_path)
    return calculate_secondary_structure(fasta_path, s4_python_program_path, threshold)


def calculate_secondary_structure(
    input_fasta_path: str, s4_python_program_path: str, threshold: float = 5
) -> list[SecondaryStructure]:
    output = subprocess.run(
        [
            "python",
            s4_python_program_path,
            "-t",
            "horiz",
            input_fasta_path,
        ],
        capture_output=True,
        check=True,
    )
    decoded_output = output.stdout.decode()
    _, _, secondary_structure_sets = decoded_output.partition("#")
    return list(
        map(
            lambda ss_str: _process_secondary_structure(ss_str, threshold),
            secondary_structure_sets,
        )
    )


def _process_secondary_structure(ss_str: str, threshold: float) -> SecondaryStructure:
    res = ss_str.split("\n")
    conf = res[2][res[2].rfind(" ") + 1 :]
    pred = res[3][res[3].rfind(" ") + 1 :]

    filtered_pred = _filter_prediction_by_confidence(conf, pred, threshold)
    n_h, n_e, n_c, f_h, f_e, f_c = _count_secondary_structure(filtered_pred)

    return SecondaryStructure(
        pred=pred,
        filtered_pred=filtered_pred,
        threshold=threshold,
        n_helix=n_h,
        n_sheet=n_e,
        n_coil=n_c,
        f_helix=f_h,
        f_sheet=f_e,
        f_coil=f_c,
    )


def _filter_prediction_by_confidence(conf: str, pred: str, threshold: float) -> str:
    filtered_pred = ""
    for i, c in enumerate(conf):
        if int(c) >= threshold:
            filtered_pred += pred[i]
    return filtered_pred


def _count_secondary_structure(filtered_pred: str):
    n_h = filtered_pred.count("H")
    n_e = filtered_pred.count("E")
    n_c = filtered_pred.count("C")
    n = len(filtered_pred)
    f_h = n_h / n if n > 0 else 0
    f_e = n_e / n if n > 0 else 0
    f_c = n_c / n if n > 0 else 0
    return n_h, n_e, n_c, f_h, f_e, f_c
