# Quick File Creator plugin for Sublime Text 2

Plugin to quickly create a file in a directory of your choosing.

Normally, to create a file in ST2, you open a new tab and click "Save" or "Save As". Then you have to locate the directory where you want to save the file using the standard system dialog, which often starts in a directory completely unrelated to your project...

This plugin, on the other hand, presents you with a quick panel showing all the directories in your project (determined by the (first) root directory in your side panel) and lets you select a directory from the list using the standard fuzzy filtering feature of ST2. If you are currently editing a file, the directory containing that file is located at the top of the list to make it even easier to save the new file in the same directory. When you have selected a directory, you are prompted to input the file name, and that's it!

## Excluded directories

Some directories, such as those named "tmp" or ".git", are excluded by default in order to make the directory listing easier to navigate. You can override this setting by specifying a list of regular expressions in your preferences (it might be a good idea to copy the one in SublimeQuickFileCreator.sublime-settings and modify it).

Note that each pattern is anchored to the beginning and end of the directory name, so you should not use ^ or $ in your patterns.

Example setting:

    {
      "excluded_dir_patterns": [
        "tmp", ".git", ".svn"
      ]
    }