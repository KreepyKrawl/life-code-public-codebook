#!/usr/bin/env python3
import hashlib, random

BIO_MAPS = {
    'RY': {'A':'A','G':'A','C':'C','T':'C'},
    'MK': {'A':'A','C':'A','G':'C','T':'C'},
    'WS': {'A':'A','T':'A','C':'C','G':'C'},
}

CONTROL_TUPLES = {
    'C01': ('RY','RY','MK','MK'),
    'C02': ('RY','WS','RY','MK'),
    'C03': ('MK','MK','MK','RY'),
    'C04': ('RY','WS','MK','RY'),
    'C05': ('MK','RY','MK','WS'),
    'C06': ('MK','MK','WS','RY'),
    'C07': ('MK','MK','MK','WS'),
    'C08': ('WS','MK','WS','RY'),
    'C09': ('RY','MK','WS','WS'),
    'C10': ('RY','MK','MK','WS'),
    'C11': ('WS','WS','RY','WS'),
    'C12': ('RY','MK','MK','RY'),
}
STATE_INDEX={'A':0,'C':1,'G':2,'T':3}
DNA_COMP=str.maketrans('ACGT','TGCA')


def seed64(representation, triad_id, fold, replicate):
    s=f'LIFE_CODE|EXP-0003|N1|{representation}|{triad_id}|{fold}|{replicate}'
    return int(hashlib.sha256(s.encode('utf-8')).hexdigest()[:16],16)


def reverse_complement(seq):
    s=seq.upper()
    if set(s)-set('ACGT'):
        raise ValueError('reverse complement input must be ACGT only')
    return s.translate(DNA_COMP)[::-1]


def project_sequence(seq, representation):
    seq=seq.upper()
    if set(seq)-set('ACGT'):
        raise ValueError('projection input must be ACGT only')
    if representation=='ACGT':
        return seq
    if representation in BIO_MAPS:
        m=BIO_MAPS[representation]
        return ''.join(m[b] for b in seq)
    if representation in CONTROL_TUPLES:
        maps=CONTROL_TUPLES[representation]
        prev='A'
        out=[]
        for b in seq:
            active=BIO_MAPS[maps[STATE_INDEX[prev]]]
            out.append(active[b])
            prev=b
        return ''.join(out)
    raise ValueError(f'unknown representation: {representation}')


def fit_first_order(seq):
    if not seq:
        raise ValueError('empty sequence')
    alphabet=tuple(sorted(set(seq)))
    start={a:0 for a in alphabet}
    start[seq[0]]+=1
    transitions={a:{b:0 for b in alphabet} for a in alphabet}
    for a,b in zip(seq,seq[1:]):
        transitions[a][b]+=1
    return alphabet,start,transitions


def _draw(rng, counts, alphabet):
    total=sum(counts.get(a,0) for a in alphabet)
    if total<=0:
        return alphabet[rng.randrange(len(alphabet))]
    x=rng.randrange(total)
    acc=0
    for a in alphabet:
        acc+=counts.get(a,0)
        if x<acc:return a
    return alphabet[-1]


def generate_n1(seq, seed):
    alphabet,start,transitions=fit_first_order(seq)
    rng=random.Random(seed)
    first=_draw(rng,start,alphabet)
    out=[first]
    while len(out)<len(seq):
        prev=out[-1]
        out.append(_draw(rng,transitions.get(prev,{}),alphabet))
    return ''.join(out)


def iter_fasta(path):
    name=None; chunks=[]
    with open(path,encoding='ascii') as f:
        for raw in f:
            line=raw.strip()
            if not line: continue
            if line.startswith('>'):
                if name is not None: yield name,''.join(chunks).upper()
                name=line[1:].split()[0]; chunks=[]
            else: chunks.append(line)
    if name is not None: yield name,''.join(chunks).upper()


def write_projected_fasta(inp,out,representation):
    with open(out,'w',encoding='ascii',newline='\n') as dst:
        for name,seq in iter_fasta(inp):
            dst.write(f'>{name}\n{project_sequence(seq,representation)}\n')


def _record_subseed(cell_seed,name,record_index,orientation=None):
    suffix=f'{name}|{record_index}' if orientation is None else f'{name}|{record_index}|{orientation}'
    return cell_seed ^ int(hashlib.sha256(suffix.encode('utf-8')).hexdigest()[:16],16)


def write_n1_fasta(inp,out,representation,triad_id,fold,replicate):
    with open(out,'w',encoding='ascii',newline='\n') as dst:
        for record_index,(name,raw_seq) in enumerate(iter_fasta(inp)):
            projected=project_sequence(raw_seq,representation)
            cell_seed=seed64(representation,triad_id,fold,replicate)
            record_seed=_record_subseed(cell_seed,name,record_index)
            null=generate_n1(projected,record_seed)
            dst.write(f'>{name}\n{null}\n')


def write_oriented_projected_fasta(inp,out,representation,orientation):
    if orientation not in ('FWD','RC'):
        raise ValueError('orientation must be FWD or RC')
    with open(out,'w',encoding='ascii',newline='\n') as dst:
        for name,raw_seq in iter_fasta(inp):
            oriented=raw_seq if orientation=='FWD' else reverse_complement(raw_seq)
            projected=project_sequence(oriented,representation)
            dst.write(f'>{name}|{orientation}\n{projected}\n')


def write_oriented_n1_fasta(inp,out,representation,triad_id,fold,replicate,orientation):
    if orientation not in ('FWD','RC'):
        raise ValueError('orientation must be FWD or RC')
    cell_seed=seed64(representation,triad_id,fold,replicate)
    with open(out,'w',encoding='ascii',newline='\n') as dst:
        for record_index,(name,raw_seq) in enumerate(iter_fasta(inp)):
            oriented=raw_seq if orientation=='FWD' else reverse_complement(raw_seq)
            projected=project_sequence(oriented,representation)
            record_seed=_record_subseed(cell_seed,name,record_index,orientation)
            null=generate_n1(projected,record_seed)
            dst.write(f'>{name}|{orientation}\n{null}\n')
