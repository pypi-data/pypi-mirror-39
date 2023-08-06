#!/usr/bin/env python3
 
#Author: Erik Bergstrom

#Contact: ebergstr@eng.ucsd.edu

import os
import sys
import re



def convertVCF (project, vcf_path, genome, output_path):
	files = os.listdir(vcf_path)
	first_indel = True
	first_SNV = True

	snv = False
	indel = False
	first_incorrect_file = True
	for file in files:
		file_name = file.split(".")
		sample = file_name[0]
		if file == '.DS_Store':
			continue
		with open (vcf_path + file) as f:
			for lines in f:
				if lines[0] == "#":
					continue
				else:
					try:
						line = lines.strip().split('\t')
						chrom = line[0]
						if len(chrom) > 2:
							chrom = chrom[3:]
						start = line[1]
						ref = line[3]
						mut = line[4]
						int(start)
					except:
						if first_incorrect_file:
							print("The given input files do not appear to be in the correct vcf format. Skipping this file: ", file)
							first_incorrect_file = False
						continue

					if len(ref) == 1 and len(mut) == 1 and ref != "-" and ref != "-":
						snv = True
						if first_SNV:
							outputFile = output_path + "SNV/" + project + ".genome"
							os.system("rm -f " + outputFile)
							if not os.path.exists(output_path + "SNV/"):
								os.mkdir(output_path + 'SNV/')
							out_snv = open(outputFile, "w") 
							first_SNV = False

						print("\t".join([project, sample, ".", genome, "SNV", chrom, start, start, ref, mut, "SOMATIC"]), file=out_snv)

					else:
						indel = True
						if first_indel:
							outputFile = output_path + "INDEL/" + project + ".genome"
							os.system("rm -f " + outputFile)
							if not os.path.exists(output_path + "INDEL/"):
								os.mkdir(output_path + "INDEL/")
							out_indel = open(outputFile, "w") 
							first_indel = False

						print("\t".join([project, sample, ".", genome, "INDEL", chrom, start, start, ref, mut, "SOMATIC"]), file=out_indel)

		first_incorrect_file = True


	out_snv.close()
	out_indel.close()
	return(snv, indel)


def convertTxt (project, vcf_path, genome, output_path):
	files = os.listdir(vcf_path)
	first_indel = True
	first_SNV = True	

	snv = False
	indel = False
	first_incorrect_file = True
	for file in files:
		if file == '.DS_Store':
			continue
		with open (vcf_path + file) as f:
			for lines in f:
				try:
					line = lines.strip().split('\t')
					sample = line[1]
					genome = line[3]
					chrom = line[5]
					if len(chrom) > 2:
						chrom = chrom[3:]
					start = line[6]
					end = line[7]
					ref = line[8]
					mut = line[9]
					int(start)
					int(end)
				except:
					if first_incorrect_file:
						print("The given input files do not appear to be in the correct simple text format. Skipping this file: ", file)
						first_incorrect_file = False
					continue

				if len(ref) == 1 and len(mut) == 1 and ref != "-" and ref != "-":
					snv = True
					if first_SNV:
						outputFile = output_path + "SNV/" + project + ".genome"
						os.system("rm -f " + outputFile)
						if not os.path.exists(output_path + "SNV/"):
							os.mkdir(output_path + 'SNV/')
						out_snv = open(outputFile, "w") 
						first_SNV = False

					print("\t".join([project, sample, ".", genome, "SNV", chrom, start, start, ref, mut, "SOMATIC"]), file=out_snv)
				
				else:
					indel = True
					if first_indel:
						outputFile = output_path + "INDEL/" + project + ".genome"
						os.system("rm -f " + outputFile)
						if not os.path.exists(output_path + "INDEL/"):
							os.mkdir(output_path + "INDEL/")
						out_indel = open(outputFile, "w") 
						first_indel = False

					print("\t".join([project, sample, ".", genome, "INDEL", chrom, start, start, ref, mut, "SOMATIC"]), file=out_indel)

		first_incorrect_file = True

	out_snv.close()
	out_indel.close()
	return(snv, indel)

def convertMAF (project, vcf_path, genome, output_path):
	files = os.listdir(vcf_path)
	first_indel = True
	first_SNV = True	

	snv = False
	indel = False
	first_incorrect_file = True
	for file in files:
		if file == '.DS_Store':
			continue
		name = file.split(".")
		sample = name[0]
		with open (vcf_path + file) as f:
			for lines in f:
				try:
					line = lines.strip().split('\t')
					genome = line[3]
					chrom = line[4]
					if len(chrom) > 2:
						chrom = chrom[3:]
					start = line[5]
					end = line[6]
					ref = line[10]
					mut = line[47]
					int(start)
					int(end)
				except:
					if first_incorrect_file:
						print("The given input files do not appear to be in the correct MAF format. Skipping this file: ", file)
						first_incorrect_file = False
					continue
				if len(ref) == 1 and len(mut) == 1 and ref != "-" and ref != "-":
					snv = True
					if first_SNV:
						outputFile = output_path + "SNV/" + project + ".genome"
						os.system("rm -f " + outputFile)
						if not os.path.exists(output_path + "SNV/"):
							os.mkdir(output_path + 'SNV/')
						out_snv = open(outputFile, "w") 
						first_SNV = False

					print("\t".join([project, sample, ".", genome, "SNV", chrom, start, start, ref, mut, "SOMATIC"]), file=out_snv)
				
				else:
					indel = True
					if first_indel:
						outputFile = output_path + "INDEL/" + project + ".genome"
						os.system("rm -f " + outputFile)
						if not os.path.exists(output_path + "INDEL/"):
							os.mkdir(output_path + "INDEL/")
						out_indel = open(outputFile, "w") 
						first_indel = False

					print("\t".join([project, sample, ".", genome, "INDEL", chrom, start, start, ref, mut, "SOMATIC"]), file=out_indel)

		first_incorrect_file = True

	out_snv.close()
	out_indel.close()
	return(snv, indel)


def convertICGC (project, vcf_path, genome, output_path):
	files = os.listdir(vcf_path)
	first_indel = True
	first_SNV = True	

	snv = False
	indel = False
	first_incorrect_file = True
	for file in files:
		if file == '.DS_Store':
			continue
		with open (vcf_path + file) as f:
			for lines in f:
				try:
					line = lines.strip().split('\t')
					sample = line[1]
					icgc_sample_id = line[4]
					chrom = line[8]
					if len(chrom) > 2:
						chrom = chrom[3:]
					start = int(line[9])
					end = line[10]
					genome = line[12]
					ref = line[15]
					mut = line[16]
					if ref == '-':
						mut = '-' + mut
					elif mut == '-':
						start -= 1
						ref = '-' + ref
					int(start)
					int(end)
				except:
					if first_incorrect_file:
						print("The given input files do not appear to be in the correct ICGC format.")
						first_incorrect_file = False
					continue

				if len(ref) == 1 and len(mut) == 1 and ref != "-" and ref != "-":
					snv = True
					if first_SNV:
						outputFile = output_path + "SNV/" + project + ".genome"
						os.system("rm -f " + outputFile)
						if not os.path.exists(output_path + "SNV/"):
							os.mkdir(output_path + 'SNV/')
						out_snv = open(outputFile, "w") 
						first_SNV = False

					print("\t".join([project, sample, ".", genome, "SNV", chrom, start, start, ref, mut, "SOMATIC"]), file=out_snv)
				
				else:
					indel = True
					if first_indel:
						outputFile = output_path + "INDEL/" + project + ".genome"
						os.system("rm -f " + outputFile)
						if not os.path.exists(output_path + "INDEL/"):
							os.mkdir(output_path + "INDEL/")
						out_indel = open(outputFile, "w") 
						first_indel = False

					print("\t".join([project, sample, ".", genome, "INDEL", chrom, start, start, ref, mut, "SOMATIC"]), file=out_indel)

		first_incorrect_file = True

	out_snv.close()
	out_indel.close()
	return(snv, indel)



