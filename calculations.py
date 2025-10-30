from math import log, sqrt, erf, exp


def d1C(precoAcao: float, strikePrice: float, riskFree: float, sigma: float, tempo: float) -> float:
    """
    precoAcao = Preço da ação Atual,
    strikePrice, Preço do Strike da Opção,
    riskFree = Taxa livre de risco anualizada como float ex: (0.12)
    sigma: Volatilidade anualizada como float
    tempo = prazo até vencimento em anos ex: (0.5 =~ 6 meses) 
    """

    if any(v <= 0 for v in (tempo, sigma, precoAcao, strikePrice)):
        raise ValueError(f"Todos os inputs (tempo, sigma, precoAcao, strikePrice) devem ser positivos.")

    numerador = log(precoAcao/strikePrice) + (riskFree + (sigma ** 2) /2) * tempo 
    denominador = sigma * sqrt(tempo)

    return numerador / denominador



def d2C(d1: float, sigma: float, tempo: float) -> float:
    return d1 - sigma * sqrt(tempo) 


def nCdf(x: float) -> float:
    return 0.5 * (1 + erf(x / sqrt(2.0)))



def callPrice(precoAcao: float, strikePrice: float, riskFree: float, sigma: float, tempo: float) -> float:
    
    # 1. Calcular d1 e d2
    try:
        d1 = d1C(precoAcao, strikePrice, riskFree, sigma, tempo)
        d2 = d2C(d1, sigma, tempo)
    except ValueError as e:
        # Repassa o erro de validação (ex: tempo <= 0)
        raise e
    
    # 2. Calcular N(d1) e N(d2)
    N_d1 = nCdf(d1)
    N_d2 = nCdf(d2)
    
    # 3. Calcular os termos da fórmula
    termo_1 = precoAcao * N_d1
    termo_2 = strikePrice * exp(-riskFree * tempo) * N_d2
    
    preco_call = termo_1 - termo_2
    return preco_call



def putPrice(precoAcao: float, strikePrice: float, riskFree: float, sigma: float, tempo: float) -> float:
    
    # 1. Calcular d1 e d2 (usando a d1C corrigida)
    try:
        d1 = d1C(precoAcao, strikePrice, riskFree, sigma, tempo)
        d2 = d2C(d1, sigma, tempo)
    except ValueError as e:
        # Repassa o erro de validação
        raise e
    
    # 2. Calcular N(-d1) e N(-d2)
    # Note que os sinais estão invertidos em relação à Call
    N_minus_d1 = nCdf(-d1)
    N_minus_d2 = nCdf(-d2)
    
    # 3. Calcular os termos da fórmula da Put
    # P = K * exp(-r * T) * N(-d2) - S * N(-d1)
    termo_1 = strikePrice * exp(-riskFree * tempo) * N_minus_d2
    termo_2 = precoAcao * N_minus_d1
    
    preco_put = termo_1 - termo_2
    return preco_put



if __name__ == "__main__":
    S = 100.0  # Preço da Ação
    K = 105.0  # Strike
    r = 0.05   # Taxa Juros (5%)
    sig = 0.2  # Volatilidade (20%)
    T = 0.5    # Tempo (6 meses)

    try:
        precoCall = callPrice(S, K, r, sig, T)
        precoPut = putPrice(S, K, r, sig, T)
        print(f"Preço da Opção de Compra (Call): {precoCall:.4f}")
        print(f"Preço da Opção de Venda (Put): {precoPut:.4f}")
    except ValueError as e:
        print(f"Erro no cálculo: {e}")
