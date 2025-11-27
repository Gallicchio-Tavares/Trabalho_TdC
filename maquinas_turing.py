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
        count_0 = 0
        count_1 = 0
        
        while self.head > 0:
            self.move_left()
            
        while True:
            symbol = self.read()
            if symbol == '_':
                break
            elif symbol == '0':
                count_0 += 1
            elif symbol == '1':
                count_1 += 1
            self.move_right()
        
        if count_1 == 0:
            return count_0 == 0  
        else:
            return count_0 == 2 * count_1



class lang_C(TuringMachineBase):
    # só negamos a B
    def run(self): 
        temp = lang_B("".join(self.tape).rstrip('_'))
        resultado = temp.run()
        return not resultado


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
