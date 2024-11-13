from numpy.typing import NDArray
from aiupred import aiupred_lib


(embedding_model, regression_model, device) = aiupred_lib.init_models()


def calc_disorder(seq: str) -> NDArray:
    return aiupred_lib.predict_disorder(seq, embedding_model, regression_model, device)
