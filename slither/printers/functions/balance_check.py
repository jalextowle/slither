"""
    Module printing summary of the contract
"""

from prettytable import PrettyTable
from slither.printers.abstract_printer import AbstractPrinter
from slither.core.declarations.function import Function

class BalanceWritten(AbstractPrinter):

    ARGUMENT = 'balance-written'
    HELP = 'Print the functions that allow arbitrary write-access to a state variable named balance'

    @staticmethod
    def get_msg_sender_checks(function):
        all_functions = function.all_internal_calls() + [function] + function.modifiers

        all_nodes = [f.nodes for f in all_functions if isinstance(f, Function)]
        all_nodes = [item for sublist in all_nodes for item in sublist]

        all_conditional_nodes = [n for n in all_nodes if\
                                 n.contains_if() or n.contains_require_or_assert()]
        all_conditional_nodes_on_msg_sender = [str(n.expression) for n in all_conditional_nodes if\
                                               'msg.sender' in [v.name for v in n.solidity_variables_read]]
        return all_conditional_nodes_on_msg_sender

    def output(self, _filename):
        """
            _filename is not used
            Args:
                _filename(string)
        """

        for contract in self.contracts:
            txt = "\nContract %s\n"%contract.name
            table = PrettyTable(["Function"])
            for function in contract.functions:
                if function.visibility == "public" or function.visibility == "external":
                    msg_sender_condition = self.get_msg_sender_checks(function)
                    if not msg_sender_condition:
                        state_variables_written = [v.name for v in function.all_state_variables_written()]
                        if "balance" in state_variables_written:
                            table.add_row([function.name])
            self.info(txt + str(table))
