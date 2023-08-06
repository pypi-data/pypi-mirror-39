#
#     SOFTWARE HISTORY
#
#    Date            Ticket#       Engineer       Description
#    ------------    ----------    -----------    --------------------------
#    09/10/14         #3623        randerso       Manually created, do not regenerate
#


class DeactivateSiteRequest(object):

    def __init__(self, siteID=None, plugin=None):
        self.siteID = siteID
        self.plugin = plugin

    def getSiteID(self):
        return self.siteID

    def setSiteID(self, siteID):
        self.siteID = siteID

    def getPlugin(self):
        return self.plugin

    def setPlugin(self, plugin):
        self.plugin = plugin
