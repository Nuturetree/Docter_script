#--------pipeline submission tasks of juicer--
#-----------------nutures---------------------
#----------------20200812---------------------

import os
import re
import sys
import time
import argparse
import datetime

def main(argv):
    parser = argparse.ArgumentParser(description="")
    parser.add_argument('-g', '--genomefile', required=True,help="List of genome files to be processed")
    #parser.add_argument('-c', '--hicfile', required=True, help='List of hic files to be processed')
    args = parser.parse_args()
    startTime = datetime.datetime.now()
    print "Starting ======",startTime.strftime('%Y-%m-%d %H:%M:%S'),"======"
    gen_file = args.genomefile
    #hic_file = args.hicfile
    #print gen_file,hic_file 
    for line in open(gen_file):
        name = line.strip()
        print name
        #bwa_index(name)
        sites_sizes(name)
        #Restriction_sites(name)
        #chromosome_sizes(name)
def sites_sizes(name):
    path , genome_name = name.rsplit('/',1)[0], name.rsplit('/',1)[1]
    normal_name = genome_name.rsplit('.',1)[0]
    HindIII_path_name = '{}/juicer/restriction_sites/{}_HindIII.txt'.format(path,normal_name)
    Sizes_path_name = '{}/juicer/restriction_sites/{}.sizes'.format(path,normal_name)
    reference_path = '{}/{}/{}'.format(path, 'juicer','references')
    #print reference_path 
    #os.system('mkdir -p ' + reference_path)
    restriction_sizes = '{}/{}/{}'.format(path, 'juicer', 'sites_sizes') 
    print restriction_sizes
    #os.system('mkdir -p ' + restriction_sizes)
    #os.system('mv {} {}'.format(name,reference_path))
    #print 'mv {} {}'.format(name,reference_path)
    genome_path = '{}/{}'.format(reference_path,normal_name)
    new_genome = '{}.fa'.format(genome_path)
    sites_name = '{}_HindIII.txt'.format(genome_path)
    sizes_name = '{}.sizes'.format(genome_path)  
    #print new_genome 
    while os.path.isfile(new_genome) == False:
        time.sleep(1)
        print 'waiting.............'
    if os.path.isfile(genome_path) == False:
        job_name = genome_name.split('.')[0] + 'py'
        restriction_site = "bsub -q smp -J {} -e %J.err -o %J.out -R span[hosts=1] 'python ~/biosoft/juicer-master/misc/generate_site_positions.py HindIII {} {}'".format(job_name,genome_path,new_genome)
        print restriction_site
        #os.system(restriction_site)
    #time.sleep(600)
    #while os.path.isfile(sites_name) == False:
    #print "waiting again .............."
    chrom_size = "awk 'BEGIN{OFS=\"\\t\"}{print $1, $NF}' %s > %s " %(sites_name,sizes_name)
    #print chrom_size
    os.system(chrom_size)
    os.system("mv {} {}".format(sites_name,restriction_sizes))
    os.system("mv {} {}".format(sizes_name,restriction_sizes))
    bwa_load = "module load BWA/0.7.17"
    #os.system(bwa_load)
    job_name =  genome_name.split('.')[0] + 'bwa'
    bwa_run = "bsub -q smp -J {} -e %J.err -o %J.out -R span[hosts=1] 'bwa index {}'".format(job_name, new_genome)
    print bwa_run
    #os.system(bwa_run)

if __name__ == "__main__":
    print sys.argv[1:]
    main(sys.argv[1:])

