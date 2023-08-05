#!/usr/bin/python


import mr_demuxy
from mr_demuxy import pe_demuxer_dist
#from mr_demuxy.pe_demuxer_dist import pe_demuxer_dist
#from .mr_demuxy import pe_demuxer_dist

def main():
    pe_class = pe_demuxer_dist.PEDemux()
    pe_class.main_loop()

if __name__ == '__main__':
    main()
