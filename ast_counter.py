import os
import ast
from pprint import pprint
from tabulate import tabulate


def create_file(file_name, content="\n"):
    with open(file_name,"x") as main_file:
        main_file.write(content)
        print(f"""File {file_name} has been saved to your directory""")
    main_file.close()
    return main_file



def ast_maker(filename, outfile):

    try:
        state = create_file(outfile)
    except:
        raise("Error file already exists.")
    
    with open(filename, "r") as source:
        tree = ast.parse(source.read())

    analyzer = Analyzer(filename=filename)
    analyzer.visit(tree)
    depth_of_tree = calc_depth_ast(tree)
    analyzer.report(outfile, depth_of_tree)
    # project = pyFile(filename=filename)
    # project.create_record(analyzer)
    return tree
    #state.close()


class Analyzer(ast.NodeVisitor):
    def __init__(self, filename):
        self.pythonFile = filename
        self.literals = { "constant":[], "num":[], "str":[], 
                       "formattedValue":[], "joinedStr":[], 
                        "bytes":[], "list":[], "tuple":[], "set":[], 
                          "dict":[], "ellipsis":[], "nameConstant":[]}
       
        self.variables ={"name":[], "load":[], "store":[], 
                         "del":[], "starred":[] }
        
        self.expressions = {"expr":[], "namedExpr":[], "unaryOp":[],
                            "uAdd":[], "uSub":[], "not":[],
                            "invert":[], "binOp":[], "add":[],
                            "sub":[], "mult":[], "div":[], "floorDiv":[],
                            "mod":[], "pow":[], "lShift":[], "rShift":[],
                            "bitOr":[], "bitXor":[], "bitAnd":[], "matMult":[],
                            "boolOp":[], "and":[], "or":[], "compare":[], 
                            "eq":[], "notEq":[], "lt":[], "ltE":[], "gt":[],
                            "gtE":[], "is":[], "in":[], "isNot":[], "notIn":[], "call":[], 
                            "keyword":[], "ifExp":[], "attribute":[]}
        
        self.subscripting = {"subscript":[], "index":[],
                             "slice":[],"extSlice":[]}
        
        self.comprehensions = {"listComp":[], "setComp":[], "generatorExp":[],
                               "dictComp":[], "comprehension":[]}
        
        self.statements = {"assign":[], "annAsign":[], "augAssign":[],
                           "print":[], "raise":[], "assert":[], "delete":[],
                           "pass":[]}
        
        self.imports = {"import":[], "importFrom":[], "alias":[]}

        self.controlFlow = {"if":[], "for":[], "break":[], "while":[], "break":[], 
                            "continue":[], "try":[], "tryFinally":[], "tryExcept":[],
                            "exceptHandler":[], "with":[], "withitem":[]}
        
        self.definitions = {"functionDef":[], "lambda":[], "arguments":[],
                            "arg":[], "return":[], "yield":[], "yeildFrom":[],
                            "global":[], "nonlocal":[], "classDef":[]}
        self.top = {"module":[], "interactive":[], "expression":[]}

    
    #fuctions for Literals
    def visit_Constant(self, node):
        self.literals["constant"].append(node.value) 
        self.generic_visit(node)

    def visit_Num(self, node):
        self.literals["num"].append(node.n)
        self.generic_visit(node)

    def visit_Str(self, node):
        self.literals["str"].append(node.s)
        self.generic_visit(node)

    def visit_FormattedValue(self, node):
        self.literals["formattedValue"].append(node.value)
        self.generic_visit(node)
    
    # def visit_JoinedStr(self, node):
    #     for alias in node.values:
    #         self.literals["joinedStr"].append(alias.s)
    #     self.generic_visit(node)
    
    def visit_Bytes(self, node):
        self.literals["bytes"].append(node.s)
        self.generic_visit(node)

    def visit_List(self, node):
        #appends the size of list
        self.literals["list"].append(len(node.elts))
        self.generic_visit(node)

    def visit_Tuple(self, node):
        self.literals["tuple"].append(len(node.elts))
        self.generic_visit(node)

    def visit_Set(self, node):
        
        self.literals["set"].append(len(node.elts))
        self.generic_visit(node)

    def visit_Dict(self, node):
        self.literals["dict"].append(node.keys)
        self.generic_visit(node)

    def visit_Ellipsis(self, node):
        self.literals["ellipsis"].append("0")
        self.generic_visit(node)

    def visit_NameConstant(self, node):
        self.literals["nameConstant"].append(node.value)
        self.generic_visit(node)

    # #functions for variables
    def visit_Name(self, node):
        self.variables["name"].append(node.id)
        self.generic_visit(node)

    def visit_Load(self, node):
        self.variables["load"].append("0")
        self.generic_visit(node)

    def visit_Store(self, node):
        self.variables["store"].append("0")
        self.generic_visit(node)

    def visit_Del(self, node):
        self.variables["del"].append("0")
        self.generic_visit(node)

    def visit_Starred(self, node):
        self.variables["starred"].append(node.value)
        self.generic_visit(node)


    # #functions for expressions
    def visit_Expr(self, node):
        self.expressions["expr"].append(node.value)
        self.generic_visit(node)
    
    def visit_NamedExpr(self, node):
        self.expressions["namedExpr"].append(node.target)
        self.generic_visit(node)

    def visit_UnaryOp(self, node):
        self.expressions["unaryOp"].append(node.op)
        self.generic_visit(node)

    def visit_UAdd(self, node):
        self.expressions["uAdd"].append("0")
        self.generic_visit(node)

    def visit_USub(self, node):
        self.expressions["uSub"].append("0")
        self.generic_visit(node)

    def visit_Not(self, node):
        self.expressions["not"].append("0")
        self.generic_visit(node)

    def visit_Invert(self, node):
        self.expressions["invert"].append("0")
        self.generic_visit(node)

    def visit_BinOp(self, node):
        self.expressions["binOp"].append(node.op)
        self.generic_visit(node)

    def visit_Add(self, node):
        self.expressions["add"].append("0")
        self.generic_visit(node)

    def visit_Sub(self, node):
        self.expressions["sub"].append("0")
        self.generic_visit(node)

    def visit_Mult(self, node):
        self.expressions["mult"].append("0")
        self.generic_visit(node)
    
    def visit_Div(self, node):
        self.expressions["div"].append("0")
        self.generic_visit(node)

    def visit_FloorDiv(self, node):
        self.expressions["floorDiv"].append("0")
        self.generic_visit(node)

    def visit_Mod(self, node):
        self.expressions["mod"].append("0")
        self.generic_visit(node)

    def visit_Pow(self, node):
        self.expressions["pow"].append("0")
        self.generic_visit(node)
    
    def visit_LShift(self, node):
        self.expressions["lShift"].append("0")
        self.generic_visit(node)

    def visit_RShift(self, node):
        self.expressions["rShift"].append("0")
        self.generic_visit(node)

    def visit_BitOr(self, node):
        self.expressions["bitOr"].append("0")
        self.generic_visit(node)
    
    def visit_BitXor(self, node):
        self.expressions["bitXor"].append("0")
        self.generic_visit(node)
    
    def visit_BitAnd(self, node):
        self.expressions["bitAnd"].append("0")
        self.generic_visit(node)

    def visit_MatMult(self, node):
        self.expressions["matMult"].append("0")
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        self.expressions["boolOp"].append(node.op)
        self.generic_visit(node)

    def visit_And(self, node):
        self.expressions["and"].append("0")
        self.generic_visit(node)
    
    def visit_Or(self, node):
        self.expressions["or"].append("0")
        self.generic_visit(node)

    def visit_Compare(self, node):
        self.expressions["compare"].append(node.ops)
        self.generic_visit(node)

    def visit_Eq(self, node):
        self.expressions["eq"].append("0")
        self.generic_visit(node)

    def visit_NotEq(self, node):
        self.expressions["notEq"].append("0")
        self.generic_visit(node)

    def visit_Lt(self, node):
        self.expressions["lt"].append("0")
        self.generic_visit(node)

    def visit_LtE(self, node):
        self.expressions["ltE"].append("0")
        self.generic_visit(node)

    def visit_Gt(self, node):
        self.expressions["gt"].append("0")
        self.generic_visit(node)

    def visit_GtE(self, node):
        self.expressions["gtE"].append("0")
        self.generic_visit(node)

    def visit_Is(self, node):
        self.expressions["is"].append("0")
        self.generic_visit(node)

    def visit_IsNot(self, node):
        self.expressions["isNot"].append("0")
        self.generic_visit(node)

    def visit_In(self, node):
        self.expressions["in"].append("0")
        self.generic_visit(node)

    def visit_NotIn(self, node):
        self.expressions["notIn"].append("0")
        self.generic_visit(node)

    def visit_Call(self, node):
        self.expressions["call"].append(node.func)
        self.generic_visit(node)

    def visit_keyword(self, node):
        self.expressions["keyword"].append([node.arg, node.value])
        self.generic_visit(node)

    def visit_IfExp(self, node):
        self.expressions["ifExp"].append([node.test, node.body, node.orelse])
        self.generic_visit(node)

    def visit_Attribute(self, node):
        self.expressions["attribute"].append(node.value)
        self.generic_visit(node)



    # #functions for subsctipting
        
    def visit_Subscript(self, node):
        self.subscripting["subscript"].append(node.value)
        self.generic_visit(node)

    def visit_Index(self, node):
        self.subscripting["index"].append(node.value)
        self.generic_visit(node)

    def visit_Slice(self, node):
        self.subscripting["slice"].append("0")
        self.generic_visit(node)

    def visit_ExtSlice(self, node):
        self.subscripting["extSlice"].append("0")
        self.generic_visit(node)


    # #functions for comprehensions
    def visit_ListComp(self, node):
        self.comprehensions["listComp"].append("0")
        self.generic_visit(node)

    def visit_SetComp(self, node):
        self.comprehensions["setComp"].append("0")
        self.generic_visit(node)

    def visit_GeneratorExp(self, node):
        self.comprehensions["generatorExp"].append("0")
        self.generic_visit(node)

    def visit_DictComp(self, node):
        self.comprehensions["dictComp"].append("0")
        self.generic_visit(node)

    def visit_Comprehension(self, node):
        self.comprehensions["comprehension"].append("0")
        self.generic_visit(node)

    # #functions for statements
        
    def visit_Assign(self, node):
        self.statements["assign"].append(node.value)
        self.generic_visit(node)

    def visit_AnnAssign(self, node):
        self.statements["annAssign"].append(node.target)
        self.generic_visit(node)

    def visit_AugAssign(self, node):
        #i.e a += 1
        self.statements["augAssign"].append(node.target)
        self.generic_visit(node)

    def visit_Print(self, node):
        self.statements["print"].append(node.values)
        self.generic_visit(node)

    def visit_Raise(self, node):
        self.statements["raise"].append(node.exc)
        self.generic_visit(node)

    def visit_Assert(self, node):
        self.statements["assert"].append(node.msg)
        self.generic_visit(node)

    def visit_Delete(self, node):
        self.statements["delete"].append(node.targets)
        self.generic_visit(node)

    def visit_Pass(self, node):
        self.statements["pass"].append("0")
        self.generic_visit(node)

    # #functions for Imports
        
    def visit_Import(self, node):
        self.imports["import"].append(node.names)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        self.imports["importFrom"].append(node.names)
        self.generic_visit(node)

    def visit_Alias(self, node):
        self.imports["alias"].append(node.name)
        self.generic_visit(node)

    # #functions for Control Flow
    
    def visit_If(self, node):
        self.controlFlow["if"].append("0")
        self.generic_visit(node)

    def visit_For(self, node):
        self.controlFlow["for"].append("0")
        self.generic_visit(node)

    def visit_While(self, node):
        self.controlFlow["while"].append("0")
        self.generic_visit(node)

    def visit_Break(self, node):
        self.controlFlow["break"].append("0")
        self.generic_visit(node)

    def visit_Continue(self, node):
        self.controlFlow["continue"].append("0")
        self.generic_visit(node)

    def visit_Try(self, node):
        self.controlFlow["try"].append("0")
        self.generic_visit(node)

    def visit_TryFinally(self, node):
        self.controlFlow["tryFinally"].append("0")
        self.generic_visit(node)
    
    def visit_ExecptHandler(self, node):
        self.controlFlow["execptHandler"].append(node.name)
        self.generic_visit(node)

    def visit_With(self, node):
        self.controlFlow["with"].append(node.items)
        self.generic_visit(node)

    def visit_Withitem(self, node):
        self.controlFlow["withitem"].append("0")
        self.generic_visit(node)

    # #functions for definitions
    def visit_FunctionDef(self, node):
        self.definitions["functionDef"].append(node.name)
        self.generic_visit(node)

    def visit_Lambda(self, node):
        self.definitions["lambda"].append(node.body)
        self.generic_visit(node)

    def visit_Arguments(self, node):
        self.definitions["arguments"].append(node.args)
        self.generic_visit(node)

    def visit_Arg(self, node):
        self.definitions["arg"].append(node.arg)
        self.generic_visit(node)

    def visit_Return(self, node):
        self.definitions["return"].append(node.value)
        self.generic_visit(node)

    def visit_Yield(self, node):
        self.definitions["yield"].append(node.value)
        self.generic_visit(node)

    def visit_YieldFrom(self, node):
        self.definitions["yieldFrom"].append(node.value)
        self.generic_visit(node)

    def visit_Global(self, node):
        self.definitions["global"].append(node.names)
        self.generic_visit(node)

    def visit_Nonlocal(self, node):
        self.definitions["nonlocal"].append(node.names)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        self.definitions["classDef"].append(node.name)
        self.generic_visit(node)

    # #Functions for top
    def visit_Module(self, node):
        self.top["module"].append("0")
        self.generic_visit(node)

    def visit_Interactive(self, node):
        self.top["interactive"].append("0")
        self.generic_visit(node)

    def visit_Expression(self, node):
        self.top["expression"].append("0")
        self.generic_visit(node)





    #printing Functions
    def printLiterals(self, outFileName):
        f = open(outFileName, "a")
        f.write("\n\n\n\nCLASS TYPE: Literals\n")
        header = ["TYPE", "QUANTITY"]
        data = []
        for key in self.literals.keys():
            if(len(self.literals[key])==0):
                continue
            data.append([key, len(self.literals[key])])
        if(len(data)!=0):
            f.write(tabulate(data, header, tablefmt = "grid"))
        f.close()
        
    
    def printVariables(self, outFileName):
        f = open(outFileName, "a")
        f.write("\n\n\n\nCLASS TYPE: Variables\n")
        header = ["TYPE", "QUANTITY"]
        data = []
        for key in self.variables.keys():
            if(len(self.variables[key])==0):
                continue
            data.append([key, len(self.variables[key])])
        if(len(data)!=0):
            f.write(tabulate(data, header, tablefmt = "grid"))
        f.close()

    def printExpressions(self, w):
        f = open(w, "a")
        f.write("\n\n\n\nCLASS TYPE: Expressions\n")
        header = ["TYPE", "QUANTITY"]
        data = []
        for key in self.expressions.keys():
            if(len(self.expressions[key])==0):
                continue
            data.append([key, len(self.expressions[key])])
        if(len(data)!=0):
            f.write(tabulate(data, header, tablefmt = "grid"))
        f.close()

    def printSubcripting(self, q):
        f = open(q, "a")
        f.write("\n\n\n\nCLASS TYPE: Subscripting\n")
        header = ["TYPE", "QUANTITY"]
        data = []
        for key in self.subscripting.keys():
            if(len(self.subscripting[key])==0):
                continue
            data.append([key, len(self.subscripting[key])])
        if(len(data)!=0):
            f.write(tabulate(data, header, tablefmt = "grid"))
        f.close()


    def printComprehensions(self, w):
        f = open(w, "a")
        f.write("\n\n\n\nCLASS TYPE: Comprehensions\n")
        header = ["TYPE", "QUANTITY"]
        data = []
        for key in self.comprehensions.keys():
            if(len(self.comprehensions[key])==0):
                continue
            data.append([key, len(self.comprehensions[key])])
        if(len(data)!=0):
            f.write(tabulate(data, header, tablefmt = "grid"))
        f.close()

    def printStatements(self, w):
        f = open(w, "a")
        f.write("\n\n\n\nCLASS TYPE: Statements\n")
        header = ["TYPE", "QUANTITY"]
        data = []
        for key in self.statements.keys():
            if(len(self.statements[key])==0):
                continue
            data.append([key, len(self.statements[key])])
        if(len(data)!=0):
            f.write(tabulate(data, header, tablefmt = "grid"))
        f.close()


    def printImports(self, w):
        f = open(w, "a")
        f.write("\n\n\n\nCLASS TYPE: Imports\n")
        header = ["TYPE", "QUANTITY"]
        data = []
        for key in self.imports.keys():
            if(len(self.imports[key])==0):
                continue
            data.append([key, len(self.imports[key])])
        if(len(data)!=0):
            f.write(tabulate(data, header, tablefmt = "grid"))
        f.close()


    def printControlFlow(self, w):
        f = open(w, "a")
        f.write("\n\n\n\nCLASS TYPE: Control Flow\n")
        header = ["TYPE", "QUANTITY"]
        data = []
        for key in self.controlFlow.keys():
            if(len(self.controlFlow[key])==0):
                continue
            data.append([key, len(self.controlFlow[key])])
        
        if(len(data)!=0):
            f.write(tabulate(data, header, tablefmt = "grid"))
        f.close()

    def printDefinitions(self, w):
        f = open(w, "a")
        f.write("\n\n\n\nCLASS TYPE: Definitions\n")
        header = ["TYPE", "QUANTITY"]
        data = []
        for key in self.definitions.keys():
            if(len(self.definitions[key])==0):
                continue
            data.append([key, len(self.definitions[key])])
        if(len(data)!=0):
            f.write(tabulate(data, header, tablefmt = "grid"))
        f.close()


    def printTop(self, w):
        f = open(w, "a")
        f.write("\n\n\n\nCLASS TYPE: Top Level Nodes\n")
        header = ["TYPE", "QUANTITY"]
        data = []
        for key in self.top.keys():
            if(len(self.top[key])==0):
                continue
            data.append([key, len(self.top[key])])
        if(len(data)!=0):
            f.write(tabulate(data, header, tablefmt = "grid"))
        f.close()
   

    def report(self, outFileName, depth):
        f = open(outFileName, "a")
        f.write("AST CLASS COUNT FOR FILE: {}\nFINAL TREE DEPTH: {}\n".format(self.pythonFile, depth))
        f.close()
        self.printLiterals(outFileName)
        self.printVariables(outFileName)
        self.printExpressions(outFileName)
        self.printSubcripting(outFileName)
        self.printComprehensions(outFileName)
        self.printStatements(outFileName)
        self.printImports(outFileName)
        self.printDefinitions(outFileName)
        self.printControlFlow(outFileName)
        self.printTop(outFileName)
        


    


# class pyFile():
#     def __init__(self, filename):
#         self.file = filename
#         self.literals = []
#         self.variables = []
#         self.expressions = []
#         self.subcripting = []
#         self.comprehensions = []
#         self.statements = []
#         self.imports = []
#         self.controlflow = []
#         self.definitions = []
    
#     def create_record(self, asts):
#         #definitions
#         data = []
#         for key in asts.definitions.keys():
#             if(len(asts.definitions[key])==0):
#                 continue
#             data.append([key, len(asts.definitions[key])])
#         for obj in data:
#             self.definitions.append(obj)

#         print(f"number of definitions: {data}")


def calc_depth_ast(root):
    return 1 + max((calc_depth_ast(child)
                    for child in ast.iter_child_nodes(root)),
                default = 0)
        
        

def gather_data(input_directory, output_directory):
    # Walk through the directory
    output_file = output_directory + "/" 
    for root, dirs, files in os.walk(input_directory):
        for f in files:
            # Check if the file has a .py extension
            if f.endswith('.py'):
                out = output_file + f.split(".")[0] +".txt"
                file_path = os.path.join(root, f)

                #analyze the data for each file
                root = ast_maker(file_path, out)

                

  


if __name__ == "__main__":
    #Sample python files come from
    #https://github.com/nihathalici/The-Big-Book-of-Small-Python-Projects/tree/main
    
    
    while(True):
        print("Type 'Q' to quit at any time.\n")
        state = input("ENTER PYTHON FILE DIRECTORY:\n>> ")
        if(state=="Q" or state=="q"):
            break
        out = input("ENTER OUTPUT FILE DIRECTORY:\n>> ")
        if(out=="Q" or out=="q"):
            break
        gather_data(state, out)
        
    exit(0)


