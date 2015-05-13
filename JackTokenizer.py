class TokenType:
    KEYWORD = 1
    SYMBOL = 2
    IDENTIFIER = 3
    INT_CONST = 4
    STRING_CONST = 5


class Keyword:
    CLASS = 1
    METHOD = 2
    FUNCTION = 3
    CONSTRUCTOR = 4
    INT = 5
    BOOLEAN = 6
    CHAR = 7
    VOID = 8
    VAR = 9
    STATIC = 10
    FIELD = 12
    LET = 13
    DO = 14
    IF = 15
    ELSE = 16
    WHILE = 17
    RETURN = 18
    TRUE = 19
    FALSE = 20
    NULL = 21
    THIS = 22

Symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+',
           '-', '*', '/', '&', '|', '<', '>', '=', '~']


class JackTokenizer(object):

    def __init__(self, filePath):
        """
        Opens the input file and get ready to tokenize it.
        """
        self.file = open(filePath)
        self.current_token = None
        self.current_token_type = None

        self.next_token = None
        self.next_token_type = None
        self.readNextToken()

    def hasMoreTokens(self):
        """
        Do we have more tokens in the input?
        """
        return self.file.re

    def advance(self):
        """
        Gets the next token from the input and makes it the current
        token. This method should only be called if hasMoreTokens()
        is true. Initially there is no current token.
        """
        pass

    def tokenType(self):
        """
        Returns the type of the current token.
        """
        pass

    def keyWord(self):
        """
        Returns the keyword which is the current token. Should be
        called only when tokenType() is KEYWORD.
        """
        pass

    def symbol(self):
        """
        Returns the character which is the current token. Should
        be called only when tokenType() is SYMBOL.
        """
        pass

    def identifier(self):
        """
        Returns the identifier which is the current token. Should
        be called only when tokenType() is IDENTIFIER.
        """
        pass

    def intVal(self):
        """
        Returns the integer value which is the current token.
        Should be called only when tokenType() is INT_CONST.
        """
        pass

    def stringVal(self):
        """
        Returns the string value which is the current token. Should
        be called only when tokenType() is STRING_CONST.
        """
        pass

    def readNextToken(self):
        self.readNullCharacters()

        c = self.peekChar()

        if c == '':
            self.next_token = None
            self.next_token_type = None
            return

        if c == '"':
            self.next_token = self.readStringConstant()
            self.next_token_type = TokenType.STRING_CONST
            return

        if c == '/':
            c = self.readChar()
            if (self.peekChar() in ['/', '*']):
                self.readComment()
                self.readNextToken()
                return
            else:
                self.next_token = c
                self.next_token_type = TokenType.SYMBOL
                return

        if c in Symbols:
            self.next_token = self.readChar()
            self.next_token_type = TokenType.SYMBOL
            return

        if c >= '0' and c <= '9':
            self.next_token = self.readIntegerConstant()
            self.next_token_type = TokenType.INT_CONST
            return

        if ((c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or (c == '_')):
            self.readKeywordOfIdentifier()

        raise "Bad character"

    def readComment(self):
        c = self.readChar()
        if (c == '/'):
            while (self.readChar() != '\n'):
                pass
        elif (c == '*'):
            first = self.readChar()
            second = self.readChar()
            while not (first == '*' and second == '/'):
                first = second
                second = self.readChar()
        else:
            raise "Error reading comment."

    def readStringConstant(self):
        pass  # TODO:

    def readIntegerConstant(self):
        pass  # TODO:

    def readKeywordOfIdentifier(self):
        pass  # TODO:

    def readNullCharacters(self):
        while (self.peekChar() in [' ', '\r', '\n', '\t']):
            self.readChar()

    def readChar(self):
        return self.file.read(1)

    def peekChar(self):
        pos = self.file.tell()
        char = self.file.read(1)
        self.file.seek(pos)
        return char

    def close(self):
        self.file.close()
