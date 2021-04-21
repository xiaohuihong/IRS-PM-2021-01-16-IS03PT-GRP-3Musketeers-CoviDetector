import json
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse
from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings
import logging
import os
from . import chatter

class ChatterBotAppView(TemplateView):
    template_name = 'app.html'


class ChatterBotApiView(View):
    """
    Provide an API endpoint to interact with ChatterBot.
    """
    logging.basicConfig(level=logging.INFO)
 #   chatterbot = ChatBot(
#        'Covid FAQ Chat Bot',
#
 #       logic_adapters= [
 #               {
 #                   "import_path": "chatterbot.logic.BestMatch",
 #                   "statement_comparison_function": "chatterbot.comparisons.LevenshteinDistance",
 #                   "response_selection_method": "chatterbot.response_selection.get_first_response",
 #                   "maximum_similarity_threshold": 0.9
 #               }
 #       ],
 #       read_only=True,
#    )
    
#    chatterbot = ChatBot(**settings.CHATTERBOT)
    print("===================================test==================================")
    
    cwd = os.getcwd()
    data_path = os.path.join(cwd + '\\example_app\\data\\')
    excel_name = 'COVID_FAQ.xlsx'
    worksheet_name = 'FAQ'
    threshold=0.6

    covid_faq_chatbot = chatter.faq_chatbot_initialize("Covid FAQ Chat Bot", excel_path=data_path+excel_name, worksheet_name=worksheet_name)
    covid_nlp_chatbot = chatter.nlp_chatbot_initialize("Covid NLP Chat Bot", data_path)
    def post(self, request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.

        * The JSON data should contain a 'text' attribute.
        """
        input_data = json.loads(request.body.decode('utf-8'))

        if 'text' not in input_data:
            return JsonResponse({
                'text': [
                    'The attribute "text" is required.'
                ]
            }, status=400)
        print(input_data['text'])
        #response = self.chatterbot.get_response(input_data['text'])
        response = chatter.get_answer(self.covid_faq_chatbot, self.covid_nlp_chatbot, input_data['text'], self.threshold)
        #response_data = response.serialize()
        
        return JsonResponse({
                'text': [
                    response
                ]
            }, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        return JsonResponse({
            'name': self.chatterbot.name
        })
