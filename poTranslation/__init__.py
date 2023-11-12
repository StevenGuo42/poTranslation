import polib
import click
import os

from tqdm import tqdm

from poTranslation.core import Translator




class CLIHandler:
    def __init__(self, args):
        self.po_file_path = args['po_file_path']
        self.source_language = args['source_language']
        self.locale = args['dest_language'] # dest_language is renamed to locale
        self.lang = args['lang']
        self.out_path = args['out_path']
        self.env_path = args['env_path']
        self.directory = args['directory']
        self.domain = args['domain']
        self.force = args['force']
        self.verbose = args['verbose']
        self.quiet = args['quiet']
        self.write = args['write']
        
        if self.quiet and self.verbose:
            raise ValueError("Error: Can't be both quiet and verbose.")
        
        
        if not self.po_file_path and not self.directory:
            raise ValueError("Error: PO file <path> or <directory> is not specified.")
        
        if self.po_file_path and not self.quiet:
            print(f"Translating PO file: '{self.po_file_path}'", end="")
        if self.directory:
            if self.po_file_path:
                raise ValueError("Error: PO file <path> and <directory> cannot be specified at the same time.")
            if self.out_path:
                raise ValueError("Error: <out_path> cannot be specified when <directory> is specified.")
            
            if not self.locale and not self.quiet:
                print("Iterating through all <locale> directory in <directory>.")
            if not self.domain and not self.quiet:
                print("Iterating through all '<domain>.po' file in '<locale>/LC_MESSAGES'")
            if not self.quiet:
                print(f"Translating PO files in {self.directory}", end="")
                
        if not self.source_language:
            raise ValueError("Error: Source language is not specified.")
        


        
        
        
        
        

    def handle_translation(self):
        if self.po_file_path:
            self.translation_helper(self.po_file_path)
        

        elif self.directory:
            path = []

            if self.locale:
                path.append(os.path.join(self.directory, self.locale, 'LC_MESSAGES'))
            else:
                for dirname in os.scandir(self.directory): # iterate through all <locale> dir
                    if dirname.is_dir():
                        path.append(os.path.join(dirname.path, 'LC_MESSAGES'))


            new_path = []
            
            for i, p in enumerate(path):
                if self.domain:
                    path[i] = os.path.join(p, self.domain + '.po')
                else:          
                    for filename in os.scandir(p): # iterate through all <domain> file
                        if filename.is_file() and filename.name.endswith('.po'):
                            new_path.append(os.path.join(p, filename.name))
                    path = new_path
            
            for p in path:
                self.translation_helper(p)
            

        
        


    def translation_helper(self, path):

        try:
            po = polib.pofile(path)
        except Exception as e:
            raise ValueError(f"Error: Can't PO file '{path}': {e}")
        
        
        dest_language = po.metadata.get('Language')

        if dest_language:
            if self.locale and dest_language != self.locale:
                if not self.quiet:
                    print(f"Warning: User specified locale '{self.locale}' is "
                          f"different from PO file locale '{dest_language}'.")
                dest_language = self.locale # user override
        else: 
            if self.locale:
                dest_language = self.locale
            else:
                raise ValueError(f"Error: Destination language is not specified"
                                 f" and can't be loaded from PO file '{path}'.")
                
        
        translator = Translator(dest_language, self.source_language, self.lang, self.env_path)
        
        
        if not self.quiet:
            print(f" using '{translator.service}' service ", end="")
            if self.directory:
                print(f"\nTranslating PO file: '{os.path.basename(path)}' ", end="")
            print(f"from '{self.source_language}' to '{dest_language}'")
        
        
        if self.force:
            entries = po
        else:
            entries = po.untranslated_entries()
            
        if not self.verbose and not self.quiet:
            entries = tqdm(entries, desc='Translating', unit='entries')
        
        for entry in entries:
            text_to_translate = entry.msgid
            translated_text, error = translator.translate(text_to_translate)
            if error and not self.quiet:
                print(f"Error: Can't translate '{text_to_translate}': {error}")
            else:
                entry.msgstr = translated_text
                if self.verbose and not self.quiet:
                    print(f"Translated '{text_to_translate}' to '{translated_text}'")
        
        if self.write:
            save_path = ''
            if self.out_path:
                save_path = self.out_path
            elif self.po_file_path or self.directory:
                save_path = path
            else:
                raise ValueError("Error: Can't determine save path.")
            
            po.save(save_path)
            
            if not self.quiet:
                print(f"Translation complete. Updated PO file saved at: '{save_path}'")
        else:
            if not self.quiet:
                print("Translation complete. PO file NOT saved.")
        

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'], 
                        show_default=True,
                        max_content_width=120,)

@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('po_file_path', default='', type=click.Path())
# @click.argument('source-language', default='en', type=str)
# @click.argument('dest-language', default='', type=str)
@click.option('-s', '--source_language', default='en', 
              help='Translate from (language).', type=str)
@click.option('-l', '--locale', 'dest_language', 
              help='Translate to (language).  [default: (load from .po file)]', type=str)
@click.option('-L', '--lang', default='python', 
              help='Programming langrage of formatted string.', type=str)
@click.option('-o', '--output', 'out_path', 
              help='Path to the output file.  [default: {po_file_path}]', type=click.Path())
@click.option('-e', '--env', 'env_path', 
              help='Path to the env file.  [default: (load from cwd and parent dir)]', type=click.Path())
@click.option('-d', '--directory', 
              help='Directory of the PO files.', type=click.Path())
@click.option('-D', '--domain', 
              help='Domain of the PO file.', type=str)
@click.option('-F', '--force', is_flag=True, help='Force translation of all entries.')
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose output.')
@click.option('-q', '--quiet', is_flag=True, help='Suppress output.')
@click.option('-w', '--write', is_flag=True, default=True, help='Write to the file.')
def translate(po_file_path, source_language, dest_language, lang, out_path, env_path, directory, domain, force, verbose, quiet, write):
    """
    This command translates a PO file.\n
    If directory is specified, default file path is <directory>/<locale>/LC_MESSAGES/<domain>.mo
    """
    
    args = click.get_current_context().params  # Get all command line parameters
    args['po_file_path'] = po_file_path
    cli_handler = CLIHandler(args)  # Initialize your CLIHandler with the provided arguments
    cli_handler.handle_translation()  # Call the translation handler

if __name__ == '__main__':
    translate()