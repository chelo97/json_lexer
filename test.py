from JSON_lex import JSONLexer
import sys
import os

def run(fname):
    """
    Test del analizador lexico que genera un archivo con los tokens de la fuente
    :return:
    """

    # direccion y nombre del archivo resultante, dentro de la carpeta /tests
    log_fname = "output.log"
    log_path = os.path.join(os.getcwd(), "tests", log_fname)

    # crear el archivo
    open(log_path, "w")

    # agrega todos las salidas/errores dentro del archivo
    sys.stdout = open(log_path, "a")
    sys.stderr = open(log_path, "a")

    try:
        # direccion de la fuente json, dentro de la carpeta /tests
        test_path = os.path.join(os.getcwd(), "tests", fname)

        # lleer .json
        with open(test_path, "r") as f:
            inp = f.read()
            
        # crear instancia del lexer
        json_lexer = JSONLexer()

        # construir lexer y leer los tokens
        json_lexer.build()
        json_lexer.input(inp)
        
        # variable para guardar el nro de linea anterior
        lineno_last = None

        # agrega los tokens al archivo .log
        with open(log_path, "a") as f:
            while True:
                token = json_lexer.token()
                
                # cuando ya no haya tokens sale del bucle
                if not token:
                    break;
                
                # guarda el nro. de linea actual
                lineno_cur = token.lineno
                
                '''si el nro de linea anterior esta cargado y es diferente al actual,
                escribe nueva linea con indentacion'''
                if lineno_last is not None and lineno_last != lineno_cur:
                    f.write('\n' + ''.rjust(json_lexer.find_column(inp, token)))
                elif lineno_last is not None and lineno_last == lineno_cur:
                    # si son las mismas lineas, escribe una caracter en blanco
                    f.write(' ')

                #escribe los tokens
                f.write(token.type)
                
                # guarda el nro de linea anterior para la siguiente secuencia
                lineno_last = lineno_cur
            
            f.write('\nEOF')

    except FileNotFoundError:
        pass
        
    return


if __name__ == "__main__":
    run("fuente.json")
