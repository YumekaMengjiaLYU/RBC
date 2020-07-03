import flywheel
import argparse
import logging
import subprocess
import sys
import os
import warnings
from pathlib import Path
from bids import BIDSLayout

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


def process_subject(client, subject_label, project_label):
    '''
    get the subject object
    '''

    proj = client.projects.find_first('label="{}"'.format(project_label))
    subjects = proj.subjects()
    subject_obj = [x for x in subjects if x.label == subject_label]
    return subject_obj


def run_afni(path_to_file, filename, rec_label='refaced', dry_run=True, verbose=True):
    '''
    run afni reface, using rec_label as the value in the rec-<value> filename

    returns the new filename, the returncode and std out
    '''

    assert Path(path_to_file, filename).exists()

    refaced_filename = filename.replace("_T1w.nii.gz", "_rec-{}_T1w.nii.gz".format(rec_label))
    process = ['@afni_refacer_run', '-input', str(Path(path_to_file, filename)),'-mode_reface', '-prefix', str(Path(path_to_file, refaced_filename))]

    if dry_run:
        process.insert(0, 'echo')
        os.system('cp {} {}'.format(str(Path(path_to_file, filename)), str(Path(path_to_file, refaced_filename))))
    if verbose:
        print("Running:\n", " ".join(process))

    p = subprocess.Popen(process, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    if out is None:
        out = ''
    return refaced_filename, p.returncode, out


def replace_t1w(acquisition_obj, original_filename, replacement_filename, replacement_path, rec_label, dry_run=True, verbose=True):
    '''
    upload a refaced T1 to an acquisition to replace an original
    '''

    for f in acquisition_obj.files:

        old_name = get_nested(f.info, 'BIDS', 'Filename')
        if old_name == original_filename:
            info = f.info.copy()
            break

    info['BIDS']['Filename'] = replacement_filename
    info['BIDS']['Rec'] = rec_label

    if not dry_run:
        acquisition_obj.upload_file(replacement_path + replacement_filename)

        acquisition_obj = acquisition_obj.reload()

        acquisition_obj.update_file_info(replacement_filename, info)

        if verbose:
            logger.info("deleting existing T1")

        modified = acquisition_obj.delete_file(original_filename)

        if modified['modified'] != 1:
            return 1
        else:
            return 0
    else:
        if verbose:
            logger.info("New BIDS file:\n{}".format(info))
        return 0


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
        "--subject",
        help="The subject label to upload the T1w to on Flywheel",
        action='store',
        required=True,
        type=str,
        default=None
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
        "--api-key",
        help="API Key",
        action='store',
        default=None
    )

    return parser


def main():

    parser = get_parser()
    args = parser.parse_args()

    warnings.filterwarnings("ignore", category=FutureWarning)
    if args.api_key:
        client = flywheel.Client(args.api_key)
    else:
        client = flywheel.Client()
    assert client, "Your Flywheel CLI credentials aren't set!"

    if args.verbose:
        logger.info("Finding matching subject on Flywheel...")
    subject_obj = process_subject(client, args.subject, args.project)
    assert len(subject_obj) == 1 and subject_obj[0].label == args.subject, "Correct subject not found!"

    subject_obj = subject_obj.pop()

    if args.verbose:
        logger.info("Subject found. Finding T1 scan...")

    t1w = None

    sessions = subject_obj.sessions()
    for i, ses in enumerate(sessions):

        if args.verbose:
            logger.info("Processing session {} of {}".format(i+1, len(sessions)))

        acquisitions = [client.get(a.id) for a in ses.acquisitions()]

        for acq in acquisitions:

            for f in acq.files:
                if f.type != 'nifti':
                    continue

                mod = get_nested(f, 'info', 'BIDS', 'Modality')
                flywheel_filename = get_nested(f, 'info', 'BIDS', 'Filename')
                _, local_filename = find_t1_in_bids(args.directory, args.subject, ses.label)

                if (mod == "T1w") and (str(flywheel_filename) == str(local_filename)):

                    t1w = acq

        assert t1w, "No T1w scans found in Flywheel subject!"

        if args.verbose:
            logger.info("Processing T1w...")

        path_to_t1, input_filename = find_t1_in_bids(args.directory, args.subject, ses.label)

        # run refacing
        refaced_file, status, output = run_afni(

            str(path_to_t1), str(input_filename), args.rec,
            dry_run=args.dry_run, verbose=args.verbose

        )

        print(input_filename, refaced_file, path_to_t1)

        if status != 0:
            logger.error("There was a problem running afni!")
            if args.verbose:
                logger.error(output.decode("utf-8"))
            return 1

        if args.verbose:
            logger.info("Replacing T1w with newly refaced version...")
        replace_t1w(t1w, input_filename, refaced_file, path_to_t1, args.rec, dry_run=True, verbose=args.verbose)

if __name__ == '__main__':
    logger.info("Done!")
    sys.exit(main())
