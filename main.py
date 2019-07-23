# Trevor Ramey 
# Interpreter Programming Project
# CS 3361 Concepts of Programming Languages

# Global  Variables

VAR = 'VAR'
AND = 'AND'
OR = 'OR'
TAG = 'TAG'
IMPLY = 'IMPLY'
equalsTo = 'equalsTo'
NOT = 'NOT'
TRUE ='TRUE'
FALSE = 'FALSE'
Lbracket ='Lbracket'
Rbracket ='Rbracket'
END = 'END'
SEMI = 'SEMI'


def main():
    while True:
        try:
            String = input('Enter Expression: ')
        except EOFError:
            break
        if not String:   
            continue

        try:
            lexer = Lex(String)
            interpreter = Interpreter(lexer)
            result = interpreter.eval()
            print(result)
        except (SyntaxError, ValueError) as err:
            print(str(err))


class Lex(object):

  def __init__(self, String):
    self.text = String
    self.pos = 0
    self.current = String[self.pos]

  def next_character(self):
    self.pos += 1
    if self.pos <= len(self.text) - 1:
      self.current = self.text[self.pos]
    else:
      self.current = None

  def whitespace(self):
    while self.current is not None and self.current.isspace():
      self.next_character()

  @staticmethod
  def error(expecting=None, got=None):
    # Will rase a invalid character error
    if expecting is not None:
      raise ValueError('Expecting \'{expecting}\','' got \'{got}\' instead.'.format(expecting=expecting,got=got))
    else:
      raise ValueError('Invalid character: \'{got}\''.format(got=got))

  def implies(self):
    #Creates an imply '->' character for a Token object 
    # compile what should be a '->'
    placeHolder = self.current
    self.next_character()
    combination = placeHolder + self.current

    if combination == "->":
      self.next_character()
      return combination
    else:
      self.error(expecting="->", got=combination)
  
  def var(self):
    current = self.current
    if current.islower():
      self.next_character()
      return current
    else:
      self.error(expecting="Lower character", got=current)

  
  def equalsTo(self):
    #Creates an imply ':=' character for a Token object 
    placeHolder = self.current
    self.next_character()
    combination = placeHolder + self.current
    if combination == ":=":
      self.next_character()
      return combination
    else:
     self.error(expecting="->", got=combination)
  
  def get_next_token(self):
    while self.current is not ".":
      if self.current is None:
        self.error(expecting=".", got=self.current)
      
      elif self.current.isspace():
        self.whitespace()
        continue

      elif self.current == "^":
        self.next_character()
        return Token(AND, "^")

      elif self.current == "V":
        self.next_character()
        return Token(OR, "V")
      
      elif self.current == "#":
        self.next_character()
        return Token(TAG,"#")

      elif self.current == "-":
        return Token(IMPLY, self.implies())

      elif self.current == ":":
        return Token(equalsTo, self.equalsTo())

      elif self.current == "~":
        self.next_character()
        return Token(NOT, "~")
      
      elif self.current == ";":
        self.next_character()
        return Token(SEMI,";")

      elif self.current == "T":
        self.next_character()
        return Token(TRUE, "T")

      elif self.current == "F":
        self.next_character()
        return Token(FALSE, "F")
      
      elif self.current.islower():
        self.next_character
        return Token(VAR, self.var())
        return

      elif self.current == "(":
        self.next_character()
        return Token(Lbracket, "(")

      elif self.current == ")":
        self.next_character()
        return Token(Rbracket, ")")
      else:
        self.error(got=self.current)  # invalid character (?)
        break

    return Token(END, ".")  # EOF reached

class Token(object):

  def __init__(self,token_type,value):
    self.token_type = token_type
    self.value = value
  
  def _str_(self):
    return 'Token({token_type}, {value})'.format(
      token_type = self.token_type,
      value = self.value
    )

class Interpreter(object):
  
  def __init__(self,lex):
    self.lex = lex
    self.current_token = self.lex.get_next_token()
    self.stack = []
  
  @staticmethod
  def error(expecting, got):
    if expecting is not None and got is not None:
      raise SyntaxError('Expecting \'{expecting}\','' got \'{got}\' instead.'.format(
        expecting = expecting,
        got = got,
      ))
    else:
      raise SyntaxError('SyntaxError')
  
  def pick_off(self, token_type):
    if self.current_token.token_type == token_type:
      self.current_token = self.lex.get_next_token()
    else:
      self.error(expecting = token_type, got = self.current_token.token_type)

  def eval(self):
    if self.B():
      return str(self.stack)
  
  def B(self):
    if self.VA():
      return self.current_token.token_type == END
    elif self.IT():
        return self.current_token.token_type == END
    else:
      self.error(expecting = ' # , ~ , T , F, lower_var , ( ', got= self.current_token.value)
      return False

  def VA(self):
    if self.current_token.token_type == TAG:
      self.pick_off(TAG)
      if self.current_token.token_type == VAR:
        self.pick_off(VAR)
        if self.current_token.token_type == equalsTo:
          self.pick_off(equalsTo)
          if self.IT():
            if self.current_token.token_type == SEMI:
              self.pick_off(SEMI)
              if self.VA():
                return True
              else:
                return False
            else:
              return False
          else: 
            return False
        else:
          return False
      else:
        return False
    elif self.current_token.token_type in (END , SEMI , Rbracket):
      return True
    else:
      return False



        


  def IT(self):
    if self.CT():
      return self.IT_tail()
    else:
      self.error(expecting = ' ~ , T , F , lower_var , ( , Fail IT', got = self.current_token.value)
      return False

  def IT_tail(self):

    if self.current_token.token_type == IMPLY:
      self.pick_off(IMPLY)
      if self.CT():
        if self.IT_tail():
          interim_second = self.stack.pop()
          interim_first = self.stack.pop()
          self.stack.append((not interim_first) or interim_second)
          return True
        else:
          return False
      else:
        return False
    elif self.current_token.token_type in (END, Rbracket):
      return True
    else:
      self.error(expecting = ' -> , . , ; , ), Fail IT_tail', got = self.current_token.value)
      return False





  
  def CT(self):
    if self.L():
      return self.CT_Tail()
    else:
      self.error(expecting = '∼, T, F, lower_var,( , Fail CT', got = self.current_token.value)
      return False

  def CT_Tail(self):
    if self.current_token.token_type == OR:
      self.pick_off(OR)
      if self.L():
        if self.CT_Tail:
          interim = self.stack.pop()
          interim1 = self.stack.pop()
          self.stack.append(interim or interim1)
          return True
        else:
          return False
      else:
        return False
    elif self.current_token.token_type == AND:
      self.pick_off(AND)
      if self.L():
          interim2 = self.stack.pop()
          interim1 = self.stack.pop()
          self.stack.append(interim1 and interim2)
          return self.CT_Tail
      else:
        return False
    elif self.current_token.token_type in (IMPLY, END , Rbracket):
      return True
    else:
      self.error(expecting = 'V , ^ , -> , . , ;,), Fail CT_tail', got = self.current_token.value)
      return False


  def L(self):
    #Literal
    if self.current_token.token_type == NOT:
      self.pick_off(NOT)
      if self.L():
        interim = self.stack.pop()
        self.stack.append(not interim)
        return True
      else:
        return False
    elif self.A():
      return True
    else:
      self.error(expecting = 'T , F , lower_var , ( , ~, Fail L', got = self.current_token.value)
      return False

  def A(self):
    #Atom
    if self.current_token.token_type == TRUE:
      self.pick_off(TRUE)
      self.stack.append(True)
      return True
    elif self.current_token.token_type == FALSE:
      self.pick_off(FALSE)
      self.stack.append(False)
      return True
    elif self.current_token.token_type == VAR:
      self.pick_off(VAR)
      return True
    elif self.current_token.token_type == Lbracket:
      self.pick_off(Lbracket)
      if self.IT():
        if self.current_token.token_type == Rbracket:
          self.pick_off(Rbracket)
          return True
        else:
          return False
      else:
        return False
    else:
      self.error(expecting = 'T, F , lower_var, ~ , (, Fail A', got = self.current_token.value)
      return False



if __name__ == '__main__':
    main()
