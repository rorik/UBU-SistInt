import io, os, sys, types

from IPython import get_ipython
from nbformat import read
from IPython.core.interactiveshell import InteractiveShell



def importCode(code, name, add_to_sys_modules=False):
    """ 
    code can be any object containing code -- string, file object, or
    compiled code object. Returns a new module object initialized
    by dynamically importing the given code and optionally adds it
    to sys.modules under the given name.
    """
    import imp
    module = imp.new_module(name)

    if add_to_sys_modules:
        import sys
        sys.modules[name] = module
    exec(code,module.__dict__)

    return module

def cargaCodigoDinamico(path,name,code_key = '# Cargar Celda'):
    """
    Carga el código creado en el notebook para poder ser 
    utilizado desde clases externas al notebook
    
    Parámetros: 
        
    """
    moduleName = name 
    shell = InteractiveShell.instance()
    # carga el notebook en la variable nb
    with io.open(path, 'r', encoding='utf-8') as f:
        nb = read(f, 4)
    
    # se crea un modulo dinamicamente con nombre moduleName
    mod = types.ModuleType(moduleName)
    mod.__dict__['get_ipython'] = get_ipython
    sys.modules[moduleName] = mod 
    
    code_to_load = ""
    
    # Carga las celdas de tipo code, que empiezan por "# Cargar Celda"
    for cell in nb.cells:
        if cell.cell_type == 'code':
            # convierte la entrada en codigo ejecutable
            code = shell.input_transformer_manager.transform_cell(cell.source)
            
            if code.startswith(code_key):
                # añade esta celda al codigo que se va a cargar
                code_to_load=code_to_load+"\n"+code  
    return importCode(code_to_load,moduleName)
