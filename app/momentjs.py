from jinja2 import Markup


class momentjs(object):
    """ create a wrapper for moment.js that we can invoke from the templates """
    def __init__(self, timestamp):
        self.timestamp = timestamp

    def render(self, format):
        """ Returns a string that Moment.js can parse and work with.
            Wrapping the string in a Markup object tells Jinja2
            that this string should not be escaped."""
        return Markup(
            "<script>\ndocument.write(moment(\"%s\").%s);\n</script>" %
            (self.timestamp.strftime("%Y-%m-%dT%H:%M:%S Z"), format))

    def format(self, fmt):
        return self.render("format(\"%s\")" % fmt)

    def calendar(self):
        return self.render("calendar()")

    def fromNow(self):
        return self.render("fromNow()")
