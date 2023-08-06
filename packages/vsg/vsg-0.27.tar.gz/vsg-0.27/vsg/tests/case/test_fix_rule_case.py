import os
import unittest

from vsg.rules import case
from vsg import vhdlFile

# Read in test file used for all tests
oFile = vhdlFile.vhdlFile(os.path.join(os.path.dirname(__file__),'..','case','case_test_input.vhd'))
oFileSequential = vhdlFile.vhdlFile(os.path.join(os.path.dirname(__file__),'..','case','case_sequential_test_input.vhd'))
#oFileComment = vhdlFile.vhdlFile(os.path.join(os.path.dirname(__file__),'..','case','case_comment_test_input.vhd'))

class testFixRuleCaseMethods(unittest.TestCase):

    def test_fix_rule_001(self):
        oRule = case.rule_001()
        dExpected = []
        oRule.fix(oFile)
        oRule.analyze(oFile)
        self.assertEqual(oRule.violations, dExpected)

    def test_fix_rule_002(self):
        oRule = case.rule_002()
        dExpected = []
        oRule.fix(oFile)
        oRule.analyze(oFile)
        self.assertEqual(oRule.violations, dExpected)

    def test_fix_rule_003(self):
        oRule = case.rule_003()
        dExpected = []
        oRule.fix(oFile)
        oRule.analyze(oFile)
        self.assertEqual(oRule.violations, dExpected)

    def test_fix_rule_004(self):
        oRule = case.rule_004()
        dExpected = []
        oRule.fix(oFile)
        oRule.analyze(oFile)
        self.assertEqual(oRule.violations, dExpected)

    def test_fix_rule_005(self):
        oRule = case.rule_005()
        dExpected = []
        oRule.fix(oFile)
        oRule.analyze(oFile)
        self.assertEqual(oRule.violations, dExpected)

    def test_fix_rule_006(self):
        oRule = case.rule_006()
        dExpected = []
        oRule.fix(oFile)
        oRule.analyze(oFile)
        self.assertEqual(oRule.violations, dExpected)

    def test_fix_rule_007(self):
        oRule = case.rule_007()
        dExpected = []
        oRule.fix(oFile)
        oRule.analyze(oFile)
        self.assertEqual(oRule.violations, dExpected)

    def test_fix_rule_008(self):
        oRule = case.rule_008()
        dExpected = []
        oRule.fix(oFile)
        oRule.analyze(oFile)
        self.assertEqual(oRule.violations, dExpected)

    def test_fix_rule_009(self):
        oRule = case.rule_009()
        dExpected = []
        oRule.fix(oFile)
        oRule.analyze(oFile)
        self.assertEqual(oRule.violations, dExpected)

    def test_fix_rule_010(self):
        oRule = case.rule_010()
        dExpected = []
        oRule.fix(oFile)
        oRule.analyze(oFile)
        self.assertEqual(oRule.violations, dExpected)

    def test_fix_rule_011(self):
        oRule = case.rule_011()
        dExpected = []
        oRule.fix(oFile)
        oRule.analyze(oFile)
        self.assertEqual(oRule.violations, dExpected)

    def test_fix_rule_012(self):
        oRule = case.rule_012()
        self.assertEqual(oFileSequential.lines[11].isSequential,False)
        self.assertEqual(oFileSequential.lines[11].indentLevel,3)
        dExpected = []
        oRule.fix(oFileSequential)
        oRule.analyze(oFileSequential)
        self.assertEqual(oRule.violations, dExpected)
        self.assertEqual(oFileSequential.lines[11].line,'      when 0 =>')
        self.assertEqual(oFileSequential.lines[11].indentLevel,3)
        self.assertEqual(oFileSequential.lines[12].line,' b <= \'0\';')
        self.assertEqual(oFileSequential.lines[12].indentLevel, oFileSequential.lines[11].indentLevel + 1)
        self.assertEqual(oFileSequential.lines[12].isSequential, True)
        self.assertEqual(oFileSequential.lines[12].insideCaseWhen, False)
        self.assertEqual(oFileSequential.lines[13].line,'      when 1 =>')

        self.assertEqual(oFileSequential.lines[25].line,'      when 0 =>')
        self.assertEqual(oFileSequential.lines[25].hasComment, False)
        self.assertEqual(oFileSequential.lines[25].hasInlineComment, False)
        self.assertEqual(oFileSequential.lines[25].commentColumn, None)
        self.assertEqual(oFileSequential.lines[26].line,' b <= \'1\'; -- Comment')
        self.assertEqual(oFileSequential.lines[26].hasComment, True)
        self.assertEqual(oFileSequential.lines[26].hasInlineComment, True)
        self.assertEqual(oFileSequential.lines[26].commentColumn, 11)
        self.assertEqual(oFileSequential.lines[27].line,'      when others =>')
        self.assertEqual(oFileSequential.lines[28].line,' null;')
        self.assertEqual(oFileSequential.lines[28].insideSequential, False)
        self.assertEqual(oFileSequential.lines[28].isSequentialEnd, False)
        self.assertEqual(oFileSequential.lines[28].isSequential, False)
        self.assertEqual(oFileSequential.lines[28].sequentialAlignmentColumn, None)

    def test_fix_rule_013(self):
        oRule = case.rule_013()
        dExpected = []
        oRule.fix(oFile)
        oRule.analyze(oFile)
        self.assertEqual(oRule.violations, dExpected)

    def test_fix_rule_014(self):
        oRule = case.rule_014()
        dExpected = []
        oRule.fix(oFile)
        oRule.analyze(oFile)
        self.assertEqual(oRule.violations, dExpected)
        self.assertEqual(oFile.lines[43].line, '    case boolean_1 or')

    def test_fix_rule_015(self):
        oRule = case.rule_015()
        dExpected = []
        oRule.fix(oFile)
        oRule.analyze(oFile)
        self.assertEqual(oRule.violations, dExpected)
        self.assertEqual(oFile.lines[45].line, '   boolean_3 is')

    def test_fix_rule_016(self):
        oRule = case.rule_016()
        dExpected = []
        oRule.fix(oFile)
        oRule.analyze(oFile)
        self.assertEqual(oRule.violations, dExpected)
        self.assertEqual(oFile.lines[48].line, '      when STATE_1 or')
        self.assertEqual(oFile.lines[55].line, '      when STATE_2 =>')
        self.assertEqual(oFile.lines[61].line, '      when STATE_3 or')
 
    def test_fix_rule_017(self):
        oRule = case.rule_017()
        dExpected = []
        oRule.fix(oFile)
        oRule.analyze(oFile)
        self.assertEqual(oRule.violations, dExpected)
        self.assertEqual(oFile.lines[83].line, '    end case;') 
