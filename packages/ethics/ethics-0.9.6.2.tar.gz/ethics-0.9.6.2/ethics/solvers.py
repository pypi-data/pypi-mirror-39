from ethics.language import Not, And, Or, Causes, Gt, Eq, U, Impl, Formula, Exists, Forall
import copy

class Branch:
    def __init__(self, formulas):
        self.formulas = []
        self.unexpanded = []
        self.formulas += formulas
        self.unexpanded += [f for f in formulas if not self.isLiteral(f)]
        self.interventions = {}
        self.varCounter = 0

    def isLiteral(self, f):
        if isinstance(f, str):
            return True
        if isinstance(f, Not) and isinstance(f.f1, str):
            return True
        return False

    def firstUnexpandedNonForallFormula(self):
        for f in self.unexpanded:
            if not isinstance(f, Forall):
                return f
        return None

    def setUnexpanded(self, formulas):
        self.unexpanded = []
        self.unexpanded += formulas
    
    def setInterventions(self, formulas):
        self.interventions = copy.deepcopy(formulas)

    def addIntervention(self, cause, effect):
        if cause not in self.interventions:
            self.interventions[cause] = []
        if effect not in self.interventions[cause]:
            self.interventions[cause] += [effect]

    def addFormula(self, formula):
        if formula not in self.formulas:
            self.formulas += [formula]
            if not self.isLiteral(formula):
                self.unexpanded += [formula]
    
    def isSaturated(self):
        for f in self.unexpanded:
            if not isinstance(f, Forall): # Forall will expand in every iteration
                return False
        return True
        
    def isClosed(self):
        for f in self.formulas:
            if Formula.getNegation(f) in self.formulas:
                self.unexpanded = [] # Saturate it 
                return True
        for k in self.interventions:
            for v in self.interventions[k]:
                if Not(v) in self.interventions[k]:
                    self.unexpanded = [] # Saturate it 
                    return True
        return False

    def generateNewVariable(self):
        self.varCounter += 1
        return "new_var_"+str(self.varCounter)

    def getAllLiteralsInFormula(self, f):
        if isinstance(f, str):
            return [f]
        elif isinstance(f, Not) and isinstance(f.f1, str):
            return [f]
        elif isinstance(f, Gt) or isinstance(f, Eq):
            if f.f1 == 0:
                return [f.f2.t1]
            elif f.f2 == 0:
                return [f.f1.t1]
        elif isinstance(f, Not):
            return self.getAllLiteralsInFormula(f.f1)
        elif isinstance(f, And) or isinstance(f, Or) or isinstance(f, Impl) or isinstance(f, Causes):
            return self.getAllLiteralsInFormula(f.f1) + self.getAllLiteralsInFormula(f.f2)
        else:
            return []

    def getAllLiteralsInBranch(self):
        lits = []        
        for f in self.formulas:
            lits += self.getAllLiteralsInFormula(f)
        return lits

    def printModel(self):
        s = ""
        for f in self.formulas:
            if isinstance(f, str):
                s += f+" "
            if isinstance(f, Eq):
                s += str(f)+" "
            if isinstance(f, Gt):
                s += str(f)+" "
        return s
    
class Tableau:
    def __init__(self, formulas):
        self.branches = []
        
    def addBranch(self, branch):
        self.branches += [branch]
        
    def unsaturatedBranchExists(self):
        for b in self.branches:
            if not b.isSaturated():
                return True
        return False
        
    def openBranchExists(self):
        for b in self.branches:
            if not b.isClosed():
                return True, b
        return False, None

class SatSolver:

    def satisfiable(self, formulas):
        t = Tableau(formulas)
        t.addBranch(Branch(formulas))
        while t.unsaturatedBranchExists():
            b = None
            for i in t.branches:
                if not i.isClosed() and not i.isSaturated():
                    b = i
                    break
            if b != None:
                while not b.isClosed() and not b.isSaturated():
                    f = b.firstUnexpandedNonForallFormula()
                    if isinstance(f, Not) and isinstance(f.f1, Not):
                        b.unexpanded.remove(f)
                        b.addFormula(f.f1.f1)
                    elif isinstance(f, str):
                        b.unexpanded.remove(f)
                    elif isinstance(f, And):
                        b.unexpanded.remove(f)
                        b.addFormula(f.f1)
                        b.addFormula(f.f2)
                    elif isinstance(f, Not) and isinstance(f.f1, Or):
                        b.unexpanded.remove(f)
                        b.addFormula(Not(f.f1))
                        b.addFormula(Not(f.f2))
                    elif isinstance(f, Or):
                        b.unexpanded.remove(f)
                        b2 = Branch(b.formulas)
                        b2.setUnexpanded(b.unexpanded)
                        b2.setInterventions(b.interventions)
                        b2.addFormula(Not(f.f1))
                        b2.addFormula(f.f2)
                        t.branches += [b2]
                        b.addFormula(f.f1)
                    elif isinstance(f, Not) and isinstance(f.f1, And):
                        b.unexpanded.remove(f)
                        b2 = Branch(b.formulas)
                        b2.setUnexpanded(b.unexpanded)
                        b2.setInterventions(b.interventions)
                        b2.addFormula(f.f1.f1)
                        b2.addFormula(Not(f.f1.f2))
                        t.branches += [b2]
                        b.addFormula(Not(f.f1.f1))
                    elif isinstance(f, Impl):
                        b.unexpanded.remove(f)
                        b.addFormula(Or(Not(f.f1), f.f2))
                    elif isinstance(f, Not) and isinstance(f.f1, Impl):
                        b.unexpanded.remove(f)
                        b.addFormula(f.f1.f1)
                        b.addFormula(Not(f.f1.f2))
                    elif isinstance(f, Causes):
                        b.unexpanded.remove(f)
                        b.addFormula(f.f1)
                        b.addFormula(f.f2)
                        b.addIntervention(f.f1, Formula.getNegation(f.f1))
                        b.addIntervention(f.f1, Formula.getNegation(f.f2))
                    elif isinstance(f, Not) and isinstance(f.f1, Causes):
                        b.unexpanded.remove(f)
                        b.addFormula(Or(Not(f.f1.f1), Not(f.f1.f2)))
                        b2 = Branch(b.formulas)
                        b2.setUnexpanded(b.unexpanded)
                        b2.setInterventions(b.interventions)
                        b2.addIntervention(f.f1.f1, Formula.getNegation(f.f1.f1))
                        b2.addIntervention(f.f1.f1, f.f1.f2)
                    elif isinstance(f, Eq): # Assumes Eq(0, U(c)) or Eq(U(c), 0)
                        b.unexpanded.remove(f)
                        if f.f1 == 0:
                            term = f.f2
                            b.addFormula(Eq(term, 0))
                        else:
                            term = f.f1
                            b.addFormula(Eq(0, term))
                        b.addFormula(Not(Gt(0, term)))
                        b.addFormula(Not(Gt(term, 0)))
                    elif isinstance(f, Not) and isinstance(f.f1, Eq):
                        b.unexpanded.remove(f)
                        if f.f1.f1 == 0:
                            term = f.f1.f2
                        else:
                            term = f.f1.f1
                        b.addFormula(Or(Gt(0, term), Gt(term, 0)))
                    elif isinstance(f, Gt): # Assumes Gt(0, U(c)) or Gt(U(c), 0)
                        b.unexpanded.remove(f)
                        if f.f1 == 0:
                            term = f.f2
                            b.addFormula(And(Not(Eq(0, term)), Not(Gt(term, 0))))
                        else:
                            term = f.f1
                            b.addFormula(And(Not(Eq(0, term)), Not(Gt(0, term))))
                    elif isinstance(f, Not) and isinstance(f.f1, Gt):
                        b.unexpanded.remove(f)
                        if f.f1.f1 == 0:
                            term = f.f1.f2
                            b.addFormula(Or(Gt(term, 0), Eq(0, term)))
                        else:
                            term = f.f1.f1
                            b.addFormula(Or(Gt(0, term), Eq(0, term)))
                    elif isinstance(f, Exists):
                        b.unexpanded.remove(f)
                        b.addFormula(Formula.substituteVariable(f.f1, b.generateNewVariable(), f.f2))
                    elif isinstance(f, Not) and isinstance(f.f1, Exists):
                        b.unexpanded.remove(f)
                        b.addFormula(Forall(f.f1.f1, Not(f.f1.f2)))
                    elif isinstance(f, Not) and isinstance(f.f1, Forall):
                        b.unexpanded.remove(f)
                        b.addFormula(Exists(f.f1.f1, Not(f.f1.f2)))
                    for f in b.unexpanded:
                        if isinstance(f, Forall):
                            for l in b.getAllLiteralsInBranch():
                                b.addFormula(Formula.substituteVariable(f.f1, l, f.f2))
        return t.openBranchExists()
        
        
if __name__ == '__main__':
    f = [Exists("x", Causes("a", "x")), Forall("x", Impl(Causes("a", "x"), Gt(U("x"), 0)))]
    #f = [Not(Not(Causes("a", "a"))), Not(Causes("a", "c"))]    
    s = SatSolver()
    b, br = s.satisfiable(f)
    print(b, None if br is None else br.printModel(), None if br is None else br.interventions)
