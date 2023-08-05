import os

import rope.base.project
import rope.refactor.encapsulate_field
import rope.refactor.inline
import rope.refactor.introduce_parameter
import rope.refactor.localtofield
import rope.refactor.multiproject
import rope.refactor.rename
import rope.refactor.move
import rope.refactor.usefunction
from rope.base.change import ChangeToData, DataToChange

from .auto_import import AutoImportMixin
from .change_signature import ChangeSignatureMixin
from .code_assist import CodeAssistMixin
from .extract import ExtractMixin
from .history import HistoryMixin
from .imports import ImportsMixin
from .move import MoveMixin
from .findit import FinditMixin
from .validate import validate


def get_all_resources(proj):
    '''Generate a sequence of (path, is_folder) tuples for all
    resources in a project.

    Args:
      proj: The rope Project to scan.

    Returns: An iterable over all resources in a Project, with a tuple
      (path, is_folder) for each.
    '''
    todo = ['']
    while todo:
        res_path = todo[0]
        todo = todo[1:]
        res = proj.get_resource(res_path)
        yield(res.path, res.is_folder())

        if res.is_folder():
            todo.extend((child.path for child in res.get_children()))


class Workspace(AutoImportMixin,
                ChangeSignatureMixin,
                CodeAssistMixin,
                ExtractMixin,
                HistoryMixin,
                ImportsMixin,
                MoveMixin,
                FinditMixin):
    """An actor that controls access to an underlying Rope project.
    """
    def __init__(self,
                 root_project_dir,
                 cross_project_dirs=[]):
        AutoImportMixin.__init__(self)

        self._root_project = rope.base.project.Project(root_project_dir)

        self._cross_projects = dict()

        cross_dirs = set(cross_project_dirs)
        cross_dirs.discard(root_project_dir)
        for cross_dir in cross_dirs:
            self.add_cross_project(cross_dir)

    def close(self):
        self.root_project.close()

    def add_cross_project(self, directory):
        """Add a cross project rooted at `directory`."""
        self._cross_projects[directory] = rope.base.project.Project(directory)

    def remove_cross_project(self, directory):
        """Remove the cross project rooted at `directory`."""
        del self._cross_projects[directory]

    @property
    def root_project(self):
        return self._root_project

    @property
    def cross_projects(self):
        return self._cross_projects.values()

    @property
    def projects(self):
        yield self.root_project
        for cp in self.cross_projects:
            yield cp

    def to_relative_path(self, path, project=None):
        '''Get a version of a path relative to the project root.

        If ``path`` is already relative, then it is unchanged. If
        ``path`` is absolute, then it is made relative to the project
        root.

        Args:
          path: The path to make relative.
          project: The project to use as the root directory [default: root project]

        Returns: ``path`` relative to the project root.

        '''
        project = project or self.root_project

        if os.path.isabs(path):
            path = os.path.relpath(
                os.path.realpath(path),
                project.root.real_path)
        return path

    def get_resource(self, path):
        return self.root_project.get_resource(
            self.to_relative_path(path))

    def get_file(self, path):
        return self.root_project.get_file(
            self.to_relative_path(path))

    def get_folder(self, path):
        return self.root_project.get_folder(
            self.to_relative_path(path))

    def get_changes(self,
                    refactoring_type,
                    path,
                    refactoring_args,
                    change_args):
        """Calculate the changes for a specific refactoring.

        Args:
          refactoring_type: The class of the refactoring to perform (e.g.
            `rope.refactor.rename.Rename`)
          path: The path to the resource in the project.
          refactoring_args: The sequence of args to pass to the
            `refactoring_type` constructor.
          change_args: The sequence of args to pass to
            `MultiProjectRefactoring.get_all_changes`.

        Returns: All changes that would be performed by the refactoring. A list
          of the form `[[<project>, [<change set>]]`.
        """
        refactoring = refactoring_type(
            self.root_project,
            self.get_resource(
                self.to_relative_path(
                    path)),
            *refactoring_args)
        multi_project_refactoring = rope.refactor.MultiProjectRefactoring(
            refactoring, self.cross_projects)
        return multi_project_refactoring(
            self.root_project,
            *change_args).get_all_changes(*change_args)

    def perform(self, changes):
        self.root_project.do(changes)

    @validate
    def rename(self, path, offset, new_name,
               in_hierarchy=False, unsure=None, docs=False):
        """Rename the object in ``path`` at ``offset``.

        Args:
          in_hierarchy: when renaming a method this keyword forces
            to rename all matching methods in the hierarchy
          docs: when ``True`` rename refactoring will rename
            occurrences in comments and strings where the name is
            visible.  Setting it will make renames faster, too.
          unsure: decides what to do about unsure occurrences.
            If `None`, they are ignored.  Otherwise ``unsure`` is
            called with an instance of `occurrence.Occurrence` as
            parameter.  If it returns `True`, the occurrence is
            considered to be a match.

        Returns: All changes performed by the refactoring. A list of the form
          `[[<project>, [<change set>]]`.
        """
        ref = rope.refactor.rename.Rename(
            self.root_project,
            self.get_resource(path),
            offset)
        return ref.get_changes(
            new_name,
            in_hierarchy=in_hierarchy,
            unsure=unsure,
            docs=docs)

    @validate
    def move(self, path, offset, dest_path):
        ref = rope.refactor.move.create_move(
            self.root_project,
            self.get_resource(path),
            offset)
        return ref.get_changes(self.get_resource(dest_path))

    @validate
    def inline(self, path, offset):
        ref = rope.refactor.inline.create_inline(
            self.root_project,
            self.get_resource(path),
            offset)
        return ref.get_changes()

    @validate
    def introduce_parameter(self, path, offset, parameter):
        ref = rope.refactor.introduce_parameter.IntroduceParameter(
            self.root_project,
            self.get_resource(path),
            offset)
        return ref.get_changes(parameter)

    @validate
    def encapsulate_field(self, path, offset):
        ref = rope.refactor.encapsulate_field.EncapsulateField(
            self.root_project,
            self.get_resource(path),
            offset)
        return ref.get_changes()

    @validate
    def local_to_field(self, path, offset):
        ref = rope.refactor.localtofield.LocalToField(
            self.root_project,
            self.get_resource(path),
            offset)
        return ref.get_changes()

    @validate
    def use_function(self, path, offset):
        ref = rope.refactor.usefunction.UseFunction(
            self.root_project,
            self.get_resource(path),
            offset)
        return ref.get_changes()

    def __repr__(self):
        return 'Project("{}")'.format(
            self.root_project.root.real_path)

    def __str__(self):
        return repr(self)

    def _root_to_project(self, root):
        if root == self.root_project.root.real_path:
            return self.root_project
        return self.cross_projects[root]


def changes_to_data(changes):
    return ChangeToData()(changes)


def data_to_changes(workspace, data):
    return DataToChange(workspace.root_project)(data)
