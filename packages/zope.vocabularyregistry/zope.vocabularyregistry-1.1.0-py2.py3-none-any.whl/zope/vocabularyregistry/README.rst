=====================================
 Component-based Vocabulary Registry
=====================================

This package provides a vocabulary registry for zope.schema,
based on the component architecture.

It replaces the zope.schema's simple vocabulary registry
when ``zope.vocabularyregistry`` package is imported, so it's done
automatically. All we need is provide vocabulary factory
utilities:

  >>> import zope.vocabularyregistry
  >>> from zope.component import provideUtility
  >>> from zope.schema.interfaces import IVocabularyFactory
  >>> from zope.schema.vocabulary import SimpleTerm
  >>> from zope.schema.vocabulary import SimpleVocabulary

  >>> def SomeVocabulary(context=None):
  ...     terms = [SimpleTerm(1), SimpleTerm(2)]
  ...     return SimpleVocabulary(terms)

  >>> provideUtility(SomeVocabulary, IVocabularyFactory,
  ...                name='SomeVocabulary')

Now we can get the vocabulary using standard zope.schema
way:

  >>> from zope.schema.vocabulary import getVocabularyRegistry
  >>> vr = getVocabularyRegistry()
  >>> voc = vr.get(None, 'SomeVocabulary')
  >>> [term.value for term in voc]
  [1, 2]


Configuration
=============

This package provides configuration that ensures the vocabulary
registry is established:


  >>> from zope.configuration import xmlconfig
  >>> _ = xmlconfig.string(r"""
  ... <configure xmlns="http://namespaces.zope.org/zope" i18n_domain="zope">
  ...   <include package="zope.vocabularyregistry" />
  ... </configure>
  ... """)
