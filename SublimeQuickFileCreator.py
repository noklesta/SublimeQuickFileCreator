import os
import re
import sublime
import sublime_plugin


class QuickCreateFileCreatorBase(sublime_plugin.WindowCommand):
    relative_paths = []
    full_torelative_paths = {}
    rel_path_start = 0

    def doCommand(self):
        self.construct_excluded_pattern()
        self.build_relative_paths()
        if len(self.relative_paths) == 1:
            self.selected_dir = self.relative_paths[0]
            self.selected_dir = self.full_torelative_paths[self.selected_dir]
            self.window.show_input_panel(self.INPUT_PANEL_CAPTION, '', self.file_name_input, None, None)
        elif len(self.relative_paths) > 1:
            self.move_current_directory_to_top()
            self.window.show_quick_panel(self.relative_paths, self.dir_selected)
        else:
            view = self.window.active_view()
            self.selected_dir = os.path.dirname(view.file_name())
            self.window.show_input_panel(self.INPUT_PANEL_CAPTION, '', self.file_name_input, None, None)

    def construct_excluded_pattern(self):
        patterns = [pat.replace('|', '\\') for pat in self.get_setting('excluded_dir_patterns')]
        self.excluded = re.compile('|'.join(patterns))

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
        folders = self.window.folders()
        view = self.window.active_view()
        self.relative_paths = []
        self.full_torelative_paths = {}
        for path in folders:
            rootfolders = os.path.split(path)[-1]
            self.rel_path_start = len(os.path.split(path)[0]) + 1
            if not self.excluded.search(rootfolders):
                self.full_torelative_paths[rootfolders] = path
                self.relative_paths.append(rootfolders)

            for base, dirs, files in os.walk(path):
                for dir in dirs:
                    relative_path = os.path.join(base, dir)[self.rel_path_start:]
                    if not self.excluded.search(relative_path):
                        self.full_torelative_paths[relative_path] = os.path.join(base, dir)
                        self.relative_paths.append(relative_path)

    def move_current_directory_to_top(self):
        view = self.window.active_view()
        if view.file_name():
            cur_dir = os.path.dirname(view.file_name())[self.rel_path_start:]
            if cur_dir in self.full_torelative_paths:
                i = self.relative_paths.index(cur_dir)
                self.relative_paths.insert(0, self.relative_paths.pop(i))
            else:
                self.relative_paths.insert(0, os.path.dirname(view.file_name()))
        return

    def dir_selected(self, selected_index):
        if selected_index != -1:
            self.selected_dir = self.relative_paths[selected_index]
            self.selected_dir = self.full_torelative_paths[self.selected_dir]
            self.window.show_input_panel(self.INPUT_PANEL_CAPTION, '', self.file_name_input, None, None)

    def file_name_input(self, file_name):
        full_path = os.path.join(self.selected_dir, file_name)

        if os.path.lexists(full_path):
            sublime.error_message('File already exists:\n%s' % full_path)
            return
        else:
            self.create_and_open_file(full_path)

    def create(self, filename):
        base, filename = os.path.split(filename)
        self.create_folder(base)

    def create_folder(self, base):
        if not os.path.exists(base):
            parent = os.path.split(base)[0]
            if not os.path.exists(parent):
                self.create_folder(parent)
            os.mkdir(base)


class QuickCreateFileCommand(QuickCreateFileCreatorBase):
    INPUT_PANEL_CAPTION = 'File name:'

    def run(self):
        self.doCommand()

    def create_and_open_file(self, path):
        if not os.path.exists(path):
            self.create(path)
        self.window.open_file(path)


class QuickCreateDirectoryCommand(QuickCreateFileCreatorBase):
    INPUT_PANEL_CAPTION = 'Folder name:'

    def run(self):
        self.doCommand()

    def create_and_open_file(self, path):
        self.create_folder(path)
