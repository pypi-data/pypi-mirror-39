'''
 * Copyright 2018 IBM Corporation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
'''

import sys
from antlr4 import *
from .stanLexer import stanLexer
from .stanParser import stanParser
from .stanListener import stanListener
from antlr4.error.ErrorListener import ErrorListener


def parseExpr(expr):
    node = ast.parse(expr).body[0].value
    return node

def atomIsLvalue(a):
    if a.variable() is not None:
        return True
    if a.arrayAccess is not None:
        return atomIsLvalue(a.arrayAccess)
    return False

def exprIsLvalue(e):
    if e.atom() is not None:
        return atomIsLvalue(e.atom())
    return False

class StanStats(stanListener):
    def __init__(self):
        self.stats = {
            'calls' : [],
            'left_expr' : 0,
            'target' : 0,
        }

    def exitCallExpr(self, ctx):
        if ctx.f is not None:
            f = ctx.IDENTIFIER().getText()
            self.stats['calls'].append(f)
        elif ctx.id1 is not None:
            id1 = ctx.IDENTIFIER().getText()
            self.stats['calls'].append(id1)

    def exitAssignStmt(self, ctx):
        if ctx.sample is not None:
            if not exprIsLvalue(ctx.le):
                self.stats['left_expr'] += 1
        if ctx.op and ctx.PLUS_EQ() is not None:
            if ctx.lvalue().IDENTIFIER().getText() == 'target':
                self.stats['target'] += 1

    def exitParametersBlock(self, ctx):
        pass


####################

class MyErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print('Line ' + str(line) + ':' + str(column) +
              ': Syntax error, ' + str(msg))
        raise SyntaxError


def stream2parsetree(stream):
    lexer = stanLexer(stream)
    stream = CommonTokenStream(lexer)
    parser = stanParser(stream)
    parser._listeners = [MyErrorListener()]
    tree = parser.program()
    return tree


def parsetree2stats(tree):
    stan2stats = StanStats()
    walker = ParseTreeWalker()
    walker.walk(stan2stats, tree)
    stats = stan2stats.stats
    return stats


def stan2stats(stream):
    tree = stream2parsetree(stream)
    stats = parsetree2stats(tree)
    return stats


def stan2statsFile(filename):
    stream = FileStream(filename)
    return stan2stats(stream)


def stan2statsStr(str):
    stream = InputStream(str)
    return stan2stats(stream)


def compute_stats(code_string=None, code_file=None):
    if not (code_string or code_file) or (code_string and code_file):
        assert False, "Either string or file but not both must be provided."
    if code_string:
        stats = stan2statsStr(code_string)
    else:
        stats = stan2statsFile(code_file)
    return stats

def main(argv):
    if (len(argv) <= 1):
        assert False, "File name expected"
    for i in range(1, len(argv)):
        print('# -------------')
        print('#', argv[i])
        print('# -------------')
        stats = compute_stats(code_file=argv[i])
        print(stats)


if __name__ == '__main__':
    main(sys.argv)
