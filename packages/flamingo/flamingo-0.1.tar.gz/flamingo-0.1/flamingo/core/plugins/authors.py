import os


class Authors:
    def contents_parsed(self, context):
        content_key = getattr(context.settings, 'I18N_CONTENT_KEY', 'id')

        for content in context.contents:
            if not content['authors']:
                content['authors'] = []

            else:
                content['authors'] = [a.strip()
                                      for a in content['authors'].split(',')]

        authors = sum(context.contents.values('authors'), [])

        # gen author pages
        for author in authors:
            output = os.path.join('authors/{}.html'.format(author))

            context.contents.add(**{
                content_key: '_author/{}'.format(author),
                'output': output,
                'url': '/' + output,
                'author': author,
                'template': 'author.html',
            })

        # gen author list
        context.contents.add(**{
            content_key: '_authors',
            'output': 'authors.html',
            'url': '/authors.html',
            'authors': authors,
            'template': 'authors.html',
        })
