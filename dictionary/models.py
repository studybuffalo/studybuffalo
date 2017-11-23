from django.db import models

class DictionaryType(models.Model):
    """Dictionary type for creation of specific dictionary categories"""
    dictionary_name = models.CharField(max_length=50,)
    
    def __str__(self):
        return self.dictionary_name

class Language(models.Model):
    """Language of the word"""
    language = models.CharField(max_length=25,)
    
    def __str__(self):
        return self.language

class MonitoredApplication(models.Model):
    """Name of application to be monitored for dictionary items"""
    application_name = models.CharField(max_length=50,)

    class Meta:
        permissions = (
            ("can_view", "Can view the dictionary review application"),
        )

    def __str__(self):
        return self.application_name

class MonitoredModel(models.Model):
    """Name of a model to be included from an application"""
    monitored_application = models.ForeignKey(
        to="MonitoredApplication",
        on_delete=models.CASCADE,
    )
    model_name = models.CharField(max_length=50,)

    def __str__(self):
        return self.model_name

class MonitoredField(models.Model):
    """Name of a field to be included from a model"""
    monitored_model = models.ForeignKey(
        to="MonitoredModel",
        on_delete=models.CASCADE,
    )
    dictionary_type = models.ForeignKey(
        to="DictionaryType",
        on_delete=models.CASCADE,
    )
    language = models.ForeignKey(
        to="Language",
        on_delete=models.CASCADE,
    )
    field_name = models.CharField(max_length=50,)
    
    def __str__(self):
        return self.field_name

class Word(models.Model):
    """A single word in the dictionary"""
    dictionary_type = models.ForeignKey(
        to="DictionaryType",
        on_delete=models.SET_NULL,
        null=True,
    )
    language = models.ForeignKey(
        to="Language",
        on_delete=models.SET_NULL,
        null=True,
    )
    word = models.CharField(max_length=50,)
    
    def __str__(self):
        return self.word

class WordPending(models.Model):
    """A single word pending inclusion into Word"""
    dictionary_type = models.ForeignKey(
        to="DictionaryType",
        on_delete=models.SET_NULL,
        null=True,
    )
    language = models.ForeignKey(
        to="Language",
        on_delete=models.SET_NULL,
        null=True,
    )
    word = models.CharField(max_length=50,)
    
    class Meta:
        verbose_name = "Word (Pending)"
        verbose_name_plural = "Words (Pending)"

    def __str__(self):
        return self.word

class ExcludedWord(models.Model):
    """A single word that will not be included in the dictionary"""
    dictionary_type = models.ForeignKey(
        to="DictionaryType",
        on_delete=models.SET_NULL,
        null=True,
    )
    language = models.ForeignKey(
        to="Language",
        on_delete=models.SET_NULL,
        null=True,
    )
    word = models.CharField(max_length=50,)
    
    def __str__(self):
        return self.word