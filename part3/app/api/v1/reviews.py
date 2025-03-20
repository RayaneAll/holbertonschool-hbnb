from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

# Model for detailed review information
review_output_model = api.model('ReviewOutput', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user'),
    'place_id': fields.String(description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @jwt_required()  # ✅ Seul un utilisateur connecté peut poster une review
    def post(self):
        """Register a new review"""
        try:
            review_data = api.payload
            current_user = get_jwt_identity()  # ✅ Récupérer l'utilisateur connecté

            # Vérifier si l'utilisateur est propriétaire du lieu
            place = facade.get_place(review_data["place_id"])
            if place["owner"]["id"] == current_user["id"]:
                return {'message': "You cannot review your own place."}, 400

            # Vérifier si l'utilisateur a déjà laissé une review pour ce lieu
            existing_review = facade.get_review_by_user_and_place(current_user["id"], review_data["place_id"])
            if existing_review:
                return {'message': "You have already reviewed this place."}, 400

            # Assigner l'ID de l'utilisateur connecté à la review
            review_data["user_id"] = current_user["id"]

            review = facade.create_review(review_data)
            return review, 201
        except ValueError as e:
            return {'message': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return reviews, 200

@api.route('/<string:review_id>')
@api.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if review is None:
            api.abort(404, f"Review with ID {review_id} not found")
        return review, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()  # ✅ Seul l'auteur peut modifier sa review
    def put(self, review_id):
        """Update a review"""
        try:
            current_user = get_jwt_identity()
            review = facade.get_review(review_id)

            if review is None:
                api.abort(404, f"Review with ID {review_id} not found")

            if review["user_id"] != current_user["id"]:
                return {'message': "Unauthorized action"}, 403  # ✅ Vérifier si l'utilisateur est l'auteur

            review_data = api.payload
            result = facade.update_review(review_id, review_data)
            return result, 200
        except ValueError as e:
            return {'message': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()  # ✅ Seul l'auteur peut supprimer sa review
    def delete(self, review_id):
        """Delete a review"""
        current_user = get_jwt_identity()
        review = facade.get_review(review_id)

        if review is None:
            api.abort(404, f"Review with ID {review_id} not found")

        if review["user_id"] != current_user["id"]:
            return {'message': "Unauthorized action"}, 403  # ✅ Vérifier si l'utilisateur est l'auteur

        result = facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200