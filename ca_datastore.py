#!bin/python3
# coding=utf-8

'''
Load Cellular Automaton information from external storage
'''

import subprocess
# import defusedxml.sax
from commontools import constant
from commontools import XmlLintChecker
from defusedxml import defuse_stdlib


class CellularAutomatonLoader:
    """
    Load Cellular Automaton information from external storage
    """

    # This is to handle xml format information, as well as some simpler structures

    # pylint: disable=invalid-name,missing-docstring,no-method-argument,multiple-statements
    @constant
    def BLOCKSIZE(): return 65536  # buffer size for processing files
    @constant
    def DTDVALIDATION(): return ['xmllint', '--noout', '--nonet', '--nocatalogs', '--dtdvalid']
    # Other options can be modified or inserted, but the final option MUST be
    # '--dtdvalid', to allow the code to append the dtd file specification
    #  '--load-trace'. '--nonet', '--nocatalogs', '--noout', '--recover'
    #  '--relaxng', «schema»
    #  '--schema', «schema»
    @constant
    def SCHEMAVALIDATION(): return ['xmllint', '--noout', '--nonet', '--nocatalogs', '--schema']
    # pylint: enable=invalid-name,missing-docstring,no-method-argument,multiple-statements

    def __init__(self, file=None):
        # monkey patch to attempt to block [maliciously] malformed xml from causing bomb problems
        defuse_stdlib()
        self.xml_lint_checker = XmlLintChecker()

    # end def __init__(…)

    def validate_against_external_dtd(self, file, dtd):
        '''check for valid xml data structure according to external dtd'''
        lint_cmd = self.DTDVALIDATION + [dtd] + [file]
        rslt = subprocess.run(lint_cmd, stderr=subprocess.PIPE)
        # Found that stderr might not be empty even when returncode is 0.  The
        # example case was an error in the xmlns uri.  Dtd said it was valid,
        # but ?basic? xml disagrees (leading zero before http)

        return self.xml_lint_checker.parse(rslt)

    def validate_against_schema(self, file, sch):
        '''check for valid xml data structure according to external schema'''
        print('validate_against_schema lint command')  # TRACE
        lint_cmd = self.SCHEMAVALIDATION + [sch] + [file]
        rslt = subprocess.run(lint_cmd, stderr=subprocess.PIPE)
        is_valid = self.xml_lint_checker.parse(rslt)
        print('end validate_against_schema')  # TRACE
        return is_valid
# end class CellularAutomatonLoader


def mymain():
    '''wrapper for test/start code so that variables do not look like constants'''
    # exercise / demo class functionality
    print('Exercising CellularAutomatonLoader class')

    ca_ldr = CellularAutomatonLoader()
    # ca_ldr = CellularAutomatonLoader(file="conway.xml")
    # err_file = 'a'
    # tst_file = 'conway.xml'
    tst_file = 'ca.xml'
    # err_validator = 'b'

    # # r = ca_ldr.validate_against_external_dtd(err_file, err_validator)
    # # r = ca_ldr.validate_against_external_dtd(tst_file, err_validator)
    # r = ca_ldr.validate_against_external_dtd(tst_file, 'ca.dtd')
    # print('')
    # msg = r['message']
    # if msg == b'' and r['state'] == 'valid':
    #     msg = b'xml file is valid for the specified dtd\n'
    # rpt_msg =  msg.decode("utf-8") if type(msg) == type(b'') else msg
    # print('The validation by dtd state is "{}", and the message is\n{}'.format(
    #     r['state'], rpt_msg))

    # r = ca_ldr.validate_against_schema(err_file, err_validator)
    # r = ca_ldr.validate_against_schema('a', 'ca.xsd')
    xsd_rslt = ca_ldr.validate_against_schema(tst_file, 'ca.xsd')
    # xsd_rslt = ca_ldr.validate_against_schema(tst_file, 'ca1.xsd')
    print('')
    msg = xsd_rslt['message']
    if msg == b'' and xsd_rslt['state'] == 'valid':
        msg = b'xml file is valid for the specified schema\n'
    rpt_msg = msg.decode("utf-8") if isinstance(msg, bytes) else msg
    print('The validation by schema state is "{}", and the message is\n{}'.format(
        xsd_rslt['state'], rpt_msg))

    print('Done exercising CellularAutomatonLoader class')


# Standalone module execution
if __name__ == "__main__":
    mymain()
