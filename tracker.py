from flask import Flask, request, make_response
from math import sqrt
from doorlock import DoorLock
import pprint

# Create the application instance
app = Flask(__name__)

first_lat = 37.70441666932894
first_lon = -77.39275739218024

# Global Lock class variable
lock = DoorLock()


@app.route('/tracker', methods=['POST'])
def tracker():
    global lock

    content = request.json
    coordinates = content['locations'][0]['geometry']['coordinates']

    latitude = coordinates[1]
    longitude = coordinates[0]

    distance = sqrt((latitude - first_lat)**2 + (longitude - first_lon)**2)
    print(distance)

    # If door is locked and phone comes close to lock
    if not lock.open and distance <= 10:
        lock.moveServo(200, 100, -1)
        lock.open = True
    elif lock.open and distance > 10:
        lock.moveServo(100, 200, 1)
        lock.open = False
    
    return make_response("Success", 201)

# If we're running in stand alone mode, run the application
if __name__ == '__main__':
    try:
        app.run(debug=True, host='0.0.0.0', port=1024)
    except:
        print("\nThanks for trying our Lock!")

	
