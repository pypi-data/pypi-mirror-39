class PerfectoExecutionContext:
    def __init__(self, webdriver, tags=None, job=None, project=None, customFields=[]):
        if webdriver is None:
            raise 'Missing required webdriver argument. Call your builder\'s withWebDriver() method'
        self.webdriver = webdriver
        self.job = job
        self.project = project
        self.context_tags = tags
        self.customFields = {}
        if (len(customFields) > 0):
            for cf in customFields:
                self.customFields.update(cf.dict)
