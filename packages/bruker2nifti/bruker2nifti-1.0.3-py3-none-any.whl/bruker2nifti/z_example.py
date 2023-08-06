import os


from bruker2nifti.converter import Bruker2Nifti

if __name__ == '__main__':
    pfo_in = '/Users/sebastiano/Downloads/z_test_scan'
    pfo_out = '/Users/sebastiano/Downloads/out'
    print(os.path.isdir(pfo_out))
    # instantiate a converter
    bru = Bruker2Nifti(pfo_in, pfo_out, study_name=None)
    # select the options (attributes) you may want to change - the one shown below are the default one:
    bru.verbose = 2
    bru.correct_slope = True
    bru.correct_offset = False
    bru.get_acqp = True
    bru.get_method = True
    bru.get_reco = True
    bru.nifti_version = 1
    bru.qform_code = 1
    bru.sform_code = 2
    bru.save_human_readable = True
    bru.save_b0_if_dwi = True

    # Check that the list of scans and the scans names automatically selected makes some sense:
    print(bru.scans_list)
    print(bru.list_new_name_each_scan)
    print(bru.study_name)
    # call the function convert, to convert the study:
    bru.convert()

