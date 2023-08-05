# Copyright (c) 2018, Vienna University of Technology (TU Wien), Department
# of Geodesy and Geoinformation (GEO).
# All rights reserved.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL VIENNA UNIVERSITY OF TECHNOLOGY,
# DEPARTMENT OF GEODESY AND GEOINFORMATION BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


class FilenameObj(object):
    def __init__(self, attributes):
        for key, value in attributes.items():
            setattr(self, key, value)


class SmartFilename(object):

    """
    SmartFilename class handles file names with pre-defined field names
    and field length.
    """

    def __init__(self, fields, fields_def, ext=None, pad='-', delimiter='_'):
        """
        Define name of fields, length, pad and delimiter symbol.

        Parameters
        ----------
        fields : dict
            Name of fields (keys) and (values).
        field_def : OrderedDict
            Name of fields (keys) in right order and length (values).
        ext : str, optional
            File name extension (default: None).
        pad : str, optional
            Padding symbol (default: '-').
        delimiter : str, optional
            Delimiter (default: '_')
        """
        self.fields = fields
        self.fields_def = fields_def
        self.ext = ext
        self.delimiter = delimiter
        self.pad = pad
        self._check_def()
        self.obj = FilenameObj(self.fields)
        self.full_string = self._build_fn()


    def _check_def(self):
        """
        Check if fields names and length comply with definition.

        """
        for key, value in self.fields.items():
            if key in self.fields_def:
                if len(value) > self.fields_def[key]['len']:
                    raise ValueError("Length does not comply with "
                                     "definition: {:} > {:}".format(
                                         len(value), self.fields_def[key]['len']))
                if 'delim' not in self.fields_def[key].keys():
                    self.fields_def[key]['delim'] = True
            else:
                raise KeyError("Field name undefined: {:}".format(key))


    def _build_fn(self):
        """
        Build file name based on fields, padding and length.

        Returns
        -------
        filename : str
            Filled file name.

        """
        filename = ''
        for name, keys in self.fields_def.items():

            length = keys['len']
            delimiter = self.delimiter if keys['delim'] else ''

            if name in self.fields:
                if filename == '':
                    filename = self.fields[name].ljust(length, self.pad)
                else:
                    filename += delimiter + \
                        self.fields[name].ljust(length, self.pad)
            else:
                if filename == '':
                    filename = self.pad * length
                else:
                    filename += delimiter + self.pad * length

        if self.ext is not None:
            filename += self.ext

        return filename


    def get_field(self, key):
        '''
        Returns the string of the field with given key.

        Parameters
        ----------
        key : str
            name of the field

        Returns
        -------
        str
            part of the filename associated with given key

        '''
        field = self.fields[key]
        field_obj = getattr(self.obj, key)
        if (field_obj != field) and (len(field_obj) <= self.fields_def[key]['len']):
            field = field_obj
            self[key] = field

        return field.replace(self.pad, '')


    def __getitem__(self, key):

        return self.get_field(key)


    def __setitem__(self, key, value):

        if key in self.fields_def:
            if len(value) > self.fields_def[key]['len']:
                raise ValueError("Length does not comply with "
                                 "definition: {:} > {:}".format(
                                     len(value), self.fields_def[key]['len']))
            else:
                self.fields[key] = value
                setattr(self.obj, key, value.replace(self.pad, ''))
        else:
            raise KeyError("Field name undefined: {:}".format(key))


    def __repr__(self):

        return self._build_fn()
