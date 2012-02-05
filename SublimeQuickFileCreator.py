import os
import re
import sublime
import sublime_plugin


class QuickCreateFileCommand(sublime_plugin.WindowCommand):
    def run(self):
        if not self.find_root():
            return

        self.construct_excluded_pattern()
        self.build_relative_paths()
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
        self.relative_paths = ['.']
        for base, dirs, files in os.walk(self.root):
            [dirs.remove(dir) for dir in dirs if self.excluded.search(dir)]

            for dir in dirs:
                relative_path = os.path.join(base, dir)[self.rel_path_start:]
                self.relative_paths.append(relative_path)

    def dir_selected(self, selected_index):
        print selected_index
