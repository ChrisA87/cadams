from flask_restx import Namespace, Resource, fields
from .security import require_public_apikey, format_response
from ..wordle.wordle import return_candidates


api = Namespace(
    name='Wordle',
    description='An endpoint for wordle solution suggestions.',
    path='/wordle')


wordle_suggestion_params = api.model('WordleSuggestions', {
    'pattern': fields.String(
        description='Known-position letters pattern. Use underscores for unknown letters. e.g. "___th"'),
    'include_letters': fields.String(
        description='Letters known to exist in the word, but positions are unknown.'),
    'exclude_letters': fields.String(
        description='Letters known not to exist in the word.')})


@api.route('/suggest')
@api.doc(security='apikey')
class WordleSuggestions(Resource):
    @format_response
    @require_public_apikey
    @api.expect(wordle_suggestion_params, validate=True)
    def post(self):
        return return_candidates(**api.payload)
