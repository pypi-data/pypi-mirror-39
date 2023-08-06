name = "hyvebrain"
import requests, json

class Hyvebrain:

    URL_ENDPOINT = "https://api.hyvebrain.com/v/testing/"

    def __init__( self ):
        self.text_content = ""
        self.functions = []
        self._return_natural_language_raw_data = 0
        self._natural_language_raw_data = None

    def get_current_token_index( self ):
        self.functions.append( "get_current_token_index" )
        return self
    def get_current_sentence_index( self ):
        self.functions.append( "get_current_sentence_index" )
        return self

    def get_pos_tag( self ):
        self.functions.append( "get_pos_tag" )
        return self
    def get_depe_hti( self ):
        self.functions.append( "get_depe_hti" )
        return self
    def get_depe_label( self ):
        self.functions.append( "get_depe_label" )
        return self
    def get_pos_tag_str( self ):
        self.functions.append( "get_pos_tag_str" )
        return self
    def get_depe_label_str( self ):
        self.functions.append( "get_depe_label_str" )
        return self
    def get_lemma( self ):
        self.functions.append( "get_lemma" )
        return self
    def get_text_content_token( self ):
        self.functions.append( "get_text_content_token" )
        return self

    def get_token_index_list( self ):
        self.functions.append( "get_token_index_list" )
        return self
    def get_pos_tag_list( self ):
        self.functions.append( "get_pos_tag_list" )
        return self
    def get_depe_hti_list( self ):
        self.functions.append( "get_depe_hti_list" )
        return self
    def get_depe_label_list( self ):
        self.functions.append( "get_depe_label_list" )
        return self
    def get_pos_tag_str_list( self ):
        self.functions.append( "get_pos_tag_str_list" )
        return self
    def get_depe_label_str_list( self ):
        self.functions.append( "get_depe_label_str_list" )
        return self
    def get_lemma_list( self ):
        self.functions.append( "get_lemma_list" )
        return self
    def get_text_content_token_list( self ):
        self.functions.append( "get_text_content_token_list" )
        return self

    def get_sentence_index_list( self ):
        self.functions.append( "get_sentence_index_list" )
        return self
    def get_text_content_sentence_list( self ):
        self.functions.append( "get_text_content_sentence_list" )
        return self
    def get_sentence_index_of_token_index_list( self ):
        self.functions.append( "get_sentence_index_of_token_index_list" )
        return self

    def get_sentence_index_root( self ):
        self.functions.append( "get_sentence_index_root" )
        return self
    def get_pos_tag_sentence_root( self ):
        self.functions.append( "get_pos_tag_sentence_root" )
        return self
    def get_depe_hti_sentence_root( self ):
        self.functions.append( "get_depe_hti_sentence_root" )
        return self
    def get_depe_label_sentence_root( self ):
        self.functions.append( "get_depe_label_sentence_root" )
        return self
    def get_pos_tag_str_sentence_root( self ):
        self.functions.append( "get_pos_tag_str_sentence_root" )
        return self
    def get_depe_label_str_sentence_root( self ):
        self.functions.append( "get_depe_label_str_sentence_root" )
        return self
    def get_lemma_sentence_root( self ):
        self.functions.append( "get_lemma_sentence_root" )
        return self
    def get_text_content_sentence_root( self ):
        self.functions.append( "get_text_content_sentence_root" )
        return self

    def get_sentence_root_list( self ):
        self.functions.append( "get_sentence_root_list" )
        return self
    def get_pos_tag_sentence_root_list( self ):
        self.functions.append( "get_pos_tag_sentence_root_list" )
        return self
    def get_depe_hti_sentence_root_list( self ):
        self.functions.append( "get_depe_hti_sentence_root_list" )
        return self
    def get_depe_label_sentence_root_list( self ):
        self.functions.append( "get_depe_label_sentence_root_list" )
        return self
    def get_pos_tag_str_sentence_root_list( self ):
        self.functions.append( "get_pos_tag_str_sentence_root_list" )
        return self
    def get_depe_label_str_sentence_root_list( self ):
        self.functions.append( "get_depe_label_str_sentence_root_list" )
        return self
    def get_lemma_sentence_root_list( self ):
        self.functions.append( "get_lemma_sentence_root_list" )
        return self
    def get_text_content_sentence_root_list( self ):
        self.functions.append( "get_text_content_sentence_root_list" )
        return self

    def get_branch_index_list_of_sentence_index( self ):
        self.functions.append( "get_branch_index_list_of_sentence_index" )
        return self
    def get_index_list_of_equal_hti( self ):
        self.functions.append( "get_index_list_of_equal_hti" )
        return self

    def get_master_index( self ):
        self.functions.append( "get_master_index" )
        return self
    def get_pos_tag_master( self ):
        self.functions.append( "get_pos_tag_master" )
        return self
    def get_depe_hti_master( self ):
        self.functions.append( "get_depe_hti_master" )
        return self
    def get_depe_label_master( self ):
        self.functions.append( "get_depe_label_master" )
        return self
    def get_pos_tag_str_master( self ):
        self.functions.append( "get_pos_tag_str_master" )
        return self
    def get_depe_label_str_master( self ):
        self.functions.append( "get_depe_label_str_master" )
        return self
    def get_lemma_master( self ):
        self.functions.append( "get_lemma_master" )
        return self
    def get_text_content_master( self ):
        self.functions.append( "get_text_content_master" )
        return self

    def get_master_index_list( self ):
        self.functions.append( "get_master_index_list" )
        return self

    def get_slave_index_list( self ):
        self.functions.append( "get_slave_index_list" )
        return self
    def get_pos_tag_slave_index_list( self ):
        self.functions.append( "get_pos_tag_slave_index_list" )
        return self
    def get_depe_hti_slave_index_list( self ):
        self.functions.append( "get_depe_hti_slave_index_list" )
        return self
    def get_depe_label_slave_index_list( self ):
        self.functions.append( "get_depe_label_slave_index_list" )
        return self
    def get_pos_tag_str_slave_index_list( self ):
        self.functions.append( "get_pos_tag_str_slave_index_list" )
        return self
    def get_depe_label_str_slave_index_list( self ):
        self.functions.append( "get_depe_label_str_slave_index_list" )
        return self
    def get_lemma_slave_index_list( self ):
        self.functions.append( "get_lemma_slave_index_list" )
        return self
    def get_text_content_slave_index_list( self ):
        self.functions.append( "get_text_content_slave_index_list" )
        return self

    def get_slave_index_list_of_token_index_list( self ):
        self.functions.append( "get_slave_index_list_of_token_index_list" )
        return self
    def get_pos_tag_slave_index_list_of_token_index_list( self ):
        self.functions.append( "get_pos_tag_slave_index_list_of_token_index_list" )
        return self
    def get_depe_hti_slave_index_list_of_token_index_list( self ):
        self.functions.append( "get_depe_hti_slave_index_list_of_token_index_list" )
        return self
    def get_depe_label_slave_index_list_of_token_index_list( self ):
        self.functions.append( "get_depe_label_slave_index_list_of_token_index_list" )
        return self
    def get_pos_tag_str_slave_index_list_of_token_index_list( self ):
        self.functions.append( "get_pos_tag_str_slave_index_list_of_token_index_list" )
        return self
    def get_depe_label_str_slave_index_list_of_token_index_list( self ):
        self.functions.append( "get_depe_label_str_slave_index_list_of_token_index_list" )
        return self
    def get_lemma_slave_index_list_of_token_index_list( self ):
        self.functions.append( "get_lemma_slave_index_list_of_token_index_list" )
        return self
    def get_text_content_slave_index_list_of_token_index_list( self ):
        self.functions.append( "get_text_content_slave_index_list_of_token_index_list" )
        return self

    def get_branch_token_index_to_root_index_list( self ):
        self.functions.append( "get_branch_token_index_to_root_index_list" )
        return self
    def get_branch_root_index_to_token_index_list( self ):
        self.functions.append( "get_branch_root_index_to_token_index_list" )
        return self
    def get_branch_index_list( self ):
        self.functions.append( "get_branch_index_list" )
        return self
    def get_branch_root_index( self ):
        self.functions.append( "get_branch_root_index" )
        return self

    def get_pos_tag_UNKNOWN( self ):
        self.functions.append( "get_pos_tag_UNKNOWN" )
        return self
    def get_pos_tag_ADJ( self ):
        self.functions.append( "get_pos_tag_ADJ" )
        return self
    def get_pos_tag_ADP( self ):
        self.functions.append( "get_pos_tag_ADP" )
        return self
    def get_pos_tag_ADV( self ):
        self.functions.append( "get_pos_tag_ADV" )
        return self
    def get_pos_tag_CONJ( self ):
        self.functions.append( "get_pos_tag_CONJ" )
        return self
    def get_pos_tag_DET( self ):
        self.functions.append( "get_pos_tag_DET" )
        return self
    def get_pos_tag_NOUN( self ):
        self.functions.append( "get_pos_tag_NOUN" )
        return self
    def get_pos_tag_NUM( self ):
        self.functions.append( "get_pos_tag_NUM" )
        return self
    def get_pos_tag_PRON( self ):
        self.functions.append( "get_pos_tag_PRON" )
        return self
    def get_pos_tag_PRT( self ):
        self.functions.append( "get_pos_tag_PRT" )
        return self
    def get_pos_tag_PUNCT( self ):
        self.functions.append( "get_pos_tag_PUNCT" )
        return self
    def get_pos_tag_VERB( self ):
        self.functions.append( "get_pos_tag_VERB" )
        return self
    def get_pos_tag_X( self ):
        self.functions.append( "get_pos_tag_X" )
        return self
    def get_pos_tag_AFFIX( self ):
        self.functions.append( "get_pos_tag_AFFIX" )
        return self

    def get_pos_tag_UNKNOWN_str( self ):
        self.functions.append( "get_pos_tag_UNKNOWN_str" )
        return self
    def get_pos_tag_ADJ_str( self ):
        self.functions.append( "get_pos_tag_ADJ_str" )
        return self
    def get_pos_tag_ADP_str( self ):
        self.functions.append( "get_pos_tag_ADP_str" )
        return self
    def get_pos_tag_ADV_str( self ):
        self.functions.append( "get_pos_tag_ADV_str" )
        return self
    def get_pos_tag_CONJ_str( self ):
        self.functions.append( "get_pos_tag_CONJ_str" )
        return self
    def get_pos_tag_DET_str( self ):
        self.functions.append( "get_pos_tag_DET_str" )
        return self
    def get_pos_tag_NOUN_str( self ):
        self.functions.append( "get_pos_tag_NOUN_str" )
        return self
    def get_pos_tag_NUM_str( self ):
        self.functions.append( "get_pos_tag_NUM_str" )
        return self
    def get_pos_tag_PRON_str( self ):
        self.functions.append( "get_pos_tag_PRON_str" )
        return self
    def get_pos_tag_PRT_str( self ):
        self.functions.append( "get_pos_tag_PRT_str" )
        return self
    def get_pos_tag_PUNCT_str( self ):
        self.functions.append( "get_pos_tag_PUNCT_str" )
        return self
    def get_pos_tag_VERB_str( self ):
        self.functions.append( "get_pos_tag_VERB_str" )
        return self
    def get_pos_tag_X_str( self ):
        self.functions.append( "get_pos_tag_X_str" )
        return self
    def get_pos_tag_AFFIX_str( self ):
        self.functions.append( "get_pos_tag_AFFIX_str" )
        return self

    def get_pos_tag_UNKNOWN_list( self ):
        self.functions.append( "get_pos_tag_UNKNOWN_list" )
        return self
    def get_pos_tag_ADJ_list( self ):
        self.functions.append( "get_pos_tag_ADJ_list" )
        return self
    def get_pos_tag_ADP_list( self ):
        self.functions.append( "get_pos_tag_ADP_list" )
        return self
    def get_pos_tag_ADV_list( self ):
        self.functions.append( "get_pos_tag_ADV_list" )
        return self
    def get_pos_tag_CONJ_list( self ):
        self.functions.append( "get_pos_tag_CONJ_list" )
        return self
    def get_pos_tag_DET_list( self ):
        self.functions.append( "get_pos_tag_DET_list" )
        return self
    def get_pos_tag_NOUN_list( self ):
        self.functions.append( "get_pos_tag_NOUN_list" )
        return self
    def get_pos_tag_NUM_list( self ):
        self.functions.append( "get_pos_tag_NUM_list" )
        return self
    def get_pos_tag_PRON_list( self ):
        self.functions.append( "get_pos_tag_PRON_list" )
        return self
    def get_pos_tag_PRT_list( self ):
        self.functions.append( "get_pos_tag_PRT_list" )
        return self
    def get_pos_tag_PUNCT_list( self ):
        self.functions.append( "get_pos_tag_PUNCT_list" )
        return self
    def get_pos_tag_VERB_list( self ):
        self.functions.append( "get_pos_tag_VERB_list" )
        return self
    def get_pos_tag_X_list( self ):
        self.functions.append( "get_pos_tag_X_list" )
        return self
    def get_pos_tag_AFFIX_list( self ):
        self.functions.append( "get_pos_tag_AFFIX_list" )
        return self

    def get_pos_tag_UNKNOWN_str_list( self ):
        self.functions.append( "get_pos_tag_UNKNOWN_str_list" )
        return self
    def get_pos_tag_ADJ_str_list( self ):
        self.functions.append( "get_pos_tag_ADJ_str_list" )
        return self
    def get_pos_tag_ADP_str_list( self ):
        self.functions.append( "get_pos_tag_ADP_str_list" )
        return self
    def get_pos_tag_ADV_str_list( self ):
        self.functions.append( "get_pos_tag_ADV_str_list" )
        return self
    def get_pos_tag_CONJ_str_list( self ):
        self.functions.append( "get_pos_tag_CONJ_str_list" )
        return self
    def get_pos_tag_DET_str_list( self ):
        self.functions.append( "get_pos_tag_DET_str_list" )
        return self
    def get_pos_tag_NOUN_str_list( self ):
        self.functions.append( "get_pos_tag_NOUN_str_list" )
        return self
    def get_pos_tag_NUM_str_list( self ):
        self.functions.append( "get_pos_tag_NUM_str_list" )
        return self
    def get_pos_tag_PRON_str_list( self ):
        self.functions.append( "get_pos_tag_PRON_str_list" )
        return self
    def get_pos_tag_PRT_str_list( self ):
        self.functions.append( "get_pos_tag_PRT_str_list" )
        return self
    def get_pos_tag_PUNCT_str_list( self ):
        self.functions.append( "get_pos_tag_PUNCT_str_list" )
        return self
    def get_pos_tag_VERB_str_list( self ):
        self.functions.append( "get_pos_tag_VERB_str_list" )
        return self
    def get_pos_tag_X_str_list( self ):
        self.functions.append( "get_pos_tag_X_str_list" )
        return self
    def get_pos_tag_AFFIX_str_list( self ):
        self.functions.append( "get_pos_tag_AFFIX_str_list" )
        return self



    # text_content #
    def setTextContent( self, text_content ):
        self.text_content = text_content
        return self

    def appendTextContent( self, text_content ):
        self.text_content += text_content
        return self

    def clearTextContent( self ):
        self.text_content = ""
        return self

    # functions #
    def clearFunctions( self ):
        self.functions = []
        return self

    # return_natural_language_raw_data #
    def return_natural_language_raw_data( self, boolean ):
        if boolean :
            self._return_natural_language_raw_data = 1
        else:
            self._return_natural_language_raw_data = 0
        return self

    # natural_language_raw_data #
    def natural_language_raw_data( self, natural_language_raw_data ):
        self._natural_language_raw_data = natural_language_raw_data
        return self

    # build #
    def build( self ):
        json_obj = { "text_content" : self.text_content, "functions": self.functions, "return_natural_language_raw_data": self._return_natural_language_raw_data, "natural_language_raw_data": self._natural_language_raw_data } 
        payload = json.dumps( json_obj )
        return requests.post( self.URL_ENDPOINT, payload )

