#!/usr/bin/env python3
"""Deterministic EXP-0002 FASTA normalization under frozen LIFE-CODE rules."""
from pathlib import Path
import argparse,hashlib,json,re
RUN=re.compile(rb"[ACGTacgt]+")
def sha256(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()
def normalize(raw_path,out_fasta,out_map,out_report):
 raw_path=Path(raw_path).resolve();out_fasta=Path(out_fasta).resolve();out_map=Path(out_map).resolve();out_report=Path(out_report).resolve()
 out_fasta.parent.mkdir(parents=True,exist_ok=True);out_map.parent.mkdir(parents=True,exist_ok=True);out_report.parent.mkdir(parents=True,exist_ok=True)
 source_records=source_chars=acgt=amb=segments=0
 record_index=0;record_token=None;record_pos=0;seg_start=None;seg=bytearray()
 with open(raw_path,'rb') as src, open(out_fasta,'wb') as fa, open(out_map,'w',encoding='utf-8',newline='') as mp:
  mp.write('segment_id\tsource_record_index\tsource_record_token\tstart0\tend0\tlength\n')
  def flush():
   nonlocal segments,seg_start,seg,acgt
   if not seg: seg_start=None; return
   segments+=1;sid=f'LCSEG{segments:012d}';end0=seg_start+len(seg)
   fa.write(f'>{sid}\n'.encode('ascii'));fa.write(seg);fa.write(b'\n')
   tok=(record_token or f'RECORD_{record_index}').replace('\t',' ')
   mp.write(f'{sid}\t{record_index}\t{tok}\t{seg_start}\t{end0}\t{len(seg)}\n')
   acgt+=len(seg);seg=bytearray();seg_start=None
  for raw_line in src:
   if raw_line.startswith(b'>'):
    flush();source_records+=1;record_index=source_records
    h=raw_line[1:].strip();t=h.split(None,1)[0] if h else f'RECORD_{record_index}'.encode()
    record_token=t.decode('utf-8','replace');record_pos=0;continue
   if record_index==0:
    if raw_line.strip(): raise RuntimeError('sequence before first FASTA header')
    continue
   line=raw_line.strip()
   if not line: continue
   source_chars+=len(line);cursor=0
   for m in RUN.finditer(line):
    if m.start()>cursor: flush();amb+=m.start()-cursor
    s=m.group(0).upper()
    if seg_start is None: seg_start=record_pos+m.start()
    seg.extend(s);cursor=m.end()
   if cursor<len(line): flush();amb+=len(line)-cursor
   record_pos+=len(line)
  flush()
 if source_records==0: raise RuntimeError('no FASTA records')
 if acgt+amb!=source_chars: raise RuntimeError('normalization accounting mismatch')
 if segments==0: raise RuntimeError('zero normalized segments')
 report={'normalization_semantics':'uppercase_split_at_every_non_ACGT_preserve_source_record_and_coordinates','output_fasta_representation':'two_physical_lines_per_normalized_segment','raw_fasta_path':str(raw_path),'raw_fasta_sha256':sha256(raw_path),'normalized_fasta_path':str(out_fasta),'normalized_fasta_sha256':sha256(out_fasta),'coordinate_map_path':str(out_map),'coordinate_map_sha256':sha256(out_map),'source_record_count':source_records,'source_sequence_characters':source_chars,'source_acgt_bases':acgt,'source_ambiguous_bases':amb,'normalized_segment_count':segments,'normalized_acgt_bases':acgt,'invariants':{'all_source_sequence_characters_accounted':True,'all_ACGT_bases_retained':True,'no_non_ACGT_base_in_analysis_segments':True,'no_cross_ambiguity_exact_word_possible':True}}
 out_report.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');return report
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--raw',required=True);ap.add_argument('--out-fasta',required=True);ap.add_argument('--out-map',required=True);ap.add_argument('--out-report',required=True);a=ap.parse_args()
 print(json.dumps(normalize(a.raw,a.out_fasta,a.out_map,a.out_report),indent=2))
if __name__=='__main__':main()
