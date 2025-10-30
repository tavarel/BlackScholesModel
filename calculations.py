from math import log, sqrt, erf, exp, pi

# TODO -> 1. Passar para OOP 
# TODO -> 2. Fazer funções para calcular as gregas



def d1C(precoAcao: float, strikePrice: float, riskFree: float, sigma: float, tempo: float) -> float:
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
    
    try:
        d1 = d1C(precoAcao, strikePrice, riskFree, sigma, tempo)
        d2 = d2C(d1, sigma, tempo)
    except ValueError as e:
        raise e
    
    N_d1 = nCdf(d1)
    N_d2 = nCdf(d2)
    
    termo_1 = precoAcao * N_d1
    termo_2 = strikePrice * exp(-riskFree * tempo) * N_d2
    
    preco_call = termo_1 - termo_2
    return preco_call



def putPrice(precoAcao: float, strikePrice: float, riskFree: float, sigma: float, tempo: float) -> float:
    
    try:
        d1 = d1C(precoAcao, strikePrice, riskFree, sigma, tempo)
        d2 = d2C(d1, sigma, tempo)
    except ValueError as e:
        raise e
    
    N_minus_d1 = nCdf(-d1)
    N_minus_d2 = nCdf(-d2)
    
    termo_1 = strikePrice * exp(-riskFree * tempo) * N_minus_d2
    termo_2 = precoAcao * N_minus_d1
    
    preco_put = termo_1 - termo_2
    return preco_put



if __name__ == "__main__":
    S = 100.0  
    K = 105.0  
    r = 0.05   
    sig = 0.2  
    T = 0.5    

    try:
        precoCall = callPrice(S, K, r, sig, T)
        precoPut = putPrice(S, K, r, sig, T)
        print(f"Preço da Opção de Compra (Call): {precoCall:.4f}")
        print(f"Preço da Opção de Venda (Put): {precoPut:.4f}")
    except ValueError as e:
        print(f"Erro no cálculo: {e}")
