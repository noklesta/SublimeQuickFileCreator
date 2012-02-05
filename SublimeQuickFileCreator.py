import os
import re
import sublime
import sublime_plugin


class QuickCreateFileCommand(sublime_plugin.WindowCommand):
    ROOT_DIR_PREFIX = '[root: '
    ROOT_DIR_SUFFIX = ']'

    def run(self):
        if not self.find_root():
            return

        self.construct_excluded_pattern()
        self.build_relative_paths()
        self.move_current_directory_to_top()
        self.window.show_quick_panel(self.relative_paths, self.dir_selected)

    def find_root(self):
        folders = self.window.folders()
        if len(folders) == 0:
            sublime.error_message('Could not find project root')
            return False

        self.root = folders[0]
        self.rel_path_start = len(self.root) + 1
        return True

    def construct_excluded_pattern(self):
        settings = sublime.load_settings("SublimeQuickFileCreator.sublime-settings")
        self.excluded = re.compile('^' + '|'.join(settings.get('excluded_dir_patterns')) + '$')

    def build_relative_paths(self):
        self.relative_paths = [self.ROOT_DIR_PREFIX + os.path.split(self.root)[-1] + self.ROOT_DIR_SUFFIX]
        for base, dirs, files in os.walk(self.root):
            [dirs.remove(dir) for dir in dirs if self.excluded.search(dir)]

            for dir in dirs:
                relative_path = os.path.join(base, dir)[self.rel_path_start:]
                self.relative_paths.append(relative_path)

    def move_current_directory_to_top(self):
        view = self.window.active_view()

        if view:
            cur_dir = os.path.dirname(view.file_name())[self.rel_path_start:]
            for path in self.relative_paths:
                if path == cur_dir:
                    i = self.relative_paths.index(path)
                    self.relative_paths.insert(0, self.relative_paths.pop(i))
                    break

    def dir_selected(self, selected_index):
        if selected_index != -1:
            self.selected_dir = self.relative_paths[selected_index]
            self.window.show_input_panel('File name:', '', self.file_name_input, None, None)

    def file_name_input(self, file_name):
        if self.selected_dir.startswith(self.ROOT_DIR_PREFIX):
            dir = ''
        else:
            dir = self.selected_dir

        full_path = os.path.join(self.root, dir, file_name)
        if os.path.lexists(full_path):
            sublime.error_message('File already exists:\n%s' % full_path)
            return
        else:
            self.create_and_open_file(full_path)

    def create_and_open_file(self, path):
        open(path, 'w')
        self.window.open_file(path)
