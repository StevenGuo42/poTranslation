import polib
import click


from tqdm import tqdm

from .core import Translator




class CLIHandler:
    def __init__(self, args):
        

        try:
            self.po = polib.pofile(args["po_file_path"])
        except Exception as e:
            raise ValueError(f"Error: Can't PO file: {e}")
        
        if not args["dest_language"]:
            # get dest_language from the PO file
            dest_language = self.po.metadata.get('Language')
            if not dest_language:
                raise ValueError("Error: Destination language is not specified.")

        self.translator = Translator(dest_language, args["source_language"], args["lang"], args["env_path"])
        self.args = args

    def handle_translation(self):
        

        
        if self.args["force"]:
            entries = self.po
        else:
            entries = self.po.untranslated_entries()
            
        if not self.args["verbose"] and not self.args["quiet"]:
            entries = tqdm(entries, desc='Translating', unit='entry')
        
        for entry in entries:
            text_to_translate = entry.msgid
            translated_text, error = self.translator.translate(text_to_translate)
            if error and not self.args["quiet"]:
                print(f"Error: Can't translate '{text_to_translate}': {error}")
            else:
                entry.msgstr = translated_text
                if self.args["verbose"] and not self.args["quiet"]:
                    print(f"Translated '{text_to_translate}' to '{translated_text}'")
        if self.args["write"]:
            self.po.save(self.args["po_file_path"])
            if not self.args["quiet"]:
                print(f"Translation complete. Updated PO file saved at: {self.args['po_file_path']}")
        else:
            if not self.args["quiet"]:
                print("Translation complete. PO file NOT saved.")



CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'], 
                        show_default=True,
                        max_content_width=120,)

@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-s', '--source-language', default='en', help='Source language for translation.', type=str)
@click.option('-d', '--dest-language', help='Destination language for translation.  [default: (load from .po file)]', type=str)
@click.option('-l', '--lang', default='python', help='Programming langrage of formatted string.', type=str)
@click.option('-f', '--file', 'out_file_path', help='Path to the output file.  [default: {po_file_path}]', type=click.Path())
@click.option('-e', '--env', 'env_path', help='Path to the env file.  [default: (load from cwd and parent dir)]', type=click.Path())
@click.option('-F', '--force', is_flag=True, help='Force translation of all entries.')
@click.option('-v', '--verbose', is_flag=True, help='Enable verbose output.')
@click.option('-q', '--quiet', is_flag=True, help='Suppress output.')
@click.option('-w', '--write', is_flag=True, default=True, help='Write to the file.')
@click.argument('po_file_path', type=click.Path(exists=True))
def translate(po_file_path, source_language, dest_language, lang, out_file_path, env_path, force, verbose, quiet, write):
    """This command translates a PO file."""
    
    args = click.get_current_context().params  # Get all command line parameters
    args['po_file_path'] = po_file_path
    cli_handler = CLIHandler(args)  # Initialize your CLIHandler with the provided arguments
    cli_handler.handle_translation()  # Call the translation handler

if __name__ == '__main__':
    cli()