# Definition of the version number
import os

__all__ = ["__version__"]

# major, minor, patch, -extra
version_info = 4, 10, 0

# Nice string for the version
__version__ = '.'.join(map(str, version_info))


# auto -extra based on commit hash (if not tagged as release)
scriptdir = os.path.dirname(__file__)
gitdir = os.path.abspath(scriptdir + '/../.git')
if os.path.isdir(gitdir):
    extra = None
    # Open config file to check if we are in tqdm project
    with open(os.path.join(gitdir, 'config'), 'r') as fh_config:
        if 'tqdm' in fh_config.read():
            # Open the HEAD file
            with open(os.path.join(gitdir, 'HEAD'), 'r') as fh_head:
                extra = fh_head.readline().strip()
            # If we are in a branch, HEAD will point to a file containing the latest commit
            if 'ref:' in extra:
                # Get reference file path
                ref_file = extra[5:]
                # Get branch name
                branch_name = ref_file.split('/')[-1]

                # Sanitize path of ref file
                # get full path to ref file
                ref_file_path = os.path.abspath(os.path.join(gitdir, ref_file))
                # check that we are in git folder (by stripping the git folder from the ref file path)
                if os.path.relpath(ref_file_path, gitdir).replace('\\', '/') != ref_file:
                    # Trying to get out of git folder, not good!
                    extra = None
                else:
                    # Else the file file is inside git, all good
                    # Open the ref file
                    with open(ref_file_path, 'r') as fh_branch:
                        commit_hash = fh_branch.readline().strip()
                        extra = commit_hash[:8] + ' (branch: ' + branch_name + ')'

            # Else we are in detached HEAD mode, we directly have a commit hash
            else:
                extra = extra[:8]  # limit to the first 8 symbols of the hash

    # Append to version string
    if extra is not None:
        __version__ += '-' + extra
