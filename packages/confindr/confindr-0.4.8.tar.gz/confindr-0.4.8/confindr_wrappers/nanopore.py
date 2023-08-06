#!/usr/bin/env python

from Bio import pairwise2
import pysam


class ReadInfo:
    def __init__(self, read_name, align_start, align_end):
        self.read_name = read_name
        self.align_start = int(align_start)
        self.align_end = int(align_end)
        assert self.align_end > self.align_start


def get_reads_aligned_to_gene(bam_file, gene_name):
    read_info = list()
    bamfile = pysam.AlignmentFile(bam_file, 'rb')
    reads_aligned = bamfile.fetch(contig=gene_name)
    for read in reads_aligned:
        x = ReadInfo(read.query_name, read.query_alignment_start, read.query_alignment_end)
        read_info.append(x)
    return read_info


def get_overhang_regions(read_info_list, index):
    # TODO: Handle gzipped files
    start_sequences = list()
    end_sequences = list()
    for read_info in read_info_list:
        start_seq = index[read_info.read_name].seq[read_info.align_start - 2000:read_info.align_start - 1000]
        end_seq = index[read_info.read_name].seq[read_info.align_end + 1000:read_info.align_end + 2000]
        start_sequences.append(start_seq)
        end_sequences.append(end_seq)
    return start_sequences, end_sequences


def get_rmlst_regions(read_info_list, index):
    # TODO: Handle gzipped files
    sequences = list()
    for read_info in read_info_list:
        seq = index[read_info.read_name].seq[read_info.align_start:read_info.align_end]
        sequences.append(seq)
    return sequences


def find_percent_id(sequence_list):
    percent_id_list = list()
    for i in range(len(sequence_list)):
        for j in range(i, len(sequence_list)):
            if i != j:
                num_identities = pairwise2.align.globalxx(sequence_list[i], sequence_list[j], score_only=True)
                sequence_length = min(len(sequence_list[i]), len(sequence_list[j]))
                if num_identities:
                    percent_id = 100.0 * num_identities/sequence_length
                    percent_id_list.append(percent_id)
    return percent_id_list


