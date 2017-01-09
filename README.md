# Better Snippet Manager

You can list all your snippets (even in infinite sub-folders, they're listed in one panel, for quick access)
You can create some snippet interactively.

The two command are available in the command palette.

## Usage

You can create a new snippet by selecting up in the command palette `BetterSnippetManager: Create New Snippet`.

It's going to ask you different *snippet specific* questions: the `trigger`, the `description`, the `scope`.

If you're not aware of any of them, I strongly recommend having a look at [the community powered unofficial documentation][snippets-doc]

In addition, it's also going to ask you the `folder` to save this snippet in, and the `file name` of you snippet.

The folder name is defined with the scope you're currently in. So, if you're writing `JSON`, it's going to propose you to save this in a `json` folder (because the scope is `source.json`). You can of course change this (note that if you put nothing in, it's going to put it at the root of your folder (in this case `User`)).

The `file name` has to have the extension `.sublime-snippet` to be taken into account by Sublime Text. So, it's added by default. The name alone is defined by the trigger you chose earlier in the process, but you can change this as well.

Once this is done, it'll create the snippet file, and open it in Sublime Text for you.

*The content of the snippet is the content of your selection when you created ran `BetterSnippetManager: Create New Snippet` (it can be empty, it's just a little trick)*

## All your snippets in one folder

If you're use to put all you snippets inside a folder, you can configure BetterSnippetManager take this into consideration when listing and creating your snippets.

You need to edit *BetterSnippetManager*'s settings (not your global ones). To do so, you can search up in the command palette `Preferences: BetterSnippetManager Settings`, or use the menus `Preferences → Packages Settings → BetterSnippetManager`.

In the *right* file, you can add this:

```json
"snippets_folder": "my_snippet_folder"
```

and, like this, BetterSnippetManager will go straight into this folder (so don't list the snippet outside of it, which shouldn't be a problem).

## Installation

Because it is not available on package control for now, you have to add this repo "manually" to your list.

### Using package control

1. Open up the command palette (`ctrl+shift+p`), and find `Package Control: Add Repository`. Then enter the URL of this repo: `https://github.com/math2001/BetterSnippetManager` in the input field.
2. Open up the command palette again and find `Package Control: Install Package`, and just search for `BetterSnippetManager`. (just a normal install)

### Using the command line

```bash
cd "%APPDATA%\Sublime Text 3\Packages"             # on window
cd ~/Library/Application\ Support/Sublime\ Text\ 3 # on mac
cd ~/.config/sublime-text-3                        # on linux

git clone "https://github.com/math2001/BetterSnippetManager"
```

> Which solution do I choose?

It depends of your needs:

- If you intend to just use BetterSnippetManager, then pick the first solution (Package Control), **you'll get automatic update**.
- On the opposite side, if you want to tweak it, use the second solution. Note that, to get updates, you'll have to `git pull`

[snippets-doc]: http://docs.sublimetext.info/en/latest/extensibility/snippets.html
