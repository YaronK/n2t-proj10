import JackTokenizer


class Keyword:
    CLASS = 'class'
    METHOD = 'method'
    FUNCTION = 'function'
    CONSTRUCTOR = 'constructor'
    INT = 'int'
    BOOLEAN = 'boolean'
    CHAR = 'char'
    VOID = 'void'
    VAR = 'var'
    STATIC = 'static'
    FIELD = 'field'
    LET = 'let'
    DO = 'do'
    IF = 'if'
    ELSE = 'else'
    WHILE = 'while'
    RETURN = 'return'
    TRUE = 'true'
    FALSE = 'false'
    NULL = 'null'
    THIS = 'this'


class CompilationEngine:
    def __init__(self, inputPath, outputPath):
        self.tokenizer = JackTokenizer(inputPath)

    def CompileClass(self):
        """
        Compiles a complete class.
        """
        pass

    def CompileClassVarDec(self):
        """
        Compiles a static declaration or a field declaration.
        """
        pass

    def CompileSubroutine(self):
        """
        Compiles a complete method, function, or constructor.
        """
        pass

    def CompileParameterList(self):
        """
        Compiles a (possibly empty) parameter list,
        not including the enclosing "()".
        """
        pass

    def CompileVarDec(self):
        """
        Compiles a var declaration.
        """
        pass

    def CompileStatements(self):
        """
        Compiles a sequence of statements, not including the
        enclosing "{}".
        """
        pass

    def CompileDo(self):
        """
        Compiles a do statement.
        """
        pass

    def CompileLet(self):
        """
        Compiles a let statement.
        """
        pass

    def CompileWhile(self):
        """
        Compiles a while statement.
        """
        pass

    def CompileReturn(self):
        """
        Compiles a return statement.
        """
        pass

    def CompileIf(self):
        """
        Compiles an if statement, possibly with a trailing
        else clause.
        """
        pass

    def CompileExpression(self):
        """
        Compiles an expression.
        """
        pass

    def CompileTerm(self):
        """
        Compiles a term.
        """
        pass

    def CompileExpressionList(self):
        """
        Compiles a (possibly empty) comma-separated
        list of expressions.
        """
        pass
