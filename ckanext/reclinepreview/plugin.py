from logging import getLogger

import ckan.plugins as p
import ckan.plugins.toolkit as toolkit

log = getLogger(__name__)

interesting_formats = ['csv', 'xls', 'tsv']

class ReclinePreview(p.SingletonPlugin):
    """This extension previews resources using recline

    This extension implements two interfaces

      - ``IConfigurer`` allows to modify the configuration
      - ``IResourcePreview`` allows to add previews
    """
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IResourcePreview, inherit=True)
    p.implements(p.IConfigurable, inherit=True)

    def update_config(self, config):
        ''' Set up the resource library, public directory and
        template directory for the preview
        '''
        toolkit.add_public_directory(config, 'theme/public')
        toolkit.add_template_directory(config, 'theme/templates')
        toolkit.add_resource('theme/public', 'ckanext-reclinepreview')

    def configure(self, config):
        formats = toolkit.aslist(
            config.get('ckanext.reclinepreview.formats', interesting_formats))
        self.interesting_formats = set(interesting_formats) & set(formats) 
        
    def can_preview(self, data_dict):
        # if the resource is in the datastore then we can preview it with recline
        if data_dict['resource'].get('datastore_active'):
            return True
        format_lower = data_dict['resource']['format'].lower()
        return format_lower in self.interesting_formats 

    def preview_template(self, context, data_dict):
        return 'recline.html'
