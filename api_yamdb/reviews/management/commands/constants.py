MTM_MODELS = ['title_genre',]

APPS = [
    'users',
    'reviews',
        ]

PATH = 'static/data'

APPS_AND_MODELS = {
    'reviews': [
        'category',
        'genre',
        'title',
        'title_genre',
        'review',
        'comment', 
    ],
    'users': [
        'user',
        ]
}
