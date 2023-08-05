from contextlib import ExitStack

import bgdata
import bgpack
import tabix

from bgvep.globals import BGVEPError
from bgvep.maps import SEQUENCE_NAME_MAPS


class ReaderError(BGVEPError):
    pass


class Tabix:

    def __init__(self, genome, vep_build):
        self.file = bgdata.get_path('vep', 'wgs_tabix', '{}_{}'.format(genome, vep_build))
        self.tb = None
        self.map = SEQUENCE_NAME_MAPS.get(genome, {})

    def __enter__(self):
        self.tb = tabix.open(self.file)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return True

    def get(self, chromosome, start, stop):
        chr_ = self.map.get(chromosome, chromosome)
        try:
            for row in self.tb.query("{}".format(chr_), start, stop):
                yield row
        except tabix.TabixError:
            raise ReaderError('Tabix error in {}: {}-{}'.format(chromosome, start, stop))


class BGPack(ExitStack):

    def __init__(self, genome, vep_build):
        super().__init__()
        name = bgdata.get_path('vep', 'mostsevere', '{}_{}'.format(genome, vep_build))
        self.reader = bgpack.get_unpacker(name)
        self.ctx = None
        self.map = SEQUENCE_NAME_MAPS.get(genome, {})

    def __enter__(self):
        super().__enter__()
        self.ctx = self.enter_context(self.reader)
        return self

    def get(self, chromosome, start, stop):
        chr_ = self.map.get(chromosome, chromosome)
        yield from self.ctx.get(chr_, start, stop)
