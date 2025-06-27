from lexer import TokenType

class SyntacticAnalyzer:
    def __init__(self, tokens):
        self.__tokens = tokens
        self.__current_position = 0
        self.__current_token = self.__tokens[0] if tokens else None
    
    def __advance(self):
        """Avanza al siguiente token"""
        self.__current_position += 1
        if self.__current_position < len(self.__tokens):
            self.__current_token = self.__tokens[self.__current_position]
        else:
            self.__current_token = None
    
    def __match(self, expected_type):
        """Verifica si el token actual es del tipo esperado"""
        if self.__current_token and self.__current_token.type == expected_type:
            self.__advance()
            return True
        return False
    
    def parse(self):
        """Inicia el análisis sintáctico"""
        if not self.__tokens:
            raise SyntaxError("No hay tokens para analizar")
        
        return self.__parse_sentence()
    
    def __parse_sentence(self):
        """<sentence> → <noun_phrase> <verb_phrase> ."""
        if not self.__parse_noun_phrase():
            raise SyntaxError("Se esperaba una frase nominal")
        
        if not self.__parse_verb_phrase():
            raise SyntaxError("Se esperaba una frase verbal")
        
        if not self.__match(TokenType.DOT):
            raise SyntaxError("Se esperaba un punto al final de la oración")
        
        # Verificar que no haya tokens adicionales
        if self.__current_token is not None:
            raise SyntaxError("Tokens adicionales después del punto")
        
        return True
    
    def __parse_noun_phrase(self):
        """<noun_phrase> → <article> <adjective_list> <noun> | <article> <noun>"""
        if not self.__match(TokenType.ARTICLE):
            return False
        
        # Intentar parsear lista de adjetivos (opcional)
        self.__parse_adjective_list()
        
        if not self.__match(TokenType.NOUN):
            raise SyntaxError("Se esperaba un sustantivo después del artículo")
        
        return True
    
    def __parse_adjective_list(self):
        """<adjective_list> → <adjective> | <adjective> <adjective_list>"""
        if self.__current_token and self.__current_token.type == TokenType.ADJECTIVE:
            self.__advance()
            # Recursivamente parsear más adjetivos
            self.__parse_adjective_list()
            return True
        return False
    
    def __parse_verb_phrase(self):
        """<verb_phrase> → <verb> | <verb> <prep_phrase>"""
        if not self.__match(TokenType.VERB):
            return False
        
        # Intentar parsear frase preposicional (opcional)
        self.__parse_prep_phrase()
        
        return True
    
    def __parse_prep_phrase(self):
        """<prep_phrase> → <preposition> <noun_phrase>"""
        if self.__current_token and self.__current_token.type == TokenType.PREPOSITION:
            self.__advance()
            if not self.__parse_noun_phrase():
                raise SyntaxError("Se esperaba una frase nominal después de la preposición")
            return True
        return False

def analyze_syntactic(tokens):
    """
    Función principal para el análisis sintáctico
    """
    analyzer = SyntacticAnalyzer(tokens)
    return analyzer.parse()