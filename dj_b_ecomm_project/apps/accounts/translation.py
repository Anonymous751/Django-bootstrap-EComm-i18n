from modeltranslation.translator import register, TranslationOptions
from .models import CustomUser, Profile

@register(CustomUser)
class UserTranslationOptions(TranslationOptions):
    fields = ('bio', 'location', 'display_name')
    
@register(Profile)
class ProfileTranslationOptions(TranslationOptions):
    fields = ('display_name',)