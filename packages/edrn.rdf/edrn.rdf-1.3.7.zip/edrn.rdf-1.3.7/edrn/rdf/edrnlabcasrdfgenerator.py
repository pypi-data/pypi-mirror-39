# encoding: utf-8
# Copyright 2012 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''EDRNLabcas RDF Generator. An RDF generator that describes EDRN biomarker mutation statistics using Biomuta webservices.
'''

from Acquisition import aq_inner
from edrn.rdf import _
from five import grok
from interfaces import IGraphGenerator
from rdfgenerator import IRDFGenerator
from rdflib.term import URIRef, Literal
from utils import validateAccessibleURL
from urllib2 import urlopen
from zope import schema
from mysolr import Solr

import rdflib

ecasURIPrefix = 'urn:edrn:'
edrnURIPrefix = 'http://edrn.nci.nih.gov/rdf/schema.rdf#'

_edrnlabcasPredicates = {
    u'AnalyticMethods': 'AnalyticMethodsPredicateURI',
    u'AnalyticResults': 'AnalyticResultsPredicateURI',
    u'CollaborativeGroup': 'CollaborativeGroupPredicateURI',
    u'DataCustodian': 'DataCustodianPredicateURI',
    u'DataCustodianEmail': 'DataCustodianEmailPredicateURI',
    u'DataCustodianPhone': 'DataCustodianPhonePredicateURI',
    u'DataDisclaimer': 'DataDisclaimerPredicateURI',
    u'DataSetName': 'DataSetNamePredicateURI',
    u'DatasetDescription': 'DatasetDescriptionPredicateURI',
    u'DatasetId': 'DatasetIdPredicateURI',
    u'DatasetURL': 'DatasetURLPredicateURI',
    u'Date': 'DatePredicateURI',
    u'DateDatasetFrozen': 'DateDatasetFrozenPredicateURI',
    u'Description': 'DescriptionPredicateURI',
    u'Discipline': 'DisciplinePredicateURI',
    u'EligibilityCriteria': 'EligibilityCriteriaPredicateURI',
    u'GrantSupport': 'GrantSupportPredicateURI',
    u'InstrumentDetails': 'InstrumentDetailsPredicateURI',
    u'InvestigatorName': 'InvestigatorNamePredicateURI',
    u'LeadPI': 'LeadPIPredicateURI',
    u'LeadPI_fullname': 'LeadPI_fullnamePredicateURI',
    u'MethodDetails': 'MethodDetailsPredicateURI',
    u'PlannedSampleSize': 'PlannedSampleSizePredicateURI',
    u'ProteomicsExperimentType': 'ProteomicsExperimentTypePredicateURI',
    u'ProtocolId': 'ProtocolIDPredicateURI',
    u'PubMedID': 'PubMedIDPredicateURI',
    u'PublishState': 'PublishStatePredicateURI',
    u'RecommendedSoftware': 'RecommendedSoftwarePredicateURI',
    u'ResearchSupport': 'ResearchSupportPredicateURI',
    u'ResultsAndConclusionSummary': 'ResultsAndConclusionSummaryPredicateURI',
    u'InstitutionId': 'SiteIDPredicateURI',
    u'Species': 'SpeciesPredicateURI',
    u'SpecificAims': 'SpecificAimsPredicateURI',
    u'SpecimenType': 'SpecimenTypePredicateURI',
    u'StudyBackground': 'StudyBackgroundPredicateURI',
    u'StudyConclusion': 'StudyConclusionPredicateURI',
    u'StudyDescription': 'StudyDescriptionPredicateURI',
    u'StudyDesign': 'StudyDesignPredicateURI',
    u'StudyId': 'StudyIdPredicateURI',
    u'StudyMethods': 'StudyMethodsPredicateURI',
    u'StudyName': 'StudyNamePredicateURI',
    u'StudyObjective': 'StudyObjectivePredicateURI',
    u'StudyResults': 'StudyResultsPredicateURI',
    u'Technology': 'TechnologyPredicateURI',
    u'Consortium': 'ConsortiumPredicateURI',
    u'AccessGrantedTo': 'AccessGrantedToPredicateURI',
    u'QAState': 'QAStatePredicateURI',
    u'Organ': 'organPredicateURI',
    u'site': 'sitePredicateURI' 
}

_graph_obj_mapping = {
    u'ProtocolId': ['protocolPredicateURI', 'http://edrn.nci.nih.gov/data/protocols/'],
    u'InstitutionId': ['sitePredicateURI', 'http://edrn.nci.nih.gov/data/sites/'],
    u'Organ': ['organPredicateURI', 'http://edrn.nci.nih.gov/data/body-systems/']
}

class IEDRNLabcasRDFGenerator(IRDFGenerator):
    '''DMCC Committee RDF Generator.'''
    webServiceURL = schema.TextLine(
        title=_(u'Web Service URL'),
        description=_(u'The Uniform Resource Locator to the DMCC SOAP web service.'),
        required=True,
        constraint=validateAccessibleURL,
    )
    typeURI = schema.TextLine(
        title=_(u'Type URI'),
        description=_(u'Uniform Resource Identifier naming the type of edrnlabcas objects described by this generator.'),
        required=True,
    )
    uriPrefix = schema.TextLine(
        title=_(u'URI Prefix'),
        description=_(u'The Uniform Resource Identifier prepended to all edrnlabcas described by this generator.'),
        required=True,
    )

class EDRNLabcasGraphGenerator(grok.Adapter):
    '''A graph generator that produces statements about EDRN's committees using the DMCC's fatuous web service.'''
    grok.provides(IGraphGenerator)
    grok.context(IEDRNLabcasRDFGenerator)
    def generateGraph(self):
        graph = rdflib.Graph()
        context = aq_inner(self.context)
        inputPredicates = None
        solr_conn = Solr(base_url=context.webServiceURL, version=4)
        solr_query = {'q': '*:*', 'rows': 100}
        solr_response = solr_conn.search(**solr_query)
        results = {}
        for obj in solr_response.documents:
            obj['sourceurl'] = context.uriPrefix + obj.get("id")
            results[obj.get("id")] = obj
        graph.bind('edrn',ecasURIPrefix)
        graph.bind('x',edrnURIPrefix)
        # Get the mutations
        for datasetid in results.keys():
            datasetid_friendly = datasetid.replace("(","_").replace(")","_").replace("+","_").replace(",","_").replace(".","")
            subjectURI = URIRef(context.typeURI + datasetid_friendly)
            graph.add((subjectURI, rdflib.RDF.type, URIRef("{}{}".format(context.typeURI,datasetid_friendly))))
            for key in results[datasetid].keys():
                if key not in _edrnlabcasPredicates.keys():
                    continue
                predicateURI = URIRef(getattr(context, _edrnlabcasPredicates[key]))
                try:
                  graph.add((subjectURI, predicateURI, Literal(results[datasetid][key][0].strip())))
                  if key in _graph_obj_mapping.keys():
                      predicateURI = URIRef(getattr(context, _graph_obj_mapping[key][0]))
                      #Watch out for text that isn't equivalent to protocols in labcas
                      if "No Associated Protocol" not in results[datasetid][key][0].strip():
                          for item_split in results[datasetid][key][0].strip().split(","):
                              graph.add((subjectURI, predicateURI, URIRef("{}{}".format(_graph_obj_mapping[key][1],item_split.strip()))))
                except Exception as e:
                  print str(e)
        # C'est tout.
        return graph
