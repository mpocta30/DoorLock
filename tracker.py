from doorlock import DoorLock
from flask import Flask, request, make_response
from flask_restful import Resource, Api
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
api = Api(app, prefix="/tracker")
auth = HTTPBasicAuth()

USER_DATA = {
    "admin": "SuperSecretPwd"
}

@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password


class OpenDoor(Resource):
    @auth.login_required
    def post(self):
        global lock

        # If door is locked and phone comes close to lock
        if not lock.open:
            lock.moveServo(200, 100, -1)
            lock.open = True
        
            return make_response("Open!", 201)
        else:
            return make_response("Door is already open!", 503)


class CloseDoor(Resource):
    @auth.login_required
    def post(self):
        global lock

        if lock.open:
            lock.moveServo(100, 200, 1)
            lock.open = False

            return make_response("Closed!", 201)
        else:
            return make_response("Door is already closed!", 503)



api.add_resource(OpenDoor, '/open')
api.add_resource(CloseDoor, '/close')


# Global Lock class variable
lock = DoorLock()


# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    try:
        app.run(debug=False, host='0.0.0.0', port=1024)
    except:
        print("\nThanks for trying our Lock!")

	
