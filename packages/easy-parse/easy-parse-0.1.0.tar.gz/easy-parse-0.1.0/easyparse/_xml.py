import json
import xml.sax


class XmlToJsonHandler(xml.sax.ContentHandler):

    def __init__(self):
        """
        Initialize necessary parsing state variables
        """
        self._json_dict = {}
        self._pointer_path = []

        self._depth_dict_counts = {}
        self._current_depth = 0
        self._was_last_tag_end = False
        self._current_content = ''


        self._ATTRIBUTE_PREFIX = '@'
        self._CONTENT_PREFIX = '#text'

    def startElement(self, tag, attributes):
        """
        Hook method called during start tags
        """
        self._current_depth += 1
        if self._current_depth - 1 not in self._depth_dict_counts:
            self._depth_dict_counts[self._current_depth - 1] = {}
        if tag not in self._depth_dict_counts[self._current_depth - 1]:
            self._depth_dict_counts[self._current_depth - 1][tag] = 1
        else:
            self._depth_dict_counts[self._current_depth - 1][tag] += 1
        self._pointer_path.\
            append([tag, int(self._depth_dict_counts[self._current_depth - 1]
                                                    [tag])-1])
        self._was_last_tag_end = False
        self._init_with_pointer_path()
        self._add_attributes_with_pointer_path(attributes.items())

    def endElement(self, tag):
        """
        Hook method called during end tags
        """
        if len(self._current_content) != 0:
            self._assign_with_pointer_path(self._current_content)
            self._current_content = ''
        if self._was_last_tag_end:
            del self._depth_dict_counts[len(self._depth_dict_counts) - 1]
        self._pointer_path.pop()
        self._was_last_tag_end = True
        self._current_depth -= 1

    def characters(self, content):
        """
        Hook method called between tags
        """
        self._current_content += str(content).strip()

    def _init_with_pointer_path(self):
        """
        Initializes or updates the current node
        """
        assignment_string = 'self._json_dict'
        for key_tuple in self._pointer_path[:-1]:
            assignment_string += '["' + key_tuple[0] + '"]' \
                if key_tuple[1] == 0 \
                else '["' + key_tuple[0] + '"][' + str(key_tuple[1]) + ']'
        assignment_string += '["' + self._pointer_path[-1][0] + '"]'
        if self._pointer_path[-1][1] == 0:
            assignment_string += '= {}'
        elif self._pointer_path[-1][1] == 1:
            assignment_string += \
                ' = [str(' + assignment_string + ') if isinstance(' \
                + assignment_string + ', str) else dict(' + assignment_string \
                + '), {}]'
        else:
            assignment_string += '.append({})'

        exec(assignment_string)

    def _add_attributes_with_pointer_path(self, attribute_pairs):
        """
        Add attributes at the current node
        """
        if len(attribute_pairs) == 0:
            return()

        attr_dict = {}
        assignment_string = 'self._json_dict'
        for key_tuple in self._pointer_path[:-1]:
            assignment_string += \
                '["' + key_tuple[0] + '"]' \
                if key_tuple[1] == 0 \
                else '["' + key_tuple[0] + '"][' + str(key_tuple[1]) + ']'
        assignment_string += '["' + self._pointer_path[-1][0] + '"]'

        exec('global attr_dict; attr_dict = {}')
        for key, value in attribute_pairs:
            exec('attr_dict["' + self._ATTRIBUTE_PREFIX + '" + "' + key
                 + '"] = "' + value + '"')

        if self._pointer_path[-1][1] == 0:
            assignment_string += ' = dict(' + str(attr_dict) + ')'
        elif self._pointer_path[-1][1] == 1:
            assignment_string += ' = [dict(' + assignment_string \
                + '[0]), dict(' + str(attr_dict) + ')]'
        else:
            assignment_string += '[len(' + assignment_string + ')-1] = dict(' \
                + str(attr_dict) + ')'

        exec(assignment_string)

    def _assign_with_pointer_path(self, content):
        """
        Add content at the current node
        """
        assignment_string = 'self._json_dict'
        for key_tuple in self._pointer_path[:-1]:
            assignment_string += \
                '["' + key_tuple[0] + '"]' \
                if key_tuple[1] == 0 \
                else '["' + key_tuple[0] + '"][' + str(key_tuple[1]) + ']'
        assignment_string += '["' + self._pointer_path[-1][0] + '"]'

        is_empty = None
        exec('global is_empty; is_empty = len(' + assignment_string + ') == 0')
        if self._pointer_path[-1][1] == 0:
            if not is_empty:
                assignment_string += '["' + self._CONTENT_PREFIX + '"]'
            assignment_string += ' = str(content)'
        elif self._pointer_path[-1][1] == 1:
            if is_empty:
                assignment_string += \
                    ' = [dict(assignment_string), str(content)]'
            else:
                assignment_string += \
                    '[1]["' + self._CONTENT_PREFIX + '"]  = str(content)'
        else:
            if is_empty:
                assignment_string += '.append(str(content))'
            else:
                assignment_string += '[len(' + assignment_string + ')-1]["' \
                    + self._CONTENT_PREFIX + '"]  = str(content)'

        exec(assignment_string)

    def get_json_dict(self):
        return(self._json_dict)


def xml_to_json(xml_input_path, json_output_path):
    """
    Utilizes the xml parser to convert the given xml to json
    """
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    xml_handler = XmlToJsonHandler()
    parser.setContentHandler(xml_handler)
    parser.parse(xml_input_path)

    with open(json_output_path, 'w') as f:
        json.dump(xml_handler.get_json_dict(), f)
