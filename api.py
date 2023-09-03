from flask import request, jsonify
from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required

api = Api()
api.init_app(app)

class UploadImage(Resource):
    @jwt_required()
    def post(self):
        # Handle image upload and processing here
        uploaded_image = request.files['image']
        image_name = uploaded_image.filename
        # Process the image and get its name

        return jsonify(message=f"Uploaded image: {image_name}")

api.add_resource(UploadImage, '/upload')

