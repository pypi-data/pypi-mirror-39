def transform_date(date):
    index = date.find(' ')
    date = (date[:index] + 'T' + date[index+1:] +
            ":00.12345+00:00").replace(':','%3A').replace('+','%2B')
    return date


def transform_boolean(value):
    if value:
        return '1'
    else:
        return '0'


def transform_tone(tone):
    if 'negative':
        return '-1'
    elif 'neutral':
        return '0'
    else:
        return '1'
