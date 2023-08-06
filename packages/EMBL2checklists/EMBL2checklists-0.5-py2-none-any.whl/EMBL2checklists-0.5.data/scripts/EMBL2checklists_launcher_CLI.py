#!python
# -*- coding: utf-8 -*-

if __name__ == '__main__':
    
    import sys, os
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'EMBL2checklists'))
    import CLIOps

    CLIOps.start_EMBL2checklists_CLI()
