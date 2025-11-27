class TuringMachineBase:
    def __init__(self, tape):
        self.tape = list(tape) + ['_']
        self.head = 0

    def read(self):
        if self.head < 0:
            self.tape.insert(0, '_')
            self.head = 0
        if self.head >= len(self.tape):
            self.tape.append('_')
        return self.tape[self.head]

    def write(self, symbol):
        self.tape[self.head] = symbol

    def move_left(self):
        self.head -= 1

    def move_right(self):
        self.head += 1


class lang_A(TuringMachineBase):
    """
    L = {w | w possui o mesmo número de 0s e 1s}
    """
    def run(self):
        while True:
            symbol = self.read()

            if symbol == '_':
                return True

            if symbol == '0':
                self.write('X')
                self.move_right()

                while True:
                    s = self.read()
                    if s == '1':
                        self.write('Y')
                        while self.head > 0:
                            self.move_left()
                        break
                    elif s in ['X', 'Y', '0']:
                        self.move_right()
                    else:
                        return False

            elif symbol == '1':
                self.write('Y')
                self.move_right()

                while True:
                    s = self.read()
                    if s == '0':
                        self.write('X')
                        while self.head > 0:
                            self.move_left()
                        break
                    elif s in ['X', 'Y', '1']:
                        self.move_right()
                    else:
                        return False

            else:
                self.move_right()


class lang_B(TuringMachineBase):
    """
    L = { w | para cada 1 existem exatamente dois 0s } (ou seja, o dobro)
    Temos: #0 = 2 x #1 E se #1 = 0 então #0 = 0
    
    na minha interpretação, se não tem 1s, não podemos ter 0s. pq o dobro de zero é zero.
    """
    def run(self):
        # Estado: procurando 1 não marcado
        while True:
            # Voltar ao início
            while self.head > 0:
                self.move_left()
            
            # Procurar um '1' não marcado
            found_1 = False
            while True:
                symbol = self.read()
                if symbol == '_':  # Fim da fita
                    break
                elif symbol == '1':  # Encontrou 1 não marcado
                    found_1 = True
                    self.write('Y')  # Marcar o 1
                    break
                self.move_right()
            
            if not found_1:
                # Não encontrou mais 1s - verificar se não sobrou 0 não marcado
                while self.head > 0:
                    self.move_left()
                while True:
                    symbol = self.read()
                    if symbol == '0':  # Sobrou 0 não marcado - REJEITA
                        return False
                    elif symbol == '_':  # Fim - ACEITA
                        return True
                    self.move_right()
            
            # Para este 1, precisamos encontrar 2 zeros não marcados
            zeros_encontrados = 0
            while zeros_encontrados < 2:
                # Voltar ao início para procurar zeros
                while self.head > 0:
                    self.move_left()
                
                found_zero = False
                while True:
                    symbol = self.read()
                    if symbol == '_':  # Fim sem zeros suficientes
                        return False
                    elif symbol == '0':  # Encontrou zero não marcado
                        self.write('X')  # Marcar o zero
                        zeros_encontrados += 1
                        found_zero = True
                        break
                    self.move_right()
                
                if not found_zero:
                    return False



class lang_C(TuringMachineBase):
    """
    complemento de b
    L = { w | #0 ≠ 2 X #1 }
    """
    def run(self):
        # Estratégia: tentar executar o processo de langB
        # Se langB aceita, nós rejeitamos, e vice-versa
        
        # Fazer uma cópia da fita para não modificar a original
        fita_original = self.tape.copy()
        posicao_original = self.head
        
        # Simular langB
        temp = lang_B("".join(self.tape).rstrip('_'))
        resultado_b = temp.run()
        
        # Restaurar fita original
        self.tape = fita_original
        self.head = posicao_original
        
        return not resultado_b


if __name__ == "__main__":
    tests = ["", "01", "0011", "0101", "001", "00011"]

    for w in tests: # teste mais simples
        print("\nEntrada:", repr(w))
        print("A:", lang_A(w).run())
        print("B:", lang_B(w).run())
        print("C", lang_C(w).run())
        
    testes_2 = ["0000", "1111", "0101010101", "000110011001", "001000100010001", "111110111101111011111011111011111"]
        
    for c in testes_2:
        print("\n Entrada:", repr(c))
        print("A:", lang_A(c).run())
        print("B:", lang_B(c).run())
        print("C:", lang_C(c).run())
        
    # TESTE ESPECÍFICO PARA lang_B
    testes_b = ["", "0000", "001", "00011", "01", "000111"]
    print("\n=== TESTES ESPECÍFICOS lang_B ===")
    for w in testes_b:
        tm = lang_B(w)
        result = tm.run()
        print(f"Entrada: '{w}' -> B: {result} (esperado: {len(w.replace('1','')) == 2 * len(w.replace('0',''))})")
