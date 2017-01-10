# -*- encoding: utf-8 -*-
import sublime, sublime_plugin
import os

def md(*args): sublime.message_dialog(' '.join([str(arg) for arg in args]))

def user_friendly(path):
    path = computer_friendly(path)
    return path.replace(os.path.expanduser('~'), '~').replace(os.path.sep, '/')

def get_settings():
    return sublime.load_settings('BetterSnippetManager.sublime-settings')

def computer_friendly(path):
    """Also makes sure the path is valid"""
    if '~' in path:
        path = path[path.rfind("~"):]
    if ':' in path:
        path = path[path.rfind(':')-1:]
    path = path.replace('~', os.path.expanduser('~'))
    path = path.replace('/', os.path.sep)
    return path

template = """<snippet>
    <content><![CDATA[
%s
]]></content>
    <tabTrigger>%s</tabTrigger>
    <scope>%s</scope>
    <description>%s</description>
</snippet>
"""

class BetterSnippetManagerEditCommand(sublime_plugin.WindowCommand):

    """List every snippet in the User folder"""

    def __list_all_snippets(self, path, all_snippets):
        if path is None: path = self.SNIPPETS_PATH
        for item in os.listdir(path):
            if os.path.isdir(os.path.join(path, item)):
                self.__list_all_snippets(os.path.join(path, item),
                                         all_snippets)
            elif os.path.splitext(item)[1] == '.sublime-snippet':
                all_snippets.append(
                    os.path.join(path, item) \
                        .replace(self.SNIPPETS_PATH, '') \
                        .replace(os.path.sep, '/')[1:])
        return all_snippets

    def on_done(self, index):
        if index == -1:
            return self.window.run_command('close')
        path = os.path.join(self.SNIPPETS_PATH, self.all_snippets[index])
        self.window.open_file(path)

    def on_highlighted(self, index):
        path = os.path.join(self.SNIPPETS_PATH, self.all_snippets[index])
        self.window.open_file(path, sublime.TRANSIENT)

    def run(self):
        snippets_folder = get_settings().get('snippets_folder')
        self.SNIPPETS_PATH = os.path.join(sublime.packages_path(), 'User')
        if snippets_folder:
            self.SNIPPETS_PATH = os.path.join(self.SNIPPETS_PATH,
                                              snippets_folder)

        self.all_snippets = self.__list_all_snippets(self.SNIPPETS_PATH, [])
        self.window.show_quick_panel(self.all_snippets, self.on_done, 0, 0,
                                     self.on_highlighted)

class BetterSnippetManagerCreateCommand(sublime_plugin.TextCommand):

    def escape(self, string):
        return string.replace('<', '&gt;').replace('>', '&lt;')

    def run(self, edit):
        v = self.view
        sels = v.sel()

        self.window = v.window()
        self.scopes = v.scope_name(sels[0].begin()).strip()
        self.snippet_content = "\n".join([v.substr(region) for region in sels])
        self.window.show_input_panel('Trigger: ', '', self.set_trigger, None,
                                     None)

    def set_trigger(self, trigger):
        self.trigger = self.escape(trigger)
        self.window.show_input_panel('Description: ', '', self.set_description,
                                     None, None)

    def set_description(self, description):
        self.description = self.escape(description)
        scopes = self.scopes.replace(' ', ', ')
        self.window.show_input_panel('Scope: ', scopes, self.set_scopes,
                                            None, None)
        sel = view.sel()
        sel.clear()
        sel.add(sublime.Region(0, len(self.scopes.split(' ', 1)[0])))
        view.run_command('invert_selection')

    def set_scopes(self, scopes):
        self.scopes = self.escape(scopes)
        folder = self.scopes.split(' ')[0].split('.')[-1]
        view = self.window.show_input_panel('Folder: ', folder,
                                            self.set_folder, None, None)

    def set_folder(self, folder):
        self.folder = folder
        self.ask_file_name()

    def ask_file_name(self):
        input_view = self.window.show_input_panel('File Name: ',
                                                  self.trigger \
                                                    + '.sublime-snippet',
                                                  self.make_snippet, None,
                                                  None)
        sel = input_view.sel()
        sel.clear()
        sel.add(sublime.Region(0, len(os.path.splitext(os.path.basename(
                                        self.trigger))[0])))

    def make_snippet(self, file_name):
        file_path = os.path.join(sublime.packages_path(), 'User',
                                 get_settings().get('snippets_folder') or '',
                                 computer_friendly(self.folder), file_name)

        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))

        snippet_content = template % (self.snippet_content, self.trigger,
                                  self.scopes, self.description)
        if int(sublime.version()) >= 3000:
            # escape $ because it's inserting a *snippet*, not just simple
            # content. Thanks to #2
            self.window.run_command('open_file', {
                'file': file_path,
                'contents': snippet_content.replace('\\', '\\\\').replace('$', '\\$')
            })
        else:
            if os.path.exists(file_path):
                if not sublime.ok_cancel_dialog('Override %s?' % file_name):
                    return self.ask_file_name()
            with open(file_path, 'wb') as file:
                file.write(bytes(snippet_xml))
            self.window.open_file(file_path)
