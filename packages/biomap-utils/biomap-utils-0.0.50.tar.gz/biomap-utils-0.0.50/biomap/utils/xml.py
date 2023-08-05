def xml_to_json(root, tag_prefix=None, on_tag={}):
    '''
    Parses a XML element to JSON format.

    This is a relatively generic function parsing a XML element
    to JSON format. It does not guarantee any specific formal
    behaviour but is empirically known to "work well" with respect
    to the author's needs. External verification of the returned
    results by the user is therefore instrumental.

    For bigger XML elements the whole procedure may take a while,
    so the philosophy should be to save the laboriously mapped
    JSON data structure to a file once you have it. This of course
    also means that this functions is probably of little value
    when you have to constantly JSONify big XMLs. In summary,
    this function is mostly useful for one-time parsing of XML to
    JSON for subsequent use of the resulting JSON data instead of
    the XML-formated data.

    Args:
        root: A XML element
        tag_prefix: A tag prefix which will be cut from the keys
        on_tag: User-defined parsing for elements identified by tag

    Returns:
        A Python data structure corresponding to the JSON mapping
        of the supplied XML element
    '''

    def get_key(tag):
        if tag_prefix is not None:
            return tag.split(tag_prefix)[1]
        return tag

    def parse_element(elmt):
        key = get_key(elmt.tag)

        if key in on_tag:
            return on_tag[key](elmt)

        items = dict(elmt.items())
        if len(elmt) == 0:
            if items:
                return { **items, **{key : elmt.text} }
            else:
                return elmt.text
        else:
            tags = {child.tag for child in elmt}
            max_children = max({len(child) for child in elmt})
            if len(tags) == 1:
                value_list = [parse_element(child) for child in elmt]
                if items:
                    return { **items, **{key : value_list} }
                else:
                    return value_list
            elif len(tags) > 1:
                tag2children = {tag: [] for tag in tags}
                for child in elmt:
                    tag2children[child.tag].append(child)

                if max_children == 0:
                    value_dict = {get_key(tag) : [child.text for child in children] if len(children) > 1
                                                 else children[0].text
                                                 for tag, children in tag2children.items()}
                else:
                    value_dict = {get_key(tag) : [parse_element(child) for child in children] if len(children) > 1
                                                 else parse_element(children[0])
                                                 for tag, children in tag2children.items()}
                if items:
                    return { **items, **value_dict }
                else:
                    return value_dict

    # ---
    return parse_element(root)
