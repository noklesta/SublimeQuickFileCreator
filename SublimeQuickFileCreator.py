import os
import re
import sublime
import sublime_plugin


class QuickCreateFileCreatorBase(sublime_plugin.WindowCommand):
    ROOT_DIR_PREFIX = '[root: '
    ROOT_DIR_SUFFIX = ']'

    def doCommand(self):
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
        patterns = [re.escape(pat) for pat in self.get_setting('excluded_dir_patterns')]
        self.excluded = re.compile('^' + '|'.join(patterns) + '$')

    def get_setting(self, key):
        settings = None
        view = self.window.active_view()

        if view:
            settings = self.window.active_view().settings()

        if settings and settings.has('SublimeQuickFileCreator') and key in settings.get('SublimeQuickFileCreator'):
            # Get project-specific setting
            results = settings.get('SublimeQuickFileCreator')[key]
        else:
            # Get user-specific or default setting
            settings = sublime.load_settings('SublimeQuickFileCreator.sublime-settings')
            results = settings.get(key)
        return results

    def build_relative_paths(self):
        self.relative_paths = [self.ROOT_DIR_PREFIX + os.path.split(self.root)[-1] + self.ROOT_DIR_SUFFIX]
        for base, dirs, files in os.walk(self.root):
            dirs_copy = dirs[:]
            [dirs.remove(dir) for dir in dirs_copy if self.excluded.search(dir)]

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
            self.window.show_input_panel(self.INPUT_PANEL_CAPTION, '', self.file_name_input, None, None)

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


class QuickCreateFileCommand(QuickCreateFileCreatorBase):
    INPUT_PANEL_CAPTION = 'File name:'

    def run(self):
        self.doCommand()

    def create_and_open_file(self, path):
        open(path, 'w')
        self.window.open_file(path)


class QuickCreateDirectoryCommand(QuickCreateFileCreatorBase):
    INPUT_PANEL_CAPTION = 'Folder name:'

    def run(self):
        self.doCommand()

    def create_and_open_file(self, path):
        os.mkdir(path)
