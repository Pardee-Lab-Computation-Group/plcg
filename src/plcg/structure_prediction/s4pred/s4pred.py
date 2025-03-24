import subprocess
import os
from typing import NamedTuple, cast, overload

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


@overload
def calc_secondary_structure(
    s4pred_path: str, seq: str | list[str], *, threshold: int | float = ...
) -> list[SecondaryStructure]: ...
@overload
def calc_secondary_structure(
    s4pred_path: str, *, fasta_path: str, threshold: int | float = ...
) -> list[SecondaryStructure]: ...
def calc_secondary_structure(
    s4pred_path: str, seq=None, fasta_path=None, threshold: int | float = 5
) -> list[SecondaryStructure]:
    if seq is not None:
        fasta_path = _create_temp_fasta(seq)
    fasta_path = cast(str, fasta_path)

    output = _run_s4pred(s4pred_path, fasta_path)

    if seq is not None:
        os.remove(fasta_path)

    secondary_structures = _parse_s4pred_output(output, threshold)
    return secondary_structures


def _create_temp_fasta(seq: str | list[str]) -> str:
    fasta_path = "./tmp.fasta"
    if isinstance(seq, str):
        seq = [seq]
    save_fasta_file(seq, fasta_path)
    return fasta_path


def _run_s4pred(s4pred_path: str, fasta_path: str) -> str:
    result = subprocess.run(
        [
            "python",
            f"{s4pred_path}/run_model.py",
            "-t",
            "horiz",
            fasta_path,
        ],
        capture_output=True,
        check=True,
    )
    return result.stdout.decode()


def _parse_s4pred_output(
    output: str, threshold: int | float
) -> list[SecondaryStructure]:
    ss_data = output.split("#")[1:]
    return list(
        map(lambda ss_str: _process_secondary_structure(ss_str, threshold), ss_data)
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
    return "".join(pred[i] for i, c in enumerate(conf) if int(c) >= threshold)


def _count_secondary_structure(filtered_pred: str):
    n_h = filtered_pred.count("H")
    n_e = filtered_pred.count("E")
    n_c = filtered_pred.count("C")
    n = len(filtered_pred)
    f_h = n_h / n if n > 0 else 0
    f_e = n_e / n if n > 0 else 0
    f_c = n_c / n if n > 0 else 0
    return n_h, n_e, n_c, f_h, f_e, f_c
