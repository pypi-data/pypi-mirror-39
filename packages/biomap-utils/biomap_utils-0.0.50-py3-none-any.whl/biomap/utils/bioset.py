'''
http://software.broadinstitute.org/cancer/software/gsea/wiki/index.php/Data_formats
'''

import os

class BioSetTypeException(Exception):
    pass

class BioSet(set):
    def __init__(self, name, genes, description='', metadata=None):
        # the name of the geneset
        if not isinstance(name, str):
            raise BioSetTypeException('GeneSet name need to be a string.')
        self.name = name
        # the gene set
        for gene in genes:
            if not isinstance(gene, str):
                raise BioSetTypeException('Gene ids must be strings.')
        super().__init__(genes)
        # a description
        if not isinstance(description, str):
            raise BioSetTypeException('GeneSet description must be a string.')
        self.description = description
        # arbitrary metadata
        self.metadata = metadata

    def __hash__(self):
        return hash(self.name)

    def __and__(self, other):
        name = self.name+'_AND_'+other.name
        genes = self.intersection(other)
        return BioSet(name, *genes)

    @classmethod
    def from_grp(cls, path, name=None, description='', metadata=None):
        if not name:
            name = os.path.basename(path).split('.')[0]
        with open(path, 'r') as grpf:
            genes = {line.strip() for line in grpf if line[0] != '#'}
        return cls(name=name, genes=genes, description=description, metadata=metadata)

    def to_grp(self, path, comment_header=None):
        if len(self) == 0:
            return None
        with open(path, 'w') as grpf:
            if comment_header:
                grpf.write('# '+comment_header+'\n')
            for gene in self:
                grpf.write(gene+'\n')

    def map(self, id_mapper, FROM, TO, inplace=True):
        if len(self) == 0:
            return None
        mapped_ids = id_mapper.map(list(self), FROM, TO)
        if TO in id_mapper.definition['list_valued_keys']:
            mapped_ids = [lst for lst in mapped_ids if lst]
            mapped_ids = {ID for IDlist in mapped_ids for ID in IDlist if IDlist}
        mapped_ids = set(mapped_ids)
        if inplace:
            former_IDs = [ID for ID in self]
            for ID in former_IDs:
                self.remove(ID)   # bad
            for ID in mapped_ids:
                self.add(ID)
        else:
            return BioSet(name=self.name,
                          genes=mapped_ids,
                          description=self.description,
                          metadata=self.metadata)

    @classmethod
    def from_gmt(cls, name, gmtpath, comment='#', metadata=None):
        with open(path, 'r') as gmtf:
            for line in gmtf:
                if line[0] == comment:
                    continue
                line.strip()
                data = line.split('\t')
                name_here = data[0]
                if name != name_here:
                    continue
                description = data[1]
                genes = data[2:-1]
                genes = { gene for gene in genes if len(gene) > 0 }
                return cls(name=name,
                           genes=genes,
                           description=description,
                           metadata=metadata)
        print('A gene set of name %s is not contained in %s.' % (name, gmtpath))
        return None


class BioSetCollection(dict):
    def __init__(self, name, *biosets):
        self.name = name
        super().__init__( {bs.name: bs for bs in biosets} )

    @property
    def min_len(self):
        return min(len(bs) for _, bs in self.items())

    @property
    def max_len(self):
        return max(len(bs) for _, bs in self.items())

    @property
    def avg_len(self):
        return sum(len(bs) for _, bs in self.items()) / len(self)

    @classmethod
    def from_gmt(cls, path, name=None, comment='#'):
        with open(path, 'r') as gmtf:
            biosets = set()
            for line in gmtf:
                if line[0] == comment:
                    continue
                line.strip()
                data = line.split('\t')
                name = data[0]
                description = data[1]
                genes = data[2:]
                genes = { gene.strip() for gene in genes if len(gene) > 0 }
                biosets.add( BioSet(name=name,
                                    genes=genes,
                                    description=description,
                                    metadata={'from_gmt':path}) )
        if name is None:
            name = path
        return cls(name, *biosets)

    @classmethod
    def generator_from_gmt(cls, path, comment='#'):
        pass

    def to_gmt(self, path):
        if len(self) == 0:
            return None
        with open(path, 'w') as gmtf:
            for name, geneset in self.items():
                esc = '\n' if not geneset else '\t'
                gmtf.write(name+'\t')
                gmtf.write(geneset.description+esc)
                for gene in geneset:
                    gmtf.write('\t'+gene)
                if geneset:
                    gmtf.write('\n')

    @classmethod
    def from_gmx(cls, path, name=None):
        with open(path, 'r') as gmxf:
            names = [name.strip() for name in gmxf.readline().split('\t')]
            descriptions = [desc.strip() for desc in gmxf.readline().split('\t')]
            rows = [[gene.strip() for gene in line.split('\t')] for line in gmxf]
            genes = [{row[i] for row in rows
                             if i < len(row) and row[i] != ''}
                     for i in range(len(names))]
            genesets = { GeneSet(names[i], gs, descriptions[i]) for i, gs in enumerate(genes) }
        if name is None:
            name = path
        return cls(name, *genesets)

    @classmethod
    def generator_from_gmx(cls, path):
        pass

    def to_gmx(self, path):

        def write_header(gmxf, genesets):
            gmxf.write(genesets[0].name)
            for geneset in genesets[1:]:
                gmxf.write('\t'+geneset.name)
            gmxf.write('\n')

        def write_descriptions(self, gmxf, genesets):
            descriptions = [gs.description for gs in genesets]
            gmxf.write(descriptions[0])
            for desc in descriptions[1:]:
                gmxf.write('\t'+desc)
            gmxf.write('\n')

        def write_genes(self, gmxf, genesets):
            max_len = self.max_len
            gmx_data = [list(gs) + (max_len-len(gs))*[''] for gs in genesets]
            for i in range(max_len):
                gmxf.write(gmx_data[0][i])
                for j in range(1,len(self)):
                    gmxf.write('\t'+gmx_data[j][i])
                gmxf.write('\n')

        if len(self) == 0:
            return None
        with open(path, 'w') as gmxf:
            genesets = [gs for _, gs in self.items()]
            write_header(gmxf, genesets)
            write_descriptions(self, gmxf, genesets)
            write_genes(self, gmxf, genesets)

    @classmethod
    def from_grp(cls, path, name=None, description='', coll_name='', metadata=None):
        if coll_name is None:
            coll_name = path
        return cls( coll_name, BioSet.from_grp(path, name, description, metadata) )

    def to_grp(self, path, name, comment_header=None):
        self[name].to_grp(path, comment_header)

    def map(self, id_mapper, FROM, TO, inplace=True):
        if inplace:
            self.map_inplace(id_mapper, FROM, TO)
        else:
            return self.map_not_inplace(id_mapper, FROM, TO)

    def map_inplace(self, id_mapper, FROM, TO):
        for _, geneset in self.items():
            geneset.map(id_mapper, FROM, TO, inplace=True)

    def map_not_inplace(self, id_mapper, FROM, TO):
        genesets = {gs.map(id_mapper, FROM, TO, inplace=False) for _, gs in self.items()}
        return BioSetCollection(*genesets)

    def union(self, genesets):
        union = set()
        return BioSet('union', union.union(*[self[name] for name in genesets]))
