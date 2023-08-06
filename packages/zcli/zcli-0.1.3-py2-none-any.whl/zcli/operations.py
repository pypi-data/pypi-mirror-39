import re
import time
from decimal import Decimal


MINCONF = 6
WAIT_INTERVAL = 45


class BadInput (Exception):
    def __init__(self, value, why):
        self.value = value
        self.why = why
        Exception.__init__(self, 'Bad Input {!r}: {}'.format(value, why))


class ZcashOperations (object):
    """Useful operations performed with a ZcashCli."""

    def __init__(self, cli):
        self.cli = cli

    def iter_blocks(self, blockhash=None):
        if blockhash is None:
            blockhash = self.cli.getblockhash(1)

        while blockhash is not None:
            block = self.cli.getblock(blockhash)
            yield block
            blockhash = block.get('nextblockhash')

    def iter_transactions(self, startblockhash=None):
        for block in self.iter_blocks(startblockhash):
            for txid in block['tx']:
                yield (block, self.cli.getrawtransaction(txid, 1))

    def get_taddr_balances(self):
        balances = {}
        for unspent in self.cli.listunspent():
            addr = unspent['address']
            amount = unspent['amount']
            balances[addr] = amount + balances.get(addr, Decimal(0))
        return balances

    def wait(self, ui, opidsandtxids, minconf=MINCONF, interval=WAIT_INTERVAL):
        assert isinstance(opidsandtxids, (list, set)), opidsandtxids

        completedtxids = []
        (opidstatuses, pendingtxids) = \
            self._segregate_opids_and_txids(opidsandtxids)

        while opidstatuses or pendingtxids:
            ui.debug('opidstatuses {!r}', opidstatuses)
            ui.debug('pendingtxids {!r}', pendingtxids)

            ui.status(
                ('Waiting {} seconds for {} incomplete operations '
                 'and {} unconfirmed transactions.'),
                interval,
                len(opidstatuses),
                len(pendingtxids),
            )
            time.sleep(interval)

            (newtxids, opidstatuses) = self._poll_opids(ui, opidstatuses)
            pendingtxids.extend(newtxids)

            (newcompletedtxids, pendingtxids) = \
                self._poll_txids(ui, pendingtxids, minconf)
            completedtxids.extend(newcompletedtxids)

        return completedtxids

    @staticmethod
    def _segregate_opids_and_txids(opidsandtxids):
        rgx = re.compile(
            r'''
              ^(?P<OPID>
                 opid-
                 [0-9a-f]{8}-
                 [0-9a-f]{4}-
                 [0-9a-f]{4}-
                 [0-9a-f]{4}-
                 [0-9a-f]{12}
              )$
            | ^(?P<TXID>
                 [0-9a-f]{64}
              )$
            ''',
            re.VERBOSE | re.IGNORECASE,
        )

        opidstatuses = {}
        txids = []

        for opidortxid in opidsandtxids:
            m = rgx.match(opidortxid)
            if m is None:
                raise BadInput(
                    opidortxid,
                    'Neither an operation id (opid) nor transaction id (txid)',
                )
            else:
                opid = m.group('OPID')
                if opid:
                    opidstatuses[opid] = 'unknown'
                else:
                    txid = m.group('TXID')
                    assert opid is None and txid is not None, \
                        're.match postcondition failure: {!r}'.format(
                            m,
                        )
                    txids.append(txid)

        return (opidstatuses, txids)

    def _poll_opids(self, ui, opidstatuses):
        assert isinstance(opidstatuses, dict), ('precondition', opidstatuses)

        newtxids = []
        remainingopids = {}

        if not opidstatuses:
            return (newtxids, remainingopids)

        for opinfo in self.cli.z_getoperationstatus(opidstatuses.keys()):
            ui.debug('opid status info {!r}', opinfo)

            opid = opinfo['id']
            newstatus = opinfo['status']
            oldstatus = opidstatuses[opid]

            if newstatus != oldstatus:
                ui.status(
                    'Operation {} transition: {!r} -> {!r}',
                    opid,
                    oldstatus,
                    newstatus,
                )

            if newstatus in {'queued', 'executing'}:
                remainingopids[opid] = newstatus
            else:
                # remove the status and check that it didn't change:
                [opinfo2] = self.cli.z_getoperationresult([opid])
                assert opinfo == opinfo2, (opinfo, opinfo2)

                if newstatus == 'success':
                    txid = opinfo['result']['txid']
                    newtxids.append(txid)
                else:
                    ui.handle_failure(
                        'Unexpected status {!r} for OPID {!r}.',
                        newstatus,
                        opid,
                    )

        return (newtxids, remainingopids)

    def _poll_txids(self, ui, txids, minconf):
        completed, pending = [], []

        for txid in txids:
            confs = self.cli.gettransaction(txid)['confirmations']
            ui.debug('txid {!r} confirmations {!r}', txid, confs)

            if confs < 0:
                ui.handle_failure(
                    'Transaction {!r} unconfirmed due to reorg (confs = {}).',
                    txid,
                    confs,
                )
            elif confs < minconf:
                pending.append(txid)
            else:
                completed.append(txid)
                ui.status(
                    'Transaction {!r} final ({} >= {} confirmations)',
                    txid,
                    confs,
                    minconf,
                )

        return completed, pending
