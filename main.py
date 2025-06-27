import sys
import os
from lexer import analyze_lexical
from parser import analyze_syntactic

def process_file(input_filename, output_filename):
    """
    Procesa el archivo de entrada línea por línea y genera el archivo de salida
    """
    try:
        # Verificar que el archivo de entrada existe
        if not os.path.exists(input_filename):
            print(f"Error: El archivo '{input_filename}' no existe.")
            return False
        
        # Leer el archivo de entrada
        with open(input_filename, 'r', encoding='utf-8') as input_file:
            lines = input_file.readlines()
        
        # Procesar cada línea
        results = []
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line:  # Saltar líneas vacías
                continue
            
            result = {
                'line_number': line_num,
                'sentence': line,
                'status': 'OK',
                'error_type': None,
                'error_message': None
            }
            
            try:
                # Análisis Léxico
                tokens = analyze_lexical(line)
                
                # Análisis Sintáctico
                analyze_syntactic(tokens)
                
            except ValueError as e:
                # Error léxico
                result['status'] = 'ERROR'
                result['error_type'] = 'LÉXICO'
                result['error_message'] = str(e)
                
            except SyntaxError as e:
                # Error sintáctico
                result['status'] = 'ERROR'
                result['error_type'] = 'SINTÁCTICO'
                result['error_message'] = str(e)
                
            except Exception as e:
                # Error general
                result['status'] = 'ERROR'
                result['error_type'] = 'GENERAL'
                result['error_message'] = str(e)
            
            results.append(result)
        
        # Escribir el archivo de salida
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            output_file.write("ANÁLISIS LÉXICO Y SINTÁCTICO - LITTLE ENGLISH\n")
            output_file.write("=" * 50 + "\n\n")
            
            for result in results:
                output_file.write(f"Línea {result['line_number']}: {result['sentence']}\n")
                
                if result['status'] == 'OK':
                    output_file.write("✓ ANÁLISIS EXITOSO\n")
                else:
                    output_file.write(f"✗ ERROR {result['error_type']}: {result['error_message']}\n")
                
                output_file.write("-" * 40 + "\n\n")
            
            # Resumen
            total_lines = len(results)
            successful_lines = sum(1 for r in results if r['status'] == 'OK')
            error_lines = total_lines - successful_lines
            
            output_file.write("RESUMEN\n")
            output_file.write("=" * 20 + "\n")
            output_file.write(f"Total de líneas procesadas: {total_lines}\n")
            output_file.write(f"Análisis exitosos: {successful_lines}\n")
            output_file.write(f"Errores encontrados: {error_lines}\n")
        
        print(f"Procesamiento completado. Resultados guardados en '{output_filename}'.")
        print(f"Revisar el archivo '{output_filename}' para ver los resultados detallados.")
        return True
        
    except Exception as e:
        print(f"Error al procesar archivos: {e}")
        return False

def main():
    """
    Función principal del programa
    """
    # Verificar argumentos de línea de comandos
    if len(sys.argv) != 3:
        print("\n" + "="*60)
        print("ERROR: Número incorrecto de argumentos")
        print("="*60)
        print("Uso: python main.py <archivo_entrada> <archivo_salida>")
        print("Ejemplo: python main.py sentences.txt results.txt")
        print("\nDescripción:")
        print("  <archivo_entrada> : Archivo con oraciones a analizar")
        print("  <archivo_salida>  : Archivo donde se guardarán los resultados")
        print("="*60)
        
        # Mostrar archivos disponibles en el directorio actual
        try:
            files = [f for f in os.listdir('.') if f.endswith('.txt')]
            if files:
                print(f"\nArchivos .txt disponibles en el directorio actual:")
                for file in files:
                    print(f"  - {file}")
        except:
            pass
        
        sys.exit(1)
    
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    
    print("\n" + "="*60)
    print("ANALIZADOR LÉXICO Y SINTÁCTICO - LITTLE ENGLISH")
    print("="*60)
    print(f"Archivo de entrada: {input_filename}")
    print(f"Archivo de salida:  {output_filename}")
    print("-"*60)
    
    success = process_file(input_filename, output_filename)
    
    if success:
        print("="*60)
        print("✓ PROCESAMIENTO COMPLETADO EXITOSAMENTE")
        print("="*60)
        sys.exit(0)
    else:
        print("="*60)
        print("✗ ERROR EN EL PROCESAMIENTO")
        print("="*60)
        sys.exit(1)

if __name__ == "__main__":
    main()