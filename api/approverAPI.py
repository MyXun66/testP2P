import app


class approverAPI():
    def __init__(self):
        self.approve_url = app.BASE_URL + '/member/realname/approverealname'
        self.getapprove_url = app.BASE_URL + '/member/member/getapprove'

    def approve(self, session, realname, cardId):
        data = {"realname": realname, "card_id": cardId}
        # 其中files={'x': 'y'}是为了构造多消息体x,y,没有实在意义
        response = session.post(self.approve_url, data=data, files={'x': 'y'})
        return response

    def getApprove(self, session):
        response = session.post(self.getapprove_url)
        return response