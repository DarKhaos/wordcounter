from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import re
from copy import copy
from typing import Dict, List
from .data import get_blacklist


class WordCounter:
    __COMMON_WORDS_TO_DELETE = 100
    
    @staticmethod
    def __get_number_of_words(text: str) -> Dict[str, int]:
        word_count = {}
        words = re.findall(r"[\w]+", text)
        for word in words:
            if word_count.get(word, None) is not None:
                word_count[word] = word_count.get(word) + 1
            else:
                word_count[word] = 1
        sorted_word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_word_count)

    @staticmethod
    def __discard_common_words(sorted_word_count: Dict[str, int], blacklist: List[str]) -> Dict[str, int]:
        result = copy(sorted_word_count)
        discard_count = 0
        for discarded_word in blacklist:
            if discard_count < WordCounter.__COMMON_WORDS_TO_DELETE and result.get(discarded_word, None) is not None:
                del result[discarded_word]
                discard_count += 1
        return result
    
    @staticmethod
    def get_number_of_words(data: str) -> Dict[str, int]:
        number_of_words = WordCounter.__get_number_of_words(data)
        return WordCounter.__discard_common_words(number_of_words, get_blacklist())


def __get_bad_request() -> Response:
    return Response({"detail": "Invalid payload."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def count_words(request):
    data = None
    if 'multipart/form-data' in request.headers['content-type']:
        if request.FILES.get('file') is None:
            return __get_bad_request()
        file = request.FILES.get('file')
        data = file.read().decode('utf-8')
    elif not isinstance(request.data, str):
        return __get_bad_request()
    else:
        data = request.data
    return Response(WordCounter.get_number_of_words(data))