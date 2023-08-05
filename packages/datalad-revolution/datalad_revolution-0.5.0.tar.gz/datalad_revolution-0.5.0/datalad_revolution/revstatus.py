# emacs: -*- mode: python; py-indent-offset: 4; tab-width: 4; indent-tabs-mode: nil -*-
# ex: set sts=4 ts=4 sw=4 noet:
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
#
#   See COPYING file distributed along with the datalad package for the
#   copyright and license terms.
#
# ## ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ### ##
"""Report status of a dataset (hierarchy)'s work tree"""

__docformat__ = 'restructuredtext'


import logging
import os.path as op
from six import (
    iteritems,
    text_type,
)
from collections import OrderedDict

import datalad.support.ansi_colors as ac

from datalad.utils import (
    assure_list,
)
from datalad.interface.base import (
    Interface,
    build_doc,
)
from datalad.interface.utils import eval_results
from datalad.interface.common_opts import (
    recursion_limit,
    recursion_flag,
)

from datalad_revolution.dataset import (
    RevolutionDataset as Dataset,
    EnsureDataset,
    datasetmethod,
    require_dataset,
    resolve_path,
    path_under_dataset,
    get_dataset_root,
)
import datalad_revolution.utils as ut

from datalad.support.constraints import EnsureNone
from datalad.support.constraints import EnsureStr
from datalad.support.constraints import EnsureChoice
from datalad.support.param import Parameter

lgr = logging.getLogger('datalad.revolution.status')


state_color_map = {
    'untracked': ac.RED,
    'modified': ac.RED,
    'added': ac.GREEN,
}


def _yield_status(ds, paths, annexinfo, untracked, recursion_limit, queried, cache):
    # take the datase that went in first
    repo_path = ds.repo.pathobj
    lgr.debug('query %s.status() for paths: %s', ds.repo, paths)
    status = ds.repo.diffstatus(
        fr='HEAD' if ds.repo.get_hexsha() else None,
        to=None,
        paths=paths if paths else None,
        untracked=untracked,
        # TODO think about potential optimizations in case of
        # recursive processing, as this will imply a semi-recursive
        # look into subdatasets
        ignore_submodules='other',
        _cache=cache)
    if annexinfo and hasattr(ds.repo, 'get_content_annexinfo'):
        # this will ammend `status`
        ds.repo.get_content_annexinfo(
            paths=paths if paths else None,
            init=status,
            eval_availability=annexinfo in ('availability', 'all'),
            ref=None)
    for path, props in iteritems(status):
        cpath = ds.pathobj / path.relative_to(repo_path)
        yield dict(
            props,
            path=str(cpath),
            # report the dataset path rather than the repo path to avoid
            # realpath/symlink issues
            parentds=ds.path,
        )
        queried.add(ds.pathobj)
        if recursion_limit and props.get('type', None) == 'dataset':
            subds = Dataset(str(cpath))
            if subds.is_installed():
                for r in _yield_status(
                        subds,
                        None,
                        annexinfo,
                        untracked,
                        recursion_limit - 1,
                        queried,
                        cache):
                    yield r


@build_doc
class RevStatus(Interface):
    """Report on the state of dataset content.

    This is an analog to `git status` that is simultaneously crippled and more
    powerful. It is crippled, because it only supports a fraction of the
    functionality of its counter part and only distinguishes a subset of the
    states that Git knows about. But it is also more powerful as it can handle
    status reports for a whole hierarchy of datasets, with the ability to
    report on a subset of the content (selection of paths) across any number
    of datasets in the hierarchy.

    *Path conventions*

    All reports are guaranteed to use absolute paths that are underneath the
    given or detected reference dataset, regardless of whether query paths are
    given as absolute or relative paths (with respect to the working directory,
    or to the reference dataset, when such a dataset is given explicitly).
    Moreover, so-called "explicit relative paths" (i.e. paths that start with
    '.' or '..') are also supported, and are interpreted as relative paths with
    respect to the current working directory regardless of whether a reference
    dataset with specified.

    When it is necessary to address a subdataset record in a superdataset
    without causing a status query for the state _within_ the subdataset
    itself, this can be achieved by explicitly providing a reference dataset
    and the path to the root of the subdataset like so::

      datalad rev-status --dataset . subdspath

    In contrast, when the state of the subdataset within the superdataset is
    not relevant, a status query for the content of the subdataset can be
    obtained by adding a trailing path separator to the query path (rsync-like
    syntax)::

      datalad rev-status --dataset . subdspath/

    When both aspects are relevant (the state of the subdataset content
    and the state of the subdataset within the superdataset), both queries
    can be combined::

      datalad rev-status --dataset . subdspath subdspath/

    When performing a recursive status query, both status aspects of subdataset
    are always included in the report.


    *Content types*

    The following content types are distinguished:

    - 'dataset' -- any top-level dataset, or any subdataset that is properly
      registered in superdataset
    - 'directory' -- any directory that does not qualify for type 'dataset'
    - 'file' -- any file, or any symlink that is placeholder to an annexed
      file
    - 'symlink' -- any symlink that is not used as a placeholder for an annexed
      file

    *Content states*

    The following content states are distinguished:

    - 'clean'
    - 'added'
    - 'modified'
    - 'deleted'
    - 'untracked'
    """
    # make the custom renderer the default one, as the global default renderer
    # does not yield meaningful output for this command
    result_renderer = 'tailored'

    _params_ = dict(
        dataset=Parameter(
            args=("-d", "--dataset"),
            doc="""specify the dataset to query.  If
            no dataset is given, an attempt is made to identify the dataset
            based on the current working directory""",
            constraints=EnsureDataset() | EnsureNone()),
        path=Parameter(
            args=("path",),
            metavar="PATH",
            doc="""path to be evaluated""",
            nargs="*",
            constraints=EnsureStr() | EnsureNone()),
        annex=Parameter(
            args=('--annex',),
            metavar='MODE',
            constraints=EnsureChoice(None, 'basic', 'availability', 'all'),
            doc="""Switch whether to include information on the annex
            content of individual files in the status report, such as
            recorded file size. By default no annex information is reported
            (faster). Three report modes are available: basic information
            like file size and key name ('basic'); additionally test whether
            file content is present in the local annex ('availability';
            requires one or two additional file system stat calls, but does
            not call git-annex), this will add the result properties
            'has_content' (boolean flag) and 'objloc' (absolute path to an
            existing annex object file); or 'all' which will report all
            available information (presently identical to 'availability').
            """),
        untracked=Parameter(
            args=('--untracked',),
            metavar='MODE',
            constraints=EnsureChoice('no', 'normal', 'all'),
            doc="""If and how untracked content is reported when comparing
            a revision to the state of the work tree. 'no': no untracked
            content is reported; 'normal': untracked files and entire
            untracked directories are reported as such; 'all': report
            individual files even in fully untracked directories."""),
        recursive=recursion_flag,
        recursion_limit=recursion_limit)

    @staticmethod
    @datasetmethod(name='rev_status')
    @eval_results
    def __call__(
            path=None,
            dataset=None,
            annex=None,
            untracked='normal',
            recursive=False,
            recursion_limit=None):
        ds = require_dataset(
            dataset, check_installed=True, purpose='status reporting')

        paths_by_ds = OrderedDict()
        if path:
            # sort any path argument into the respective subdatasets
            for p in sorted(assure_list(path)):
                # it is important to capture the exact form of the
                # given path argument, before any normalization happens
                # for further decision logic below
                orig_path = str(p)
                p = resolve_path(p, dataset)
                root = get_dataset_root(str(p))
                if root is None:
                    # no root, not possibly underneath the refds
                    yield dict(
                        action='status',
                        path=p,
                        refds=ds.path,
                        status='error',
                        message='path not underneath this dataset',
                        logger=lgr)
                    continue
                else:
                    if dataset and root == str(p) and \
                            not orig_path.endswith(op.sep):
                        # the given path is pointing to a dataset
                        # distinguish rsync-link syntax to identify
                        # the dataset as whole (e.g. 'ds') vs its
                        # content (e.g. 'ds/')
                        super_root = get_dataset_root(op.dirname(root))
                        if super_root:
                            # the dataset identified by the path argument
                            # is contained in a superdataset, and no
                            # trailing path separator was found in the
                            # argument -> user wants to address the dataset
                            # as a whole (in the superdataset)
                            root = super_root

                root = ut.Path(root)
                ps = paths_by_ds.get(root, [])
                ps.append(p)
                paths_by_ds[root] = ps
        else:
            paths_by_ds[ds.pathobj] = None

        queried = set()
        content_info_cache = {}
        while paths_by_ds:
            qdspath, qpaths = paths_by_ds.popitem(last=False)
            if qpaths and qdspath in qpaths:
                # this is supposed to be a full query, save some
                # cycles sifting through the actual path arguments
                qpaths = []
            # try to recode the dataset path wrt to the reference
            # dataset
            # the path that it might have been located by could
            # have been a resolved path or another funky thing
            qds_inrefds = path_under_dataset(ds, qdspath)
            if qds_inrefds is None:
                # nothing we support handling any further
                # there is only a single refds
                yield dict(
                    path=text_type(qdspath),
                    refds=ds.path,
                    action='status',
                    status='error',
                    message=(
                        "dataset containing given paths is not underneath "
                        "the reference dataset %s: %s",
                        ds, qpaths),
                )
                continue
            elif qds_inrefds != qdspath:
                # the path this dataset was located by is not how it would
                # be referenced underneath the refds (possibly resolved
                # realpath) -> recode all paths to be underneath the refds
                qpaths = [qds_inrefds / p.relative_to(qdspath) for p in qpaths]
                qdspath = qds_inrefds
            if qdspath in queried:
                # do not report on a single dataset twice
                continue
            qds = Dataset(str(qdspath))
            for r in _yield_status(
                    qds,
                    qpaths,
                    annex,
                    untracked,
                    recursion_limit
                    if recursion_limit is not None else -1
                    if recursive else 0,
                    queried,
                    content_info_cache):
                yield dict(
                    r,
                    refds=ds.path,
                    action='status',
                    status='ok',
                )

    @staticmethod
    def custom_result_renderer(res, **kwargs):  # pragma: no cover
        from datalad.ui import ui
        if not res['status'] == 'ok' or res.get('state', None) == 'clean':
            # logging reported already
            return
        path=res['path']
        #path = res['path'].relative_to(res['refds']) \
        #    if res.get('refds', None) else res['path']
        type_ = res.get('type', res.get('type_src', ''))
        max_len = len('untracked(directory)')
        ui.message('{fill}{state}: {path}{type_}'.format(
            fill=' ' * max(0, max_len - len(res['state'])),
            state=ac.color_word(
                res['state'],
                state_color_map.get(res['state'], ac.WHITE)),
            path=path,
            type_=' ({})'.format(
                ac.color_word(type_, ac.MAGENTA) if type_ else '')))
