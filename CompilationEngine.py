from JackTokenizer import TokenType, Tokenizer


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
        self.tokenizer = Tokenizer(inputPath)
        self.tokenizer.advance()
        self.indentLevel = 0

    def CompileClass(self):
        """
        Compiles a complete class.
        """
        self.EnterScope("class")

        self.ConsumeKeyword([Keyword.CLASS])
        self.ConsumeIdentifier()  # className
        self.ConsumeSymbol('{')

        while (self.IsKeyword(Keyword.VAR)):
            self.CompileClassVarDec()

        # subroutineDec*
        while (self.IsType(TokenType.KEYWORD) and
               self.tokenizer.keyword() in [Keyword.CONSTRUCTOR,
                                            Keyword.FUNCTION, Keyword.METHOD]):
            self.CompileSubroutine()

        self.ConsumeSymbol('}')

        self.ExitScope("class")

    def CompileClassVarDec(self):
        """
        Compiles a static declaration or a field declaration.
        """
        self.EnterScope("classVarDec")

        self.ConsumeKeyword([Keyword.STATIC, Keyword.FIELD])
        self.ConsumeType()
        self.ConsumeIdentifier()  # varName

        while (self.IsSymbol(',')):
            self.ConsumeSymbol(',')
            self.ConsumeIdentifier()  # varName

        self.ConsumeSymbol(';')

        self.ExitScope("classVarDec")

    def CompileSubroutine(self):
        """
        Compiles a complete method, function, or constructor.
        """
        self.EnterScope("subroutineDec")

        self.ConsumeKeyword([Keyword.CONSTRUCTOR, Keyword.FUNCTION,
                             Keyword.METHOD])
        if (self.IsKeyword(Keyword.VOID)):
            self.ConsumeKeyword([Keyword.VOID])
        else:
            self.ConsumeType()

        self.ConsumeIdentifier()  # subroutineName

        self.ConsumeSymbol('(')
        self.CompileParameterList()
        self.ConsumeSymbol(')')

        self.CompileSubroutineBody()

        self.ExitScope("subroutineDec")

    def CompileSubroutineBody(self):
        self.EnterScope("subroutineBody")

        self.ConsumeSymbol('{')
        while (self.IsKeyword(Keyword.VAR)):
            self.CompileVarDec()
        self.CompileStatements()
        self.ConsumeSymbol('}')

        self.ExitScope("subroutineBody")

    def CompileParameterList(self):
        """
        Compiles a (possibly empty) parameter list,
        not including the enclosing "()".
        """
        self.EnterScope("parameterList")

        if (not self.IsSymbol(')')):
            self.ConsumeType()
            self.ConsumeIdentifier()

        while(self.IsSymbol(',')):
            self.ConsumeSymbol(',')
            self.ConsumeType()
            self.ConsumeIdentifier()

        self.ExitScope("parameterList")

    def CompileVarDec(self):
        """
        Compiles a var declaration.
        """
        self.EnterScope("varDec")

        self.ConsumeKeyword([Keyword.VAR])
        self.ConsumeType()
        self.ConsumeIdentifier()  # varName
        while (self.IsSymbol(',')):
            self.ConsumeSymbol(',')
            self.ConsumeIdentifier()  # varName

        self.ConsumeSymbol(';')

        self.ExitScope("varDec")

    def CompileStatements(self):
        """
        Compiles a sequence of statements, not including the
        enclosing "{}".
        """
        self.EnterScope("statements")
        self.ExitScope("statements")

    def CompileDo(self):
        """
        Compiles a do statement.
        """
        self.EnterScope("doStatement")
        self.ExitScope("doStatement")

    def CompileLet(self):
        """
        Compiles a let statement.
        """
        self.EnterScope("letStatement")
        self.ExitScope("letStatement")

    def CompileWhile(self):
        """
        Compiles a while statement.
        """
        self.EnterScope("whileStatement")
        self.ExitScope("whileStatement")

    def CompileReturn(self):
        """
        Compiles a return statement.
        """
        self.EnterScope("returnStatement")
        self.ExitScope("returnStatement")

    def CompileIf(self):
        """
        Compiles an if statement, possibly with a trailing
        else clause.
        """
        self.EnterScope("ifStatement")
        self.ExitScope("ifStatement")

    def CompileExpression(self):
        """
        Compiles an expression.
        """
        self.EnterScope("expression")
        self.ExitScope("expression")

    def CompileTerm(self):
        """
        Compiles a term.
        """
        self.EnterScope("term")
        self.ExitScope("term")

    def CompileExpressionList(self):
        """
        Compiles a (possibly empty) comma-separated
        list of expressions.
        """
        self.EnterScope("expressionList")
        self.ExitScope("expressionList")

    def IsKeyword(self, keyword):
        return (self.IsType(TokenType.KEYWORD) and
                self.tokenizer.keyword() == keyword)

    def IsSymbol(self, symbol):
        return (self.IsType(TokenType.SYMBOL) and
                self.tokenizer.symbol() == symbol)

    def IsType(self, tokenType):
        return self.tokenizer.tokenType() == tokenType

    def ConsumeType(self):
        if (self.tokenizer.tokenType() == TokenType.IDENTIFIER):
            self.ConsumeIdentifier()
        else:
            self.ConsumeKeyword([Keyword.INT, Keyword.CHAR, Keyword.BOOLEAN])

    def ConsumeKeyword(self, keywordList):
        self.VerifyTokenType(TokenType.KEYWORD)
        actual = self.tokenizer.keyword()
        if actual not in keywordList:
            raise Exception("Expected keywords: {}, Actual: {}".
                            format(keywordList, actual))
        self.OutputTag("keyword", actual)
        self.tokenizer.advance()

    def ConsumeSymbol(self, symbol):
        self.VerifyTokenType(TokenType.SYMBOL)
        actual = self.tokenizer.symbol()
        if actual != symbol:
            raise Exception("Expected symbol: {}, Actual: {}".
                            format(symbol, actual))
        self.OutputTag("symbol", actual)
        self.tokenizer.advance()

    def ConsumeIntegerConstant(self):
        self.VerifyTokenType(TokenType.INT_CONST)
        self.OutputTag("integerConstant", self.tokenizer.intVal())
        self.tokenizer.advance()

    def ConsumeStringConstant(self):
        self.VerifyTokenType(TokenType.STRING_CONST)
        self.OutputTag("stringConstant", self.tokenizer.stringVal())
        self.tokenizer.advance()

    def ConsumeIdentifier(self):
        self.VerifyTokenType(TokenType.IDENTIFIER)
        self.OutputTag("identifier", self.tokenizer.identifier())
        self.tokenizer.advance()

    def VerifyTokenType(self, tokenType):
        actual = self.tokenizer.tokenType()
        if actual != tokenType:
            raise Exception("Expected token type: {}, Actual: {}".
                            format(tokenType, actual))

    def EnterScope(self, name):
        self.Output("<{}>".format(name))
        self.indentLevel += 1

    def ExitScope(self, name):
        self.indentLevel -= 1
        self.Output("</{}>".format(name))

    def OutputTag(self, tag, value):
        self.Output("<{}> {} </{}>".format(tag, value, tag))

    def Output(self, text):
        print ("\t" * self.indentLevel) + text

if __name__ == '__main__':
    inputPath = r"C:\Users\Dana\Google Drive\Masters\Nand2Tetris\projects\10\ArrayTest\Main.jack"

    engine = CompilationEngine(inputPath, "")
    engine.CompileClass()
