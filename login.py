import requests
import base64
import struct
from flask import Flask, request, jsonify

app = Flask(__name__)

PAYLOAD_B64 = "AgAAABlk4Ag/1npC4JfbDM8l6L8EUNk0+me89vLfv5ZingpyOOkgXXXyjPzYTzWmWSu+BYqcD47byirLZ++3dJccpF99hWppT7G5xAuU+y56WpSYsAQU5GoQpdEniUdbgJcWlPHIZLfXEy6oX9WFF+UKi4z6G1AUiCW91lY+etXrqj2omZ9m6gGrr7cnWVDBHNUsatg3VAgAAJJdt23gmZSlz9g/01jiaHgDvgKySfRB2wl3jy/GkYKu1JSzRSD/48w3ur0Zr6JPWOfMoBAvuCyoVOC7OakJ4yWtwxZ0M3vUHmCEHQCQW1KkuzqCcLPnCODAjrBxhv/mjW84H3p2XaKDpAAP3Prz7HWhMNxzvCZjJdObBaaUIFkXfR+2Eu0TZktJUUYuFsUclmxSEk9/fY+s9CtsqLr19YBiEZVijKKqr2hc5CmJ4WepNPt1wBL4F4SqWPsc6jflLoCqpZxqaEovCtVCS4cqY9QFtovIMvUM+7GymjsTt6jcUKDpLdziWSI/StP2J/byadd6SkHdzT5ajogBjd24zDDNrz/rFYy9IQDCxUZEDNIj7WGryyKrhaLVrgTu4vaqpbAwXI8GOaKbq1g/4pDc54MViHRxyUOrjKvjp7ULLsk4Usg0f0ZYD6KsmHp1CAmBXQwscm26CfLfx3kEwD6ZFS7kOvJaXgwi2jjN/7yszyxWss0Q8K2Ub/VIIxT2UVy7RPumG3Elx1pUuJCrN0LRqmQcqS7frA7/plp/iRi4fxxFM3laza8m9092xiZmrC6Sz3IsPyQRyNQi36NY5Y6KIB7Y2oLshTCYfrp1vJf/Tk9VzjLHuXG+qWU1bY7qWAkdDfNEghzxmG09cqEpHjLZnHmjxhqdRA52L0JPdiHdJo3aIgFLPY2EE4mlsT61ONSADyvd/CBUHhHcSxflyrMej85ogtDeR9RFA8V8D0sC3rmJF4t/9EQwhaPZDqIUsCX7RLFS+ywKSIgAHILILQImCBmdBROTGWDO/9lXCN2WmEtt4TSREj3qfXwGjiohyoUq+HJqLsw/6QbpMsbfK1ykPcOp/QeaPHCwvufYi0oTv2kSZurcKWXL+PLqMqhP6pd6R6v9tFy6UMsgVFfC0QR0V+lnyDVAp/KP1hudm6+ZOeItFRsY/kERtaPnn1yJntx095hfYHfJY+28BPLoBvrbZhXNlEzSiDNXdMAyu6gvpZt6QFIZakQN2OhQsqS52FLQBXHuiLu4MdoPA3jSvCk2vJGHPAJ1VRHCsFHhFZ/pIhc3xO0hnl4i7oVU3mGG05dm54+eUadJLE92ZyQczg5xhmtjO+DRY8QhEiMrWznw5Oer2WRtRh7Z7CxOBFJDNeYO1keD5IamRYOm0XND9RJbqbfq7nMbZc7fmZtEiXG2o4cNepobf3zY7GfRAZ7S3N60hSrVt+W/r+o+6hsBMbEQaq1pOa2PVjh1upDf3u7yNS47Dqhihe/1+MYdQVKEw27zZGnBT18ul1XBxR5sfUyshOrfMHEieRLFJOYxxxxRqL2/3sxDImQ5AK/LtAJ0UqAVJDvnASKBiGQyb+bIi6fv1DUKxHOK+xmNIko4VCrSNZAAll3GwxPU2ZtgaNRiY4PyazpxAIc/ruPXi7avbOayjOiRawMgUFsCVaW3nYIX4zxlZXRbVbfbQUc1SuSDn6+S08K1UqLJNn8nt0crqoc9mlJFVWP+U8Rsi6MET/hKI+WiH563UPFq01/NRCHpo1l5p3Vbhx+cJftynBQFd1aQc2oUHbGPZ4t8PVn/D/f6DdzwxQXQfDtKTZSLhPtnaQ/wY1s9kr7A7egm7AljvqAB2c0wcp8IBYuhp4kqwMyZcm8UWju/E/GpSPEkVq8XE9GInZuGHPP1tQt1TzUFGwAquNd40Sb48FD31LO77bttsY34GhoZ8Q9rWDlWCnwTTFxEYIQprfCZmlOZhsc87WWXYSEdYrtl/zDr7cNuYK1DoB22gSw/BseUncs4m0jpj1hYAd55JrCYoClWJNOX8hvFO2mBxqyCmiszc5RBk2J9o6jUCRtNMYch4DKwjWJE5ELG7YBLOaoCLfeh0+AJuFI3M02rJ/hk57/hub2xkK9DwOlFn0AQEVTeVyFHv6NjYeizKO9m9UHEZapSsS3D1rAwlVVvpnp5OKeFV71tf4MsgWZquJl3d9Jp5CML3+tWpIlV0He+vmUv6VA5w0w0B2kBvydKpETp/XlP2LxYSmYseIeidFoHAZRCy4NS5uXkIs4GrMbr0/XuaDw8dchrzJRGqvtLlkW1F/4QKpwGWL590FZvUh3YFrRr34FTWOI5m+DKX/0qaBefEt7h1CiXi8AgjNalvfwh6qMsxzuj1Mh/PAN0k+55X+fzbn7CjK9VA+ZbP0RwJ4HFell5Q+uKVg6g3qFGLz3E38Qs3L6ToEESvLi/thqi73kkfvzZWuPHADjINhyN6nR9FrXoFFgmaxbV/A+1Md3PwT+dVScRVku4kqzYaRxigY8X36v1ts333+fpiL9qwEAc+ZfvS67TT2Ngi47444DBP5OIHUjcmQl3bT5XRqzO4tKWOy+t+9LbVnlRy39f8DwoY5knFijlR9kDIgw3DMu3ZZXxhYwKOWpMe0N1fVDN7YNa6jsojAbfOYqx3FEbPLWLWH8dajjk8IDJsv41FuAiaSVvr8QI2oGqsZQdzigLIST6emxvktf6nL553ikUvwkWixgWXViEDSq3Opfrok63Qfm50Y3TTmlyqG2NKmqmp45IIKahRc4fwsRy7NAeii587Y3sqGN4ra0CzGWL0E+HMKSabQT6ObIa4Cu5eNvEKeF/2DPhyImcf5ZAczwfvPlF4DrciW82OodDeGBNldqEhDyfqtCRPrIZxMKJpXmzIbOps1XZfDMB7hvXzRkgmhyWu/gVpcSTkXyGLbAvL8Exy5u9w0OlAD1Inw5Q+SIOfkWDgb/Rd62evwuFfkqAJ9t40Akkc1Y34lrCiL0f5EioXilNtfv+SnafCVZNtggItRxcFPmjUWSc1jsaf/w9SqMvDJQg8zGHNF70G6gij+/T"

HEADERS = {
    "Content-Type": "application/grpc+proto",
    "User-Agent": "Snapchat/12.85.0.44 (iPhone9,3; iOS 15.7.5; gzip)",
    "X-Snapchat-UUID": "93F3D290-1729-4593-B346-F297C7E2F677",
    "x-snapchat-att-token": "Ci1EfdA0txvTV2_uCAnIfHe9UU4HEmr92o1p1fU40FW8inWat0leOlO-Y1ZYuckVAQAAAA==",
    "te": "trailers",
}

@app.route('/login', methods=['POST'])
def login():
    full = base64.b64decode(PAYLOAD_B64)
    r = requests.post(
        "https://us-east1-aws.api.snapchat.com/snapchat.janus.api.LoginService/LoginWithPassword",
        headers=HEADERS,
        data=full,
        timeout=15
    )
    return jsonify({"status": r.status_code, "response": r.text[:500]})

@app.route('/')
def home():
    return jsonify({"status": "alive", "endpoint": "/login", "method": "POST"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
