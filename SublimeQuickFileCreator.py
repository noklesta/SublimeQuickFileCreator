import os
import re
import sublime
import sublime_plugin


class QuickCreateFileCommand(sublime_plugin.WindowCommand):
    def run(self):
        root = self.find_root()
        if not root:
            sublime.error_message('Could not find project root')
            return False

        start_index = len(root) + 1

        settings = sublime.load_settings("SublimeQuickFileCreator.sublime-settings")
        excluded = re.compile('^' + '|'.join(settings.get('excluded_dir_patterns')) + '$')

        relative_paths = ['.']
        for base, dirs, files in os.walk(root):
            [dirs.remove(dir) for dir in dirs if excluded.search(dir)]

            for dir in dirs:
                relative_path = os.path.join(base, dir)[start_index:]
                relative_paths.append(relative_path)

        self.window.show_quick_panel(relative_paths, self.dir_selected)

    def find_root(self):
        folders = self.window.folders()
        if len(folders) == 0:
            return False
        else:
            return folders[0]

    def dir_selected(self, selected_index):
        print selected_index
