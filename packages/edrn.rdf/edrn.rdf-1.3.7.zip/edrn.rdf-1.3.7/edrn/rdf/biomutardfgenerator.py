# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''Biomuta RDF Generator. An RDF generator that describes EDRN biomarker mutation statistics using Biomuta webservices.
'''

from Acquisition import aq_inner
from edrn.rdf import _
from five import grok
from interfaces import IGraphGenerator
from rdfgenerator import IRDFGenerator
from rdflib.term import URIRef, Literal
from utils import validateAccessibleURL
from utils import splitBiomutaRows
from urllib2 import urlopen
from zope import schema
import rdflib

_biomutaPredicates = {
    u'GeneName': 'geneNamePredicateURI',
    u'UniProtAC': 'uniProtACPredicateURI',
    u'#mutated_site': 'mutCountPredicateURI',
    u'#PMID': 'pmidCountPredicateURI',
    u'#CancerDO': 'cancerDOCountPredicateURI',
    u'#AffectedProtFunSite': 'affProtFuncSiteCountPredicateURI'
}

class IBiomutaRDFGenerator(IRDFGenerator):
    '''DMCC Committee RDF Generator.'''
    webServiceURL = schema.TextLine(
        title=_(u'Web Service URL'),
        description=_(u'The Uniform Resource Locator to the DMCC SOAP web service.'),
        required=True,
        constraint=validateAccessibleURL,
    )
    typeURI = schema.TextLine(
        title=_(u'Type URI'),
        description=_(u'Uniform Resource Identifier naming the type of biomuta objects described by this generator.'),
        required=True,
    )
    uriPrefix = schema.TextLine(
        title=_(u'URI Prefix'),
        description=_(u'The Uniform Resource Identifier prepended to all biomuta described by this generator.'),
        required=True,
    )
    geneNamePredicateURI = schema.TextLine(
        title=_(u'Gene Symbol/Name Predicate URI'),
        description=_(u'The Uniform Resource Identifier of the predicate that indicates gene symbol or name.'),
        required=True,
    )
    uniProtACPredicateURI = schema.TextLine(
        title=_(u'Uniprot Accession Predicate URI'),
        description=_(u'The Uniform Resource Identifier of the predicate that indicates the associated uniprot accession.'),
        required=True,
    )
    mutCountPredicateURI = schema.TextLine(
        title=_(u'Number of Mutation Sites Predicate URI'),
        description=_(u'The Uniform Resource Identifier of the predicate that indicates the number of mutation sites.'),
        required=True,
    )
    pmidCountPredicateURI = schema.TextLine(
        title=_(u'Pubmed ID Count Predicate URI'),
        description=_(u'The Uniform Resource Identifier of the predicate that indicates the number of associated pubmed ids.'),
        required=True,
    )
    cancerDOCountPredicateURI = schema.TextLine(
        title=_(u'CancerDO Predicate URI'),
        description=_(u'The Uniform Resource Identifier of the predicate that indicates the CancerDO.'),
        required=True,
    )
    affProtFuncSiteCountPredicateURI = schema.TextLine(
        title=_(u'Affected Protein Function Site Count Predicate URI'),
        description=_(u'The Uniform Resource Identifier of the predicate that indicates the number of affected protein function sites.'),
        required=True,
    )

class BiomutaGraphGenerator(grok.Adapter):
    '''A graph generator that produces statements about EDRN's committees using the DMCC's fatuous web service.'''
    grok.provides(IGraphGenerator)
    grok.context(IBiomutaRDFGenerator)
    def generateGraph(self):
        graph = rdflib.Graph()
        context = aq_inner(self.context)
        mutations = urlopen(context.webServiceURL)
        inputPredicates = None
        # Get the mutations
        for row in mutations:
            elements = splitBiomutaRows(row.strip())
            if not inputPredicates:
                inputPredicates = elements
            else:
                geneName = elements[0].strip()
                subjectURI = URIRef(context.uriPrefix + geneName)
                graph.add((subjectURI, rdflib.RDF.type, URIRef(context.typeURI)))
                for idx in range(0,len(inputPredicates)):
                    key = inputPredicates[idx]
                    predicateURI = URIRef(getattr(context, _biomutaPredicates[key]))
                    try:
                      graph.add((subjectURI, predicateURI, Literal(elements[idx].strip())))
                    except Exception as e:
                      print str(e)

        # C'est tout.
        return graph
