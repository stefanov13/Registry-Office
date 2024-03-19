def extra_context_details_view(curr_object):
    doc_files = [
            curr_object.first_document_file,
            curr_object.second_document_file, 
            curr_object.third_document_file,
        ]
        
    extra_context = []
    names = {
        'first_document_file': 'Първи Документ',
        'second_document_file': 'Втори Документ',
        'third_document_file': 'Трети Документ',
        }

    for x in doc_files:           
        try:
            extra_context.append({'url': x.url, 'name': names[x.field.name]})
        except ValueError:
            continue

    return extra_context
