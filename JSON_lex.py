import ply.lex as lex
from ply.lex import TOKEN

class JSONLexer(object):
    tokens = (
        "STRING",
        "NUMBER",
        "LBRACE",
        "RBRACE",
        "LBRACKET",
        "RBRACKET",
        "COMMA",
        "COLON",
        "BOOLEAN",
        "NULL"
    )

    '''EXPRESIONES REGULARES'''
    # llaves y corchetes
    lbrace = r'\{'
    rbrace = r'\}'
    lbracket = r'\['
    rbracket = r'\]'

    # true, false y null
    t_BOOLEAN = r'(true|false)'
    t_NULL = r'(null)'

    # numeros
    t_NUMBER = r'(-?)(0|[1-9][0-9]*)(\.[0-9]*)?([eE][+\-]?[0-9]*)?'

    # cadenas
    t_STRING = r'"(\\[bfrnt"/\\]|[^\u0022\u005C\u0000-\u001F\u007F-\u009F]|\\u[0-9a-fA-F]{4})*"'

    # coma
    t_COMMA = r','

    # dos puntos
    t_COLON = r':'

    # ignorar todos los espacios en blanco
    t_ignore = '\t\r '
    ###########################

    def __init__(self):
        self.lexer = None

        # variable to check all lists are properly exited
        self.array_depth = 0

        # variable to check all objects are properly exited
        self.object_depth = 0

        self.last_token = None

        self.line_pos = 0
        return

    @TOKEN(lbrace)
    def t_LBRACE(self, t):
        self.object_depth += 1
        return t

    @TOKEN(rbrace)
    def t_RBRACE(self, t):
        self.object_depth -= 1
        return t

    @TOKEN(lbracket)
    def t_LBRACKET(self, t):
        self.array_depth += 1
        return t

    @TOKEN(rbracket)
    def t_RBRACKET(self, t):
        self.array_depth -= 1
        return t

    def t_NEWLINE(self, t):
        r"""\n+"""
        t.lexer.lineno += t.value.count("\n")
        self.line_pos = 0
        return
    
    def t_error(self, t):
        # Si encuentra un token no valido, lanza un error.
        raise SyntaxError("Caracter no permitido '{s}' en la line {line}, posicion {pos}."
                          .format(s=t.value[0], line=t.lexer.lineno, pos=t.lexer.lexpos))

    def build(self, **kwargs):
        """
        Construye el lexer
        :param kwargs: parametros que pasa al lex.lex
        :return:
        """
        self.lexer = lex.lex(module=self, **kwargs)
        return

    def input(self, text):
        """
        :param text: pasa el texto al lexer
        :return:
        """
        self.lexer.input(text)
        return

    def token(self):
        """
        :return: el ultimo token leido por el lexer
        """
        self.last_token = self.lexer.token()
        return self.last_token

    def find_column(self, text, token):
        """
        :return: el numero de la columna en el que se encuentra la instancia del token
        """
        line_start = text.rfind('\n', 0, token.lexpos) + 1
        return (token.lexpos - line_start) + 1
