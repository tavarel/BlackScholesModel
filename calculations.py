from math import log, sqrt

def d1(precoAcao: float, strikePrice: float, riskFree: float, sigma: float, tempo: float) -> float:
    """
    precoAcao = Preço da ação Atual,
    strikePrice, Preço do Strike da Opção,
    riskFree = Taxa livre de risco anualizada como float ex: (0.12)
    sigma: Volatilidade anualizada como float
    tempo = prazo até vencimento em anos ex: (0.5 =~ 6 meses) 
    """

    if any(v <= 0 for v in (tempo, sigma, precoAcao, strikePrice)):
        raise ValueError(f"Todos os inputs (tempo, sigma, precoAcao, strikePrice) devem ser positivos.")

    numerador = (precoAcao/strikePrice) + (riskFree + (sigma ** 2) /2) * tempo 
    denominador = sigma * sqrt(tempo)

    return numerador / denominador



def d2 (d1: float, sigma: float, tempo: float) -> float:
    return d1 - sigma * sqrt(tempo) 
