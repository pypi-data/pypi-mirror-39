from decimal import Decimal
from functable import FunctionTable
from zcli.acctab import AccumulatorTable


COMMANDS = FunctionTable()


class BaseCommand (object):
    @staticmethod
    def add_arg_parser(p):
        return

    @staticmethod
    def post_process_args(opts, usage_error):
        return opts


@COMMANDS.register
class list_balances (BaseCommand):
    """List all known address balances."""

    @staticmethod
    def run(_ui, ops):
        balances = AccumulatorTable()

        # Gather t-addr balances:
        for utxo in ops.cli.listunspent():
            if utxo['spendable'] is True:
                balances[utxo['address']] += utxo['amount']

        # Gather t-addr balances:
        for zaddr in ops.cli.z_listaddresses():
            balances[zaddr] = Decimal(
                ops.cli.z_getbalance(zaddr),
            )

        return {
            'total': sum(balances.values()),
            'addresses': dict(
                (k, v)
                for (k, v)
                in balances.iteritems()
                if v > 0
            ),
        }


@COMMANDS.register
class send (BaseCommand):
    """Send from an address to multiple recipients."""

    @staticmethod
    def add_arg_parser(p):
        p.add_argument(
            'SOURCE',
            help='Source address.',
        )

        p.add_argument(
            'DESTINFO',
            nargs='+',
            help='''
                Destination arguments in repeating sequence of: ADDR
                AMOUNT MEMO. A MEMO may start with '0x' in which case
                the rest is considered a hex encoded value. A MEMO may
                start with 's:' in which case the remainder is considered
                a utf8 string. If a MEMO does not start with either, it
                is assumed to be a utf8 string. If the ADDR is a t-addr,
                the MEMO must be the empty string.
            ''',
        )

    @staticmethod
    def post_process_args(opts, usage_error):
        if len(opts.DESTINFO) == 0:
            usage_error('At least one destination must be supplied.')

        elif len(opts.DESTINFO) % 3 != 0:
            usage_error(
                ('DESTINFO must be triplets of ADDR AMOUNT MEMO; '
                 'found {!r} arguments.')
                .format(
                    len(opts.DESTINFO),
                ),
            )

        entries = []

        di = opts.DESTINFO
        for (addr, amount, rawmemo) in zip(di[0::3], di[1::3], di[2::3]):
            entry = {
                'address': addr,
                'amount': Decimal(amount),
            }

            if len(rawmemo) == 0:
                pass
            elif rawmemo.startswith('0x'):
                entry['memo'] = rawmemo[2:]
            else:
                if rawmemo.startswith('s:'):
                    rawmemo = rawmemo[2:]
                entry['memo'] = rawmemo.encode('hex')

            entries.append(entry)

        opts.DESTINFO = entries
        return opts

    @staticmethod
    def run(ui, ops, SOURCE, DESTINFO):
        opid = ops.cli.z_sendmany(SOURCE, DESTINFO)
        return wait.run(ui, ops, OPID=[opid])


@COMMANDS.register
class wait (BaseCommand):
    """Wait until all operations complete and have MINCONF confirmations."""

    @staticmethod
    def add_arg_parser(p):
        p.add_argument(
            'OPID',
            nargs='+',
            help='Operation id.',
        )

    @staticmethod
    def run(ui, ops, OPID):
        return ops.wait(ui, OPID)


@COMMANDS.register
class do (BaseCommand):
    """Run any zcashd RPC method directly."""

    @staticmethod
    def add_arg_parser(p):
        p.add_argument(
            'METHOD',
            help='The RPC method name.',
        )

        p.add_argument(
            'RPCARG',
            nargs='*',
            help='RPC arguments.',
        )

    @staticmethod
    def run(_ui, zo, METHOD, RPCARG):
        method = getattr(zo.cli, METHOD)
        return method(*RPCARG)
