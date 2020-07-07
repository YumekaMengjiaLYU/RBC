import flywheel
import argparse
import logging
import subprocess
import sys
import os
import warnings
from pathlib import Path
from bids import BIDSLayout
from FlyBIDS.BIDSLayout import FlyBIDSLayout

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('PennLINC-Refacer')


def get_nested(dct, *keys):
    for key in keys:
        try:
            dct = dct[key]
        except (KeyError, TypeError):
            return None
    return dct


def find_t1_in_bids(root_path, subject, session):
    '''
    use pybids to make the pybids object and get the T1w
    '''

    subject = str(subject.replace('sub-', ''))
    session = str(session.replace('ses-', ''))

    data = BIDSLayout(root_path)
    df = data.to_df()
    t1 = df.loc[(df['subject'] == subject) & (df['session'] == session) & (df['suffix'] == 'T1w') & (df['extension'] == 'nii.gz')]

    assert t1.shape[0] == 1, "Couldn't find proper T1w file in BIDS!"

    p = Path(t1.iloc[0]['path']).resolve()

    return p.parent, p.name


def remove_prefix(label):

    label = label.replace('sub-', '')
    label = label.replace('ses-', '')

    return label


def process_subject(client, subject_label, project_label):
    '''
    get the subject object
    '''

    proj = client.projects.find_first('label="{}"'.format(project_label))
    subjects = proj.subjects()
    subject_obj = [x for x in subjects if remove_prefix(x.label) == remove_prefix(subject_label)]
    return subject_obj


def run_afni(path_to_file, filename, rec_label='refaced', dry_run=True, verbose=True):
    '''
    run afni reface, using rec_label as the value in the rec-<value> filename

    returns the new filename, the returncode and std out
    '''

    assert Path(path_to_file, filename).exists()

    refaced_filename = filename.replace("_T1w.nii.gz", "_rec-{}_T1w.nii.gz".format(rec_label))
    process = (['docker', 'run', '-ti', '--user $(id -u):$(id -g)', '-v', str(Path(path_to_file)) + ':' + '/home/',
                'pennlinc/afni_refacer', '-input', str(Path('/home/', filename)),
                '-mode_reface', '-prefix', str(Path('/home/', refaced_filename))])

    if dry_run:
        process.insert(0, 'echo')
        os.system('cp {} {}'.format(str(Path(path_to_file, filename)), str(Path(path_to_file, refaced_filename))))
    if verbose:
        print("Running:\n", " ".join(process))

    p = subprocess.Popen(' '.join(process), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.wait()
    out, err = p.communicate()

    if out is None:
        out = ''
    return refaced_filename, p.returncode, out


def replace_t1w(client, local_bids, flywheel_bids, rec_label='refaced', dry_run=True, verbose=True, delete=False):
    '''
    upload a refaced T1 to an acquisition to replace an original
    '''

    acquisition_obj = client.get(flywheel_bids['id'])
    original_filename = flywheel_bids['Filename']
    replacement_filename = flywheel_bids['Filename'].replace("_T1w.nii.gz", "_rec-{}_T1w.nii.gz".format(rec_label))
    replacement_path = local_bids['path'].replace("_T1w.nii.gz", "_rec-{}_T1w.nii.gz".format(rec_label))

    for f in acquisition_obj.files:

        old_name = get_nested(f.info, 'BIDS', 'Filename')
        if old_name == original_filename:
            info = f.info.copy()
            break

    info['BIDS']['Filename'] = replacement_filename
    info['BIDS']['Rec'] = rec_label

    if not dry_run:
        acquisition_obj.upload_file(replacement_path)

        acquisition_obj = acquisition_obj.reload()

        modified = acquisition_obj.update_file_info(replacement_filename, info)

        if verbose:
            logger.info("deleting existing T1")
        
        if delete:
            modified = acquisition_obj.delete_file(original_filename)

        if modified['modified'] != 1:
            return False
        else:
            return True
    else:
        if verbose:
            logger.info("New BIDS file:\n{}".format(info['BIDS']['Filename']))
        return True


def get_parser():

    parser = argparse.ArgumentParser(
        description="Reface T1w scan and upload it to Flywheel")
    parser.add_argument(
        "--project",
        help="The project on Flywheel",
        default='ReproBrainChart',
        required=False
    )
    parser.add_argument(
        "--directory",
        help="Path to existing BIDS directory on disk with a T1w to be refaced",
        default=".",
        required=True,
        type=str
    )
    parser.add_argument(
        "--rec",
        help="The value to put in the new filename for the BIDS field rec-<value>",
        default='refaced',
        action='store',
        required=False
    )
    parser.add_argument(
        "--verbose",
        help="Print ongoing messages of progress",
        action='store_true',
        default=False
    )
    parser.add_argument(
        "--dry-run",
        help="Don't apply changes",
        action='store_true',
        default=False
    )
    parser.add_argument(
        "--delete",
        help="Delete original file on Flywheel.",
        action='store_true',
        default=False
    )
    parser.add_argument(
        "--api-key",
        help="API Key",
        action='store',
        default=None
    )

    return parser


def main():

    # Init
    parser = get_parser()
    args = parser.parse_args()

    warnings.filterwarnings("ignore", category=FutureWarning)
    if args.api_key:
        client = flywheel.Client(args.api_key)
    else:
        client = flywheel.Client()
    assert client, "Your Flywheel CLI credentials aren't set!"

    if args.verbose:
        logger.info("Scanning BIDS directory for data...")

    local_bids = BIDSLayout(args.directory)
    local_bids_df = local_bids.to_df()
    local_t1s = (local_bids_df.loc[(local_bids_df['suffix'] == 'T1w')
        & (local_bids_df['extension'] == 'nii.gz')]
        )

    assert local_t1s.shape[0] >= 1, logger.error("No T1w files found in dataset!")

    if args.verbose:
        logger.info("Found the following subjects:\n{}".format(' '.join(local_t1s.subject.values)))
    if args.verbose:
        logger.info("Finding matching subjects on Flywheel...")

    for i, row in local_t1s.iterrows():
        
        print("\n")
        row_processed = False

        flywheel_bids = FlyBIDSLayout(args.project, str('sub-' + row['subject']))
        flywheel_bids_df = flywheel_bids.to_df()
        flywheel_t1s = (flywheel_bids_df.loc[ (flywheel_bids_df['Filename'].str.contains('T1w')) &
            (flywheel_bids_df['Filename'].str.contains('.nii.gz'))]
            )

        for i, row2 in flywheel_t1s.iterrows():
            if row['subject'] == row2['subject']:

                if args.verbose:
                    logger.info("Subject {} found. Refacing local T1w...".format(row['subject']))

                path_to_t1 = Path(row['path']).resolve().parent
                input_filename = Path(row['path']).resolve().name

                refaced_file, status, output = run_afni(

                    str(path_to_t1), str(input_filename), args.rec,
                    dry_run=args.dry_run, verbose=args.verbose

                )

                if args.verbose:
                    logger.info("Replacing T1w with newly refaced version...")
                row_processed = replace_t1w(client, row, row2, args.rec, dry_run=True, verbose=args.verbose, delete=args.delete)


        if not row_processed:

            logger.error("Subject {} not processed!".format(row['subject']))

if __name__ == '__main__':

    sys.exit(main())
