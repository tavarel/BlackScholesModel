from math import log, sqrt, erf, exp, pi

# TODO -> 2. Fazer funções para calcular as gregas

class OpcoesBlackScholes:
    """
    Classe para calcular o preço de opções de compra (Call) e venda (Put)
    usando o modelo Black-Scholes.
    """

    def __init__(self, precoAcao: float, strikePrice: float, riskFree: float, sigma: float, tempo: float):
        """
        Inicializa a classe com os parâmetros do modelo.
        """
        # A validação de inputs (positivos) pode ser feita aqui.
        if any(v <= 0 for v in (tempo, sigma, precoAcao, strikePrice)):
            raise ValueError("Todos os inputs (tempo, sigma, precoAcao, strikePrice) devem ser positivos.")

        self.S = precoAcao
        self.K = strikePrice
        self.r = riskFree
        self.sig = sigma
        self.T = tempo

    # --- Métodos Auxiliares (Estáticos ou Privados) ---
    
    @staticmethod
    def _d1C(precoAcao: float, strikePrice: float, riskFree: float, sigma: float, tempo: float) -> float:
        """
        Calcula o parâmetro d1 do modelo Black-Scholes.
        """
        numerador = log(precoAcao / strikePrice) + (riskFree + (sigma ** 2) / 2) * tempo 
        denominador = sigma * sqrt(tempo)
        return numerador / denominador

    @staticmethod
    def _d2C(d1: float, sigma: float, tempo: float) -> float:
        """
        Calcula o parâmetro d2 do modelo Black-Scholes.
        """
        return d1 - sigma * sqrt(tempo) 

    @staticmethod
    def _nCdf(x: float) -> float:
        """
        Calcula a Função de Distribuição Acumulada da Normal Padrão (N(x)).
        """
        return 0.5 * (1 + erf(x / sqrt(2.0)))

    # --- Métodos Principais ---

    def precoCall(self) -> float:
        """
        Calcula o preço da Opção de Compra (Call).
        """
        # Reutiliza os métodos e atributos da classe
        d1 = self._d1C(self.S, self.K, self.r, self.sig, self.T)
        d2 = self._d2C(d1, self.sig, self.T)
        
        N_d1 = self._nCdf(d1)
        N_d2 = self._nCdf(d2)
        
        termo_1 = self.S * N_d1
        termo_2 = self.K * exp(-self.r * self.T) * N_d2
        
        preco_call = termo_1 - termo_2
        return preco_call

    def precoPut(self) -> float:
        """
        Calcula o preço da Opção de Venda (Put).
        """
        # Reutiliza os métodos e atributos da classe
        d1 = self._d1C(self.S, self.K, self.r, self.sig, self.T)
        d2 = self._d2C(d1, self.sig, self.T)
        
        # A Black-Scholes para Put usa N(-d1) e N(-d2)
        N_minus_d1 = self._nCdf(-d1)
        N_minus_d2 = self._nCdf(-d2)
        
        termo_1 = self.K * exp(-self.r * self.T) * N_minus_d2
        termo_2 = self.S * N_minus_d1
        
        preco_put = termo_1 - termo_2
        return preco_put


if __name__ == "__main__":
    S = 100.0  # Preço da Ação
    K = 105.0  # Strike Price
    r = 0.05   # Taxa Livre de Risco
    sig = 0.2  # Volatilidade (Sigma)
    T = 0.5    # Tempo para Maturidade (em anos)

    try:
        # 1. Cria uma instância da classe, passando todos os parâmetros
        opcoes = OpcoesBlackScholes(S, K, r, sig, T)
        
        # 2. Chama os métodos sem precisar passar os parâmetros novamente
        precoCall = opcoes.precoCall()
        precoPut = opcoes.precoPut()
        
        print(f"Preço da Ação (S): {S}, Strike (K): {K}, Tempo (T): {T}")
        print(f"Preço da Opção de Compra (Call): {precoCall:.4f}")
        print(f"Preço da Opção de Venda (Put): {precoPut:.4f}")
        

    except ValueError as e:
        print(f"Erro no cálculo: {e}")