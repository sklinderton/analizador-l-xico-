import re
from enum import Enum

class TokenType(Enum):
    ARTICLE = "ARTICLE"
    ADJECTIVE = "ADJECTIVE"
    NOUN = "NOUN"
    VERB = "VERB"
    PREPOSITION = "PREPOSITION"
    DOT = "DOT"
    UNKNOWN = "UNKNOWN"

class Token:
    def __init__(self, token_type, value, position):
        self.__type = token_type
        self.__value = value
        self.__position = position
    
    @property
    def type(self):
        return self.__type
    
    @property
    def value(self):
        return self.__value
    
    @property
    def position(self):
        return self.__position
    
    def __repr__(self):
        return f"Token({self.__type}, '{self.__value}', {self.__position})"

class LexicalAnalyzer:
    def __init__(self):
        # Diccionarios de palabras para Little English
        self.__articles = {"the", "a", "an"}
        self.__adjectives = {"big", "small", "red", "blue", "green", "old", "young", "tall", "short", "happy", "sad"}
        self.__nouns = {"cat", "dog", "house", "car", "book", "table", "chair", "man", "woman", "child", "tree", "flower"}
        self.__verbs = {"is", "are", "was", "were", "runs", "walks", "sits", "stands", "eats", "drinks", "sleeps", "reads"}
        self.__prepositions = {"in", "on", "at", "under", "over", "by", "with", "from", "to"}
    
    def tokenize(self, line):
        """
        Realiza el análisis léxico de una línea
        Retorna una lista de tokens o lanza una excepción en caso de error
        """
        tokens = []
        line = line.strip()
        
        if not line:
            raise ValueError("Línea vacía")
        
        # Separar por espacios y manejar el punto final
        words = []
        current_word = ""
        
        for char in line:
            if char == ' ':
                if current_word:
                    words.append(current_word)
                    current_word = ""
            elif char == '.':
                if current_word:
                    words.append(current_word)
                    current_word = ""
                words.append('.')
            else:
                current_word += char
        
        if current_word:
            words.append(current_word)
        
        # Convertir palabras a tokens
        position = 0
        for word in words:
            word_lower = word.lower()
            
            if word == '.':
                tokens.append(Token(TokenType.DOT, word, position))
            elif word_lower in self.__articles:
                tokens.append(Token(TokenType.ARTICLE, word_lower, position))
            elif word_lower in self.__adjectives:
                tokens.append(Token(TokenType.ADJECTIVE, word_lower, position))
            elif word_lower in self.__nouns:
                tokens.append(Token(TokenType.NOUN, word_lower, position))
            elif word_lower in self.__verbs:
                tokens.append(Token(TokenType.VERB, word_lower, position))
            elif word_lower in self.__prepositions:
                tokens.append(Token(TokenType.PREPOSITION, word_lower, position))
            else:
                raise ValueError(f"Token desconocido: '{word}' en posición {position}")
            
            position += len(word) + 1
        
        return tokens

def analyze_lexical(line):
    """
    Función principal para el análisis léxico
    """
    analyzer = LexicalAnalyzer()
    return analyzer.tokenize(line)