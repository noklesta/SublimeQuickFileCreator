# Quick File Creator plugin for Sublime Text 2

Plugin to quickly create a file or a subdirectory using ST2's fuzzy filtering feature.

Normally, in order to create a file or directory in ST2, you navigate to the directory in the side panel, right click on the directory and choose "New File" or "New Folder". Alternatively, you can create a new file by opening a new tab and clicking "Save" or "Save As". Then you have to locate the directory where you want to save the file using the standard system dialog (which may start in a directory completely unrelated to your project if you don't have any files already opened).

This plugin, on the other hand, presents you with a quick panel showing all the directories in your project (determined by the (first) root directory in your side panel) and lets you select a directory from the list using the standard fuzzy filtering feature of ST2. If you are currently editing a file, the directory containing that file is located at the top of the list to make it even easier to create the new file or subdirectory in the same directory. When you have selected a directory, you are prompted to input the file or subdirectory name, and that's it!

## Installation

### Package Control

The easiest way to install this is with [Package
Control](http://wbond.net/sublime\_packages/package\_control).

 * If you just went and installed Package Control, you probably need to restart Sublime Text 2 before doing this next bit.
 * Bring up the Command Palette (Command+Shift+p on OS X, Control+Shift+p on Linux/Windows).
 * Select "Package Control: Install Package" (it'll take a few seconds)
 * Select Quick File Creator when the list appears.

Package Control will automatically keep Quick File Creator up to date with the latest
version.

### Clone from GitHub

Alternatively, you can clone the repository directly from GitHub into your Packages directory:

    git clone http://github.com/noklesta/SublimeQuickFileCreator

## Key bindings

The plugin does not install any key bindings automatically. You can set up
your own key bindings like this:

    { "keys": ["super+ctrl+n"], "command": "quick_create_file" },
    { "keys": ["super+ctrl+d"], "command": "quick_create_directory" }

If you are using Vintage mode and want to use sequences of non-modifier keys,
you can restrict the key bindings to command mode like this:

    { "keys": [" ", "n"], "command": "quick_create_file", "context": [{"key": "setting.command_mode"}] },
    { "keys": [" ", "d"], "command": "quick_create_directory", "context": [{"key": "setting.command_mode"}] }

## Excluded directories

Some directories, such as those named "tmp" or ".git", are excluded by default in order to make the directory listing easier to navigate. You can override this setting by specifying a list of regular expressions in your preferences (it might be a good idea to copy the one in SublimeQuickFileCreator.sublime-settings and modify it).

Note that each pattern is anchored to the beginning and end of the directory name, so you should not use ^ or $ in your patterns.

Example setting:

    {
      "excluded_dir_patterns": [
        "tmp", ".git", ".svn"
      ]
    }

## Future work
As far as I have been able to establish, ST2 does not currently support programmatically selecting a directory in the side bar (please correct me if I'm wrong!). If ST2 includes this ability in the future, I will make any newly created subdirectories become immediately selected in the side bar.

## Licence

All of SublimeQuickFileCreator is licensed under the MIT licence.

  Copyright (c) 2012 Anders Nøklestad

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.