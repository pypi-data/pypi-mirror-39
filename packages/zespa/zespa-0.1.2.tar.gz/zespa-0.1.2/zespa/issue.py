class Issue:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id', 0)  # GitHub issue id
        self.estimate = kwargs.get('estimate', 0)  # ZenHub Estimate Point
        self.labels = kwargs.get('labels', [])   # GitHub labels
        self.title = None  # GitHub issue title

    def __str__(self):
        return f'ID: {self.id}, Title: {self.title}, Estimate: {self.estimate}, Labels: {self.labels}'
